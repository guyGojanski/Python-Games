import tkinter as tk
import random
from GUI import HangmanGUI
from art import stages
from word import word_list


class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.reset_game()
        print(f"Test Mode - The word is: {self.chosen_word}")  # for debug

        self.root.mainloop()

    def handle_guess(self, char):
        # Ignore repeated guesses and non-letter input before changing game state.
        if char in self.guessed:
            self.ui.display_message(
                "Already Guessed",
                f"You already guessed '{char.upper()}'. Try a different letter.",
                game_over=False,
            )
            return

        if not ("a" <= char <= "z") or len(char) != 1:
            self.ui.display_message(
                "Invalid Input",
                "Please enter a single letter (a-z).",
                game_over=False,
            )
            return

        self.guessed.append(char)

        # Correct letters reveal every matching position.
        if char in self.chosen_word:
            for i, letter in enumerate(self.chosen_word):
                if letter == char:
                    self.word_print[i] = char
            self.ui.update_word(self.word_print)
        else:
            # Wrong guesses reduce attempts and move the hangman forward one stage.
            self.tries -= 1
            self.ui.update_canvas(stages[self.tries])

        self.ui.update_stats(self.tries, self.guessed)
        self.check_finish()

    def reset_game(self):
        self.chosen_word = random.choice(word_list)
        self.word_print = ["_" for _ in self.chosen_word]
        self.tries = 6
        self.guessed = []

        for widget in self.root.winfo_children():
            widget.destroy()

        self.ui = HangmanGUI(self.root, self.handle_guess)
        self.ui.update_word(self.word_print)
        self.ui.update_canvas(stages[self.tries])

    def check_finish(self):
        if "_" not in self.word_print:
            self.ui.show_celebration(
                "YOU WON!",
                f"The word was: {self.chosen_word}",
                "assets/weWon.mp3",
                self.reset_game,
            )
        elif self.tries == 0:
            self.ui.show_celebration(
                "GAME OVER",
                f"The word was: {self.chosen_word}",
                "assets/weLose.mp3",
                self.reset_game,
            )


if __name__ == "__main__":
    GameController()
