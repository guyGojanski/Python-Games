import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os


class HangmanGUI:
    def __init__(self, root, guess_callback, help_callback):
        self.root = root
        self.guess_callback = guess_callback
        self.help_callback = help_callback
        self.animation_running = False
        self.root.title("Hangman Pro")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#151926")

        self._setup_ui()

    def _setup_ui(self):
        self.card = tk.Frame(
            self.root, bg="#22263a", highlightthickness=1, highlightbackground="#343a57"
        )
        self.card.pack(fill="both", expand=True, padx=18, pady=18)

        self.header = tk.Label(
            self.card,
            text="HANGMAN",
            font=("Helvetica", 28, "bold"),
            bg="#22263a",
            fg="#f5a524",
            pady=18,
        )
        self.header.pack()

        self.subtitle = tk.Label(
            self.card,
            text="Guess the word before the sketch is complete.",
            font=("Arial", 11),
            bg="#22263a",
            fg="#c0c4d6",
        )
        self.subtitle.pack(pady=(0, 14))

        self.canvas = tk.Canvas(
            self.card, width=320, height=260, bg="#2d334d", highlightthickness=0, bd=0
        )
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(
            self.card,
            text="",
            font=("Courier", 30, "bold"),
            bg="#22263a",
            fg="#eef1f8",
            pady=16,
        )
        self.word_label.pack(pady=(10, 6))
        self.input_frame = tk.Frame(self.card, bg="#22263a")
        self.input_frame.pack(pady=(6, 10))

        self.entry = tk.Entry(
            self.input_frame,
            font=("Arial", 20, "bold"),
            width=4,
            justify="center",
            bg="#363c59",
            fg="#ffffff",
            insertbackground="white",
            borderwidth=0,
            relief="flat",
        )
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.on_guess())
        self.entry.focus_set()

        self.guess_btn = tk.Button(
            self.input_frame,
            text="GUESS",
            command=self.on_guess,
            bg="#f5a524",
            fg="#1c2030",
            font=("Arial", 12, "bold"),
            activebackground="#ffd166",
            activeforeground="#1c2030",
            padx=16,
            pady=6,
            relief="flat",
            cursor="hand2",
        )
        self.guess_btn.pack(side="left")

        self.help_btn = tk.Button(
            self.card,
            text="HELP (Lose 1 Life)",
            command=self.on_help,
            bg="#343a57",
            fg="#f5a524",
            font=("Arial", 12, "bold"),
            activebackground="#ffd166",
            activeforeground="#1c2030",
            padx=16,
            pady=6,
            relief="flat",
            cursor="hand2",
        )
        self.help_btn.pack(pady=(5, 15))

        self.tip_label = tk.Label(
            self.card,
            text="One letter only. Press Enter to submit.",
            font=("Arial", 14),
            bg="#22263a",
            fg="#8e95b3",
        )
        self.tip_label.pack(pady=(0, 10))

        self.status_frame = tk.Frame(self.card, bg="#272c43")
        self.status_frame.pack(fill="x", padx=18, pady=(4, 10))

        self.stats_label = tk.Label(
            self.status_frame,
            text="Attempts Left: 6",
            font=("Arial", 18, "bold"),
            bg="#272c43",
            fg="#d9e1ff",
            pady=12,
        )
        self.stats_label.pack()

        self.used_label = tk.Label(
            self.card,
            text="Used: ",
            font=("Arial", 14, "italic"),
            bg="#22263a",
            fg="#8e95b3",
            pady=8,
        )
        self.used_label.pack()

    def on_help(self):
        if hasattr(self, "help_callback"):
            self.help_callback()

    def on_guess(self):
        char = self.entry.get()
        self.entry.delete(0, tk.END)
        if char:
            self.guess_callback(char)

    def update_word(self, word_array):
        self.word_label.config(text="   ".join(word_array))

    def update_stats(self, tries, used):
        self.stats_label.config(text=f"Attempts Left: {tries}")
        self.used_label.config(text=f"Used: {', '.join(used)}")

    def update_canvas(self, stage_text):
        self.canvas.delete("all")
        self.canvas.create_text(
            160, 130, text=stage_text, font=("Courier New", 14, "bold"), fill="#f7f2ea"
        )

    def display_message(self, title, message, game_over=False):
        messagebox.showinfo(title, message)
        if game_over:
            self.root.destroy()

    def show_celebration(self, title, message, sound_file, restart_callback):
        self.animation_running = True
        pygame.mixer.init()
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, sound_file)
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error loading sound: {e}")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.celebration_canvas = tk.Canvas(
            self.root, width=1200, height=800, bg="#151926", highlightthickness=0
        )
        self.celebration_canvas.pack(fill="both", expand=True)

        self.celebration_canvas.create_text(
            600, 300, text=title, font=("Helvetica", 60, "bold"), fill="#f5a524"
        )
        self.celebration_canvas.create_text(
            600, 400, text=message, font=("Arial", 24), fill="#eef1f8"
        )

        restart_btn = tk.Button(
            self.root,
            text="PLAY AGAIN",
            command=restart_callback,
            bg="#f5a524",
            fg="#1c2030",
            font=("Arial", 18, "bold"),
            padx=20,
            pady=10,
            relief="flat",
            cursor="hand2",
        )

        self.celebration_canvas.create_window(600, 550, window=restart_btn)

        self.particles = []
        colors = ["#ef1d8d", "#06c9f0", "#ffffff", "#f5a524"]
        for _ in range(100):
            p = {
                "id": self.celebration_canvas.create_rectangle(
                    0, 0, 10, 10, fill=random.choice(colors), outline=""
                ),
                "x": random.randint(0, 1200),
                "y": random.randint(-800, 0),
                "speed": random.randint(5, 15),
            }
            self.particles.append(p)

        self.animate_confetti()

    def animate_confetti(self):
        if not self.animation_running:
            return

        for p in self.particles:
            p["y"] += p["speed"]
            if p["y"] > 800:
                p["y"] = -20
                p["x"] = random.randint(0, 1200)

            try:
                self.celebration_canvas.coords(
                    p["id"], p["x"], p["y"], p["x"] + 10, p["y"] + 10
                )
            except tk.TclError:
                self.animation_running = False
                return

        self.root.after(30, self.animate_confetti)

    def stop_animation(self):
        self.animation_running = False
