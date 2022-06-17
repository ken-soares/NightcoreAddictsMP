import json
import pygame
from tkinter import *
from tkinter import filedialog

#variables
playlist = []
f = open("config.json")
data = json.load(f)
default_color = data["default-color"]
warning_color = data["warning-color"]
bg_color = data["bg-color"]
bg_button_color = data["bg-button-color"]
current_volume = float(data["default-volume"])
default_file_path = data["default-file-path"]
title_font_size = data["title-font-size"]
regular_font_size = data["regular-font-size"]
playlist_dir = data["playlist-dir"]
using_symbols = data["symbols"]
usr_font = data["font"]
startup_sound = data["startup_sound"]
image_logo = data['logo-image']
pygame.init()
pygame.mixer.init()
startup_sound_file = pygame.mixer.Sound("Misc/click-short.ogg")

if startup_sound:
    pygame.mixer.Sound.play(startup_sound_file)

#window creation
root = Tk()
root.title("NightcoreAddictsMP ver 1.0.0")
root.resizable(height = None, width = None)
root.wm_minsize(400, 500)
root.config(bg=bg_color)
root.resizable(False, False)

c = []
titles = "" 
x= 0

def load_pl():
    global c
    pl_name = filedialog.askopenfilename(initialdir=playlist_dir, title="Please select a file")
    g = open(pl_name, "r+")
    pl_con = g.read()
    pl_con = pl_con.replace("[","")
    pl_con = pl_con.replace("]","")
    pl_con = pl_con.replace("'", '')
    print(pl_con)
    pl_con = pl_con.split(",")
    for song in pl_con:
        c.append(song)
    print(c)
def save_pl():
    global c
    filename = playlist_dir + save_text.get()+".txt"
    print(filename)
    print(c)
    try:
        g = open(filename, "x")
        g.write(str(c))
    except Exception as e:
        print(e)    

def stop_song():
    pygame.mixer.music.stop()
    
def forward():
    global x
    if x < len(c):
        x += 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load(c[x])
        pygame.mixer.music.play(0)

def back():
    global x
    if x > 0:
        x -= 1
        pygame.mixer.music.stop()
        pygame.mixer.music.load(c[x])
        pygame.mixer.music.play(0)
    
def add_to_playlist():
    global c
    filename = filedialog.askopenfilename(initialdir=default_file_path, title="Please select a file")
    if filename != "":
        c.append(filename)
        print(c)

def music():
    try:
        pygame.mixer.music.load(c[x])
        pygame.mixer.music.play(0)
        que()
    except:
        song_title_label.config(fg = warning_color, text="Invalid file format")

def que():
    global x, c
    stuff = pygame.mixer.music.get_busy()
    if stuff:
        song_title = c[x].split("/")
        song_title = song_title[-1]
        with open("Misc/now_playing_obs.txt", "w") as g:
            g.write(song_title + " ")
            g.close
    else:
        song_title = "Stopped playing"
        song_title_label.config(fg=warning_color, text = song_title)
        with open("Misc/now_playing_obs.txt", "w") as g:
            g.write(" ")
            g.close
    if len(song_title) > 36:
        song_title = song_title[0:33] + "...\n"
    else:
        song_title = song_title + "\n"
    song_title_label.config(fg=default_color, text =str(song_title))
    pos = pygame.mixer.music.get_pos()
    if int(pos) == -1:
        if x < len(c) -1:
            x += 1
            pygame.mixer.music.load(c[x])
            pygame.mixer.music.play(0)            
    root.after(1, que)

def reduce_volume():
    try:
        global current_volume
        if current_volume > float(0):
            current_volume = current_volume - float(0.1)
            current_volume = round(current_volume,1)
        if current_volume <= 0.3 or current_volume >= 0.7:
            volume_label.config(fg=warning_color,text="❕Volume: "+str(current_volume))
        else:
            volume_label.config(fg=default_color, text="Volume: " + str(current_volume))
        print(current_volume)
        pygame.mixer.music.set_volume(current_volume)
    except Exception as e:
        print("there was an error:", e)
        pass
    
def increase_volume():
    try:
        global current_volume
        if current_volume < float(1):
            current_volume = current_volume + float(0.1)
            current_volume = round(current_volume,1)
        if current_volume >= 0.7 or current_volume <= 0.3:
            volume_label.config(fg=warning_color, text="❕Volume: "+ str(current_volume))
        else:
            volume_label.config(fg=default_color, text="Volume: " + str(current_volume))
        print(current_volume)        
        pygame.mixer.music.set_volume(current_volume)
    except Exception as e:
        print("there was an error:", e)
        pass

def pause_song():
    global IsPaused
    try:
        pygame.mixer.music.pause()
    except Exception as e:
        print(e)
        song_title_label.config(fg=warning_color, text="Track hasn't been selected yet")
        
def resume_song():
    try:
        pygame.mixer.music.unpause()
    except Exception as e:
        print(e)
        song_title_label.config(fg=warning_color, text="Track hasn't been selected yet")

#Labels

