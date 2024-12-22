import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
import sys
import time
from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener, Key
from threading import Event

ENTRY_WIDTH = 5
FRAME_WIDTH = 350
BG="#2e2e2e"
FG="white"
coordinate_entries = []
is_recording = False
current_x_entry = None
current_y_entry = None
row_widgets = {}
listener = None
locations = []
stop_event = Event()

def start_clicking():
    stop_event.clear() 
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    try:
        hours = float(interval_h_entry.get() or 0)
        minutes = float(interval_m_entry.get() or 0)
        seconds = float(interval_s_entry.get() or 0)
        milliseconds = float(interval_ms_entry.get() or 0)

        interval = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)

        if infinite_var.get():
            clicks = sys.maxsize
        else:
            clicks = int(repeat_entry.get())

        def click(x, y):
            if selected_option.get() == "Right":
                if selected_mode.get() == "Double":
                    pyautogui.doubleClick(x, y, button='right')
                else:
                    pyautogui.click(x, y, button='right')
            else:
                if selected_mode.get() == "Double":
                    pyautogui.doubleClick(x, y)
                else:
                    pyautogui.click(x, y)

        def clicker():
            for i in range(clicks):
                if stop_event.is_set():
                    break
                if not locations:
                    x, y = pyautogui.position()
                    click(x, y)
                    time.sleep(interval)
                else:
                    for x, y in list(locations):
                        click(x, y)
                        time.sleep(interval)
                if not infinite_var.get():
                    break
        threading.Thread(target=clicker).start()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def stop_clicking():
    stop_event.set()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def listen_to_click(x, y, button, pressed, row_key):
    global current_x_entry, current_y_entry, is_recording, listener
    if pressed and is_recording:
        current_x_entry.delete(0, tk.END)
        current_x_entry.insert(0, str(x))
        current_y_entry.delete(0, tk.END)
        current_y_entry.insert(0, str(y))

        if row_key < len(locations):
            locations[row_key] = (x, y)
        else:
            locations.append((x, y)) 

        listener.stop()
        is_recording = False

def delete_all_locations():
    global row_widgets

    for widget in frame.winfo_children():
        widget.destroy()

    coordinate_entries.clear()
    locations.clear()
    row_widgets = {}

def add_location():
    global row_widgets, locations

    def pick_location(x_entry, y_entry, row_key):
        global is_recording, current_x_entry, current_y_entry, listener

        if listener and listener.running:
            listener.stop()

        current_x_entry = x_entry
        current_y_entry = y_entry
        is_recording = True
        listener = Listener(on_click=lambda x, y, button, pressed: listen_to_click(x, y, button, pressed, row_key))
        listener.start()

    def delete_row(row_key):
        for widget in row_widgets[row_key]:
            widget.destroy()
        del row_widgets[row_key]
        locations.pop(row_key)
        update_row_numbers()

    def update_row_numbers():
        for index, (row_key, widgets) in enumerate(list(row_widgets.items()), start=1):
            widgets[0].config(text=str(index))

    row_key = len(row_widgets)
    row_widgets[row_key] = []

    row_label = tk.Label(frame, text=str(len(row_widgets)), width=2, anchor="w", bg=BG, fg=FG)
    row_label.grid(row=row_key, column=0, padx=5, pady=1)
    row_widgets[row_key].append(row_label)

    x_entry = tk.Entry(frame, width=ENTRY_WIDTH * 3)
    x_entry.grid(row=row_key, column=1, padx=2)
    x_entry.config(justify="center")
    row_widgets[row_key].append(x_entry)

    y_entry = tk.Entry(frame, width=ENTRY_WIDTH * 3)
    y_entry.grid(row=row_key, column=2, padx=2)
    y_entry.config(justify="center")
    row_widgets[row_key].append(y_entry)

    pick_button = tk.Button(frame, command=lambda: pick_location(x_entry, y_entry, row_key), text="Pick", border=0, padx=10)
    pick_button.grid(row=row_key, column=3)
    pick_button.config(bg=BG, fg="green", font=("TkDefaultFont", 8, "bold"))
    row_widgets[row_key].append(pick_button)

    delete_button = tk.Button(frame, text="Remove", command=lambda: delete_row(row_key), border=0, fg="red", bg=BG)
    delete_button.grid(row=row_key, column=4)
    delete_button.config(font=("TkDefaultFont", 8, "bold"))
    row_widgets[row_key].append(delete_button)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

