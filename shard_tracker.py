import tkinter as tk
import json
import os
from PIL import Image, ImageTk

SAVE_FILE = "shard_counts.json"

SHARDS = {
    "Ancient": 0,
    "Void": 0,
    "Sacred": 0,
    "Primal": 0,
    "Mythical": 0,
    "Prism": 0,
    "Remnant": 0
}

TEN_PULL_SHARDS = ["Ancient", "Void"]

SHARD_COLOURS = {
    "Ancient": "#3aa0ff",
    "Void": "#b060ff",
    "Sacred": "#ffcc33",
    "Primal": "#ff5533",
    "Mythical": "#ff5533",
    "Prism": "#ffffff",
    "Remnant": "#8b0000"
}

SHARD_IMAGES = {
    "Ancient": "ancient.png",
    "Void": "void.png",
    "Sacred": "sacred.png",
    "Primal": "primal.png",
    "Prism": "prism.png",
    "Remnant": "remnant.png"
}

# Load saved counts if available
if os.path.exists(SAVE_FILE):
    try:
        with open(SAVE_FILE, "r") as f:
            SHARDS = json.load(f)
    except:
        pass

def save_counts():
    with open(SAVE_FILE, "w") as f:
        json.dump(SHARDS, f)

def update_label(shard, label):
    label.config(text=f"{SHARDS[shard]:>5}")
    save_counts()

def add_one(shard, label):
    SHARDS[shard] += 1
    update_label(shard, label)

def add_ten(shard, label):
    SHARDS[shard] += 10
    update_label(shard, label)

def subtract_one(shard, label):
    if SHARDS[shard] > 0:
        SHARDS[shard] -= 1
    update_label(shard, label)

def reset(shard, label):
    SHARDS[shard] = 0
    update_label(shard, label)


class RaidButton(tk.Canvas):
    def __init__(self, parent, text, command=None, colour="#888", width=65, height=30, visible=True):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg="#1a1a1a")
        self.colour = colour
        self.text = text
        self.command = command
        self.visible = visible
        if visible:
            self.create_rectangle(0, 0, width, height, fill="#2a2a2a", outline=self.colour, width=2)
            self.label = self.create_text(width//2, height//2, text=text, fill="white", font=("Arial", 11, "bold"))
            if command:
                self.bind("<Button-1>", lambda e: self.command())
            self.bind("<Enter>", self.on_hover)
            self.bind("<Leave>", self.on_leave)
        else:
            self.configure(bg="#0f0f0f")

    def on_hover(self, event):
        if self.visible:
            self.itemconfig(self.label, fill="#ffffaa")

    def on_leave(self, event):
        if self.visible:
            self.itemconfig(self.label, fill="white")


def lighten(colour, amount=60):
    r = int(colour[1:3], 16)
    g = int(colour[3:5], 16)
    b = int(colour[5:7], 16)
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


root = tk.Tk()
root.title("Shard Pull Tracker")
root.configure(bg="#0f0f0f")

title = tk.Label(root, text="Shard Pull Tracker", fg="white", bg="#0f0f0f",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

loaded_images = {}

for shard in ["Ancient", "Void", "Sacred", "Primal", "Prism", "Remnant"]:
    colour = SHARD_COLOURS[shard]
    glow = lighten(colour, 80)

    outer_frame = tk.Frame(root, bg="#0f0f0f")
    outer_frame.pack(pady=3, anchor="center")

    img_path = SHARD_IMAGES.get(shard)
    if os.path.exists(img_path):
        pil_img = Image.open(img_path).convert("RGBA").resize((64, 64), Image.LANCZOS)
        loaded_images[shard] = ImageTk.PhotoImage(pil_img)
        tk.Label(outer_frame, image=loaded_images[shard], bg="#0f0f0f").grid(row=0, column=0, padx=(10, 10))
    else:
        tk.Label(outer_frame, text="?", fg="white", bg="#0f0f0f",
                 font=("Arial", 20, "bold")).grid(row=0, column=0, padx=(10, 10))

    panel_height = 120 if shard == "Primal" else 85

    panel = tk.Canvas(outer_frame, width=540, height=panel_height, bg="#0f0f0f", highlightthickness=0)
    panel.grid(row=0, column=1)
    panel.create_rectangle(5, 5, 535, panel_height - 5, outline=colour, width=3)
    panel.create_rectangle(8, 8, 532, panel_height - 8, outline=glow, width=2)

    content = tk.Frame(outer_frame, bg="#0f0f0f")
    content.place(in_=panel, x=25, y=25)

    legendary_name = "Legendary" if shard == "Primal" else shard

    tk.Label(content, text=legendary_name, fg="white", bg="#0f0f0f",
             font=("Arial", 14, "bold"), width=8, anchor="w").grid(row=0, column=0, padx=(5, 0))

    count_label = tk.Label(content, text=f"{SHARDS[shard]:>5}", fg="white", bg="#0f0f0f",
                           font=("Arial", 16, "bold"), width=6, anchor="e")
    count_label.grid(row=0, column=1, padx=(0, 2))

    btn_frame = tk.Frame(content, bg="#0f0f0f")
    btn_frame.grid(row=0, column=2)

    RaidButton(btn_frame, "+", lambda s=shard, l=count_label: add_one(s, l),
               colour=colour).grid(row=0, column=0, padx=5)

    if shard in TEN_PULL_SHARDS:
        RaidButton(btn_frame, "+10", lambda s=shard, l=count_label: add_ten(s, l),
                   colour=colour).grid(row=0, column=1, padx=5)
    else:
        RaidButton(btn_frame, "", None, colour=colour, visible=False).grid(row=0, column=1, padx=5)

    RaidButton(btn_frame, "-", lambda s=shard, l=count_label: subtract_one(s, l),
               colour=colour).grid(row=0, column=2, padx=5)

    RaidButton(btn_frame, "Reset", lambda s=shard, l=count_label: reset(s, l),
               colour=colour).grid(row=0, column=3, padx=5)

    if shard == "Primal":
        tk.Label(content, text="Mythical", fg="white", bg="#0f0f0f",
                 font=("Arial", 14, "bold"), width=8, anchor="w").grid(row=1, column=0, padx=(5, 0), pady=(6, 0))

        myth_label = tk.Label(content, text=f"{SHARDS['Mythical']:>5}", fg="white", bg="#0f0f0f",
                              font=("Arial", 16, "bold"), width=6, anchor="e")
        myth_label.grid(row=1, column=1, padx=(0, 2), pady=(6, 0))

        myth_frame = tk.Frame(content, bg="#0f0f0f")
        myth_frame.grid(row=1, column=2, pady=(6, 0))

        RaidButton(myth_frame, "+", lambda l=myth_label: add_one("Mythical", l),
                   colour=colour).grid(row=0, column=0, padx=5)

        RaidButton(myth_frame, "", None, colour=colour, visible=False).grid(row=0, column=1, padx=5)

        RaidButton(myth_frame, "-", lambda l=myth_label: subtract_one("Mythical", l),
                   colour=colour).grid(row=0, column=2, padx=5)

        RaidButton(myth_frame, "Reset", lambda l=myth_label: reset("Mythical", l),
                   colour=colour).grid(row=0, column=3, padx=5)


root.update()
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")

root.mainloop()
