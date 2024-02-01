import tkinter as tk
from tkinter import Listbox
from pathlib import Path

class MinecraftWorldListApp:
    def __init__(self, master):
        self.master = master
        master.title("Minecraft World List")

        self.world_listbox = Listbox(master)
        self.world_listbox.pack(pady=10)

        get_worlds_button = tk.Button(master, text="Get Local Worlds", command=self.get_local_worlds)
        get_worlds_button.pack(pady=10)

    def get_local_worlds(self):
        # Get the Minecraft saves directory
        saves_dir = self.get_minecraft_saves_directory()

        if saves_dir is not None:
            # List all subdirectories in the saves directory
            worlds = [world.name for world in saves_dir.iterdir() if world.is_dir()]

            # Display the world list in the Tkinter window
            self.update_world_listbox(worlds)

    def get_minecraft_saves_directory(self):
        # Replace 'your_username' with the player's Minecraft username
        minecraft_dir = Path.home() / "AppData" / "Roaming" / ".minecraft"
        saves_dir = minecraft_dir / "saves"

        if saves_dir.exists():
            return saves_dir
        else:
            print("Minecraft saves directory not found.")
            return None

    def update_world_listbox(self, world_list):
        self.world_listbox.delete(0, tk.END)  # Clear the listbox
        for world in world_list:
            self.world_listbox.insert(tk.END, world)

# Create the Tkinter window
root = tk.Tk()
app = MinecraftWorldListApp(root)

# Run the Tkinter main loop
root.mainloop()
