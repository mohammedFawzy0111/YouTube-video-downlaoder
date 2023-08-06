from pytube import YouTube
from pytube.exceptions import *
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from threading import Thread


# convert sizes
def convert_size(bytes):
    # convert constants
    KB = 1024
    MB = KB ** 2
    GB = KB ** 3
    # convert the bytes
    if bytes >= GB:
        size = "{:.2f} GB".format(bytes / GB)
    elif bytes >= MB:
        size = "{:.2f} MB".format(bytes / MB)
    elif bytes >= KB:
        size = "{:.2f} KB".format(bytes / KB)
    else:
        size = "{:.2f} bytes".format(bytes)
    return size


# download yt video
def download_yt_video():
    url = link_entry.get()
    destination = path_entry.get()
    link_entry.configure(state="disabled")
    try:
        download_btn.configure(state="disabled")
        video = YouTube(url=url, on_progress_callback=update_progress,
                        on_complete_callback=comlete_download)
    except AgeRestrictedError:
        messagebox.showerror(
            title="error", message="this video is age restricted and can not be accessed without OAuth")
    except LiveStreamError:
        messagebox.showerror(
            title="error", message="can not downlaod a live stream")
    except MembersOnly:
        messagebox.showerror(
            title="error", message="this video is members only")
    except VideoPrivate:
        messagebox.showerror(
            title="error", message="can not download private videoes")
    except VideoRegionBlocked:
        messagebox.showerror(
            title="error", message="this video is blocked in your region")
    except VideoUnavailable:
        messagebox.showerror(
            title="error", message="this video is not availavle")
    except e:
        messagebox.showerror(title="error", message=f"ERROR:{e}")

    stream = video.streams.get_highest_resolution()
    status.configure(
        text=f"Status: downloading | 0 KB/{convert_size(stream.filesize)}")
    stream.download(output_path=destination)


# progress bar updater
def update_progress(stream, chunk, bytes_remainig):
    downloaded = (stream.filesize-bytes_remainig)/stream.filesize
    progress_bar.set(downloaded)
    status.configure(
        text=f"Status: downloading | {convert_size(stream.filesize-bytes_remainig)}/{convert_size(stream.filesize)}")


def comlete_download(stream, file_path):
    link_entry.configure(state="normal")
    download_btn.configure(state="normal")
    progress_bar.set(1)
    status.configure(text="Status: download completed program is ready")


# get the default download folder
def get_default_downloads_folder():
    if os.name == 'posix':  # For Unix/Linux/MacOS
        return os.path.expanduser('~/Downloads')
    elif os.name == 'nt':  # For Windows
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return None  # Unsupported operating system


# browse folders
def pick_dir():
    directory = filedialog.askdirectory()
    if directory:
        path_entry.delete(0, "end")
        path_entry.insert(0, directory)


# build the gui
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Video Downloader")
root.geometry("600x400")
root.resizable(width=False, height=False)

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=50, expand=True)

label = ctk.CTkLabel(master=frame, text="Video Downloader", font=("Arial", 20))
label.pack(pady=10)

link_entry = ctk.CTkEntry(master=frame, width=400, height=30,
                          corner_radius=5, placeholder_text="video url")
link_entry.pack(padx=50, pady=20)

frame2 = ctk.CTkFrame(master=frame)
frame2.pack(pady=20, expand=True)

path_entry = ctk.CTkEntry(master=frame2, width=330, height=30, corner_radius=5)
path_entry.pack(padx=(0, 10), side="left")
path_entry.insert(0, get_default_downloads_folder())

browse_btn = ctk.CTkButton(master=frame2, width=60,
                           height=30, corner_radius=5, text="Browse", command=pick_dir)
browse_btn.configure(cursor="hand2")
browse_btn.pack(side="right")

download_btn = ctk.CTkButton(
    master=frame, width=100, height=30, text="Download", corner_radius=5, command=lambda: Thread(target=download_yt_video).start())
download_btn.configure(cursor="hand2")
download_btn.pack(pady=10)

info_frame = ctk.CTkFrame(master=root)
info_frame.pack(padx=50, expand=True)

status = ctk.CTkLabel(
    master=info_frame, text="Status: Ready", font=("Arial", 14))
status.pack(pady=10)

progress_bar = ctk.CTkProgressBar(
    master=info_frame, width=500, height=30, corner_radius=5, border_width=1, mode="determinate")
progress_bar.set(0)
progress_bar.pack(pady=10)

root.mainloop()
