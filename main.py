from tkinter.ttk import *
from tkinter import *

from PIL import ImageTk, Image

from pygame import mixer
from datetime import datetime
from time import sleep
import threading

from datetime import date
import calendar, schedule


# Colours:
bg_color = '#BFC9CA'
color1 = '#2E86C1'  # Blue
color2 = '#000000' # Black

# Window
window = Tk()
window.title('')
window.geometry('350x150')
window.configure(bg=bg_color)

# Frame up
frame_line = Frame(window, width=400, height=5, bg=color1)
frame_line.grid(row=0, column=0)

frame_body = Frame(window, width=400, height=290, bg=bg_color)
frame_body.grid(row=1, column=0)


# Configuring frame body and appending our icon to the main window:
img = Image.open('icon.png')
img.resize((100,100))
img = ImageTk.PhotoImage(img)

app_image = Label(frame_body, height=100, image=img, bg=bg_color)
app_image.place(x=10, y=10)

name = Label(frame_body, text= 'Alarm', height=1, font=('Ivy 25 bold'), bg=bg_color)
name.place(x=125, y=10)


# Bg and fg for background and full ground colour.
hour = Label(frame_body, text='hour', height=1, font=('Ivy 10 bold'), bg=bg_color, fg=color1)
hour.place(x=127, y=40)
c_hour = Combobox(frame_body, width=2, font=('arial 15'))
c_hour['values'] = ('00','01','02','03','04','05','06','07','08','09','10','11','12')
c_hour.current(0)
c_hour.place(x=130,y=58)

# Bg and fg for background and full ground colour.
min = Label(frame_body, text='min', height=1, font=('Ivy 10 bold'), bg=bg_color, fg=color1)
min.place(x=177, y=40)
c_min = Combobox(frame_body, width=2, font=('arial 15'))
c_min['values'] = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59')
c_min.current(0)
c_min.place(x=180,y=58)

sec = Label(frame_body, text='sec', height=1, font=('Ivy 10 bold'), bg=bg_color, fg=color1)
sec.place(x=227, y=40)
c_sec = Combobox(frame_body, width=2, font=('arial 15'))
c_sec['values'] = ('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59')
c_sec.current(0)
c_sec.place(x=230,y=58)

period = Label(frame_body, text='sec', height=1, font=('Ivy 10 bold'), bg=bg_color, fg=color1)
period.place(x=277, y=40)
c_period = Combobox(frame_body, width=3, font=('arial 15'))
c_period['values'] = ('AM', 'PM')
c_period.current(0)
c_period.place(x=280,y=58)

def song_choice():

    my_date = date.today()
    if calendar.day_name[my_date.weekday()] == 'Monday':
        return 'Monday.mp3'
    elif calendar.day_name[my_date.weekday()] == 'Tuesday':
        return 'Tuesday.mp3'
    elif calendar.day_name[my_date.weekday()] == 'Wednesday':
        return 'Wednesday.mp3'
    elif calendar.day_name[my_date.weekday()] == 'Thursday':
        return 'Thursday.mp3'
    elif calendar.day_name[my_date.weekday()] == 'Friday':
        return 'Friday.mp3'
    elif calendar.day_name[my_date.weekday()] == 'Saturday':
        return 'Saturday.mp3'
    else:
        return 'Sunday.mp3'


def activate_alarm():
# We use the Thread class to schedule the alarm's activation.
    t = threading.Thread(target=alarm, daemon=True)
    t.start()


def deactivate_alarm():
    print('Deactivated alarm: ', selected.get())
    mixer.music.stop()
    return True

# The below allows us to capture integer variables from the user and pipe them to our checkbox button. The activate
# interface will be activated as soon as the user selects the time at which they wish for the alarm to ring. We code
# a separate function to manage this.
selected = IntVar()


rad1 = Radiobutton(frame_body, font=('arial 10 bold'), value = 1, text = 'Activate', bg=bg_color, command=activate_alarm,
                   variable=selected)
rad1.place(x=125, y=95)



def simplified_sound_alarm(saved_song):
    mixer.music.load(str(saved_song))

    mixer.music.play()
    selected.set(0)
    return True

def sound_alarm():

    # For example: mixer.music.load('Monday.mp3')
    saved_song = song_choice()
    print(saved_song)
    mixer.music.load(str(saved_song))

    mixer.music.play()
    selected.set(0)


    rad2 = Radiobutton(frame_body, font=('arial 10 bold'), value=2, text='Deactivate', bg=bg_color,
                       command=deactivate_alarm, variable=selected)
    rad2.place(x=188, y=95)


    rad3 = Radiobutton(frame_body, font=('arial 10 bold'), value=3, text='Snooze', bg=bg_color,
                        command=deactivate_alarm, variable=selected)
    rad3.place(x=262, y=95)

    if rad3:
        schedule.every(5).minutes.do(simplified_sound_alarm, saved_song)
        sleep(1)
        while True:
            schedule.run_pending()
            sleep(1)


def alarm():
    while True:
        control = 1
        print(control)

# Below we obtain the relevant values from the user, as they have inputted them into our GUI framework.
        alarm_hour = c_hour.get()
        alarm_minute = c_min.get()
        alarm_sec = c_sec.get()
        alarm_period = c_period.get()
        # Below we convert AM/PM to an upper case string as required for format.
        alarm_period = str(alarm_period).upper()

        now = datetime.now()

        hour = now.strftime('%I')
        minute = now.strftime('%M')
        second = now.strftime('%S')
        period = now.strftime('%p')

        # The below checks, firstly, to see whether the entered time is now, in which case alarm should ring.
        if control == 1:
            if alarm_period == period:
                if alarm_hour == hour:
                    if alarm_minute == minute:
                        if alarm_sec == second:
                            sound_alarm()
        sleep(1)




mixer.init()

window.mainloop()
