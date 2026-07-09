import json
import urllib.request
import random
import tkinter as tk
import time 
from gtts import gTTS
import pygame
import threading
import os

pygame.mixer.init()

def get_random(max_number):
    return random.randint(0, max_number)

def load_words():
    levels = ["n5", "n4", "n3", "n2", "n1"]
    n5 = []
    n4 = []
    n3 = []
    n2 = []
    n1 = []

    all_vocab = []
    

    for level in levels:
        url = f"https://raw.githubusercontent.com/wkei/jlpt-vocab-api/main/data-source/db/{level}.json"

        with urllib.request.urlopen(url) as response:
            vocab = json.load(response)

        if level == 'n5':
            n5.extend(vocab)
        if level == 'n4':
            n4.extend(vocab)
        if level == 'n3':
            n3.extend(vocab)
        if level == 'n2':
            n2.extend(vocab)
        if level == 'n1':
            n1.extend(vocab)
        
        all_vocab.extend(vocab)

        print(f"Loaded {level}: {len(vocab)} words")

    print(f"Total words: {len(all_vocab)}")
    
    return n5, n4, n3, n2, n1, all_vocab

class words:
    n5, n4, n3, n2, n1, all_vocab  = load_words()


def create_random_word_array(vocab_list):
    shuffled_words = vocab_list.copy()
    random.shuffle(shuffled_words)
    return shuffled_words


level_dict = {
    "N5": words.n5,
    "N4": words.n4,
    "N3": words.n3,
    "N2": words.n2,
    "N1": words.n1,
    "ALL": words.all_vocab
}

