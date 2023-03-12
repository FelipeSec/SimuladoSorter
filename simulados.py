import random
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json
import os

# Change path to current directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load folder paths from config.json
CONFIG_FILE_PATH = './config.json'

with open(CONFIG_FILE_PATH) as f:
    config = json.load(f)
    SRC_FOLDERS = {k: Path(v) for k, v in config['src_folders'].items()}
    DEST_FOLDERS = {k: Path(v) for k, v in config['dest_folders'].items()}

BUTTONS = {"primeira_fase": "Primeira Fase",
           "segunda_fase": "Segunda Fase"}

class SimuladosApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x200")
        self.master.title("Simulados")
        self.master.configure(bg="#f7f7f7")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self, text="Escolha a fase do simulado:", font=("Arial", 16), bg="#f7f7f7")
        self.title_label.pack(pady=(20, 10))

        # Option buttons frame
        self.options_frame = tk.Frame(self, bg="#f7f7f7")
        self.options_frame.pack(pady=10)

        # Option buttons
        for phase, label in BUTTONS.items():
            button = tk.Button(self.options_frame, text=label, font=("Arial", 14), fg="white", bg="#333", width=15, height=2, command=lambda phase=phase: self.select_option(phase))
            button.pack(side="left", padx=(30,20))

        # Instructions label
        self.instructions_label = tk.Label(self, text="Ao clicar em uma opção, o simulado começará automaticamente.", font=("Arial", 12), bg="#f7f7f7")
        self.instructions_label.pack(pady=(10, 20))

    def select_option(self, phase):
        src_folder = SRC_FOLDERS.get(phase)
        dest_folder = DEST_FOLDERS.get(phase)
        if not src_folder or not dest_folder:
            messagebox.showerror("Erro", f"Os caminhos das pastas da fase {phase} não foram encontrados.")
            return
        files = list(src_folder.glob("*"))
        if not files:
            messagebox.showerror("Erro", f"A pasta {src_folder} está vazia.")
        else:
            random_file = random.choice(files)
            dest_file = dest_folder / random_file.name
            try:
                shutil.move(str(random_file), str(dest_file))
                subprocess.Popen(str(dest_file), shell=True)
            except OSError as e:
                messagebox.showerror("Erro", f"Não foi possível mover o arquivo selecionado para a pasta {dest_folder}. Erro: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap('./icone.ico')
    app = SimuladosApp(master=root)
    app.mainloop()
