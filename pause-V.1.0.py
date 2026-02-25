# Auteur : Nathan
# Version : 1.0
# Date : 25.02.2026
# Titre : Pause


import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Heures fixes pour les barres de progression
END_TIME_1 = "12:30"
END_TIME_2 = "15:45"

# Heure de début de la journée
START_OF_DAY = "08:15"

# Liste des heures de pause (format HH:MM)
PAUSE_TIMES = ["9:00", "9:50", "10:50", "11:40", "12:30"]


def parse_time_to_datetime(time_str):
    today = datetime.now().date()
    hour, minute = map(int, time_str.split(":"))
    return datetime(today.year, today.month, today.day, hour, minute)


def parse_pause_times():
    today = datetime.now().date()
    times = []
    for t in PAUSE_TIMES:
        hour, minute = map(int, t.split(":"))
        times.append(datetime(today.year, today.month, today.day, hour, minute))
    return times


def get_next_pause(now, pause_list):
    for p in pause_list:
        if p > now:
            return p
    return pause_list[0] + timedelta(days=1)


def get_previous_pause(now, pause_list):
    previous = None
    for p in pause_list:
        if p < now:
            previous = p
    if previous is None:
        previous = pause_list[-1] - timedelta(days=1)
    return previous


def format_remaining(delta):
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        return "0 s"

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return f"{hours} h {minutes:02d} min"
    elif minutes > 0:
        return f"{minutes} min {seconds:02d} s"
    else:
        return f"{seconds} s"


def create_app():
    root = tk.Tk()
    root.title("Prochaine pause")

    # Labels principaux
    current_time_label = tk.Label(root, font=("Arial", 14))
    current_time_label.pack(pady=10)

    next_pause_label = tk.Label(root, font=("Arial", 14))
    next_pause_label.pack(pady=10)

    # --- BARRE PRINCIPALE ---
    frame_main = tk.Frame(root)
    frame_main.pack(pady=10)

    progress_main = ttk.Progressbar(frame_main, orient="horizontal", length=300, mode="determinate")
    progress_main.pack(side="left")

    remaining_main_label = tk.Label(frame_main, font=("Arial", 12), width=12)
    remaining_main_label.pack(side="left", padx=10)

    # --- BARRE 12h30 ---
    frame_12 = tk.Frame(root)
    frame_12.pack(pady=10)

    label_12h30 = tk.Label(frame_12, text="Jusqu'à 12h30 :", font=("Arial", 12))
    label_12h30.pack(side="left")

    progress_12h30 = ttk.Progressbar(frame_12, orient="horizontal", length=250, mode="determinate")
    progress_12h30.pack(side="left", padx=10)

    remaining_12_label = tk.Label(frame_12, font=("Arial", 12), width=12)
    remaining_12_label.pack(side="left")

    # --- BARRE 15h45 ---
    frame_15 = tk.Frame(root)
    frame_15.pack(pady=10)

    label_15h45 = tk.Label(frame_15, text="Jusqu'à 15h45 :", font=("Arial", 12))
    label_15h45.pack(side="left")

    progress_15h45 = ttk.Progressbar(frame_15, orient="horizontal", length=250, mode="determinate")
    progress_15h45.pack(side="left", padx=10)

    remaining_15_label = tk.Label(frame_15, font=("Arial", 12), width=12)
    remaining_15_label.pack(side="left")

    # Préparation des heures fixes
    start_of_day = parse_time_to_datetime(START_OF_DAY)
    end_12h30 = parse_time_to_datetime(END_TIME_1)
    end_15h45 = parse_time_to_datetime(END_TIME_2)

    pause_list = parse_pause_times()
    now = datetime.now()
    start_time = get_previous_pause(now, pause_list)

    def update():
        nonlocal start_time

        now = datetime.now()
        current_time_label.config(text="Heure actuelle : " + now.strftime("%H:%M:%S"))

        # Prochaine pause
        next_pause = get_next_pause(now, pause_list)
        next_pause_label.config(text="Prochaine pause : " + next_pause.strftime("%H:%M"))

        # Barre principale
        total_main = (next_pause - start_time).total_seconds()
        elapsed_main = (now - start_time).total_seconds()
        progress_main['value'] = max(0, min(100, (elapsed_main / total_main) * 100))

        remaining_main_label.config(text=format_remaining(next_pause - now))

        # Barre 12h30
        total_12 = (end_12h30 - start_of_day).total_seconds()
        elapsed_12 = (now - start_of_day).total_seconds()
        progress_12h30['value'] = max(0, min(100, (elapsed_12 / total_12) * 100))

        remaining_12_label.config(text=format_remaining(end_12h30 - now))

        # Barre 15h45
        total_15 = (end_15h45 - start_of_day).total_seconds()
        elapsed_15 = (now - start_of_day).total_seconds()
        progress_15h45['value'] = max(0, min(100, (elapsed_15 / total_15) * 100))

        remaining_15_label.config(text=format_remaining(end_15h45 - now))

        root.after(1000, update)

    update()
    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
