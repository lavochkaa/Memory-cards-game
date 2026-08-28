import customtkinter as ctk
from client.game_controller import GameController

# Start all logic
if __name__ == "__main__":
    # Create root ctk
    root = ctk.CTk()
    root.title("Memory game")
    root.geometry("900x800")

    # Start
    app = GameController(root)
    root.mainloop()