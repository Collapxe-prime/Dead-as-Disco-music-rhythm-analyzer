# 🎵 Dead as Disco — Rhythm Analyzer

---

🇬🇧 **English** | 🇷🇺 [Русский](#-русский)

---

## 🇬🇧 English

A tool for analyzing your music before adding it to **Dead as Disco**.  
Supports **MP3, WAV, FLAC, OGG, AAC, M4A** and more.

### 📥 Download

Head to the [**Releases**](../../releases/latest) page to download the latest `.exe` — no installation required.

### ✨ Features

- 🎧 Detects **tempo (BPM)**
- 🥁 Identifies **rhythm pattern** (slow ballad / mid pop-rock / fast jazz-rock)
- 📊 Measures **rhythm stability** (deviation between beats in ms)
- ⏱ Shows **duration** and **sample rate**
- 🌐 **English / Russian** language toggle
- 🎮 Animated particle background UI

### 🖥 Running from source

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
python rythme_analyzer.py
```

### 📦 Build .exe yourself

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." rythme_analyzer.py
```

### 🛠 Tech stack

- [librosa](https://librosa.org) — audio analysis
- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) — MP3 decoding
- [tkinter](https://docs.python.org/3/library/tkinter.html) — GUI

### 📄 License

MIT

---

## 🇷🇺 Русский

Инструмент для анализа своей музыки перед добавлением в **Dead as Disco**.  
Поддерживает **MP3, WAV, FLAC, OGG, AAC, M4A** и другие форматы.

### 📥 Скачать

Перейди на страницу [**Releases**](../../releases/latest) чтобы скачать последний `.exe` — установка не требуется.

### ✨ Возможности

- 🎧 Определяет **темп (BPM)**
- 🥁 Определяет **ритмический паттерн** (медленный балладный / средний поп-рок / быстрый джаз-рок)
- 📊 Измеряет **стабильность ритма** (отклонение между ударами в мс)
- ⏱ Показывает **длительность** и **частоту дискретизации**
- 🌐 Переключение языка **English / Русский**
- 🎮 Анимированный интерфейс с частицами

### 🖥 Запуск из исходного кода

**Требования:** Python 3.10+

```bash
pip install -r requirements.txt
python rythme_analyzer.py
```

### 📦 Собрать .exe самостоятельно

```bash
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." rythme_analyzer.py
```

### 🛠 Технологии

- [librosa](https://librosa.org) — анализ аудио
- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) — декодирование MP3
- [tkinter](https://docs.python.org/3/library/tkinter.html) — графический интерфейс

### 📄 Лицензия

MIT

---

## 🤖 About / О проекте

This app was fully **Vibe Coded** using [Claude Sonnet 4.6](https://claude.ai).

Это приложение полностью **Vibe Coded** с использованием [Claude Sonnet 4.6](https://claude.ai).
