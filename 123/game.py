import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Die Karten und deren Bilder (URLs)
maps = [
    {"name": "Tanglewood", "image": "https://tse4.mm.bing.net/th/id/OIP.kfQDD5QU3RtLkdrh52OoUwHaEK?rs=1&pid=ImgDetMain"},
    {"name": "Bleasdale", "image": "https://dotesports.com/wp-content/uploads/2025/03/bleasdale-farmhouse-exterior-phasmophobia.jpg"},
    {"name": "Edgefield", "image": "https://tse1.mm.bing.net/th/id/OIP.jsFdQupGzMtKxEP8E6Su_gAAAA?rs=1&pid=ImgDetMain"},
    {"name": "Ridgeview", "image": "https://cdn-ak.f.st-hatena.com/images/fotolife/s/smart_thomas/20221231/20221231005129.png"},
    {"name": "Grafton", "image": "https://th.bing.com/th/id/R.644a52d6a8f11454a36aa1fbe12a3ab4?rik=VFIOo%2f1ti%2bf6zw&pid=ImgRaw&r=0"},
    {"name": "Willow", "image": "https://tse4.mm.bing.net/th/id/OIP.7px0FFDHivBQk4coZXoizgAAAA?rs=1&pid=ImgDetMain"}
]

# Führt das Spiel aus und zeigt das Leaderboard
class PhasmophobiaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Phasmophobia Map Guessing Game")

        # Initiale Variablen
        self.score = 0
        self.player_name = ""
        self.current_map = None
        self.leaderboard = self.load_leaderboard()

        # Spiel GUI erstellen
        self.create_widgets()

    def create_widgets(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(padx=20, pady=20)

        self.title_label = tk.Label(self.start_frame, text="Errate die Phasmophobia-Map!", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.name_label = tk.Label(self.start_frame, text="Gib deinen Namen ein:", font=("Arial", 14))
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(self.start_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.start_frame, text="Spiel Starten", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=10)

        # Spiel Frame (wird später angezeigt)
        self.game_frame = tk.Frame(self.root)
        
        self.hint_label = tk.Label(self.game_frame, text="Kartenname: ???", font=("Arial", 16))
        self.hint_label.pack(pady=10)

        self.map_image_label = tk.Label(self.game_frame)
        self.map_image_label.pack(pady=10)

        self.map_entry = tk.Entry(self.game_frame, font=("Arial", 14))
        self.map_entry.pack(pady=5)

        self.submit_button = tk.Button(self.game_frame, text="Antwort abgeben", font=("Arial", 14), command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.game_frame, text="Punkte: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Leaderboard anzeigen
        self.leaderboard_frame = tk.Frame(self.root)
        self.leaderboard_label = tk.Label(self.leaderboard_frame, text="Leaderboard", font=("Arial", 18))
        self.leaderboard_label.pack(pady=10)

        self.leaderboard_listbox = tk.Listbox(self.leaderboard_frame, font=("Arial", 14), width=30, height=10)
        self.leaderboard_listbox.pack(padx=20, pady=10)

        self.update_leaderboard()

    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Name erforderlich", "Bitte gib deinen Namen ein.")
            return

        self.start_frame.pack_forget()
        self.game_frame.pack(padx=20, pady=20)

        self.new_map()

    def new_map(self):
        self.current_map = random.choice(maps)
        self.hint_label.config(text="Kartenname: ???")
        self.map_image_label.config(image=self.load_image(self.current_map["image"]))
        self.map_entry.delete(0, tk.END)

    def load_image(self, url):
        # Hier könnte eine echte Funktion zum Laden von Bildern von einer URL stehen.
        # Für den Moment geben wir einfach ein Platzhalterbild zurück.
        return tk.PhotoImage(width=300, height=200)

    def submit_answer(self):
        user_guess = self.map_entry.get().strip()
        if user_guess.lower() == self.current_map["name"].lower():
            self.score += 1
            messagebox.showinfo("Richtig!", f"Richtig! Du hast die Karte erraten: {self.current_map['name']}")
        else:
            messagebox.showinfo("Falsch!", f"Falsch! Die richtige Antwort war: {self.current_map['name']}")

        self.score_label.config(text=f"Punkte: {self.score}")
        self.save_score()
        self.update_leaderboard()
        self.new_map()

    def save_score(self):
        if self.player_name:
            self.leaderboard.append({"name": self.player_name, "score": self.score})
            self.save_leaderboard()

    def save_leaderboard(self):
        with open("leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

    def load_leaderboard(self):
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as file:
                return json.load(file)
        return []

    def update_leaderboard(self):
        self.leaderboard_listbox.delete(0, tk.END)
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)
        for player in sorted_leaderboard:
            self.leaderboard_listbox.insert(tk.END, f"{player['name']}: {player['score']} Punkte")


if __name__ == "__main__":
    root = tk.Tk()
    game = PhasmophobiaGame(root)
    root.mainloop()
