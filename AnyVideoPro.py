import tkinter as tk
from tkinter import messagebox
import yt_dlp
import threading
import os
from pathlib import Path

class AnyVideoPro:
    def __init__(self, root):
        self.root = root
        self.root.title("AnyVideoPro - Descargador Universal")
        self.root.geometry("600x450")
        self.root.configure(bg="#121212")
        
        # Ruta: C:/Users/TuUsuario/Descargas_YT
        self.ruta_base = os.path.join(Path.home(), "Descargas_YT")
        if not os.path.exists(self.ruta_base):
            os.makedirs(self.ruta_base)

        self.setup_ui()

    def setup_ui(self):
        # Título
        tk.Label(self.root, text="AnyVideoPro", font=("Arial", 28, "bold"), bg="#121212", fg="#00d2ff").pack(pady=20)
        
        # Entrada de URL
        tk.Label(self.root, text="Pega el enlace aquí:", bg="#121212", fg="white").pack()
        self.entry_url = tk.Entry(self.root, font=("Arial", 12), width=50, bg="#1e1e1e", fg="white", insertbackground="white")
        self.entry_url.pack(pady=10)

        # Opciones
        self.var_is_playlist = tk.BooleanVar()
        tk.Checkbutton(self.root, text="¿Es una lista de reproducción?", variable=self.var_is_playlist, 
                       bg="#121212", fg="#00d2ff", selectcolor="#121212", activebackground="#121212").pack()

        self.var_format = tk.StringVar(value="mp4")
        tk.Radiobutton(self.root, text="Video (MP4)", variable=self.var_format, value="mp4", bg="#121212", fg="white").pack()
        tk.Radiobutton(self.root, text="Audio (MP3)", variable=self.var_format, value="mp3", bg="#121212", fg="white").pack()

        # Botón
        self.btn = tk.Button(self.root, text="DESCARGAR", command=self.start_thread, 
                             bg="#00d2ff", fg="black", font=("Arial", 12, "bold"), width=20)
        self.btn.pack(pady=20)

        self.lbl_status = tk.Label(self.root, text="Listo", bg="#121212", fg="#555")
        self.lbl_status.pack()

    def start_thread(self):
        url = self.entry_url.get().strip()
        if url:
            threading.Thread(target=self.download, args=(url,), daemon=True).start()
        else:
            messagebox.showwarning("Error", "Pega un link")

    def download(self, url):
        self.btn.config(state="disabled", text="Descargando...")
        self.lbl_status.config(text="Procesando...", fg="#00d2ff")
        
        formato = self.var_format.get()
        # Plantilla: Si es lista usa el título de la lista, si no, el nombre del canal
        plantilla = f"{self.ruta_base}/%(playlist_title)s/%(title)s.%(ext)s" if self.var_is_playlist.get() else f"{self.ruta_base}/%(uploader)s/%(title)s.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best' if formato == 'mp3' else 'best',
            'outtmpl': plantilla,
            'noplaylist': not self.var_is_playlist.get(),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.lbl_status.config(text="✅ ¡Completado!", fg="#00ff88")
            messagebox.showinfo("Éxito", f"Guardado en:\n{self.ruta_base}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.lbl_status.config(text="❌ Error", fg="red")
        finally:
            self.btn.config(state="normal", text="DESCARGAR")

if __name__ == "__main__":
    app = AnyVideoPro(tk.Tk())
    app.root.mainloop()