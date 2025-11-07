#!/usr/bin/env python3
import os
import signal
import subprocess
import sys
import time

SCRIPT_PATH = os.path.abspath(__file__)

def launch_overlay():
    while True:
        # Launch overlay as a separate process
        proc = subprocess.Popen([sys.executable, SCRIPT_PATH, "--child"])
        try:
            proc.wait()  # wait for overlay to exit
        except KeyboardInterrupt:
            # If parent receives Ctrl+C, terminate child and continue loop
            proc.terminate()
        # small delay to prevent rapid respawn in case of repeated crash
        time.sleep(1)

def run_overlay():
    import tkinter as tk

    # File to track overlay PID
    pid_file = "/etc/.search_cmd"
    os.makedirs(os.path.dirname(pid_file), exist_ok=True)

    # Kill previous overlay if exists
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
        except:
            pass

    # Fullscreen overlay setup
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                       height=root.winfo_screenheight(),
                       bg="black", highlightthickness=0)
    canvas.pack()

    # Display text in the center
    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2
    canvas.create_text(x, y, text="Loading...", fill="white",
                       font=("Arial", 50, "bold"))

    # Save current PID
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    # Toggle overlay hide/show
    def toggle_overlay():
        root.withdraw()
        root.after(10000, lambda: root.deiconify())
        root.after(20000, toggle_overlay)

    root.after(10000, toggle_overlay)

    # Restart if window is closed
    def on_close():
        root.destroy()
        sys.exit(0)  # allow parent watchdog to respawn

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    if "--child" in sys.argv:
        run_overlay()
    else:
        launch_overlay()
