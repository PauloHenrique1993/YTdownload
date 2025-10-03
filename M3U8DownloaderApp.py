import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ===============================
# Funções de Download
# ===============================
def baixar_segmento(url, pasta, idx):
    nome_arquivo = os.path.join(pasta, f"seg_{idx}.ts")
    try:
        r = requests.get(url, timeout=20, stream=True)
        with open(nome_arquivo, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return idx
    except Exception as e:
        print(f"❌ Erro no segmento {idx}: {e}")
        return None

def baixar_m3u8(url, saida, pasta, max_threads=10, app=None):
    try:
        r = requests.get(url, timeout=10)
        linhas = [l.strip() for l in r.text.splitlines() if l and not l.startswith("#")]

        # cria pasta temporária
        os.makedirs(pasta, exist_ok=True)

        if app:
            app.atualizar_status(url, "Baixando...")

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futuros = {executor.submit(baixar_segmento, link, pasta, i): i for i, link in enumerate(linhas)}
            for futuro in as_completed(futuros):
                idx = futuros[futuro]
                if futuro.result() is not None:
                    print(f"✅ Segmento {idx} baixado")

        # juntar tudo em um único arquivo
        with open(saida, "wb") as out:
            for i in range(len(linhas)):
                with open(os.path.join(pasta, f"seg_{i}.ts"), "rb") as f:
                    out.write(f.read())

        if app:
            app.mover_para_concluidos(url)

    except Exception as e:
        if app:
            app.atualizar_status(url, f"Erro: {e}")
        print(f"❌ Erro no download: {e}")

# ===============================
# Interface Tkinter
# ===============================
class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M3U8 Downloader com Fila")
        self.root.geometry("650x500")
        self.root.configure(bg="#f0f0f0")

        # Campos de entrada
        tk.Label(root, text="URL do vídeo (.m3u8):", bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_url = tk.Entry(root, width=70)
        self.entry_url.pack(padx=10, pady=5)

        tk.Label(root, text="Nome do arquivo de saída:", bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_nome = tk.Entry(root, width=70)
        self.entry_nome.pack(padx=10, pady=5)

        tk.Label(root, text="Pasta para salvar:", bg="#f0f0f0").pack(anchor="w", padx=10, pady=(10, 0))
        frame_pasta = tk.Frame(root, bg="#f0f0f0")
        frame_pasta.pack(fill="x", padx=10)
        self.entry_pasta = tk.Entry(frame_pasta, width=55)
        self.entry_pasta.pack(side="left", padx=(0, 5), pady=5)
        tk.Button(frame_pasta, text="📂", command=self.selecionar_pasta).pack(side="left")

        # Botão
        tk.Button(root, text="Adicionar à Fila", command=self.adicionar_fila, bg="#4CAF50", fg="white").pack(pady=10)

        # Área da Fila
        frame_fila = tk.Frame(root, bg="#f0f0f0")
        frame_fila.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(frame_fila, text="📥 Downloads na Fila:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lista_fila = tk.Listbox(frame_fila, height=7, width=90, bg="white")
        self.lista_fila.pack(fill="x", pady=5)

        tk.Label(frame_fila, text="✅ Downloads Concluídos:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lista_concluidos = tk.Listbox(frame_fila, height=7, width=90, bg="white")
        self.lista_concluidos.pack(fill="x", pady=5)

        self.downloads = {}  # {url: status}

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.entry_pasta.delete(0, tk.END)
            self.entry_pasta.insert(0, pasta)

    def adicionar_fila(self):
        url = self.entry_url.get().strip()
        nome = self.entry_nome.get().strip()
        pasta = self.entry_pasta.get().strip()

        if not url or not nome or not pasta:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        saida = os.path.join(pasta, nome + ".mp4")
        self.lista_fila.insert(tk.END, f"{url} - Aguardando...")
        self.downloads[url] = "Aguardando"

        threading.Thread(target=baixar_m3u8, args=(url, saida, "tmp_segments", 10, self), daemon=True).start()

    def atualizar_status(self, url, status):
        for i in range(self.lista_fila.size()):
            item = self.lista_fila.get(i)
            if item.startswith(url):
                self.lista_fila.delete(i)
                self.lista_fila.insert(i, f"{url} - {status}")
                break

    def mover_para_concluidos(self, url):
        for i in range(self.lista_fila.size()):
            item = self.lista_fila.get(i)
            if item.startswith(url):
                self.lista_fila.delete(i)
                break
        self.lista_concluidos.insert(tk.END, f"{url} - Concluído ✅")

# ===============================
# Rodar Aplicação
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
