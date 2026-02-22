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
        self.root.geometry("650x480")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        # CONFIGURACIÓN DE RUTA PARA CUALQUIER USUARIO
        # Esto busca la carpeta 'Downloads' (Descargas) del sistema
        self.ruta_base = os.path.join(Path.home(), "Downloads", "AnyVideoPro_Files")
        
        # Si la carpeta no existe, la crea al instante
        if not os.path.exists(self.ruta_base):
            os.makedirs(self.ruta_base)

        self.setup_ui()

    def setup_ui(self):
        # Título y Estética
        tk.Label(self.root, text="AnyVideoPro", font=("Segoe UI", 28, "bold"), 
                 bg="#121212", fg="#00d2ff").pack(pady=(30, 5))
        
        tk.Label(self.root, text="Tus videos aparecerán en la carpeta de 'Descargas'", 
                 font=("Segoe UI", 10), bg="#121212", fg="#666666").pack(pady=(0, 30))

        # Entrada de URL
        frame_input = tk.Frame(self.root, bg="#121212")
        frame_input.pack(fill="x", padx=60)

        tk.Label(frame_input, text="Pega el enlace aquí:", bg="#121212", fg="#bbbbbb", font=("Segoe UI", 10)).pack(anchor="w")
        self.entry_url = tk.Entry(frame_input, font=("Segoe UI", 12), bg="#1e1e1e", fg="white", 
                                  insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333")
        self.entry_url.pack(fill="x", ipady=12, pady=8)

        # Opciones
        frame_options = tk.Frame(self.root, bg="#121212")
        frame_options.pack(pady=25)

        self.var_is_playlist = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_options, text="¿Es una lista de reproducción?", 
                       variable=self.var_is_playlist, bg="#121212", fg="#00d2ff",
                       selectcolor="#121212", font=("Segoe UI", 10)).grid(row=0, column=0, columnspan=2, pady=10)

        self.var_format = tk.StringVar(value="mp4")
        tk.Radiobutton(frame_options, text="Video (MP4)", variable=self.var_format, value="mp4",
                       bg="#121212", fg="white", selectcolor="#00d2ff").grid(row=1, column=0, padx=40)
        tk.Radiobutton(frame_options, text="Audio (MP3)", variable=self.var_format, value="mp3",
                       bg="#121212", fg="white", selectcolor="#00d2ff").grid(row=1, column=1, padx=40)

        # Botón Descargar
        self.btn_download = tk.Button(self.root, text="INICIAR DESCARGA", command=self.start_thread,
                                    bg="#00d2ff", fg="#000000", font=("Segoe UI", 12, "bold"),
                                    relief="flat", width=25, cursor="hand2")
        self.btn_download.pack(pady=15)

        self.lbl_status = tk.Label(self.root, text="Listo para descargar", bg="#121212", fg="#555555")
        self.lbl_status.pack(pady=10)

    def start_thread(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showwarning("Atención", "Pega un enlace antes de descargar.")
            return
        threading.Thread(target=self.download_process, args=(url,), daemon=True).start()

    def download_process(self, url):
        self.btn_download.config(state="disabled", text="DESCARGANDO...")
        self.lbl_status.config(text="🔍 Procesando...", fg="#00d2ff")
        
        is_playlist = self.var_is_playlist.get()
        format_choice = self.var_format.get()

        # Organización por carpetas (Canal o Playlist)
        if is_playlist:
            output_template = f"{self.ruta_base}/%(playlist_title)s/%(title)s.%(ext)s"
        else:
            output_template = f"{self.ruta_base}/%(uploader)s/%(title)s.%(ext)s"

        ydl_opts = {
            'format': 'best' if format_choice == 'mp4' else 'bestaudio/best',
            'outtmpl': output_template,
            'noplaylist': not is_playlist,
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.lbl_status.config(text="✅ ¡Completado!", fg="#00ff88")
            
            # ESTO ABRE LA CARPETA AUTOMÁTICAMENTE AL TERMINAR
            os.startfile(self.ruta_base)
            
            messagebox.showinfo("Éxito", "Descarga finalizada. Se ha abierto la carpeta de Descargas.")
        except Exception as e:
            self.lbl_status.config(text="❌ Error", fg="#ff4444")
            messagebox.showerror("Error", str(e))
        finally:
            self.btn_download.config(state="normal", text="INICIAR DESCARGA")
            self.entry_url.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnyVideoPro(root)
    root.mainloop()