import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import pygame
from tkinter import messagebox
#from pyupdater.client import Client

def add_song():
    file_path = filedialog.askopenfilename(initialdir="./music", title="Choose a song", filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        song_name = os.path.basename(file_path)
        song_size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)
        tree.insert("", "end", text=song_name, values=(f"{song_size_mb} MB"))
        songs.append(file_path)

def add_songs_from_folder():
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                song_path = os.path.join(folder_path, file)
                song_name = os.path.basename(song_path)
                song_size_mb = round(os.path.getsize(song_path) / (1024 * 1024), 2)
                tree.insert("", "end", text=song_name, values=(f"{song_size_mb} MB"))
                songs.append(song_path)

def play_song():
    global paused
    selected_song_index = tree.index(tree.selection())
    if selected_song_index is not None:
        selected_song = songs[selected_song_index]
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        paused = False

def show_about_info():
    messagebox.showinfo("About", "Publisher: PTxr\nVersion: 2.0\nRelease date 12/30/2023")

def play_next():
    global paused
    current_song_index = tree.index(tree.selection())
    if current_song_index is not None:
        next_song_index = current_song_index + 1
        children = tree.get_children()
        if next_song_index < len(children):
            next_song = children[next_song_index]
            tree.selection_set(next_song)
            tree.focus(next_song)
            paused = False
            pygame.mixer.music.load(songs[next_song_index])
            pygame.mixer.music.play()

def play_previous():
    global paused
    current_song_index = tree.index(tree.selection())
    if current_song_index is not None:
        prev_song_index = current_song_index - 1
        children = tree.get_children()
        if prev_song_index >= 0:
            prev_song = children[prev_song_index]
            tree.selection_set(prev_song)
            tree.focus(prev_song)
            paused = False
            pygame.mixer.music.load(songs[prev_song_index])
            pygame.mixer.music.play()

def pause_song():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit the program?"):
        root.destroy()

def search_music():
    search_query = search_entry.get().lower()
    tree.selection_remove(tree.selection())
    for index, song in enumerate(songs):
        song_name = os.path.basename(song).lower()
        if search_query in song_name:
            tree.selection_add(tree.get_children()[index])
            tree.focus(tree.get_children()[index])

def set_volume(val):
    global volume_value
    volume_value = float(val) / 100
    pygame.mixer.music.set_volume(volume_value)

def play_next_song(event=None):
    play_next()

def Check_for_updates():
    """client = Client()
    client.refresh()
    app_update = client.update_check('DoctorMusicPlayer', '2.0')
    if app_update:
        messagebox.showinfo(title="Updater", message="Ažuriranje je dostupno!")
        # Pokreni proces ažuriranja
        client.update(prompt=True)
    else:
        messagebox.showinfo(title="Updater", message="Nema dostupnih ažuriranja.")
"""
    
root = Tk()
root.title("Doctor music player")
root.geometry("900x500")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)


paused = False
songs = []
volume_value = 0.5

pygame.init()

menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Add Song", command=add_song)
file_menu.add_command(label="Add Songs from Folder", command=add_songs_from_folder)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

updater_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Updater", menu=updater_menu)
updater_menu.add_command(label="Check for updates", command=Check_for_updates)

options_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=options_menu)
options_menu.add_command(label="Info", command=show_about_info)

tree = Treeview(root, columns="Size")
tree.heading("#0", text="Song Name")
tree.heading("Size", text="Size (MB)")
tree.pack(side=TOP, fill=BOTH, expand=True)

frame = Frame(root)
frame.pack()

volume_slider = Scale(frame, from_=0, to=100, orient=HORIZONTAL, command=lambda val: set_volume(val))
volume_slider.set(50)
volume_slider.pack(side=LEFT)

play_button = Button(frame, text="Play", command=play_song)
play_button.pack(side=LEFT)

next_button = Button(frame, text="Next", command=play_next)
next_button.pack(side=RIGHT)

previous_button = Button(frame, text="Previous", command=play_previous)
previous_button.pack(side=RIGHT)

pause_button = Button(frame, text="Pause", command=pause_song)
pause_button.pack(side=RIGHT)

search_frame = Frame(root)
search_frame.pack(side=BOTTOM, padx=10, pady=10)

search_entry = Entry(search_frame)
search_entry.pack(side=LEFT, padx=5)

search_button = Button(search_frame, text="Search", command=search_music)
search_button.pack(side=LEFT, padx=5)

root.after(1000, lambda: pygame.mixer.music.set_endevent(pygame.USEREVENT + 1))
root.bind(pygame.USEREVENT + 1, play_next_song)

root.mainloop()
