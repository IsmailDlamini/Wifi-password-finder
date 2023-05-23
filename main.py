
import tkinter as tk
from tkinter import *
import subprocess
from tkinter import ttk
from PIL import ImageTk, Image


main = tk.Tk()

# set_screen_position

window_width = 600
window_height = 400
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

main.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
main.configure(bg="light grey")


selected = ""

def clean_data():

    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], shell=True, text=False)
    data_sorted = data.decode('utf-8', errors="backslashreplace").split('\n')

    profiles = []

    for name in data_sorted:
        if 'All User Profile' in name:
            word_lenght = len(name.split(":")[1]) + 1
            profiles.append(name.split(":")[1][1:word_lenght])

    return(profiles)

Profile_variable = StringVar()
all_profiles = clean_data()
Profile_variable.set("Profile Menu")


def get_password(profile):

    global selected

    try:

        data_keys = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], shell=True, text=False)
        data_keys_sorted = data_keys.decode('utf-8', errors="backslashreplace").split('\n')

        profile_password = []


        for password in data_keys_sorted:
            if "Key Content" in password:
                word_lenght = len(password.split(":")[1]) + 1
                clean_pass = password.split(":")[1][1:word_lenght]
                profile_password.append(clean_pass)

        return(profile_password[0])
    except:
        selected = ""

def display_password():

    global all_profiles

    stored_pass = get_password(clean_data()[all_profiles.index(selected)])
    password_field = tk.Label(main, text="", bg='black', width=44, height=3)
    password_field.place(x=260, y=205)

    password_string = tk.Label(main, text=f'Pass={stored_pass}', bg='black', foreground='white', font=("freesansbold.ttf", 10))
    password_string.place(x=265, y=220)



def set_profile(profile):

    global profile_menu, selected, Profile_variable
    selected = Profile_variable.get()


def copy():

    global all_profiles
    
    stored_pass = get_password(clean_data()[all_profiles.index(selected)])
    main.clipboard_append(stored_pass)

def save_to_file():

    global all_profiles
    
    stored_pass = get_password(clean_data()[all_profiles.index(selected)])
    
    password_file = open('Wi-Fi_passwords.txt', "a")
    password_file.write(f'{selected} : {stored_pass}\n')


def clear():

    password_field = tk.Label(main, text="", bg='black', width=44, height=3)
    password_field.place(x=260, y=205)    


image1 = ImageTk.PhotoImage(Image.open("Logo.png"))
image_holder = tk.Button(main, image=image1, width=600, height=300)
image_holder.place(x=0, y=0)

border_bottom = tk.Label(main, text="", bg="black", width=30, height=9)
border_bottom.place(x=10, y=190)

border_top = tk.Label(main, text="", bg="light grey", width=28, height=8)
border_top.place(x=16, y=197)

selection_prompt = tk.Label(main, text="Select Profile", foreground="black", bg="light grey", font=("freesansbold.ttf", 15))
selection_prompt.place(x=55, y=175)

border_bottom2 = tk.Label(main, text="", bg="black", width=47, height=9)
border_bottom2.place(x=250, y=190)

border_top2 = tk.Label(main, text="", bg="light grey", width=45, height=8)
border_top2.place(x=256, y=197)

selection_prompt2 = tk.Label(main, text="Profile Password", foreground="black", bg="light grey", font=("freesansbold.ttf", 15))
selection_prompt2.place(x=350, y=175)

creator_credit = tk.Label(main, text="code king, copyright reserved -- code lab 2023", foreground="black", bg="light grey", font=("freesansbold.ttf", 20))
creator_credit.place(x=10, y=350)

profile_menu = tk.OptionMenu(main, Profile_variable, *all_profiles, command=set_profile)
profile_menu.place(x=40, y=210)
profile_menu.config(width=18, height=2)

search_password = tk.Button(main, text="Get Password", bg="green", width=10, command=display_password)
search_password.place(x=75, y=260)

delete_profile = tk.Button(main, text="Delete Profile", bg="red", width=10)
delete_profile.place(x=75, y=290)

password_field = tk.Label(main, text="", bg='black', width=44, height=3)
password_field.place(x=260, y=205)

copy_password = tk.Button(main, text="Copy Password", bg="grey", width=14, height=2, command=copy)
copy_password.place(x=260, y=280)

save_password = tk.Button(main, text="Save to File", bg="grey", width=14, height=2, command=save_to_file)
save_password.place(x=375, y=280)

clear_field = tk.Button(main, text="Clear", bg="grey", width=10, height=2, command=clear)
clear_field.place(x=490, y=280)

main.mainloop()
