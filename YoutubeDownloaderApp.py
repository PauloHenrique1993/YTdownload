import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from yt_dlp import YoutubeDL

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("400x200")

        # Elementos da interface
        Label(root, text="URL do YouTube:").pack(pady=5)
        self.url_entry = Entry(root, width=50)
        self.url_entry.pack(pady=5)

        Label(root, text="Pasta de destino:").pack(pady=5)
        self.folder_entry = Entry(root, width=50)
        self.folder_entry.pack(pady=5)

        Button(root, text="Selecionar Pasta", command=self.selecionar_pasta).pack(pady=5)
        Button(root, text="Baixar Música", command=self.baixar_musica).pack(pady=10)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, pasta)

    def baixar_musica(self):
        url = self.url_entry.get().strip()
        pasta = self.folder_entry.get().strip()

        if not url:
            messagebox.showerror("Erro", "Por favor, insira a URL do vídeo.")
            return

        if not pasta:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de destino.")
            return

        if not os.path.exists(pasta):
            messagebox.showerror("Erro", "A pasta selecionada não existe.")
            return

        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }
            ],
        }

        try:
            with YoutubeDL(opcoes) as ydl:
                ydl.download([url])
            messagebox.showinfo("Sucesso", "Música baixada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
