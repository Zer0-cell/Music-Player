import pygame
import os
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox, Listbox

class MusicPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Zer0 Music")
        self.window.geometry('400x400')  # Adjusted for the Listbox

        pygame.mixer.init()

        # Initialize current state variables
        self.is_playing = False
        self.is_paused = False
        self.playlist = []
        self.current_index = -1  # Keeps track of the current song index

        # Add buttons with ttkbootstrap styling
        self.load_button = ttk.Button(window, text="Load", width=10, bootstyle="primary", command=self.load_songs)
        self.load_button.pack(pady=10)

        self.play_button = ttk.Button(window, text="Play", width=10, bootstyle="success", command=self.play_song)
        self.play_button.pack(pady=10)

        self.pause_button = ttk.Button(window, text="Pause", width=10, bootstyle="warning", command=self.pause_song)
        self.pause_button.pack(pady=10)

        self.stop_button = ttk.Button(window, text="Stop", width=10, bootstyle="danger", command=self.stop_song)
        self.stop_button.pack(pady=10)

        self.next_button = ttk.Button(window, text="Next", width=10, bootstyle="info", command=self.next_song)
        self.next_button.pack(pady=10)

        self.prev_button = ttk.Button(window, text="Previous", width=10, bootstyle="info", command=self.prev_song)
        self.prev_button.pack(pady=10)

        self.quit_button = ttk.Button(window, text="Quit", width=10, bootstyle="secondary", command=self.quit_player)
        self.quit_button.pack(pady=10)

        # Create a Listbox using tkinter's Listbox widget
        self.song_listbox = Listbox(window, height=10, width=50)
        self.song_listbox.pack(pady=10)

        # Bind the listbox to play the selected song when clicked
        self.song_listbox.bind('<<ListboxSelect>>', self.on_select)

    def load_songs(self):
        """Load multiple music files."""
        files = filedialog.askopenfilenames(filetypes=[("Music Files", "*.mp3 *.wav")])
        if files:
            self.playlist = list(files)  # Store the selected files in the playlist
            self.current_index = 0  # Start from the first song
            self.update_song_listbox()  # Update the Listbox
            messagebox.showinfo("Success", f"Loaded {len(self.playlist)} songs.")
        else:
            messagebox.showwarning("Warning", "No files selected.")

    def update_song_listbox(self):
        """Update the Listbox with the loaded songs."""
        self.song_listbox.delete(0, 'end')  # Clear the listbox
        for song in self.playlist:
            self.song_listbox.insert('end', os.path.basename(song))  # Add song names to the listbox

    def on_select(self, event):
        """Play the song when a selection is made in the Listbox."""
        # Get the selected song's index
        if self.song_listbox.curselection():
            self.current_index = self.song_listbox.curselection()[0]
            self.play_song()

    def play_song(self):
        """Play the current song in the playlist."""
        if self.playlist:
            song = self.playlist[self.current_index]
            if self.is_paused:  # If paused, resume playing
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                try:
                    pygame.mixer.music.load(song)
                    pygame.mixer.music.play()
                    self.is_playing = True
                    messagebox.showinfo("Playing", f"Playing: {os.path.basename(song)}")
                except pygame.error as e:
                    messagebox.showerror("Error", f"Could not load file: {e}")
        else:
            messagebox.showwarning("Warning", "No songs loaded to play.")

    def pause_song(self):
        """Pause the current song."""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            messagebox.showinfo("Paused", "Music paused.")
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            messagebox.showinfo("Resumed", "Music resumed.")

    def stop_song(self):
        """Stop the current song."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            messagebox.showinfo("Stopped", "Music stopped.")

    def next_song(self):
        """Play the next song in the playlist."""
        if self.playlist and self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.song_listbox.select_clear(0, 'end')  # Clear selection
            self.song_listbox.select_set(self.current_index)  # Select the next song
            self.play_song()
        else:
            messagebox.showinfo("Info", "This is the last song in the playlist.")

    def prev_song(self):
        """Play the previous song in the playlist."""
        if self.playlist and self.current_index > 0:
            self.current_index -= 1
            self.song_listbox.select_clear(0, 'end')  # Clear selection
            self.song_listbox.select_set(self.current_index)  # Select the previous song
            self.play_song()
        else:
            messagebox.showinfo("Info", "This is the first song in the playlist.")

    def quit_player(self):
        """Quit the player."""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.window.quit()
        self.window.destroy()

def main():
    # Use ttkbootstrap's themed window
    root = ttk.Window(themename="darkly")  # You can choose from various themes like 'darkly', 'cosmo', etc.
    player = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
