from tkinter import *
import math
import os



# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
mark = ""
timer = None
time = 0
# sound


def beep():
    duration = 0.2  # seconds
    freq = 550  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


# ---------------------------- TIMER RESET ------------------------------- #

# ---------------------------- TIMER MECHANISM ------------------------------- #


def timer_start():
    beep()
    global reps
    reps += 1

    if reps % 8 == 0:
        count = LONG_BREAK_MIN * 60
        tm_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count = SHORT_BREAK_MIN * 60
        tm_label.config(text="Break", fg=PINK)
    else:
        count = WORK_MIN * 60
        tm_label.config(text="Work", fg=GREEN)
    count_down(count)
    start_btn.config(text="Pause", command=timer_pause)


def timer_reset():
    beep()
    global timer
    global reps
    global mark
    global time
    mark = ""
    reps = 0
    time = 0
    win.after_cancel(timer)
    tick_label.config(text=mark)
    tm_label.config(text="Timer", fg=GREEN)
    canv.itemconfig(canv_text, text="00:00")
    pause_label.config(text="")
    start_btn.config(text="Start", command=timer_start)


def timer_pause():
    beep()
    win.after_cancel(timer)
    start_btn.config(text="Start", command=timer_cont)
    pause_label.config(text="Pause")


def timer_cont():
    beep()
    count_down(time)
    start_btn.config(text="Pause", command=timer_pause)
    pause_label.config(text="")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global mark
    global reps
    global timer
    global time
    if count > 0:
        time = count
        timer = win.after(1000, count_down, count-1)
        count_min = int(math.floor(count/60))
        if count_min < 10:
            count_min = f"0{count_min}"
        count_sec = int(count % 60)
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        canv.itemconfig(canv_text, text=f"{count_min}:{count_sec}")
    else:
        if (reps+1) % 2 == 0:
            mark += "✔"
        tick_label.config(text=mark)
        beep()
        timer_start()


# ---------------------------- UI SETUP ------------------------------- #
win = Tk()
win.title("Pomodoro")
win.config(padx=100, pady=50, bg=YELLOW)
canv = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = PhotoImage(file="tomato.png")
canv.create_image(100, 112, image=img)
canv_text = canv.create_text(100, 140, text="00:00", fill="white",
                             font=(FONT_NAME, 35, "bold"))
canv.grid(column=1, row=1)

tm_label = Label(text="Timer", fg=GREEN, font=(
    FONT_NAME, 40, "bold"), bg=YELLOW)
tm_label.grid(column=1, row=0)

start_btn = Button(text="Start", font=(
    FONT_NAME, 10, "bold"), command=timer_start)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", font=(
    FONT_NAME, 10, "bold"), command=timer_reset)
reset_btn.grid(column=2, row=2)

tick_label = Label(text="", bg=YELLOW, fg=GREEN,
                   font=(FONT_NAME, 30, "bold"))
tick_label.grid(column=1, row=3)

pause_label = Label(text="", fg=RED, font=(
    FONT_NAME, 20, "bold"), bg=YELLOW)
pause_label.grid(column=1, row=4)

win.mainloop()
