import json
import urllib.request
import random
import tkinter as tk
import time 

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

    root = tk.Tk()

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", alpha_value)
    root.geometry("320x170+100+100")
    root.configure(bg="black")

    def update_selected_word():
        global selected_word

        selected_word = word_array[current_index]

        furigana_text = (
            selected_word.get("furigana")
            or selected_word.get("romaji")
            or ""
        )

        word_text = selected_word.get("word", "")
        meaning_text = selected_word.get("meaning", "")

        furigana_label.config(text=furigana_text)
        word_label.config(text=word_text)
        meaning_label.config(text=meaning_text)

        status_label.config(
            text=f"{current_level}  {current_index + 1} / {len(word_array)}"
        )

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
        word_label.config(font=("Arial", max(8, 18 + font_offset)))
        meaning_label.config(font=("Arial", max(6, 12 + font_offset)))

    def open_settings():
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")
        settings_window.geometry("220x450+450+100")
        settings_window.configure(bg="black")
        settings_window.attributes("-topmost", True)

        level_frame = tk.Frame(settings_window, bg="black")
        level_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(level_frame, text="Select JLPT Level", font=("Arial", 11), fg="white", bg="black").pack(pady=5)

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

        font_frame = tk.Frame(settings_window, bg="black")
        font_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(font_frame, text="Font Size Offset", font=("Arial", 11), fg="white", bg="black").pack()

        def on_font_change(val):
            global font_offset
            font_offset = int(val)
            update_ui_fonts()

        font_scale = tk.Scale(
            font_frame, from_=-5, to=20, orient="horizontal",
            fg="white", bg="black", highlightthickness=0, command=on_font_change
        )
        font_scale.set(font_offset)
        font_scale.pack(fill="x", padx=10)

        trans_frame = tk.Frame(settings_window, bg="black")
        trans_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(trans_frame, text="Window Transparency", font=("Arial", 11), fg="white", bg="black").pack()

        def on_alpha_change(val):
            global alpha_value
            alpha_value = float(val)
            root.attributes("-alpha", alpha_value)

        alpha_scale = tk.Scale(
            trans_frame, from_=0.1, to=1.0, resolution=0.05, orient="horizontal",
            fg="white", bg="black", highlightthickness=0, command=on_alpha_change
        )
        alpha_scale.set(alpha_value)
        alpha_scale.pack(fill="x", padx=10)

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

    prev_button = tk.Button(
        root,
        text="<",
        command=prev_word,
        fg="white",
        bg="black",
        borderwidth=0
    )
    prev_button.place(x=5, y=5, width=25, height=25)

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
        command=root.destroy,
        fg="white",
        bg="red",
        borderwidth=0
    )
    close_button.place(x=290, y=5, width=25, height=25)

    def start_move(event):
        root.x = event.x
        root.y = event.y

    def move_window(event):
        x = event.x_root - root.x
        y = event.y_root - root.y
        root.geometry(f"+{x}+{y}")

    for widget in [root, furigana_label, word_label, meaning_label, status_label]:
        widget.bind("<Button-1>", start_move)
        widget.bind("<B1-Motion>", move_window)

    update_selected_word()
    update_ui_fonts()

    root.mainloop()