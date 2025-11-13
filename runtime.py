#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import random
import tkinter as tk
from tkinter import font as tkfont

# CONFIGURATION

SCRIPT_PATH = os.path.abspath(__file__)
PID_FILE = os.path.expanduser("~/.search_cmd")

# Duration to fade in/out (seconds each)
FADE_DURATION = 1.5

# Total time each fact stays visible (milliseconds, including fades)
FACT_INTERVAL = 15000

# FUN FACTS
FUN_FACTS = [
    "Did you know that honey never spoils?",
    "Did you know that a group of flamingos is called a 'flamboyance'?",
    "Did you know that octopuses have three hearts?",
    "Did you know that bananas are berries but strawberries aren't?",
    "Did you know that sea otters hold hands while sleeping to keep from drifting apart?",
    "Did you know that wombat poop is cube-shaped?",
    "Did you know that sloths can hold their breath longer than dolphins?",
    "Did you know that Scotland has 421 words for 'snow'?",
    "Did you know that some turtles can breathe through their butts?",
    "Did you know that a day on Venus is longer than a year on Venus?",
    "Did you know that a single strand of spaghetti is called a 'spaghetto'?",
    "Did you know that the Eiffel Tower can be 15 cm taller during summer?",
    "Did you know that sea horses are monogamous?",
    "Did you know that koalas have fingerprints similar to humans?",
    "Did you know that the shortest war in history lasted 38 minutes?",
    "Did you know that lobsters taste with their feet?",
    "Did you know that sloths can rotate their heads almost 270 degrees?",
    "Did you know that some cats are allergic to humans?",
    "Did you know that a group of crows is called a 'murder'?",
    "Did you know that giraffes have no vocal cords?",
    "Did you know that penguins propose with pebbles?",
    "Did you know that sea stars can regrow their arms?",
    "Did you know that humans share 60% of their DNA with bananas?",
    "Did you know that butterflies can taste with their feet?",
    "Did you know that sharks existed before trees?",
    "Did you know that a cloud can weigh over a million pounds?",
    "Did you know that rabbits can see behind them without turning their heads?",
    "Did you know that the unicorn is Scotland’s national animal?",
    "Did you know that elephants can’t jump?",
    "Did you know that cows have best friends?",
    "Did you know that bamboo can grow up to 91 cm in a day?",
    "Did you know that flamingos can only eat with their heads upside down?",
    "Did you know that owls don’t have eyeballs but tubes?",
    "Did you know that the fingerprints of a koala are almost identical to humans?",
    "Did you know that giraffes and humans have the same number of neck vertebrae?",
    "Did you know that penguins can jump up to 6 feet in the air?",
    "Did you know that elephants are pregnant for almost two years?",
    "Did you know that a sneeze can travel over 100 miles per hour?",
    "Did you know that some frogs can change sex during their lifetime?",
    "Did you know that seahorses are the only animals where males give birth?",
    "Did you know that Venus rotates clockwise?",
    "Did you know that sea cucumbers fight predators by shooting out their organs?",
    "Did you know that koalas sleep up to 22 hours a day?",
    "Did you know that there are more stars in the universe than grains of sand on Earth?",
    "Did you know that dolphins have names for each other?",
    "Did you know that a goldfish has a memory span of at least three months?",
    "Did you know that sloths can hold their breath longer than dolphins?",
    "Did you know that sea otters have a pouch under their arms to store food?",
    "Did you know that the blue whale is the largest animal to ever exist?",
    "Did you know that sharks can live up to 500 years?",
    "Did you know that some jellyfish are biologically immortal?",
    "Gumper?"
]

# CORE LOGIC

def get_font_name():
    """Return Comic Sans if available, else DejaVu Sans."""
    try:
        available_fonts = list(tkfont.families())
    except Exception:
        available_fonts = []

    if "Comic Sans MS" in available_fonts:
        return "Comic Sans MS"
    return "DejaVu Sans"

def launch_overlay():
    """Keep overlay alive if closed."""
    while True:
        proc = subprocess.Popen([sys.executable, SCRIPT_PATH, "--child"])
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
        time.sleep(1)

def run_overlay():
    font_name = get_font_name()

    # Kill old overlay if running
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except Exception:
            pass

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 1.0)
    root.configure(bg="black")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    x, y = screen_width // 2, screen_height // 2
    text_color = "#7CFC00"
    font_weight = "bold"

    # Create one persistent text item
    current_fact = random.choice(FUN_FACTS)
    text_item = canvas.create_text(
        x, y,
        text=current_fact,
        fill=text_color,
        font=(font_name, 50, font_weight),
        width=screen_width - 100,
        justify="center"
    )

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    def resize_font_to_fit(text):
        """Adjust font size so text fits nicely on screen."""
        font_size = 50
        canvas.itemconfig(text_item, font=(font_name, font_size, font_weight), text=text)
        bbox = canvas.bbox(text_item)
        while bbox and (bbox[3] - bbox[1] > screen_height - 100) and font_size > 10:
            font_size -= 2
            canvas.itemconfig(text_item, font=(font_name, font_size, font_weight))
            bbox = canvas.bbox(text_item)

    def fade_out(step=None):
        """Fade window out before updating fact."""
        if step is None:
            step = 0.05
        alpha = root.attributes("-alpha")
        if alpha > 0:
            root.attributes("-alpha", max(alpha - step, 0))
            root.after(int(FADE_DURATION * 50 * step), lambda: fade_out(step))
        else:
            update_fact()

    def fade_in(step=None):
        """Fade window back in after updating fact."""
        if step is None:
            step = 0.05
        alpha = root.attributes("-alpha")
        if alpha < 1:
            root.attributes("-alpha", min(alpha + step, 1))
            root.after(int(FADE_DURATION * 50 * step), lambda: fade_in(step))
        else:
            # Schedule next fade out to keep total interval 15 seconds
            visible_time = FACT_INTERVAL - int(FADE_DURATION * 2000)  # subtract both fades
            root.after(max(visible_time, 0), fade_out)

    def update_fact():
        """Change fun fact and start fade in."""
        new_fact = random.choice(FUN_FACTS)
        resize_font_to_fit(new_fact)
        fade_in()

    # Start initial display
    resize_font_to_fit(current_fact)
    root.after(FACT_INTERVAL, fade_out)

    def on_close():
        """Cleanup on exit."""
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# ENTRY POINT
if __name__ == "__main__":
    if "--child" in sys.argv:
        run_overlay()
    else:
        launch_overlay()
