import os
import shutil
from PIL import Image
import imagehash
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
exts = ['.jpg', '.jpeg', '.png']
import sys
import os

if getattr(sys, 'frozen', False):
    # O programa está sendo executado em um executável
    BASE_DIR = sys._MEIPASS
else:
    # O programa está sendo executado no ambiente de desenvolvimento
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DuplicatesValidator:
    def __init__(self, master):
        self.master = master
        master.title("Validar_Fotos_Duplicadas (DeV - P3rs3ul)")
        master.geometry("800x400")

        # Criação dos widgets da interface
        self.path_label = tk.Label(master, text="Caminho das fotos:")
        self.path_label.pack()

        self.path_entry = tk.Entry(master)
        self.path_entry.pack()

        self.path_button = tk.Button(master, text="Procurar pasta", command=self.select_folder)
        self.path_button.pack()

        self.threshold_label = tk.Label(master, text="Percentual de semelhança (0-1)")
        self.threshold_label.pack()

        self.threshold_entry = tk.Entry(master)
        self.threshold_entry.pack()

        self.validate_button = tk.Button(master, text="Validar", command=self.validate_duplicates)
        self.validate_button.pack()

        # Carregar imagem como wallpaper
        self.image_path = os.path.join(os.path.dirname(__file__), "Foto.jpg")
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((800, 400))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(master, width=800, height=400)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack()

        def animate_background(self):
            self.canvas.coords(self.background, self.x_offset, self.y_offset)
            self.x_offset = (self.x_offset + 1) % self.background_width
            self.y_offset = (self.y_offset + 1) % self.background_height
            self.master.after(10, self.animate_background)

        def select_folder(self):
            # Abre uma janela de seleção de pasta e atualiza o campo de caminho
            folder_path = filedialog.askdirectory()
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_path)
        # Carregar imagem como wallpaper


    def animate_background(self):
        self.canvas.coords(self.background, self.x_offset, self.y_offset)
        self.x_offset = (self.x_offset + 1) % self.background_width
        self.y_offset = (self.y_offset + 1) % self.background_height
        self.master.after(10, self.animate_background)

    def select_folder(self):
        # Abre uma janela de seleção de pasta e atualiza o campo de caminho
        folder_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_path)

    def validate_duplicates(self):
        # Obtém o caminho da pasta e o percentual de similaridade informados pelo usuário
        folder_path = self.path_entry.get()
        similarity_threshold = float(self.threshold_entry.get())

        # Verifica se o caminho informado é válido
        if not os.path.exists(folder_path):
            messagebox.showerror("Erro", "Caminho inválido")
            return

        # Cria a pasta de duplicatas dentro da pasta 'path' se não existir
        duplicates_folder = os.path.join(folder_path, 'duplicatas')
        if not os.path.exists(duplicates_folder):
            os.makedirs(duplicates_folder)

        # Dicionário com os hashes das imagens
        hashes = {}

        # Lista para armazenar as imagens duplicadas encontradas
        duplicates = []

        # Percorre todas as subpastas e arquivos da pasta 'path'
        for subdir, dirs, files in os.walk(folder_path):
            for file in files:
                # Processa apenas arquivos de imagem com as extensões especificadas
                if os.path.splitext(file)[1].lower() in exts:
                    filepath = os.path.join(subdir, file)
                    with open(filepath, 'rb') as f:
                        # Calcula o hash da imagem e verifica se já existe no dicionário de hashes
                        img_hash = imagehash.phash(Image.open(f))
                        for h, path in hashes.items():
                            # Verifica a similaridade entre as imagens a partir dos hashes
                            similarity = 1 - (img_hash - h) / len(img_hash.hash) ** 2
                            # Verifica se a similaridade é maior que o threshold e se as imagens são diferentes
                            if similarity >= similarity_threshold and os.path.basename(filepath) != os.path.basename(path):
                                # Armazena o caminho da imagem duplicada e seu hash
                                duplicates.append((filepath, path, similarity))
                                break
                        else:
                            # Armazena o hash da imagem no dicionário
                            hashes[img_hash] = filepath

        # Move as imagens duplicadas para a pasta de duplicatas
        for duplicate in duplicates:
            src_path = duplicate[0]
            dst_path = os.path.join(duplicates_folder, os.path.basename(src_path))
            shutil.move(src_path, dst_path)
def main():
    root = tk.Tk()
    duplicates_validator = DuplicatesValidator(root)
    root.mainloop()

if __name__ == '__main__':
    main()
