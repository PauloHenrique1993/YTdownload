# 🎵 YouTube Music Downloader (GUI em Python)

Aplicação com interface gráfica em **Tkinter** para baixar músicas diretamente do YouTube no formato **MP3 de alta qualidade** usando a biblioteca `yt-dlp`.

---

## ✅ Funcionalidades

- 🎧 Baixe vídeos ou playlists inteiras do YouTube
- 🔊 Converte automaticamente para **MP3 (320kbps)**
- 🖱 Interface gráfica simples com **Tkinter**
- 📁 Permite escolher a pasta de destino para salvar os arquivos
- 🧰 Integração com `yt-dlp` e `ffmpeg` para melhor desempenho

---

## 📦 Requisitos

- Python 3.7+
- `yt-dlp`
- `ffmpeg` (deve estar no PATH ou no mesmo diretório do `.exe`)

Instale as dependências com:

```
pip install yt-dlp
```

Baixe o ffmpeg e extraia o executável (ffmpeg.exe) para o mesmo diretório do projeto ou adicione ao PATH do sistema.

▶️ Como Executar o Script (Modo Dev)
Clone este repositório ou salve o script youtube_downloader.py.

Execute com Python:
```
python youtube_downloader.py
```

💾 Como Gerar um Executável .exe (Windows)
1. Instale o PyInstaller:
bash
```
pip install pyinstaller
```

2. Execute o comando para gerar o executável:
bash
```
pyinstaller --onefile --noconsole youtube_downloader.py
```

3. O arquivo .exe será gerado na pasta dist/.

Dica: Coloque o ffmpeg.exe na mesma pasta do .exe se o sistema não o reconhecer.

📁 Estrutura do Projeto
bash
```
📦 YouTubeDownloader/
├── youtube_downloader.py        # Script principal com GUI Tkinter
├── README.md                    # Documentação do projeto
├── dist/
│   └── youtube_downloader.exe  # Executável gerado pelo PyInstaller
├── build/                       # Arquivos temporários (auto gerados)
└── __pycache__/                # Cache do Python
```

📌 Observações
* Esta aplicação é voltada para uso pessoal e educacional.
* A biblioteca yt-dlp é uma fork moderna e mantida do youtube-dl, compatível com YouTube e outros sites.
* O ffmpeg é necessário para a conversão de áudio.

✨ Personalização
Você pode personalizar:
* Ícone do executável: <p>
  Adicione a flag --icon=icone.ico ao comando do PyInstaller.

* Nome do arquivo de saída:<p>
  Use --name="MeuApp" no comando de compilação.
