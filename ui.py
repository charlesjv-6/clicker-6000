import tkinter as tk

ENTRY_WIDTH = 5
FRAME_WIDTH = 350
BG="#2e2e2e"
FG="white"

root = tk.Tk()
root.title("Clicker 6000")
root.configure(background=BG, pady=5)
root.attributes("-topmost", True)
root.resizable(False, False)
root.geometry("+400+250")

# Frames
interval_frame = tk.LabelFrame(root, text="Interval", padx=5, pady=5, width=FRAME_WIDTH, height=70, bg=BG, fg=FG)
interval_frame.grid(row=0, column=0, padx=10, sticky="w")
interval_frame.grid_propagate(False)

parent_frame = tk.LabelFrame(root, border=0, width=(FRAME_WIDTH + 10), height=100, bg=BG, fg=FG)
parent_frame.grid(row=1, column=0, pady=10, sticky="w")
parent_frame.grid_propagate(False)

button_frame = tk.LabelFrame(root, border=0, width=FRAME_WIDTH + 20, height=35, bg=BG, fg=FG, padx=5)
button_frame.grid(row=3, column=0, sticky="w")
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
# canvas.bind_all("<MouseWheel>", on_mouse_wheel)

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
add_location_button = tk.Button(header_frame, text="ADD", padx=15, border=0, bg="green", fg="white")
add_location_button.grid(row=0, column=3, padx=5, pady=1)
clear_location_button = tk.Button(header_frame, text="CLEAR", padx=10, border=0, bg="red", fg="white")
clear_location_button.grid(row=0, column=4, padx=5, pady=1)

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
option_menu.config(width=14, bg=FG, border=0, fg=BG, anchor="w", indicatoron=False)

mode_menu = tk.OptionMenu(option_frame, selected_mode, *modes)
mode_menu.grid(row=1, column=1, padx=4, pady=4)
mode_menu.config(width=14, bg=FG, border=0, fg=BG, anchor="w",  indicatoron=False)

selected_option.set(options[0])
selected_mode.set(modes[0])

def create_row_widgets(row_key, pick_location, delete_row, row_widgets, manual_update_location):
    row_key = len(row_widgets)
    row_widgets[row_key] = []

    def on_x_change(*args):
        manual_update_location(row_key, x_var.get(), None)

    def on_y_change(*args):
        manual_update_location(row_key, None, y_var.get())

    row_label = tk.Label(frame, text=str(len(row_widgets)), width=2, anchor="w", bg=BG, fg=FG)
    row_label.grid(row=row_key, column=0, padx=5, pady=1)
    row_widgets[row_key].append(row_label)

    x_var = tk.StringVar()
    x_var.trace("w", on_x_change)
    x_entry = tk.Entry(frame, width=ENTRY_WIDTH * 3)
    x_entry.grid(row=row_key, column=1, padx=2)
    x_entry.config(justify="center", textvariable=x_var)
    row_widgets[row_key].append(x_entry)

    y_var = tk.StringVar()
    y_var.trace("w", on_y_change)
    y_entry = tk.Entry(frame, width=ENTRY_WIDTH * 3)
    y_entry.grid(row=row_key, column=2, padx=2)
    y_entry.config(justify="center", textvariable=y_var)
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
start_button = tk.Button(button_frame, text="START", padx=80, fg=FG, bg="green", border=0)
start_button.grid(row=0, column=4, padx=5, pady=5)
stop_button = tk.Button(button_frame, text="STOP (Press END key)", border=0, state=tk.DISABLED, padx=80, fg=FG, bg="red")
stop_button.grid(row=0, column=5, padx=5, pady=5)
