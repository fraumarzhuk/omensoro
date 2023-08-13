from playsound import playsound
from tkinter import *
from PIL import Image, ImageTk
import math

import os
base_dir = os.path.dirname(__file__)
crowley_path = os.path.join(base_dir, './crowley.mp3')
wahoo_path = os.path.join(base_dir, './wahoo.mp3')
cr_img = os.path.join(base_dir, './cr.jpg')
az_img = os.path.join(base_dir, './az.png')
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
WHITE = "#FFFFFF"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
current_count = 0
is_paused = False
is_running = False
prev_title = "Timer"
prev_fg = GREEN
# ---------------------------- TIMER STOP ------------------------------- # 
def stop_timer():
    global prev_title, prev_fg

    if not is_running:
        return

    global is_paused
    if is_paused:
        is_paused = False
        stop_button.config(text="Pause")
        title_label.config(text=prev_title, fg=prev_fg)
        count_down(current_count)
    else:
        is_paused = True
        prev_title = title_label.cget("text")
        prev_fg = title_label.cget("foreground")
        title_label.config(text="Pause", fg=PINK)
        stop_button.config(text="Continue")
        window.after_cancel(timer)
# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- SOUNDS ------------------------------- #
def play_work():
    playsound(crowley_path)
def play_break():
    playsound(wahoo_path)
# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    global is_running
    is_running = True
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        cur_img = ImageTk.PhotoImage(Image.open(cr_img))
        canvas.image = cur_img
        canvas.create_image(100, 112, image=cur_img)
        play_break()
        prev_title, prev_fg = "Break", RED
        title_label.config(text=prev_title, fg=prev_fg)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        cur_img = ImageTk.PhotoImage(Image.open(cr_img))
        canvas.image = cur_img
        canvas.create_image(100, 112, image=cur_img)
        play_break()
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        cur_img = ImageTk.PhotoImage(Image.open(az_img))
        canvas.image = cur_img
        canvas.create_image(100, 112, image=cur_img)
        play_work()
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global current_count
    current_count = count
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0 and not is_paused:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif is_paused:
        return
    else:
        is_running = False
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Good omensoro")
window.config(padx=100, pady=50, bg=WHITE)


title_label = Label(text="Timer", fg=GREEN, bg=WHITE, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=WHITE, highlightthickness=0)
cur_img = ImageTk.PhotoImage(Image.open(az_img))
canvas.create_image(100, 112, image=cur_img)
timer_text = canvas.create_text(100, 210, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightbackground=WHITE, activeforeground=GREEN, command=start_timer)
start_button.grid(column=0, row=4)

stop_button = Button(text="Pause", highlightbackground=WHITE, activeforeground=YELLOW, command=stop_timer)
stop_button.grid(column=1, row=4)

reset_button = Button(text="Reset", highlightbackground=WHITE, activeforeground=RED, command=reset_timer)
reset_button.grid(column=2, row=4)

check_marks = Label(fg=GREEN, bg=WHITE)
check_marks.grid(column=1, row=3)

window.mainloop()
