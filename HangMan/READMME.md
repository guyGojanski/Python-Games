# Hangman Pro

![Game Screenshot](<./assets/screenshot(1).png>)
![Game Screenshot](<./assets/screenshot(2).png>)

A desktop Hangman game built with Python, `tkinter`, and `pygame`.

## Features

- Clean desktop GUI with keyboard support (`Enter` to submit)
- Random word selection each round
- Letter tracking and remaining-attempt display
- Hint button (`HELP`) that reveals one letter and costs one life
- Win/lose celebration screen with sound effects

## Project Structure

- `Play.py`: Game controller and round logic
- `GUI.py`: User interface, animations, and audio playback
- `word.py`: Word list source
- `art.py`: Hangman stage drawings
- `assets/`: Audio files and static assets
- `requirements.txt`: Python dependency list

## Requirements

- Python 3.10+
- Windows (recommended for `.exe` packaging)

## Installation & Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/guyGojanski/Python-Games.git
```

### 2. Enter the folder

```bash
cd HangMan
```

### 3.Install dependencies:

```bash
python -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Run The Game

From the `HangMan` folder:

```bash
python Play.py
```

## Gameplay Rules

- Guess one letter at a time.
- Correct guesses reveal all matching positions.
- Wrong guesses reduce your lives.
- You start with 6 lives.
- Press `HELP` to reveal a letter (costs 1 life).
- Game ends when you complete the word or run out of lives.
