# Countdown Clash Design README 

## 1.Demo Video: https://youtu.be/W1iNa6m0rv0

## 2. Setup:
To run the game ensure you have python installed, then run this command: python3 osGame.py . This will then compile and run the game. 

## 3. Game Overview
### a) Game Title: Countdown Clash
### b) Game Summary: Feeling left out from your friends during poker and blackjack night but still want to be able to join the fun with a deck of cards? Well this is the game just for you. Countdown Clash is a simple and easy card game to play where each player draws a card and the player whose card with the highest number wins. It’s that simple and quick to learn with no complicated rules. Join the fun with the simple click of a button!
### c) Core Gameplay Loop: Each player is dealt a card, and the player with the higher card wins the round. The countdown refers to the game’s timer—once it reaches zero, the game ends. We're planning to enhance the experience by adding a "best 3 out of 5" system or a score tracker for each player, so you can easily see who's winning overall.

## 4. Gameplay Mechanics
Controls: Our game design has a basic control where users only need to press the draw button to begin the round. This button can be pressed again after each round when the winner with the greater card is decided. Input scheme for this game includes a mouse or touchpad.
Core Mechanics: The core mechanics of this game include card drawing, card comparison, timer-based round and score tracker. The draw button randomly selects cards and automatically compares the highest one after each round for each player. The game then ends when the timer hits zero.
Level Progression: There is no real level progression, but with our “Best of 3/5” system implemented, each player's win contributed to a players score record and can be seen as a form of continuation of the game.
Win/Loss Conditions: Win/Loss conditions are applied every round, and with a win counter for the “Best of 3/5” system implemented we can have an overall winner for the 5 rounds once the timer has ended.

## 5. OS Concepts Card Game

This is a Python-based GUI card game that demonstrates key Operating System concepts such as multithreading, multiprocessing, inter-process communication (IPC), synchronization, deadlock detection, and time-based program termination.

Built using:

- `tkinter` for GUI
- `multiprocessing` for player processes
- `threading` for deadlock detection and concurrent game control
- `Pipe`, `Semaphore`, `Lock` for OS-style resource management

---

## Gameplay Overview

- Two virtual players draw a random card (1–13) per round.
- The GUI shows which player wins the round or if it's a tie.
- The user can keep starting rounds by clicking the "Start Round" button.
- The game auto-terminates after **5 minutes** to simulate a scheduled timeout.

---

## Features

- **Multiprocessing**: Each player is a separate process that receives messages and sends back a card.
- **Pipes (IPC)**: The main process communicates with player processes using `Pipe`.
- **Multithreading**: The GUI stays responsive by spawning a thread for each round.
- **Synchronization**: Uses `Lock` and `Semaphore` to ensure only one round runs at a time.
- **Deadlock Detection**: A background thread checks for potential deadlocks and attempts recovery.
- **Timer**: Automatically ends the game after 5 minutes using `threading.Timer`.

---

## OS Concepts Demonstrated

| Concept            | Where It’s Used                                    |
| ------------------ | -------------------------------------------------- |
| Processes          | `multiprocessing.Process` for Player 1 & 2         |
| Threads            | GUI round control and deadlock monitoring          |
| IPC                | `Pipe` used to send/receive data between processes |
| Locks              | `threading.Lock()` to protect game state           |
| Semaphores         | Ensure only one thread starts a round at a time    |
| Deadlock Detection | Detects if a thread is stuck and forcibly unlocks  |
| Timers             | 5-minute shutdown using `threading.Timer()`        |

---

## How to Run

1. Make sure you have **Python 3.8+** installed.

2. Run the game:

   ```bash
   python osGame.py
   ```