def on_press(key):
    try:
        if key == Key.end:
            stop_clicking()
    except AttributeError:
        pass

# Initialize the UI
root = tk.Tk()
root.title("Clicker 6000")
root.configure(background=BG, pady=5)
root.attributes("-topmost", True)
root.resizable(False, False)
root.geometry("+400+250")  # Format: "widthxheight+x_offset+y_offset"

keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

# Frames
interval_frame = tk.LabelFrame(root, text="Interval", padx=5, pady=5, width=FRAME_WIDTH, height=70, bg=BG, fg=FG)
interval_frame.grid(row=0, column=0, padx=10, sticky="w")
interval_frame.grid_propagate(False)

parent_frame = tk.LabelFrame(root, border=0, width=(FRAME_WIDTH + 10), height=100, bg=BG, fg=FG)
parent_frame.grid(row=1, column=0, pady=10, sticky="w")
parent_frame.grid_propagate(False)

button_frame = tk.LabelFrame(root, border=0, width=FRAME_WIDTH, height=40, bg=BG, fg=FG)
button_frame.grid(row=3, column=0, pady=10, padx=10, sticky="w")
button_frame.grid_columnconfigure(4, weight=1)
button_frame.grid_columnconfigure(5, weight=1)
button_frame.grid_propagate(False)

coordinates_frame = tk.LabelFrame(root, text="Locations (Leave empty to use cursor position)", padx=0, pady=5, width=(FRAME_WIDTH), height=200, bg=BG, fg=FG)
coordinates_frame.grid(row=2, column=0, padx=10, sticky="w")
coordinates_frame.grid_propagate(False)

header_frame = tk.LabelFrame(coordinates_frame, padx=0, pady=5, width=(FRAME_WIDTH - 4), height=30, bg=BG, fg=FG, border=0)
header_frame.grid(row=0, column=0, sticky="w", pady=5)
header_frame.grid_propagate(False)

option_frame = tk.LabelFrame(parent_frame, text="Options", width=((FRAME_WIDTH / 2) - 5), height=100, bg=BG, fg=FG)
option_frame.grid(row=1, column=0, padx=10, sticky="w")
option_frame.grid_propagate(False)

click_frame = tk.LabelFrame(parent_frame, text="Clicks", width=((FRAME_WIDTH / 2) - 5), height=100, bg=BG, fg=FG)
click_frame.grid(row=1, column=1, sticky="w")
click_frame.grid_propagate(False)

repeat_amount_frame = tk.LabelFrame(click_frame, border=0, width=165, height=40, bg=BG, fg=FG)
repeat_amount_frame.grid(row=0, column=0, sticky="w")
repeat_amount_frame.grid_propagate(False)

infinite_frame = tk.LabelFrame(click_frame, border=0, width=165, height=40, bg=BG, fg=FG)
infinite_frame.grid(row=1, column=0, sticky="w")
infinite_frame.grid_propagate(False)

# Canvas
canvas = tk.Canvas(coordinates_frame, bg=BG, height=120, width=347, highlightthickness=0)
canvas.grid(row=1, column=0, sticky="w")
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

frame = tk.Frame(canvas, bg=BG)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Interval Labels
tk.Label(interval_frame, text="hours", width=5, anchor="w", bg=BG, fg=FG).grid(row=0, column=1)
tk.Label(interval_frame, text="mins", width=5, anchor="w", bg=BG, fg=FG).grid(row=0, column=3)
tk.Label(interval_frame, text="secs", width=5, anchor="w", bg=BG, fg=FG).grid(row=0, column=5)
tk.Label(interval_frame, text="ms", width=3, anchor="w", bg=BG, fg=FG).grid(row=0, column=7)

# Options Labels
tk.Label(option_frame, text="Button", width=6, anchor="w", bg=BG, fg=FG).grid(row=0, column=0, padx=5, pady=5)
tk.Label(option_frame, text="Mode", width=6, anchor="w", bg=BG, fg=FG).grid(row=1, column=0, padx=5, pady=5)