logo = PhotoImage(file=image_logo)
logo_label = Label(root, image=logo,bg=bg_color)
logo_label.grid(sticky="W", row=0, padx=10,)
Label(root,text="\nNightcoreAddictsMP ver 1.0.0\n", bg=bg_color, font=(usr_font, title_font_size),fg=default_color).grid(sticky="N",row=0,padx=120)
Label(root,text='Please add your song with "Add to PL"', bg=bg_color, font=(usr_font, regular_font_size),fg=default_color).grid(sticky="N",row=1)
song_title_label = Label(root, bg=bg_color, font=(usr_font, regular_font_size))
song_title_label.grid(sticky="N", row=3)
volume_label = Label(root, bg=bg_color, font=(usr_font, regular_font_size))
volume_label.grid(sticky="N", row=4)
save_text = Entry(root, bg=bg_color, font=(usr_font, regular_font_size), fg=default_color)
Label(root,text='\n save playlist as:', bg=bg_color, font=(usr_font, regular_font_size),fg=default_color).grid(sticky="N",row=13)
save_text.grid(row=14, sticky="N")

#Buttons
if using_symbols:
    Button(root, text="Play⏵", bg=bg_button_color,font=(usr_font, regular_font_size),width=20,command=music, fg=default_color).grid(row=11, sticky="N")
    Button(root, text="VOL🕩", bg=bg_button_color,font=(usr_font,regular_font_size), width=10, command=reduce_volume,fg=default_color).grid(row=4,sticky="W",padx=50)
    Button(root, text="VOL🕩", bg=bg_button_color,font=(usr_font,regular_font_size), width=10, command=increase_volume,fg=default_color).grid(row=4,sticky="E",padx=50)     
    Button(root, text="Pause⏸", bg=bg_button_color,font=(usr_font,regular_font_size), width=10,command=pause_song,fg=default_color).grid(row=5,sticky="E",padx=50)
    Button(root, text="Resume⏵", bg=bg_button_color,font=(usr_font,regular_font_size),width=10, command=resume_song,fg=default_color).grid(row=5,sticky="W",padx=50)
    Button(root, text="Add to PL+", bg=bg_button_color,font=(usr_font, regular_font_size),width=10, command=add_to_playlist,fg=default_color).grid(row=8, sticky="W",padx=50)
    Button(root, text="Save PL⮷", bg=bg_button_color, font=(usr_font, regular_font_size),command=save_pl,width=8,fg=default_color).grid(row=14, sticky="W", padx=50)
    Button(root, text="Load PL⮴", bg=bg_button_color, font=(usr_font, regular_font_size),command=load_pl,width=10,fg=default_color).grid(row=8, sticky="E", padx=50)
    Button(root, text="Stop■", bg=bg_button_color, font=(usr_font, regular_font_size),command=stop_song,width=20,fg=default_color).grid(row=12,sticky="N",padx=50)
    Button(root, text="Next⇨", bg=bg_button_color, font=(usr_font, regular_font_size),command=forward,width=10,fg=default_color).grid(row=7,sticky="E",padx=50)
    Button(root, text="⇦Previous", bg=bg_button_color, font=(usr_font, regular_font_size),command=back,width=10,fg=default_color).grid(row=7,sticky="W",padx=50)
else:
    Button(root, text="Play", bg=bg_button_color,font=(usr_font, regular_font_size),width=20,command=music,fg=default_color).grid(row=11, sticky="N")
    Button(root, text="VOL-", bg=bg_button_color,font=(usr_font,regular_font_size), width=10, command=reduce_volume,fg=default_color).grid(row=4,sticky="W",padx=50)
    Button(root, text="VOL+", bg=bg_button_color,font=(usr_font,regular_font_size), width=10, command=increase_volume,fg=default_color).grid(row=4,sticky="E",padx=50)
    Button(root, text="Pause", bg=bg_button_color,font=(usr_font,regular_font_size), width=10,command=pause_song,fg=default_color).grid(row=5,sticky="E",padx=50)
    Button(root, text="Resume", bg=bg_button_color,font=(usr_font,regular_font_size),width=10, command=resume_song,fg=default_color).grid(row=5,sticky="W",padx=50)
    Button(root, text="Add to PL", bg=bg_button_color,font=(usr_font, regular_font_size),width=10, command=add_to_playlist,fg=default_color).grid(row=8, sticky="W",padx=50)
    Button(root, text="Save PL", bg=bg_button_color, font=(usr_font, regular_font_size),command=save_pl,width=8,fg=default_color).grid(row=14, sticky="W", padx=50)
    Button(root, text="Load PL", bg=bg_button_color, font=(usr_font, regular_font_size),command=load_pl,width=10,fg=default_color).grid(row=8, sticky="E", padx=50)
    Button(root, text="Stop", bg=bg_button_color, font=(usr_font, regular_font_size),command=stop_song,width=20,fg=default_color).grid(row=12,sticky="N",padx=50)
    Button(root, text="Next", bg=bg_button_color, font=(usr_font, regular_font_size),command=forward,width=10,fg=default_color).grid(row=7,sticky="E",padx=50)
    Button(root, text="Previous", bg=bg_button_color, font=(usr_font, regular_font_size),command=back,width=10,fg=default_color).grid(row=7,sticky="W",padx=50)
root.mainloop()
            
        
            
