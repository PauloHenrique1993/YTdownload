import os
import threading
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar, Radiobutton, Frame
from yt_dlp import YoutubeDL

class InstagramDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Downloader")
        # ❌ Removido geometry fixo -> Tkinter calcula automaticamente
        # self.root.geometry("500x260")

        Label(root, text="URL do Instagram (post/reel/igtv):").pack(pady=(10, 3))
        self.url_var = StringVar()
        self.url_entry = Entry(root, textvariable=self.url_var, width=70)
        self.url_entry.pack(pady=3)

        Label(root, text="Pasta de destino:").pack(pady=(8, 3))
        self.folder_var = StringVar()
        self.folder_entry = Entry(root, textvariable=self.folder_var, width=70)
        self.folder_entry.pack(pady=3)

        Button(root, text="Selecionar Pasta", command=self.selecionar_pasta).pack(pady=6)

        # Opção de escolha: vídeo ou áudio (lado a lado)
        self.download_type = StringVar(value="video")
        Label(root, text="Escolha o formato:").pack(pady=(8, 3))

        frame_format = Frame(root)
        frame_format.pack(pady=3)

        Radiobutton(frame_format, text="Vídeo (MP4)", variable=self.download_type, value="video").pack(side="left", padx=10)
        Radiobutton(frame_format, text="Áudio (MP3)", variable=self.download_type, value="audio").pack(side="left", padx=10)

        self.status_label = Label(root, text="", anchor="w", width=70)
        self.status_label.pack(pady=(6, 0))

        # Botão agora aparece sempre
        Button(root, text="Baixar", command=self.iniciar_download_thread).pack(pady=10)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.folder_var.set(pasta)

    def iniciar_download_thread(self):
        t = threading.Thread(target=self.baixar)
        t.daemon = True
        t.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                pct = downloaded / total * 100
                self.status_label.config(text=f"Baixando... {pct:.1f}%")
        elif d['status'] == 'finished':
            self.status_label.config(text="Finalizando...")

    def baixar(self):
        url = self.url_var.get().strip()
        pasta = self.folder_var.get().strip()

        if not url:
            messagebox.showerror("Erro", "Por favor, insira a URL.")
            return
        if not pasta:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de destino.")
            return
        if not os.path.exists(pasta):
            messagebox.showerror("Erro", "A pasta selecionada não existe.")
            return

        # Configurações conforme a escolha do usuário
        if self.download_type.get() == "video":
            opcoes = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(pasta, '%(uploader)s_%(id)s_%(title).100s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
            }
        else:  # apenas áudio
            opcoes = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(pasta, '%(uploader)s_%(id)s_%(title).100s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ]
            }

        self.status_label.config(text="Iniciando download...")
        try:
            with YoutubeDL(opcoes) as ydl:
                ydl.download([url])
            self.status_label.config(text="Concluído!")
            messagebox.showinfo("Sucesso", "Download finalizado com sucesso!")
        except Exception as e:
            self.status_label.config(text=f"Erro: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    root = Tk()
    app = InstagramDownloaderApp(root)
    root.mainloop()
