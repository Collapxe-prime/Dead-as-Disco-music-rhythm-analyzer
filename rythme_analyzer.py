import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import imageio_ffmpeg
import librosa
import random
import math
import ctypes

# ── Путь к ресурсам внутри .exe ───────────────────────────────────────────────
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

# Подключаем ffmpeg автоматически
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

# ── Цвета ─────────────────────────────────────────────────────────────────────
BG_COLOR       = "#0a0a0f"
ACCENT_COLOR   = "#00ffcc"
TEXT_COLOR     = "#ffffff"
BTN_BG         = "#111122"
BTN_FG         = "#00ffcc"
BTN_ACTIVE     = "#00ccaa"

# ── Переводы ──────────────────────────────────────────────────────────────────
LANGUAGES = {
    "ru": {
        "title":       "RHYTHM ANALYZER",
        "btn":         "▶  ВЫБРАТЬ ФАЙЛ",
        "placeholder": "Выбери аудиофайл для анализа",
        "loading":     "Анализирую...",
        "error":       "Ошибка",
        "error_load":  "Не удалось загрузить файл:\n",
        "file":        "Файл",
        "tempo":       "Темп",
        "pattern":     "Паттерн",
        "confidence":  "Уверен.",
        "stability":   "Стабильность",
        "duration":    "Длина",
        "samplerate":  "Частота",
        "patterns": {
            "slow":   "медленный балладный",
            "medium": "средний поп/рок",
            "fast":   "быстрый джаз/рок",
        },
        "stability_levels": {
            "very_stable": "очень стабильный",
            "stable":      "стабильный",
            "moderate":    "умеренно нестабильный",
            "unstable":    "нестабильный",
            "no_data":     "недостаточно данных",
        }
    },
    "en": {
        "title":       "RHYTHM ANALYZER",
        "btn":         "▶  CHOOSE FILE",
        "placeholder": "Choose an audio file to analyze",
        "loading":     "Analyzing...",
        "error":       "Error",
        "error_load":  "Failed to load file:\n",
        "file":        "File",
        "tempo":       "Tempo",
        "pattern":     "Pattern",
        "confidence":  "Confidence",
        "stability":   "Stability",
        "duration":    "Duration",
        "samplerate":  "Sample rate",
        "patterns": {
            "slow":   "slow ballad",
            "medium": "mid pop/rock",
            "fast":   "fast jazz/rock",
        },
        "stability_levels": {
            "very_stable": "very stable",
            "stable":      "stable",
            "moderate":    "moderately unstable",
            "unstable":    "unstable",
            "no_data":     "insufficient data",
        }
    }
}

current_lang = "en"

# ── Частицы ───────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, width, height):
        self.reset(width, height)

    def reset(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.radius = random.uniform(1, 3)
        self.speed = random.uniform(0.3, 1.0)
        self.angle = random.uniform(0, 2 * math.pi)
        self.alpha = random.randint(80, 200)

    def move(self, width, height):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.reset(width, height)


# ── Стабильность ──────────────────────────────────────────────────────────────
def calc_rhythm_stability(y, sr, lang: str) -> tuple[float, str]:
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    levels = LANGUAGES[lang]["stability_levels"]

    if len(beat_times) < 2:
        return 0.0, levels["no_data"]

    intervals = [(beat_times[i+1] - beat_times[i]) * 1000
                 for i in range(len(beat_times)-1)]
    avg = sum(intervals) / len(intervals)
    variance = sum((x - avg) ** 2 for x in intervals) / len(intervals)
    std = variance ** 0.5

    if std < 10:
        label = levels["very_stable"]
    elif std < 30:
        label = levels["stable"]
    elif std < 60:
        label = levels["moderate"]
    else:
        label = levels["unstable"]

    return round(std, 1), label


# ── Анализ ────────────────────────────────────────────────────────────────────
def analyze_audio(file_path: str, result_var: tk.StringVar,
                  btn: tk.Button, lang: str) -> None:
    t = LANGUAGES[lang]

    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
    except Exception as e:
        messagebox.showerror(t["error"], t["error_load"] + str(e))
        btn.config(state="normal")
        return

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo.item())
    cv, stability = calc_rhythm_stability(y, sr, lang)

    patterns = t["patterns"]
    if tempo < 80:
        pattern = patterns["slow"]
        confidence = round(min(1.0, (80 - tempo) / 80), 2)
    elif tempo < 120:
        pattern = patterns["medium"]
        confidence = round(min(1.0, (tempo - 80) / 40), 2)
    else:
        pattern = patterns["fast"]
        confidence = round(min(1.0, (tempo - 120) / 60), 2)

    duration = librosa.get_duration(y=y, sr=sr)

    result_var.set(
        f"{t['file']}:          {os.path.basename(file_path)}\n"
        f"{t['tempo']}:         {tempo:.1f} BPM\n"
        f"{t['pattern']}:       {pattern}\n"
        f"{t['confidence']}:    {confidence * 100:.1f}%\n"
        f"{t['stability']}:     {stability} (±{cv} ms)\n"
        f"{t['duration']}:      {duration:.1f} sec\n"
        f"{t['samplerate']}:    {sr} Hz"
    )
    btn.config(state="normal")


