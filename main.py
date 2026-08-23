import customtkinter as ctk
from game_logic import start_game_logic

# -- Root window --
root = ctk.CTk()
root.title("Memory game")
root.geometry("900x700")

# -- Frames --
menu_frame = ctk.CTkFrame(root)
game_frame = ctk.CTkFrame(root)
finish_frame = ctk.CTkFrame(root)

# -- Values --
seconds_passed = 0
timer_running = False

# -- Defines --
def start_game():
    global seconds_passed, timer_running

    # Clear values
    seconds_passed = 0
    timer_running = True

    # pkill -9 main
    menu_frame.pack_forget()

    # Delete all buttons (hardcode)
    for widget in game_frame.winfo_children():
        widget.destroy()
    
    game_frame.pack(expand=True)
    size = get_value()
    cards_buttons = start_game_logic(value, game_frame, finish_frame, stop_timer, get_seconds)

    # Realize button and label
    game_back_btn = ctk.CTkButton(game_frame, text="Back", command=back_to_menu)
    game_timer_lbl = ctk.CTkLabel(game_frame, text=f"Time: 0:0{seconds_passed}")

    # -- Grid --
    game_back_btn.grid(row=size, column=0, columnspan=size, pady=25)
    game_timer_lbl.grid(row=size + 1, column=0, columnspan=size)

    update_timer(game_timer_lbl)

# Update timer reqursion
def update_timer(timer_lbl):
    global seconds_passed
    if not timer_running:
        return

    # Calc new time
    seconds_passed += 1
    minutes = seconds_passed // 60
    secs = seconds_passed % 60
    timer_lbl.configure(text=f"Time: {minutes}:{secs:02d}")
    timer_lbl.after(1000, lambda: update_timer(timer_lbl))

# STOP STUPID
def stop_timer():
    global timer_running
    timer_running = False

# Get timer seconds
def get_seconds():
    return seconds_passed

# Delete all frames and pack menu
def back_to_menu():
    game_frame.pack_forget()
    finish_frame.pack_forget()
    menu_frame.pack(expand=True)

# Get size
def get_value():
    return int(value.split('x')[0])

# Define to auto change size
def on_size_change(value_new):
    global value
    print("selected: ", value_new)
    value = value_new

# -- Segments --
value = "4x4"
menu_seg = ctk.CTkSegmentedButton(
    menu_frame, 
    values=["4x4", "6x6", "8x8"],
    command=on_size_change
)
# Basic value
menu_seg.set("4x4") 
menu_seg.pack(padx=20, pady=20)

# -- Labels --
menu_hello_lbl = ctk.CTkLabel(menu_frame, text="Pick range buttons")
finish_lbl = ctk.CTkLabel(finish_frame, text="You are stupid guy !")

# -- Buttons --
menu_start_btn = ctk.CTkButton(menu_frame, text="Start", command=start_game)
finish_btn = ctk.CTkButton(finish_frame, text="Back", command=back_to_menu)

# -- Packs --
menu_seg.pack(padx=20, pady=20)
menu_hello_lbl.pack()
menu_start_btn.pack(padx=20, pady=20)
finish_lbl.grid(row=1,padx=20, pady=20)
finish_btn.grid(row=3, padx=20, pady = 20)
menu_frame.pack(expand=True) # Start with menu frame

root.mainloop()