# Coordinates Lables and Actions
tk.Label(header_frame, text="#", width=2, anchor="c", bg=BG, fg=FG).grid(row=0, column=0, padx=5)
tk.Label(header_frame, text="X Position", width=(ENTRY_WIDTH * 2), anchor="c", bg=BG, fg=FG).grid(row=0, column=1, padx=5)
tk.Label(header_frame, text="Y Position", width=(ENTRY_WIDTH * 2), anchor="c", bg=BG, fg=FG).grid(row=0, column=2, padx=5)
tk.Button(header_frame, text="ADD", command=add_location, padx=15, border=0, bg="green", fg="white").grid(row=0, column=3, padx=5, pady=1)
tk.Button(header_frame, text="CLEAR", command=delete_all_locations, padx=10, border=0, bg="red", fg="white").grid(row=0, column=4, padx=5, pady=1)

# Repeat Labels
tk.Label(repeat_amount_frame, text="Repeat", width=5, anchor="w", bg=BG, fg=FG).grid(row=0, column=0, padx=5, pady=8)
tk.Label(repeat_amount_frame, text="times", width=6, anchor="w", bg=BG, fg=FG).grid(row=0, column=2, padx=5, pady=8)

# Interval Entries
interval_h_entry = tk.Entry(interval_frame, width=ENTRY_WIDTH, border=0, justify="right")
interval_h_entry.grid(row=0, column=0, padx=2, pady=4)
interval_h_entry.insert(0, "0")
interval_m_entry = tk.Entry(interval_frame, width=ENTRY_WIDTH, border=0, justify="right")
interval_m_entry.grid(row=0, column=2, padx=4, pady=4)
interval_m_entry.insert(0, "0")
interval_s_entry = tk.Entry(interval_frame, width=ENTRY_WIDTH, border=0, justify="right")
interval_s_entry.grid(row=0, column=4, padx=4, pady=4)
interval_s_entry.insert(0, "0")
interval_ms_entry = tk.Entry(interval_frame, width=ENTRY_WIDTH + 3, border=0, justify="right")
interval_ms_entry.grid(row=0, column=6, padx=4, pady=4)
interval_ms_entry.insert(0, "1000")

# Options Entries
selected_option = tk.StringVar()
selected_mode = tk.StringVar()

options = ["Left", "Right"]
modes = ["Single", "Double"]

option_menu = tk.OptionMenu(option_frame, selected_option, *options)
option_menu.grid(row=0, column=1, padx=4, pady=4)
option_menu.config(width=9, bg=FG, border=0, fg=BG, anchor="w")

mode_menu = tk.OptionMenu(option_frame, selected_mode, *modes)
mode_menu.grid(row=1, column=1, padx=4, pady=4)
mode_menu.config(width=9, bg=FG, border=0, fg=BG, anchor="w")

selected_option.set(options[0])
selected_mode.set(modes[0])

# Repeat Entries
infinite_var = tk.BooleanVar(value=True)
def toggle():
    if toggle_button.config('text')[-1] == 'ON':
        toggle_button.config(text='OFF', bg="red")
        infinite_var.set(False)
    else:
        toggle_button.config(text='ON', bg="green")
        infinite_var.set(True)

toggle_button = tk.Button(infinite_frame, text="ON", bg="green", fg=FG, font=("TkDefaultFont", 8, "bold"), border=0, width=5, command=toggle, padx=5)
toggle_button.grid(row=1, column=1, padx=5, pady=5)
tk.Label(infinite_frame, text="Infinite", width=5, anchor="w", bg=BG, fg=FG).grid(row=1, column=0, padx=5)
repeat_entry = tk.Entry(repeat_amount_frame, width=ENTRY_WIDTH + 2, border=0).grid(row=0, column=1, pady=8)

# Start and Stop Buttons
start_button = tk.Button(button_frame, text="START", command=start_clicking, padx=80, fg=FG, bg="green")
start_button.grid(row=0, column=4, padx=5, pady=5)
stop_button = tk.Button(button_frame, text="STOP (Press END key)", command=stop_clicking, state=tk.DISABLED, padx=80, fg=FG, bg="red")
stop_button.grid(row=0, column=5, padx=5, pady=5)

# Run the UI
root.mainloop()