def open_file(result_var: tk.StringVar, btn: tk.Button, lang: str) -> None:
    t = LANGUAGES[lang]
    file_path = filedialog.askopenfilename(
        title=t["placeholder"],
        filetypes=[("Audio files", "*.mp3 *.wav *.flac *.ogg *.aac *.m4a"),
                   ("All files", "*.*")]
    )
    if not file_path:
        return

    result_var.set(t["loading"])
    btn.config(state="disabled")

    thread = threading.Thread(
        target=analyze_audio, args=(file_path, result_var, btn, lang))
    thread.daemon = True
    thread.start()


# ── Главное окно ──────────────────────────────────────────────────────────────
def main() -> None:
    global current_lang

    root = tk.Tk()
    root.title("Rhythm Analyzer")
    root.geometry("480x380")
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # Центрирование
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 480) // 2
    y = (root.winfo_screenheight() - 380) // 2
    root.geometry(f"480x380+{x}+{y}")

    # Иконка
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("RhythmAnalyzer")
    try:
        root.iconbitmap(resource_path("icon.ico"))
    except Exception:
        pass

    W, H = 480, 380

    # Canvas для анимированного фона
    canvas = tk.Canvas(root, width=W, height=H, bg=BG_COLOR,
                       highlightthickness=0)
    canvas.place(x=0, y=0)

    particles = [Particle(W, H) for _ in range(60)]

    def animate():
        canvas.delete("particle")
        for p in particles:
            p.move(W, H)
            r = p.radius
            brightness = int(p.alpha / 255 * 200)
            color = f"#{0:02x}{brightness:02x}{brightness // 2:02x}"
            canvas.create_oval(p.x - r, p.y - r, p.x + r, p.y + r,
                                fill=color, outline="", tags="particle")
        root.after(30, animate)

    animate()

    # ── Переключатель языка ───────────────────────────────────────────────────
    lang_var = tk.StringVar(value="EN")

    result_var = tk.StringVar(value=LANGUAGES[current_lang]["placeholder"])

    btn = tk.Button(root, text=LANGUAGES[current_lang]["btn"],
                    font=("Courier", 11, "bold"),
                    fg=BTN_FG, bg=BTN_BG,
                    activeforeground=TEXT_COLOR, activebackground=BTN_ACTIVE,
                    relief="flat", bd=0, padx=20, pady=8, cursor="hand2")

    def toggle_lang():
        global current_lang
        current_lang = "en" if current_lang == "ru" else "ru"
        lang_var.set("EN" if current_lang == "en" else "RU")
        btn.config(text=LANGUAGES[current_lang]["btn"])
        result_var.set(LANGUAGES[current_lang]["placeholder"])

    lang_btn = tk.Button(root, textvariable=lang_var,
                         font=("Courier", 9, "bold"),
                         fg=ACCENT_COLOR, bg=BTN_BG,
                         activeforeground=TEXT_COLOR, activebackground=BTN_ACTIVE,
                         relief="flat", bd=0, padx=8, pady=4, cursor="hand2",
                         command=toggle_lang)
    lang_btn.place(x=W - 52, y=10)

    # ── Заголовок ─────────────────────────────────────────────────────────────
    tk.Label(root, text="♪  RHYTHM ANALYZER",
             font=("Courier", 17, "bold"),
             fg=ACCENT_COLOR, bg=BG_COLOR).place(relx=0.5, y=18, anchor="n")

    tk.Canvas(root, width=W - 60, height=2, bg=ACCENT_COLOR,
              highlightthickness=0).place(relx=0.5, y=58, anchor="n")

    # ── Кнопка выбора файла ───────────────────────────────────────────────────
    btn.place(relx=0.5, y=78, anchor="n")
    btn.config(command=lambda: open_file(result_var, btn, current_lang))

    # ── Панель результатов ────────────────────────────────────────────────────
    tk.Canvas(root, width=W - 56, height=222,
              bg="#0d0d1a", highlightthickness=1,
              highlightbackground=ACCENT_COLOR).place(relx=0.5, y=128, anchor="n")

    result_frame = tk.Frame(root, bg="#0d0d1a")
    result_frame.place(relx=0.5, y=129, anchor="n", width=W - 60, height=220)

    tk.Label(result_frame, textvariable=result_var,
             font=("Courier", 10),
             fg=TEXT_COLOR, bg="#0d0d1a",
             justify="left", anchor="nw",
             padx=15, pady=15).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()