import pygame
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinter import ttk

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Create the music player window
window = tk.Tk()
window.title("Music Player")
window.geometry("400x400")  # Set the window size

# Playlist
playlist = []

# Store the current playback position
current_position = 0
paused = False

# Global variables
current_song_length = 0
start_time = 0
paused_time = 0

# Function to handle selecting and loading a music file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        playlist.append(file_path)
        if len(playlist) == 1:
            play_music()

# Function to handle playing the next song in the playlist
def play_next():
    if len(playlist) > 1:
        playlist.pop(0)
        play_music()

# Function to format the time in seconds to a human-readable format
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}".format(int(minutes), int(seconds))

# Function to update the music time label
def update_music_time_label():
    if pygame.mixer.music.get_busy():
        current_position = pygame.mixer.music.get_pos()
        elapsed_seconds = int((current_position // 1000) % 60)
        elapsed_minutes = int((current_position // 1000) // 60)
        total_seconds = int((current_song_length // 1000) % 60)
        total_minutes = int((current_song_length // 1000) // 60)
        time_text = f"{elapsed_minutes:02d}:{elapsed_seconds:02d} / {total_minutes:02d}:{total_seconds:02d}"
        music_time_label.config(text=time_text)
    window.after(1000, update_music_time_label)  # Update every second (1000 milliseconds)


# Function to handle the play/pause button
def play_pause_music():
    global start_time, paused, paused_time, current_position
    if pygame.mixer.music.get_busy() and not paused:
        pygame.mixer.music.pause()
        paused_time = pygame.time.get_ticks() - start_time
        paused = True
    elif paused:
        pygame.mixer.music.unpause()
        start_time = pygame.time.get_ticks() - paused_time
        paused = False
    else:
        current_position = 0  # Initialize current_position
        play_music()

# Function to handle the stop button
def stop_music():
    global current_position, paused
    pygame.mixer.music.stop()
    current_position = 0
    paused = False

# Function to show the current playlist
def show_playlist():
    if not playlist:
        messagebox.showinfo("Playlist", "No songs in the playlist.")
    else:
        playlist_text = "\n".join(playlist)
        messagebox.showinfo("Playlist", playlist_text)

# Function to update the progress bar
def update_progress_bar():
    global current_song_length, start_time, paused_time
    if pygame.mixer.music.get_busy():
        elapsed_time = pygame.time.get_ticks() - start_time - paused_time
        progress = (elapsed_time / current_song_length) * 100
        progress_bar['value'] = progress
        window.after(100, update_progress_bar)  # Update every 100 milliseconds (0.1 seconds)

# Function to handle playing the selected song
def play_music():
    global current_song_length, start_time, current_position, paused_time
    if playlist:
        current_song = playlist[0]
        pygame.mixer.music.load(current_song)
        current_song_length = pygame.mixer.Sound(current_song).get_length() * 1000  # Convert to milliseconds
        if current_position >= current_song_length:
            # If the current position is beyond the song length, start from the beginning
            current_position = 0
            paused_time = 0
        pygame.mixer.music.play(start=current_position)
        start_time = pygame.time.get_ticks() - current_position
        update_progress_bar()
        update_music_time_label()

# Create the circular button style with Lanczos method
def create_circular_button(image_path, command):
    image = Image.open(image_path)
    image = image.resize((60, 60), resample=Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    button = tk.Button(window, image=photo, command=command, borderwidth=0, highlightthickness=0)
    button.image = photo
    return button

# Create the buttons
select_button = tk.Button(window, text="Select Music", command=select_file, font=("Arial", 12, "bold"))
play_pause_button = create_circular_button("play.png", play_pause_music)
stop_button = create_circular_button("stop.png", stop_music)
next_button = create_circular_button("next.png", play_next)
playlist_button = tk.Button(window, text="Playlist", command=show_playlist, font=("Arial", 12, "bold"))
progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
music_time_label = tk.Label(window, text="00:00 / 00:00", font=("Arial", 12))

# Position the buttons at the bottom center
button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=10)
select_button.pack(pady=10)
playlist_button.pack(pady=10)
progress_bar.pack(pady=10)
music_time_label.pack()
stop_button.pack(side=tk.LEFT, padx=10)
play_pause_button.pack(side=tk.LEFT, padx=90)
next_button.pack(side=tk.RIGHT, padx=10)


# Run the tkinter event loop
window.mainloop()
