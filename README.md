# 🎵 Dead as Disco — Rhythm Analyzer

A lightweight desktop tool for analyzing the rhythmic structure of audio files.  
Supports **MP3, WAV, FLAC, OGG, AAC, M4A** and more.

---

## ✨ Features

- 🎧 Detects **tempo (BPM)**
- 🥁 Identifies **rhythm pattern** (slow ballad / mid pop-rock / fast jazz-rock)
- 📊 Measures **rhythm stability** (deviation between beats in ms)
- ⏱ Shows **duration** and **sample rate**
- 🌐 **English / Russian** language toggle
- 🎮 Animated particle background UI

---

## 📥 Download

Head to the [**Releases**](../../releases/latest) page to download the latest `.exe` — no installation required.

---

## 🖥 Running from source

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
python rythme_analyzer.py
```

---

## 📦 Build .exe yourself

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." rythme_analyzer.py
```

---

## 🛠 Tech stack

- [librosa](https://librosa.org) — audio analysis
- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) — MP3 decoding
- [tkinter](https://docs.python.org/3/library/tkinter.html) — GUI

---

## 📄 License

MIT
