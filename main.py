import customtkinter as ctk
from game_logic import start_game_logic

# -- Root window --
root = ctk.CTk()
root.title("Memory game")
root.geometry("900x600")

# -- Frames --
menu_frame = ctk.CTkFrame(root)
game_frame = ctk.CTkFrame(root)
finish_frame = ctk.CTkFrame(root)

# -- Defines --
def start_game():
    menu_frame.pack_forget()

    for widget in game_frame.winfo_children():
        widget.destroy()
    
    game_frame.pack()
    size = get_value()
    cards_buttons = start_game_logic(value, game_frame, finish_frame)

    game_back_btn = ctk.CTkButton(game_frame, text="Back", command=back_to_menu)
    game_back_btn.grid(row=size, column=0, columnspan=size, pady=25)

def back_to_menu():
    game_frame.pack_forget()
    finish_frame.pack_forget()
    menu_frame.pack()

def get_value():
    return int(value.split('x')[0])

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
finish_lbl.pack(padx=20, pady=20)
finish_btn.pack(padx=20, pady = 20)

# Start with menu frame
menu_frame.pack() 

root.mainloop()