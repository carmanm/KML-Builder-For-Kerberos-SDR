import tkinter as tk
from PIL import Image, ImageTk

#Window build
win = tk.Tk()

win.geometry("500x500")
win.title("Geo-Hound: KML Builder")

win.tk.call('wm', 'iconphoto', win._w, tk.PhotoImage(file='ball_icon.png'))


#Frame build
frame1 = tk.Frame(master=win, height=250, bg="black")
frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

frame2 = tk.Frame(master=win, height=250, bg="white")
frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

#WordArt build
Title_image = tk.PhotoImage(file = 'GeoHound_Title.png') 
Title_Label = tk.Label(image = Title_image)
Title_Label.place(x=75, y=5)


#Label build
Freq_Label = tk.Label(master=frame1, text="Frequency: ", width = 10)
Freq_Label.place(x=5, y=60)

Algorithm_Label = tk.Label(master=frame1, text="Algorithm: ", width = 10)
Algorithm_Label.place(x=250, y=60)

Array_Label = tk.Label(master=frame1, text="Array: ", width = 10)
Array_Label.place(x=5, y=85)

Gain_Label = tk.Label(master=frame1, text="Gain: ", width = 10)
Gain_Label.place(x=250, y=95)

#Options build
    #Freq select
Freq_Text = tk.Text(win, height=1, width=15)
Freq_Text.place(x=85, y=60)

Gain_Text = tk.Text(win, height=1, width=15)
Gain_Text.place(x=330, y=95)

    #Array Select
Array_OPTIONS = [
"ULA",
"UCA"
] 


variable = tk.StringVar(win)
variable.set(Array_OPTIONS[0])

Array_DropDown = tk.OptionMenu(win, variable, *Array_OPTIONS)

Array_DropDown.place(x=85, y=85)

    #Algorithm select
Algorithm_OPTIONS = [
"Bartlett",
"Capon",
"MEM",
"MUSIC"
] 


variable = tk.StringVar(win)
variable.set(Algorithm_OPTIONS[0])

Algorithm_DropDown = tk.OptionMenu(win, variable, *Algorithm_OPTIONS)

Algorithm_DropDown.place(x=330, y=60)




#Button build
Start_Button = tk.Button(
    text="Start",
    width=10,
    height=2,
    bg="grey",
    fg="black",
)

Start_Button.place(x=225, y=200)

Stop_Button = tk.Button(
    text="Stop",
    width=10,
    height=2,
    bg="grey",
    fg="black",
)

Stop_Button.place(x=325, y=200)

Pause_Button = tk.Button(
    text="Pause",
    width=10,
    height=2,
    bg="grey",
    fg="black",
)

Pause_Button.place(x=125, y=200)

win.mainloop()
