import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os

# Lista dei giochi
games_list = [
    {
        "name": "Super Mario Bros.",
        "system": "NES",
        "cover": "assets/covers/smb.png",
        "rom_keyword": "super mario bros",
        "description": "Il platform più famoso di tutti i tempi.",
        "year": 1985,
        "developer": "Nintendo",
        "publisher": "Nintendo"
    },
    {
        "name": "The Legend of Zelda",
        "system": "NES",
        "cover": "assets/covers/zelda_nes.png",
        "rom_keyword": "zelda",
        "description": "Una grande avventura fantasy tra dungeon e segreti.",
        "year": 1986,
        "developer": "Nintendo",
        "publisher": "Nintendo"
    },
    {
        "name": "Metroid",
        "system": "NES",
        "cover": "assets/covers/metroid.png",
        "rom_keyword": "metroid",
        "description": "Esplora mondi alieni nei panni di Samus Aran.",
        "year": 1986,
        "developer": "Nintendo R&D1",
        "publisher": "Nintendo"
    },
    {
        "name": "Contra",
        "system": "NES",
        "cover": "assets/covers/contra.png",
        "rom_keyword": "contra",
        "description": "Sparatorie epiche contro alieni invasori.",
        "year": 1987,
        "developer": "Konami",
        "publisher": "Konami"
    },
    {
        "name": "Castlevania",
        "system": "NES",
        "cover": "assets/covers/castlevania.png",
        "rom_keyword": "castlevania",
        "description": "Affronta Dracula in un'avventura gotica.",
        "year": 1986,
        "developer": "Konami",
        "publisher": "Konami"
    },
    {
        "name": "The Legend of Zelda: Link's Awakening",
        "system": "GB",
        "cover": "assets/covers/zelda_links_awakening.png",
        "rom_keyword": "link's awakening",
        "description": "L'avventura portatile di Link su Koholint Island.",
        "year": 1993,
        "developer": "Nintendo",
        "publisher": "Nintendo"
    },
    {
        "name": "Tetris",
        "system": "GB",
        "cover": "assets/covers/tetris.png",
        "rom_keyword": "tetris",
        "description": "Il puzzle game più iconico della storia.",
        "year": 1989,
        "developer": "Alexey Pajitnov",
        "publisher": "Nintendo"
    },
    {
        "name": "Super Mario Land",
        "system": "GB",
        "cover": "assets/covers/mario land.png",
        "rom_keyword": "mario land",
        "description": "La prima avventura portatile di Mario.",
        "year": 1989,
        "developer": "Nintendo",
        "publisher": "Nintendo"
    },
]

# Emulatori
EMULATORS = {
    "NES": "emulators/nestopia/nestopia.exe",
    "GB": "emulators/gambatte/gambatte.exe",
    "GBC": "emulators/gambatte/gambatte.exe",
}

# Cartella roms
ROMS_FOLDER = "roms/"

class ArkOSLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Retro-OS 1.2")
        self.geometry("900x800")
        self.configure(bg="#111111")
        self.resizable(False, False)

        self.selected_index = 0
        self.cover_img = None

        self.title_label = tk.Label(self, text="Retro-OS 1.2", font=("Arial Black", 28), fg="white", bg="#111111")
        self.title_label.pack(pady=10)

        self.game_name = tk.Label(self, text="", font=("Arial", 20), fg="white", bg="#111111")
        self.game_name.pack(pady=5)

        self.cover_label = tk.Label(self, bg="#111111")
        self.cover_label.pack(pady=10)


        self.description_label = tk.Label(self, text="", font=("Arial", 12), fg="white", bg="#111111", wraplength=760, justify="center")
        self.description_label.pack(pady=5)

        self.info_label = tk.Label(self, text="", font=("Arial", 10), fg="white", bg="#111111", wraplength=760, justify="center")
        self.info_label.pack(pady=5)

        self.instruction = tk.Label(self, text="Usa SU/GIÙ per navigare - ENTER per avviare", font=("Arial", 12), fg="gray", bg="#111111")
        self.instruction.pack(pady=10)

        

        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.launch_game)

        self.update_display()

    def find_rom(self, keyword):
        keyword = keyword.lower().replace(" ", "")
        for file in os.listdir(ROMS_FOLDER):
            clean_file = file.lower().replace(" ", "")
            if keyword in clean_file:
                return os.path.join(ROMS_FOLDER, file)
        return None

    def move_up(self, event):
        self.selected_index = (self.selected_index - 1) % len(games_list)
        self.update_display()

    def move_down(self, event):
        self.selected_index = (self.selected_index + 1) % len(games_list)
        self.update_display()

    def launch_game(self, event):
        game = games_list[self.selected_index]
        system = game["system"]
        keyword = game["rom_keyword"]
        emulator_path = EMULATORS.get(system)

        if not emulator_path or not os.path.exists(emulator_path):
            print(f"Errore: Emulatore per {system} non trovato!")
            return

        rom_path = self.find_rom(keyword)
        if not rom_path:
            print(f"Errore: Nessuna ROM trovata per '{game['name']}'!")
            return

        print(f"Avvio {game['name']} su {system} con ROM: {rom_path}")

        try:
            subprocess.run([emulator_path, rom_path], check=True)
        except Exception as e:
            print(f"Errore durante l'avvio del gioco: {e}")

    def update_display(self):
        game = games_list[self.selected_index]
        self.game_name.config(text=f"{game['name']} ({game['system']})")

        try:
            img = Image.open(game["cover"])
            img = img.resize((360, 260))
            self.cover_img = ImageTk.PhotoImage(img)
            self.cover_label.config(image=self.cover_img)
        except Exception as e:
            print(f"Errore caricando copertina: {e}")

        # Aggiorna descrizione e info extra
        description_text = game.get("description", "Nessuna descrizione disponibile.")
        info_text = f"Anno: {game.get('year', 'N/A')} | Developer: {game.get('developer', 'N/A')} | Publisher: {game.get('publisher', 'N/A')}"
        self.description_label.config(text=description_text)
        self.info_label.config(text=info_text)

if __name__ == "__main__":
    app = ArkOSLauncher()
    app.mainloop()