if __name__ == "__main__":

    current_level = "N5"
    word_array = create_random_word_array(level_dict[current_level])
    current_index = 0
    selected_word = word_array[current_index]

    font_offset = 0
    alpha_value = 0.7

    audio_volume = 0.7
    audio_repeat = 1

    # Timer settings
    timer = 5000  
    timer_running = True
    timer_after_id = None

    root = tk.Tk()
        
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", alpha_value)
    root.geometry("320x170+100+100")
    root.configure(bg="black")

    def update_selected_word():
        global selected_word

        selected_word = word_array[current_index]

        furigana_text = selected_word.get("furigana", "")
        romaji_text = selected_word.get("romaji", "")
        word_text = selected_word.get("word", "")
        meaning_text = selected_word.get("meaning", "")

        furigana_label.config(text=furigana_text)
        romaji_label.config(text=romaji_text)
        word_label.config(text=word_text)
        meaning_label.config(text=meaning_text)

        status_label.config(
            text=f"{current_level}  {current_index + 1} / {len(word_array)}"
        )

        play_audio()

    def reset_word_array(level):
        global current_level, word_array, current_index

        current_level = level
        word_array = create_random_word_array(level_dict[level])
        current_index = 0
        update_selected_word()

    def next_word():
        global current_index

        if current_index < len(word_array) - 1:
            current_index += 1
        else:
            reset_word_array(current_level)

        update_selected_word()

    def prev_word():
        global current_index

        if current_index > 0:
            current_index -= 1

        update_selected_word()

    def update_ui_fonts():
        furigana_label.config(font=("Arial", max(4, 8 + font_offset)))
        romaji_label.config(font=("Arial", max(6, 10 + font_offset)))
        word_label.config(font=("Arial", max(8, 18 + font_offset)))
        meaning_label.config(font=("Arial", max(6, 12 + font_offset)))

    
   # =========================
    # Audio function
    # =========================
    def play_audio():
        def run_audio():
            word_to_say = selected_word.get("word", "")
            if not word_to_say:
                return 
                
            try:
                tts = gTTS(text=word_to_say, lang='ja')
                tts.save("temp_word.mp3")

                for _ in range(audio_repeat):
                    pygame.mixer.music.load("temp_word.mp3")
                    pygame.mixer.music.set_volume(audio_volume) 
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                        
                    time.sleep(0.5) 
                    
                pygame.mixer.music.unload()
                os.remove("temp_word.mp3")
                
            except Exception as e:
                print(f"Could not play audio: {e}")

        threading.Thread(target=run_audio, daemon=True).start()

    # =========================
    # Timer functions
    # =========================

    def set_timer(seconds):
        global timer

        timer = int(seconds) * 1000

        if timer_running:
            restart_timer()

    def auto_next_word():
        global timer_after_id

        if timer_running:
            next_word()
            timer_after_id = root.after(timer, auto_next_word)

    def start_timer():
        global timer_running, timer_after_id

        if not timer_running:
            timer_running = True
            timer_after_id = root.after(timer, auto_next_word)

    def stop_timer():
        global timer_running, timer_after_id

        timer_running = False

        if timer_after_id is not None:
            root.after_cancel(timer_after_id)
            timer_after_id = None

    def restart_timer():
        global timer_after_id

        if timer_after_id is not None:
            root.after_cancel(timer_after_id)
            timer_after_id = None

        if timer_running:
            timer_after_id = root.after(timer, auto_next_word)

    def toggle_timer():
        if timer_running:
            stop_timer()
            timer_button.config(text="▶")
        else:
            start_timer()
            timer_button.config(text="⏸")

    def close_app():
        stop_timer()
        root.destroy()

    # =========================
    # Settings window
    # =========================

    def open_settings():
        settings_window = tk.Toplevel(root)
        settings_window.overrideredirect(True)
        settings_window.geometry("220x700+450+100")
        settings_window.configure(bg="black")
        settings_window.attributes("-topmost", True)

        def settings_start_move(event):
            settings_window.x = event.x
            settings_window.y = event.y

        def settings_move_window(event):
            x = event.x_root - settings_window.x
            y = event.y_root - settings_window.y
            settings_window.geometry(f"+{x}+{y}")

        title_bar = tk.Frame(settings_window, bg="gray15", height=28)
        title_bar.pack(fill="x")

        title_label = tk.Label(
            title_bar,
            text="Settings",
            font=("Arial", 10),
            fg="white",
            bg="gray15"
        )
        title_label.pack(side="left", padx=8)

        title_close = tk.Button(
            title_bar,
            text="X",
            command=settings_window.destroy,
            fg="white",
            bg="red",
            borderwidth=0
        )
        title_close.pack(side="right", padx=4, pady=3)

        title_bar.bind("<Button-1>", settings_start_move)
        title_bar.bind("<B1-Motion>", settings_move_window)
        title_label.bind("<Button-1>", settings_start_move)
        title_label.bind("<B1-Motion>", settings_move_window)

        level_frame = tk.Frame(settings_window, bg="black")
        level_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            level_frame,
            text="Select JLPT Level",
            font=("Arial", 11),
            fg="white",
            bg="black"
        ).pack(pady=5)

        for level in ["N5", "N4", "N3", "N2", "N1", "ALL"]:
            btn = tk.Button(
                level_frame,
                text=level,
                font=("Arial", 10),
                fg="white",
                bg="gray20",
                borderwidth=0,
                command=lambda lv=level: reset_word_array(lv)
            )
            btn.pack(fill="x", padx=20, pady=2)

        # Font size settings
        font_frame = tk.Frame(settings_window, bg="black")
        font_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            font_frame,
            text="Font Size Offset",
            font=("Arial", 11),
            fg="white",
            bg="black"
        ).pack()

        def on_font_change(val):
            global font_offset
            font_offset = int(float(val))
            update_ui_fonts()

        font_scale = tk.Scale(
            font_frame,
            from_=-5,
            to=20,
            orient="horizontal",
            fg="white",
            bg="black",
            highlightthickness=0,
            command=on_font_change
        )
        font_scale.set(font_offset)
        font_scale.pack(fill="x", padx=10)

        # Transparency settings
        trans_frame = tk.Frame(settings_window, bg="black")
        trans_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            trans_frame,
            text="Window Transparency",
            font=("Arial", 11),
            fg="white",
            bg="black"
        ).pack()

        def on_alpha_change(val):
            global alpha_value
            alpha_value = float(val)
            root.attributes("-alpha", alpha_value)

        alpha_scale = tk.Scale(
            trans_frame,
            from_=0.1,
            to=1.0,
            resolution=0.05,
            orient="horizontal",
            fg="white",
            bg="black",
            highlightthickness=0,
            command=on_alpha_change
        )
        alpha_scale.set(alpha_value)
        alpha_scale.pack(fill="x", padx=10)

        # Timer settings
        timer_frame = tk.Frame(settings_window, bg="black")
        timer_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            timer_frame,
            text="Auto Next Timer Seconds",
            font=("Arial", 11),
            fg="white",
            bg="black"
        ).pack()

        def on_timer_change(val):
            set_timer(int(float(val)))

        timer_scale = tk.Scale(
            timer_frame,
            from_=5,
            to=120,
            orient="horizontal",
            fg="white",
            bg="black",
            highlightthickness=0,
            command=on_timer_change
        )
        timer_scale.set(timer // 1000)
        timer_scale.pack(fill="x", padx=10)

        # Audio Volume settings
        vol_frame = tk.Frame(settings_window, bg="black")
        vol_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(vol_frame, text="Audio Volume", font=("Arial", 11), fg="white", bg="black").pack()

        def on_vol_change(val):
            global audio_volume
            audio_volume = float(val)
            pygame.mixer.music.set_volume(audio_volume)

        vol_scale = tk.Scale(
            vol_frame, from_=0.0, to=1.0, resolution=0.1, orient="horizontal",
            fg="white", bg="black", highlightthickness=0, command=on_vol_change
        )
        vol_scale.set(audio_volume)
        vol_scale.pack(fill="x", padx=10)

        # Repeat Audio Settings
        rep_frame = tk.Frame(settings_window, bg="black")
        rep_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(rep_frame, text="Audio Repeat Times", font=("Arial", 11), fg="white", bg="black").pack()

        def on_rep_change(val):
            global audio_repeat
            audio_repeat = int(val)

        rep_scale = tk.Scale(
            rep_frame, from_=1, to=3, orient="horizontal",
            fg="white", bg="black", highlightthickness=0, command=on_rep_change
        )
        rep_scale.set(audio_repeat)
        rep_scale.pack(fill="x", padx=10)

        close_btn = tk.Button(
            settings_window,
            text="Close Settings",
            font=("Arial", 10),
            fg="white",
            bg="gray30",
            borderwidth=0,
            command=settings_window.destroy
        )
        close_btn.pack(pady=15, fill="x", padx=40)

    # =========================
    # Main UI labels
    # =========================

    furigana_label = tk.Label(
        root,
        text="",
        font=("Arial", 8),
        fg="white",
        bg="black"
    )
    furigana_label.pack(expand=True, fill="both")

    word_label = tk.Label(
        root,
        text="",
        font=("Arial", 18),
        fg="white",
        bg="black"
    )
    word_label.pack(expand=True, fill="both")

    romaji_label = tk.Label(
        root,
        text="",
        font=("Arial", 10),
        fg="lightgray", 
        bg="black"
    )
    romaji_label.pack(expand=True, fill="both")

    meaning_label = tk.Label(
        root,
        text="",
        font=("Arial", 12),
        fg="white",
        bg="black",
        wraplength=300
    )
    meaning_label.pack(expand=True, fill="both")

    status_label = tk.Label(
        root,
        text="",
        font=("Arial", 8),
        fg="gray",
        bg="black"
    )
    status_label.pack(fill="x")

    # =========================
    # Main buttons
    # =========================

    prev_button = tk.Button(
        root,
        text="<",
        command=prev_word,
        fg="white",
        bg="black",
        borderwidth=0
    )
    prev_button.place(x=5, y=5, width=25, height=25)

    timer_button = tk.Button(
        root,
        text="⏸",
        command=toggle_timer,
        fg="white",
        bg="black",
        borderwidth=0
    )
    timer_button.place(x=200, y=5, width=25, height=25)

    sound_button = tk.Button(
        root,
        text="🔊",
        command=play_audio,
        fg="white",
        bg="black",
        borderwidth=0
    )
    sound_button.place(x=170, y=5, width=25, height=25)

    next_button = tk.Button(
        root,
        text=">",
        command=next_word,
        fg="white",
        bg="black",
        borderwidth=0
    )
    next_button.place(x=230, y=5, width=25, height=25)

    setting_button = tk.Button(
        root,
        text="⚙",
        command=open_settings,
        fg="white",
        bg="black",
        borderwidth=0
    )
    setting_button.place(x=260, y=5, width=25, height=25)

    close_button = tk.Button(
        root,
        text="X",
        command=close_app,
        fg="white",
        bg="red",
        borderwidth=0
    )
    close_button.place(x=290, y=5, width=25, height=25)

    # =========================
    # Drag main window
    # =========================

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def move_window(event):
        x = event.x_root - root.x
        y = event.y_root - root.y
        root.geometry(f"+{x}+{y}")

    for widget in [root, furigana_label, word_label, romaji_label, meaning_label, status_label]:
        widget.bind("<Button-1>", start_move)
        widget.bind("<B1-Motion>", move_window)

    # =========================
    # Start app
    # =========================

    update_selected_word()
    update_ui_fonts()

    timer_after_id = root.after(timer, auto_next_word)

    root.mainloop()

    