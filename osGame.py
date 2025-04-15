import tkinter as tk
from multiprocessing import Process, Pipe
from threading import Lock, Semaphore, Thread  # <- Use threading.Lock
import random
import time
import threading
import os

# Deck and logic setup
deck = list(range(1, 12)) * 4  # Simplified 52-card deck

# Synchronization tools
game_lock = Lock()
turn_semaphore = Semaphore(1)

# Deadlock flag
deadlock_detected = False

def end_game():
    print("Game timer ended!")
    os._exit(0)

# Start a 5-minute timer using threading
timer = threading.Timer(300, end_game)
timer.start()

class CardGameGUI:
    def __init__(self, root, conn1, conn2):
        self.root = root
        self.conn1 = conn1
        self.conn2 = conn2
        self.label = tk.Label(root, text="Card Game Begins!", font=("Arial", 18))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Round", command=self.start_round)
        self.start_button.pack(pady=10)

        self.status = tk.Label(root, text="", font=("Arial", 14))
        self.status.pack()

    def start_round(self):
        Thread(target=self.play_round).start()

    def play_round(self):
        try:
            turn_semaphore.acquire()
            game_lock.acquire()

            self.conn1.send("draw")
            self.conn2.send("draw")

            card1 = self.conn1.recv()
            card2 = self.conn2.recv()

            result = f"Player 1: {card1} vs Player 2: {card2}\n"
            if card1 > card2:
                result += "Player 1 wins this round!"
            elif card2 > card1:
                result += "Player 2 wins this round!"
            else:
                result += "It's a tie!"

            self.update_status(result)

        except Exception as e:
            self.update_status(f"Error: {e}")
        finally:
            game_lock.release()
            turn_semaphore.release()

    def update_status(self, msg):
        self.status.config(text=msg)

def player(conn, name):
    while True:
        try:
            msg = conn.recv()
            if msg == "draw":
                card = random.choice(deck)
                time.sleep(random.uniform(0.5, 1.5))  # Simulate thinking
                conn.send(card)
        except EOFError:
            break

def detect_deadlock():
    global deadlock_detected
    while True:
        time.sleep(10)
        if not turn_semaphore._value:
            print("Potential deadlock detected! Forcing unlock.")
            deadlock_detected = True
            try:
                game_lock.release()
                turn_semaphore.release()
            except:
                pass

if __name__ == "__main__":
    parent_conn1, child_conn1 = Pipe()
    parent_conn2, child_conn2 = Pipe()

    p1 = Process(target=player, args=(child_conn1, "Player 1"))
    p2 = Process(target=player, args=(child_conn2, "Player 2"))

    p1.start()
    p2.start()

    Thread(target=detect_deadlock, daemon=True).start()

    root = tk.Tk()
    root.title("OS Concepts Card Game")
    root.geometry("400x300")
    app = CardGameGUI(root, parent_conn1, parent_conn2)

    root.mainloop()

    p1.terminate()
    p2.terminate()