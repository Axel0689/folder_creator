import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from typing import List, Optional
from PIL import Image, ImageTk  # Importa le classi necessarie da Pillow

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", 
                         relief="solid", borderwidth=1, padx=2, pady=2)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class FolderCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Folder Creator v0.2 - by Axel0689")
        self.root.geometry("450x480")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('xpnative')
        
        self.current_dir: Optional[str] = None

        self.load_icons() # Carica le icone all'avvio
        self.create_widgets()
        self.create_tooltips()

    def load_icons(self):
        try:
            self.folder_icon = ImageTk.PhotoImage(Image.open("folder_icon.png").resize((60, 60))) # Ridimensiona l'icona se necessario
            self.select_icon = ImageTk.PhotoImage(Image.open("select_icon.png").resize((20, 20)))
        except FileNotFoundError:
            print("Icone non trovate. Assicurati che 'folder_icon.png' e 'select_icon.png' siano nella stessa cartella dello script.")
            self.folder_icon = None  # Imposta le icone a None se non vengono trovate
            self.select_icon = None

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Frame per le impostazioni del nome e numero di cartelle
        name_frame = ttk.LabelFrame(main_frame, text="Nome e Numero Cartelle", padding=(10, 5))
        name_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        ttk.Label(name_frame, text="Nome Cartella/e:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.folder_name_entry = ttk.Entry(name_frame, width=30)
        self.folder_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(name_frame, text="Numero Cartella/e:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.num_folders_spinbox = ttk.Spinbox(name_frame, from_=1, to=100, width=5)
        self.num_folders_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.num_folders_spinbox.set(1)


        # Frame per le impostazioni di creazione
        creation_frame = ttk.LabelFrame(main_frame, text="Modalità di Creazione", padding=(10, 5))
        creation_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        self.mode_var = tk.StringVar(value="incrementale")
        ttk.Radiobutton(creation_frame, text="Incrementale", variable=self.mode_var,
                        value="incrementale", command=self.on_mode_change).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(creation_frame, text="Multiplo", variable=self.mode_var,
                        value="multiplo", command=self.on_mode_change).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)


        self.nidifica_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(creation_frame, text="Nidifica", variable=self.nidifica_var,
                        command=self.update_preview).grid(row=0, column=1, padx=(20,5), pady=5, rowspan=2, sticky=tk.N)

        # Frame per il percorso
        path_frame = ttk.LabelFrame(main_frame, text="Percorso di destinazione", padding=(10, 5))
        path_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        ttk.Label(path_frame, text="Percorso:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.dir_entry = ttk.Entry(path_frame, width=40)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        select_button = ttk.Button(path_frame, text="Seleziona", command=self.select_directory)
        select_button.grid(row=0, column=2, padx=(5,0), pady=5)

        # Frame per l'anteprima
        preview_frame = ttk.LabelFrame(main_frame, text="Anteprima", padding=(10, 5))
        preview_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))

        self.preview_text = tk.Text(preview_frame, height=5, width=40, state="disabled")
        self.preview_text.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)


        # Bottone Crea Cartelle
        create_button = ttk.Button(main_frame, text="Genera Cartella/e", command=self.create_folders)
        create_button.grid(row=4, column=0, columnspan=3, pady=10)

        # Configura il grid per main_frame (spaziatura dinamica)
        main_frame.columnconfigure(0, weight=1)  # Colonna espandibile


        # Binding eventi
        self.folder_name_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        self.num_folders_spinbox.bind('<KeyRelease>', lambda e: self.update_preview())
        self.num_folders_spinbox.config(command=self.update_preview)


        # Usa l'icona per la preview (se presente)
        if self.folder_icon:
            preview_label = ttk.Label(preview_frame, image=self.folder_icon, compound=tk.LEFT) # aggiunta icona
            preview_label.grid(row=0, column=0, padx=(0,5), pady=5, sticky=tk.W) # aggiunta icona
            self.preview_text.grid(row=0, column=1, columnspan=2, padx=(0,5), pady=5, sticky=tk.W) # aggiunta icona

        else: # codice precedente senza icona, nel caso in cui non venga trovata
            ttk.Label(preview_frame).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W) # codice precedente
            self.preview_text.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W) # codice precedente
        # Bottone "Seleziona" con icona
        select_button = ttk.Button(path_frame, text="Seleziona", image=self.select_icon, compound=tk.LEFT, command=self.select_directory)
        select_button.grid(row=0, column=2, padx=(5, 0), pady=5)

        

    def create_tooltips(self):
        # Usa docstring multiline per tooltips più leggibili
        Tooltip(self.folder_name_entry, """Modalità Incrementale: crea cartelle incrementali con nome base comune.
Modalità Multiplo: crea cartelle con nomi differenti. Usa la virgola come separatore.""")
        Tooltip(self.num_folders_spinbox, "Numero di cartelle da creare (attiva solo in modalità Incrementale).")
        Tooltip(self.dir_entry, "Percorso di destinazione delle nuove cartelle.")


    def on_mode_change(self):
        is_incrementale = self.mode_var.get() == "incrementale"
        self.num_folders_spinbox.config(state="normal" if is_incrementale else "disabled")
        self.update_preview()

    def update_preview(self):
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        
        try:
            preview_text = self.get_preview_text()
            self.preview_text.insert(tk.END, preview_text)
        except ValueError as e:
            self.preview_text.insert(tk.END, f"Errore: {str(e)}")
        
        self.preview_text.config(state="disabled")

    def get_preview_text(self) -> str:
        folder_name = self.folder_name_entry.get().strip()
        if not folder_name:
            return "Inserire un nome per la cartella"

        if self.mode_var.get() == "incrementale":
            try:
                num_folders = int(self.num_folders_spinbox.get())
                folders = [f"{folder_name} {i}" for i in range(1, min(num_folders + 1, 6))]
                if num_folders > 5:
                    folders.append("...")
            except ValueError:
                return "Numero di cartelle non valido"
        else:
            folders = [name.strip() for name in folder_name.split(',') if name.strip()]
            if len(folders) > 5:
                folders = folders[:5] + ["..."]

        if not folders:
            return "Nessuna cartella da creare"

        if self.nidifica_var.get():
            return "Struttura nidificata:\n" + "\n  ".join(folders)
        return "Cartelle da creare:\n" + "\n".join(folders)

    def select_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.current_dir = selected_dir
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(tk.END, selected_dir)
            self.update_preview()

    def create_folders(self):
        if not self.validate_inputs():
            return

        try:
            self.do_create_folders()
            messagebox.showinfo("Successo", f"Cartelle create con successo in:\n{self.current_dir}")
        except OSError as e:
            messagebox.showerror("Errore", f"Impossibile creare le cartelle:\n{str(e)}")

    def validate_inputs(self) -> bool:
        if not self.folder_name_entry.get().strip():
            messagebox.showerror("Errore", "Inserire un nome per la cartella!")
            return False
        
        if not self.current_dir:
            messagebox.showerror("Errore", "Selezionare il percorso della cartella!")
            return False
        
        if self.mode_var.get() == "incrementale":
            try:
                int(self.num_folders_spinbox.get())
            except ValueError:
                messagebox.showerror("Errore", "Numero di cartelle non valido!")
                return False
        
        return True

    def do_create_folders(self):
        self.current_dir = self.dir_entry.get()  # Aggiorna current_dir dal contenuto dell'entry
        if not os.path.isdir(self.current_dir):
            raise OSError(f"Il percorso {self.current_dir} non esiste o non è una cartella")
        
        if self.mode_var.get() == "incrementale":
            num_folders = int(self.num_folders_spinbox.get())
            base_name = self.folder_name_entry.get().strip()
            folders = [f"{base_name} {i}" for i in range(1, num_folders + 1)]
        else:
            folders = [name.strip() for name in self.folder_name_entry.get().split(',') if name.strip()]

        if self.nidifica_var.get():
            current_path = self.current_dir
            for folder in folders:
                new_path = os.path.join(current_path, folder)
                os.makedirs(new_path)
                current_path = new_path
        else:
            for folder in folders:
                os.makedirs(os.path.join(self.current_dir, folder))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FolderCreator()
    app.run()