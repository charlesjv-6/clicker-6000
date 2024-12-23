import pyautogui
from tkinter import messagebox
import tkinter as tk
import threading
import sys
import time
from pynput.mouse import Listener
from pynput.keyboard import Listener as KeyboardListener, Key
from threading import Event
from ui import canvas, start_button, stop_button, interval_h_entry, interval_m_entry, interval_s_entry, interval_ms_entry, infinite_var, repeat_entry, selected_mode, selected_option, frame, root, add_location_button, clear_location_button, create_row_widgets

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

    def manual_update_location(row_key, x, y):
        if row_key < len(locations):
            if x is not None:
                locations[row_key] = (x, locations[row_key][1])
            if y is not None:
                locations[row_key] = (locations[row_key][0], y)

    def update_row_numbers():
        for index, (row_key, widgets) in enumerate(list(row_widgets.items()), start=1):
            widgets[0].config(text=str(index))

    row_key = len(row_widgets)
    create_row_widgets(row_key=row_key, pick_location=pick_location, delete_row=delete_row, row_widgets=row_widgets, manual_update_location=manual_update_location)

def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")

def on_press(key):
    try:
        if key == Key.end:
            stop_clicking()
    except AttributeError:
        pass

keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

add_location_button.config(command=add_location)
clear_location_button.config(command=delete_all_locations)
start_button.config(command=start_clicking)
stop_button.config(command=stop_clicking)
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

root.mainloop()