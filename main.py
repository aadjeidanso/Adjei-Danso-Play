import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import mutagen
from mutagen.mp3 import MP3

class AdjeidansoplayApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title and geometry of the main window
        self.title("adjeidansoplay")
        self.geometry("1000x600")  # Increased width for the sidebar
        self.configure(bg="#002244")  # Background color updated to #002244

        # Set the window icon (logo)
        self.logo_image = Image.open("mylogo.png")  # Update with the correct path to your logo
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.iconphoto(False, self.logo_photo)

        # Initialize pygame's mixer
        pygame.mixer.init()

        # Initialize track list and index
        self.track_list = ['Ayisi-Self-Made-(TrendyBeatz.com).mp3', 'Black_Sherif_-_OH_NO.mp3', 'Black-Sherif-Shut-Up.mp3','Black-Sherif-Yaya-(TrendyBeatz.com).mp3','blacksherifkilosmilos.mp3','Brown-Joel-Ft-BoyPee_Davido-Ogechi.mp3','Burna-Boy-Ye-[TrendyBeatz.com].mp3','Eminem_Not_Afraid_(thinkNews.com.ng).mp3','Fameye-Ft-Stonebwoy-Not-God-Remix.mp3','Kendrick Lamar - euphoria.mp3','simmerdown.mp3','Teni-Uyo-Meyo-Official-Audio.mp3','yesuarajay.mp3']  # Replace with your actual track paths
        self.current_track_index = 0
        self.paused = False
        self.repeat = False  # Repeat functionality state

        # Initialize playlists
        self.playlists = {}  # Dictionary to store playlists and their songs

        # Configure the style for Treeview to have distinct grid lines
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12, "bold"), background="#a21920", foreground="#a21920")
        style.configure("Custom.Treeview", rowheight=30, background="#e9e3da", foreground="#002244", fieldbackground="#e9e3da", bordercolor="#002244", borderwidth=1)
        style.map("Custom.Treeview", background=[('selected', '#002244')], foreground=[('selected', '#e9e3da')])
        style.layout("Custom.Treeview", [('Custom.Treeview.treearea', {'sticky': 'nswe'})])

        # Initialize the UI components
        self.create_widgets()

        # Display the home content by default
        self.show_home()

        # Continuously check if the track has ended
        self.check_track_end()

    def create_widgets(self):
        # Sidebar
        sidebar_frame = tk.Frame(self, width=200, bg="#a21920", relief="sunken")  # Sidebar color updated to #a21920
        sidebar_frame.pack(fill="y", side="left")

        # Logo and App Name
        logo_label = tk.Label(sidebar_frame, image=self.logo_photo, bg="#a21920")
        logo_label.pack(pady=10)

        app_name_label = tk.Label(sidebar_frame, text="adjeidansoplay", bg="#a21920", fg="#e9e3da",
                                  font=("Helvetica", 18, "bold"))  # Adjust font size and style
        app_name_label.pack(pady=5)

        # Search Bar
        search_entry = tk.Entry(sidebar_frame, bg="#e9e3da", fg="#002244", insertbackground="#002244", relief="flat")
        search_entry.insert(0, "Search")
        search_entry.pack(pady=10, padx=10, fill="x")

        # Sidebar items
        home_button = tk.Button(sidebar_frame, text="Home", bg="#a21920", fg="#e9e3da", relief="flat", anchor="w", command=self.show_home)
        home_button.pack(fill="x", padx=10, pady=5)

        library_button = tk.Button(sidebar_frame, text="Music library", bg="#a21920", fg="#e9e3da", relief="flat", anchor="w", command=self.show_music_library)
        library_button.pack(fill="x", padx=10, pady=5)

        playlist_button = tk.Button(sidebar_frame, text="Playlists", bg="#a21920", fg="#e9e3da", relief="flat", anchor="w", command=self.show_playlists)
        playlist_button.pack(fill="x", padx=10, pady=5)

        # Main content area for album art and track info
        self.content_frame = tk.Frame(self, bg="#002244")  # Content area background color updated to #002244
        self.content_frame.pack(fill="both", expand=True, side="left")

    def show_home(self):
        # Clear the current content in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Load and display the album art image as background
        album_art_image = Image.open("album.jpg")  # Replace with the actual path to your image
        album_art_image = album_art_image.resize((1400, 1000), Image.LANCZOS)  # Resize to fit the content area
        album_art = ImageTk.PhotoImage(album_art_image)

        album_art_label = tk.Label(self.content_frame, image=album_art)
        album_art_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire background

        # Keep a reference to the image to prevent it from being garbage collected
        album_art_label.image = album_art

        # Track label to display the currently playing track
        self.track_label = tk.Label(self.content_frame, text="No track playing", bg="#002244", fg="#e9e3da", font=("Helvetica", 24), borderwidth=0, highlightthickness=0)
        self.track_label.place(relx=0.5, rely=0.1, anchor="center")  # Positioning at the top center

        # Control frame for the buttons and volume control
        control_volume_frame = tk.Frame(self.content_frame, bg="#002244", bd=0)
        control_volume_frame.place(relx=0.5, rely=0.6, anchor="center")

        # Control buttons (Previous, Play, Pause, Stop, Next, Repeat)
        control_frame = tk.Frame(control_volume_frame, bg="#002244", bd=0)
        control_frame.grid(row=0, column=0)

        prev_icon = ImageTk.PhotoImage(Image.open("prev.png").resize((40, 40), Image.LANCZOS))
        play_icon = ImageTk.PhotoImage(Image.open("play.png").resize((40, 40), Image.LANCZOS))
        pause_icon = ImageTk.PhotoImage(Image.open("pause.png").resize((40, 40), Image.LANCZOS))
        stop_icon = ImageTk.PhotoImage(Image.open("stop.png").resize((40, 40), Image.LANCZOS))
        next_icon = ImageTk.PhotoImage(Image.open("next.png").resize((40, 40), Image.LANCZOS))
        repeat_icon = ImageTk.PhotoImage(Image.open("repeat.png").resize((40, 40), Image.LANCZOS))  # Add your repeat icon here

        self.prev_button = tk.Button(control_frame, image=prev_icon, command=self.prev_track, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.prev_button.image = prev_icon  # Keep a reference to prevent garbage collection
        self.prev_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(control_frame, image=play_icon, command=self.play_music, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.play_button.image = play_icon  # Keep a reference to prevent garbage collection
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(control_frame, image=pause_icon, command=self.pause_music, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.pause_button.image = pause_icon  # Keep a reference to prevent garbage collection
        self.pause_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(control_frame, image=stop_icon, command=self.stop_music, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.stop_button.image = stop_icon  # Keep a reference to prevent garbage collection
        self.stop_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(control_frame, image=next_icon, command=self.next_track, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.next_button.image = next_icon  # Keep a reference to prevent garbage collection
        self.next_button.grid(row=0, column=4, padx=10)

        self.repeat_button = tk.Button(control_frame, image=repeat_icon, command=self.toggle_repeat, bg="#002244", fg="#e9e3da", relief="flat", borderwidth=0)
        self.repeat_button.image = repeat_icon  # Keep a reference to prevent garbage collection
        self.repeat_button.grid(row=0, column=5, padx=10)

        # Volume control
        volume_frame = tk.Frame(control_volume_frame, bg="#002244")
        volume_frame.grid(row=0, column=1, padx=20)

        volume_label = tk.Label(volume_frame, text="Volume", bg="#002244", fg="#e9e3da")
        volume_label.pack(side="left")

        self.volume_control = tk.Scale(volume_frame, from_=0, to=100, orient='horizontal', resolution=1, command=self.set_volume, bg="#002244", fg="#e9e3da", troughcolor="#a21920", sliderrelief="flat", length=150)
        self.volume_control.set(100)  # Set default volume to 100%
        self.volume_control.pack(side="left")

        # Seek bar
        self.seek_bar = tk.Scale(self.content_frame, from_=0, to=100, orient='horizontal', length=600, command=self.seek_music, bg="#002244", fg="#e9e3da", troughcolor="#a21920", sliderrelief="flat")
        self.seek_bar.place(relx=0.5, rely=0.5, anchor="center")

        # Label to display current time and total time
        self.time_label = tk.Label(self.content_frame, text="00:00 / 00:00", bg="#002244", fg="#e9e3da", font=("Helvetica", 14))
        self.time_label.place(relx=0.5, rely=0.45, anchor="center")

    def show_music_library(self):
        # Clear the current content in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Display the list of songs in a table
        song_list_label = tk.Label(self.content_frame, text="Music Library", bg="#002244", fg="#e9e3da", font=("Helvetica", 24))
        song_list_label.pack(pady=10)

        song_table = ttk.Treeview(self.content_frame, columns=("Track", "Actions"), show="headings", height=10, style="Custom.Treeview")
        song_table.heading("Track", text="Track")
        song_table.heading("Actions", text="Actions")
        song_table.column("Track", anchor="w")
        song_table.column("Actions", anchor="center")

        for index, song in enumerate(self.track_list):
            song_table.insert("", "end", values=(f"{index + 1}. {song}", "Add to Playlist"))

        song_table.pack(fill="both", padx=20, pady=5)
        song_table.bind("<ButtonRelease-1>", self.on_song_click)

    def on_song_click(self, event):
        item = event.widget.identify_row(event.y)
        if item:
            col = event.widget.identify_column(event.x)
            selected_song = event.widget.item(item, "values")[0]
            if col == '#2':  # Check if the "Actions" column was clicked
                song = selected_song.split(". ", 1)[1]
                self.add_to_playlist(song)

    def add_to_playlist(self, song):
        if self.playlists:
            # Create a new window to select the playlist
            new_window = tk.Toplevel(self)
            new_window.title("Select Playlist")
            new_window.geometry("300x200")
            new_window.configure(bg="#002244")

            playlist_label = tk.Label(new_window, text="Select Playlist", bg="#002244", fg="#e9e3da", font=("Helvetica", 14))
            playlist_label.pack(pady=10)

            for playlist_name in self.playlists:
                playlist_button = tk.Button(new_window, text=playlist_name, command=lambda pn=playlist_name: self.save_to_playlist(pn, song, new_window), bg="#a21920", fg="#e9e3da")
                playlist_button.pack(pady=5)
        else:
            # If no playlists exist
            new_window = tk.Toplevel(self)
            new_window.title("Error")
            new_window.geometry("300x100")
            new_window.configure(bg="#002244")

            error_label = tk.Label(new_window, text="No playlists available", bg="#002244", fg="#ff0000", font=("Helvetica", 14))
            error_label.pack(pady=20)

    def save_to_playlist(self, playlist_name, song, window):
        if song not in self.playlists[playlist_name]:
            self.playlists[playlist_name].append(song)
        window.destroy()

    def show_playlists(self):
        # Clear the current content in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Display playlists title
        playlists_label = tk.Label(self.content_frame, text="Playlists", bg="#002244", fg="#e9e3da", font=("Helvetica", 24))
        playlists_label.pack(pady=10)

        # Display existing playlists in a table
        playlist_table = ttk.Treeview(self.content_frame, columns=("Playlist", "Actions"), show="headings", height=10, style="Custom.Treeview")
        playlist_table.heading("Playlist", text="Playlist")
        playlist_table.heading("Actions", text="Actions")
        playlist_table.column("Playlist", anchor="w")
        playlist_table.column("Actions", anchor="center")

        for playlist_name in self.playlists:
            playlist_table.insert("", "end", values=(playlist_name, "View Songs"))

        playlist_table.pack(fill="both", padx=20, pady=5)
        playlist_table.bind("<ButtonRelease-1>", self.on_playlist_click)

        # Option to create a new playlist
        new_playlist_button = tk.Button(self.content_frame, text="Create New Playlist", command=self.create_playlist, bg="#a21920", fg="#e9e3da")
        new_playlist_button.pack(pady=20)

    def on_playlist_click(self, event):
        item = event.widget.identify_row(event.y)
        if item:
            col = event.widget.identify_column(event.x)
            selected_playlist = event.widget.item(item, "values")[0]
            if col == '#2':  # Check if the "Actions" column was clicked
                self.show_playlist_songs(selected_playlist)

    def show_playlist_songs(self, playlist_name):
        # Clear the current content in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Display playlist title
        playlist_label = tk.Label(self.content_frame, text=f"Playlist: {playlist_name}", bg="#002244", fg="#e9e3da", font=("Helvetica", 24))
        playlist_label.pack(pady=10)

        # Display songs in the selected playlist in a table
        song_table = ttk.Treeview(self.content_frame, columns=("Track"), show="headings", height=10, style="Custom.Treeview")
        song_table.heading("Track", text="Track")
        song_table.column("Track", anchor="w")

        for index, song in enumerate(self.playlists[playlist_name]):
            song_table.insert("", "end", values=(f"{index + 1}. {song}",))

        song_table.pack(fill="both", padx=20, pady=5)

    def create_playlist(self):
        # Create a new window for creating a playlist
        new_window = tk.Toplevel(self)
        new_window.title("Create New Playlist")
        new_window.geometry("300x150")
        new_window.configure(bg="#002244")

        # Label and entry for the playlist name
        playlist_name_label = tk.Label(new_window, text="Playlist Name:", bg="#002244", fg="#e9e3da", font=("Helvetica", 14))
        playlist_name_label.pack(pady=10)

        playlist_name_entry = tk.Entry(new_window, bg="#e9e3da", fg="#002244")
        playlist_name_entry.pack(pady=5)

        # Button to save the new playlist
        save_button = tk.Button(new_window, text="Save Playlist", command=lambda: self.save_playlist(playlist_name_entry.get(), new_window), bg="#a21920", fg="#e9e3da")
        save_button.pack(pady=10)

    def save_playlist(self, playlist_name, window):
        if playlist_name and playlist_name not in self.playlists:
            self.playlists[playlist_name] = []
            window.destroy()
            self.show_playlists()  # Refresh the playlists view
        else:
            # Handle the case where the playlist name is empty or already exists
            error_label = tk.Label(window, text="Invalid or duplicate name", bg="#002244", fg="#ff0000", font=("Helvetica", 12))
            error_label.pack(pady=5)

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.track_label.config(text=f"Resuming: {self.track_list[self.current_track_index]}")
            self.paused = False
        else:
            # Load and play the current track
            try:
                track_path = self.track_list[self.current_track_index]
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()

                # Get the length of the track using mutagen
                audio = MP3(track_path)
                track_length = audio.info.length
                self.seek_bar.config(to=track_length)

                self.track_label.config(text=f"Playing: {track_path}")
                self.update_seek_bar()
                
            except Exception as e:
                print(f"Error playing file: {e}")

    def check_track_end(self):
        if not pygame.mixer.music.get_busy() and not self.paused:  # Check if music has ended
            self.handle_track_end()
        
        # Keep checking for the event
        self.after(1000, self.check_track_end)

    def handle_track_end(self):
        if self.repeat:
            self.play_music()
        else:
            self.next_track()

    def toggle_repeat(self):
        self.repeat = not self.repeat
        if self.repeat:
            self.repeat_button.config(bg="#90EE90", borderwidth=3, relief="solid", padx=5, pady=5)  # Make the button bigger and more prominent
        else:
            self.repeat_button.config(bg="#002244", borderwidth=0, padx=0, pady=0)  # Revert to original size and color

    def pause_music(self):
        if pygame.mixer.music.get_busy():  # Check if music is playing
            pygame.mixer.music.pause()
            self.track_label.config(text="Music Paused")
            self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.track_label.config(text="No track playing")
        self.seek_bar.set(0)
        self.paused = False

    def seek_music(self, position):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(float(position))

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)  # Adjust the volume from 0% to 100%

    def update_seek_bar(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
            self.seek_bar.set(current_pos)
            formatted_time = self.format_time(current_pos)
            total_time = self.format_time(self.seek_bar['to'])
            self.time_label.config(text=f"{formatted_time} / {total_time}")
        self.after(1000, self.update_seek_bar)

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def prev_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
        self.play_music()

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
        self.play_music()

if __name__ == "__main__":
    app = AdjeidansoplayApp()
    app.mainloop()
