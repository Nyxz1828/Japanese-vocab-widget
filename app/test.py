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

    a = 1

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
    print(all_vocab[0])
    word = all_vocab[get_random(5000)]
    print(get_random(5000))
    
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

    root = tk.Tk()

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.7)
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
        
    def auto_next_word():
        next_word()
        root.after(30000, auto_next_word)

    def prev_word():
        global current_index

        if current_index > 0:
            current_index -= 1

        update_selected_word()

    def change_level_and_close(level, window):
        reset_word_array(level)
        window.destroy()

    def open_settings():
        settings_window = tk.Toplevel(root)
        settings_window.overrideredirect(True)
        settings_window.title("Settings")
        settings_window.geometry("180x260+450+100")
        settings_window.configure(bg="black")
        settings_window.attributes("-topmost", True)

        title = tk.Label(
            settings_window,
            text="Select JLPT Level",
            font=("Arial", 12),
            fg="white",
            bg="black"
        )
        title.pack(pady=10)

        for level in ["N5", "N4", "N3", "N2", "N1", "ALL"]:
            btn = tk.Button(
                settings_window,
                text=level,
                font=("Arial", 11),
                fg="white",
                bg="gray20",
                borderwidth=0,
                command=lambda lv=level: change_level_and_close(lv, settings_window)
            )
            btn.pack(fill="x", padx=20, pady=4)
            
        adv_btn  = tk.Button(
            settings_window,text='Advance',
            font=("Arial", 8), fg="white", bg="gray20",borderwidth=0
            # command = (fill="x", padx=20, pady=4)
        )
        adv_btn.pack()

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
    
    # to update 
    root.after(30000, auto_next_word)

    root.mainloop()