import tkinter as tk

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.7)
root.geometry("300x120+100+100")

label = tk.Label(
    root,
    text="Transparent Widget",
    font=("Arial", 18),
    fg="white",
    bg="black"
)
label.pack(expand=True, fill="both")

close_button = tk.Button(
    root,
    text="X",
    command=root.destroy,
    fg="white",
    bg="red",
    borderwidth=0
)
close_button.place(x=270, y=5, width=25, height=25)

def start_move(event):
    root.x = event.x
    root.y = event.y

def move_window(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

label.bind("<Button-1>", start_move)
label.bind("<B1-Motion>", move_window)

root.mainloop()