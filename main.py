import tkinter
import customtkinter as ctk
import yt_dlp
import certifi
import os
import re

os.environ['SSL_CERT_FILE'] = certifi.where()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Video link downloader")
app.geometry("720x480")

url_bar = tkinter.StringVar()
title = ctk.CTkLabel(app, text="Insert video link", font=("Arial", 20))
link = ctk.CTkEntry(app, width=350, height=40, textvariable=url_bar)
link.pack()

def remove_ansi_escape_codes(s):
  ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
  return ansi_escape.sub('', s)

def on_progress(d):
  if d['status'] == 'downloading':
    p = remove_ansi_escape_codes(d['_percent_str'])
    pPercentage.configure(text=p)
    pPercentage.update()
    
    # Extracting and formatting the ETA
    eta_seconds = d.get('eta', 0)
    eta_minutes, eta_seconds = divmod(eta_seconds, 60)
    eta_str = f"{int(eta_minutes):02d}:{int(eta_seconds):02d}"
    etaLabel.configure(text=f"ETA: {eta_str}")
    
    progressBar.set(float(p.replace('%', ''))/100)

def startDownload():
  try:
      ydl_opts = {
        'progress_hooks': [on_progress],
        'outtmpl': '%(title)s.%(ext)s',  # Save the video with its title as the filename
      }
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url_bar.get(), download=False)
        title.configure(text=info_dict['title'], text_color="white")
        ydl.download([url_bar.get()])
        finished.configure(text="Finished")
  except Exception as e:
    print(e)
    finished.configure(text="Download error", text_color="red")

download = ctk.CTkButton(app, text="Download", width=100, height=40, command=startDownload)
download.pack(padx=10, pady=10)

finished = ctk.CTkLabel(app, text="")
finished.pack()

etaLabel = ctk.CTkLabel(app, text="ETA: 00:00")
etaLabel.pack()

# progress bar
pPercentage = ctk.CTkLabel(app, text="0%")
pPercentage.pack()
progressBar = ctk.CTkProgressBar(app, width=350)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

app.mainloop()
