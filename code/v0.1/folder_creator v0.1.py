import tkinter as tk
from tkinter import filedialog, messagebox
import os

class FolderCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Folder Creator v0.1 - by Axel0689")
        self.root.geometry("480x220")  # Set fixed window size
        self.root.resizable(False, False)  # Make window non-resizable
        self.current_dir = None

        # Nome della cartella
        tk.Label(self.root, text="Nome della cartella:").grid(row=0, column=0, padx=5, pady=5)
        self.folder_name_entry = tk.Entry(self.root, width=40)
        self.folder_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Numero di cartelle
        tk.Label(self.root, text="Numero di cartelle:").grid(row=1, column=0, padx=5, pady=5)
        self.num_folders_entry = tk.Entry(self.root, width=10)
        self.num_folders_entry.grid(row=1, column=1, padx=5, pady=5)

        # Modalità di creazione
        tk.Label(self.root, text="Modalità di generazione:").grid(row=2, column=0, padx=5, pady=5)
        self.mode_var = tk.IntVar(value=1)  # 1 for Incrementale, 2 for Unico
        self.incrementale_radio = tk.Radiobutton(self.root, text="Incrementale", variable=self.mode_var, value=1, command=lambda: self.toggle_and_change_color("Incrementale"))
        self.incrementale_radio.grid(row=2, column=1, padx=5, pady=5)
        self.unico_radio = tk.Radiobutton(self.root, text="Unico", variable=self.mode_var, value=2, command=lambda: self.toggle_and_change_color("Unico"))
        self.unico_radio.grid(row=2, column=2, padx=5, pady=5)

        # Nidifica checkbox
        self.nidifica_var = tk.BooleanVar(value=False)
        self.nidifica_checkbox = tk.Checkbutton(self.root, text="Nidifica", variable=self.nidifica_var)
        self.nidifica_checkbox.grid(row=3, column=0, padx=5, pady=5)

        # Percorso della cartella
        tk.Label(self.root, text="Percorso della cartella:").grid(row=4, column=0, padx=5, pady=5)
        self.dir_entry = tk.Entry(self.root, width=40)
        self.dir_entry.grid(row=4, column=1, padx=5, pady=5)
        self.update_dir_button = tk.Button(self.root, text="Seleziona", command=self.select_directory)
        self.update_dir_button.grid(row=4, column=2, padx=5, pady=5)

        # Bottone per creare le cartelle
        self.create_button = tk.Button(self.root, text="Crea Cartelle", command=self.create_folders)
        self.create_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Initialize color change
        self.change_color()

    def select_directory(self):
        self.current_dir = filedialog.askdirectory()
        if self.current_dir:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(tk.END, self.current_dir)

    def toggle_and_change_color(self, mode):
        if mode == "Unico":
            self.num_folders_entry.config(state="disabled")
        else:
            self.num_folders_entry.config(state="normal")
        self.change_color()

    def change_color(self):
        mode = "Incrementale" if self.mode_var.get() == 1 else "Unico"
        if mode == "Incrementale":
            self.incrementale_radio.config(bg="#0080FF")  # Azure for Incrementale
            self.unico_radio.config(bg="#CCCCC4")  # Pastel Grey for Unico
        elif mode == "Unico":
            self.incrementale_radio.config(bg="#CCCCC4")  # Pastel Grey for Incrementale
            self.unico_radio.config(bg="#0080FF")  # Azure for Unico

    def create_folders(self):
        folder_name = self.folder_name_entry.get().strip()
        dir_path = self.current_dir
        mode = "Incrementale" if self.mode_var.get() == 1 else "Unico"
        nidifica = self.nidifica_var.get()

        if not folder_name:
            messagebox.showerror("Errore", "Inserire un nome per la cartella!")
            return

        if not dir_path:
            messagebox.showerror("Errore", "Selezionare il percorso della cartella!")
            return

        try:
            os.chdir(dir_path)
            
            if mode == "Incrementale":
                num_folders = int(self.num_folders_entry.get()) if self.num_folders_entry.get().strip() else 1
                if nidifica:
                    current_path = dir_path
                    for i in range(1, num_folders + 1):
                        new_folder_name = f"{folder_name} {i}"
                        os.makedirs(os.path.join(current_path, new_folder_name))
                        current_path = os.path.join(current_path, new_folder_name)
                else:
                    for i in range(1, num_folders + 1):
                        new_folder_name = f"{folder_name} {i}"
                        os.makedirs(new_folder_name)
            elif mode == "Unico":
                unique_names = self.folder_name_entry.get().split(',')
                unique_names = [name.strip() for name in unique_names]
                if nidifica:
                    current_path = dir_path
                    for name in unique_names:
                        if name:
                            os.makedirs(os.path.join(current_path, name))
                            current_path = os.path.join(current_path, name)
                else:
                    for name in unique_names:
                        if name:
                            os.makedirs(name)
            
            messagebox.showinfo("Successo", f"Create {len(unique_names) if mode == 'Unico' else num_folders} cartelle nel percorso '{dir_path}'")
        except OSError as e:
            messagebox.showerror("Errore", f"Impossibile creare le cartelle: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FolderCreator()
    app.run()
