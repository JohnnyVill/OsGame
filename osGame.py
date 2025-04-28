import tkinter as tk
from multiprocessing import Process, Pipe
from threading import Lock, Semaphore, Thread
from PIL import Image, ImageTk
import random
import time
import threading
import os

# Deck and logic setup
deck = list(range(1, 14)) * 4  # Simplified 52-card deck

# Synchronization tools
game_lock = Lock()
turn_semaphore = Semaphore(1)

# Deadlock flag
deadlock_detected = False

# def end_game():
#     print("Game timer ended!")
#     os._exit(0)

# Start a 5-minute timer
# timer = threading.Timer(60, end_game)
# timer.start()

class CardGameGUI:
    def __init__(self, root, conn1, conn2):
        self.root = root
        self.conn1 = conn1
        self.conn2 = conn2
        self.player1_wins = 0
        self.player2_wins = 0

        self.timer = threading.Timer(30, self.end_game)
        self.timer.start()

          # Load a background image
        try:
            bg_image = Image.open("cards/CardsBackground.jpeg")  # <-- you need to add a background image
            bg_image = bg_image.resize((450, 450))
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.background_label = tk.Label(root, image=self.bg_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background image could not be loaded: {e}")
            self.root.config(bg="darkgreen")  # fallback color like poker table


        self.label = tk.Label(root, text="Card Game Begins!", font=("Arial", 20, "bold"), bg="#006400", fg="white")
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Round", command=self.start_round, font=("Arial", 14), bg="#FFD700", fg="black")
        self.start_button.pack(pady=5)

        self.canvas = tk.Canvas(root, width=400, height=180, bg="#228B22", highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=("Arial", 14), bg="#006400", fg="white")
        self.status.pack()

        self.score_label = tk.Label(root, text="Player 1 Wins: 0 | Player 2 Wins: 0", font=("Arial", 12), bg="#006400", fg="white")
        self.score_label.pack(pady=5)

        # Load all card images into a dictionary
        self.card_images = {}
        self.card_values = {}

        for i in range(2, 54):  # 2 to 53 inclusive
            img = Image.open(f"cards/{i}.png")
            img = img.resize((80, 120))
            self.card_images[i] = ImageTk.PhotoImage(img)

            value = ((i - 2) // 4) + 2
            self.card_values[i] = value

    def end_game(self):
        self.end_game_summary()

        time.sleep(3)
        self.root.quit()

    def end_game_summary(self):
        self.start_button.config(state=tk.DISABLED)
        self.label.config(text="Game Over!")
        if self.player1_wins > self.player2_wins:
            winner_text = "Player 1 is the overall winner!"
        elif self.player2_wins > self.player1_wins:
            winner_text = "Player 2 is the overall winner!"
        else:
            winner_text = "It's an overall tie!"

        self.update_status(winner_text)
        print(winner_text)

    def start_round(self):
        Thread(target=self.play_round).start()

    def play_round(self):
        try:
            turn_semaphore.acquire()
            game_lock.acquire()

            # Ask each player to draw
            self.conn1.send("draw")
            self.conn2.send("draw")

            # Receive card numbers
            card1_num = self.conn1.recv()  # Example: 2
            card2_num = self.conn2.recv()  # Example: 5

            # Lookup value and image
            card1_value = self.card_values[card1_num]
            card1_img = self.card_images[card1_num]

            card2_value = self.card_values[card2_num]
            card2_img = self.card_images[card2_num]

            # Display cards
            self.display_cards(card1_img, card2_img)

            # Compare values
            result = f"Player 1: {card1_value} vs Player 2: {card2_value}\n"
            if card1_value > card2_value:
                result += "Player 1 wins this round!"
                self.player1_wins += 1
            elif card2_value > card1_value:
                result += "Player 2 wins this round!"
                self.player2_wins += 1
            else:
                result += "It's a tie!"

            self.update_status(result)
            self.update_score()

        except Exception as e:
            self.update_status(f"Error: {e}")
        finally:
            game_lock.release()
            turn_semaphore.release()

    def display_cards(self, card1_img, card2_img):
        self.canvas.delete("all")

        self.canvas.create_image(100, 100, image=card1_img)
        self.canvas.create_image(300, 100, image=card2_img)

    def update_status(self, msg):
        self.status.config(text=msg)

    def update_score(self):
        self.score_label.config(text=f"Player 1 Wins: {self.player1_wins} | Player 2 Wins: {self.player2_wins}")

def player(conn, name):
    while True:
        try:
            msg = conn.recv()
            if msg == "draw":
                card = random.randint(2, 53)  # Random card from the deck
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
    root.title("Card Game")
    root.geometry("450x450")
    app = CardGameGUI(root, parent_conn1, parent_conn2)

    root.mainloop()

    p1.terminate()
    p2.terminate()
