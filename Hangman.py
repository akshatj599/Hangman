from tkinter import Tk, Label, Button, constants as cst, Canvas
from string import ascii_uppercase
from PIL import ImageTk, Image
from random import randint  # random integer from given range
from functools import partial  # for argument passing in button declaration's command fn

# Globals:
currword = ""
mainword = ""
category = ""
lives = 5
first = True

# Window:
window = Tk()
window.geometry("600x850")
window.title("Hangman-Save Michael")
window.configure(bg="black")
window.resizable(False, False)

# Background:
canvas = Canvas(window, width=800, height=850, bg="black")
image = ImageTk.PhotoImage(Image.open("Hangman\\test2.jpg"))
canvas.create_image(0, 0, anchor="nw", image=image)
canvas.place(x=-2, y=165)
coverupHoriz = Label(window, bg="black", width=800, height=2)
coverupHoriz.place(x=-3, y=145)
coverupVerti = Label(window, bg="black", width=1, height=850)
coverupVerti.place(x=-1, y=0)

# Head:
head = Label(window, text="HANGMAN", font=("Seaside Resort NF", 29, "bold"), fg="WHITE", bg="black")
head.place(x=145, y=2)

# Live Labels:
livelb = Label(window, text=lives, width=4, height=1, font=("Impact", 50, "italic"), fg="#0eb538", bg="black")
livelb.place(x=370, y=87)  # Count
printlb = Label(window, text="Lives", font=("PenultimateLightItal", 15), fg="white", bg="black")
printlb.place(x=426, y=175)  # Lives

# Canvas:
stickcanvas = Canvas(window, bg="WHITE", width="320", height="190", relief=cst.RAISED)
stickcanvas.place(x=60, y=82)
stickcanvas.create_line(20, 170, 300, 170, width="3")


# Functions:
def initiateMichael():
    color = "#d6d6d6"
    stickcanvas.create_oval(110, 40, 150, 80, width="1", outline=color)
    stickcanvas.create_line(130, 80, 130, 120, width="1", fill=color)
    stickcanvas.create_line(130, 120, 110, 140, width="1", fill=color)
    stickcanvas.create_line(130, 120, 150, 140, width="1", fill=color)
    stickcanvas.create_line(130, 100, 110, 80, width="1", fill=color)
    stickcanvas.create_line(130, 100, 150, 80, width="1", fill=color)
    stickcanvas.create_text(205, 65, text="#", font=("PenultimateLight", 14), fill=color)
    stickcanvas.create_text(252, 80, text="  SAVE\nMICHAEL", font=("Seaside Resort NF", 12), fill=color)


initiateMichael()


def pickword():
    global category
    global currword
    file = open("Hangman/AllWords.txt", "r")
    catlist = ["ACTORS", "CARS", "CITIES", "FOOD", "LANDMARKS", "MOVIES",
               "GAMES/SPORTS", "TV SHOWS/SERIALS"]
    i = randint(1, 160);
    c = 1
    for each in file:
        line = each.split("  ")
        if (c == i):
            temp = line[0].upper()
            currword = temp.rstrip()
            break
        c += 1
    c = 0
    for k in range(0, 141, 20):
        if i in range(k + 1, k + 21):
            category = catlist[c].lower()
            break
        c += 1
    file.close


#       print(category) #-----------------------------------------------
#       print(currword) #-----------------------------------------------

def panelty(n):
    global oval
    livelb.configure(text=lives)

    if (n == 4):
        stickcanvas.create_line(30, 25, 30, 170, width="2")
        stickcanvas.create_line(30, 25, 150, 25, width="2")
        stickcanvas.create_line(130, 25, 130, 40, width="2")
        livelb.configure(fg="#0eb538")

    if (n == 3):
        stickcanvas.create_oval(110, 40, 150, 80, width="2")
        stickcanvas.create_oval(124, 50, 126, 52, width="2", fill="black")  # eyeL
        stickcanvas.create_oval(136, 50, 138, 52, width="2", fill="black")  # eyeR
        oval = stickcanvas.create_oval(128, 63, 133, 68, width="2")
        stickcanvas.create_line(130, 80, 130, 120, width="2")
        livelb.configure(fg="#ded30d")

    if (n == 2):
        stickcanvas.create_line(130, 100, 110, 80, width="2")
        stickcanvas.create_line(130, 100, 150, 80, width="2")

    if (n == 1):
        livelb.configure(fg="#cc402b")
        stickcanvas.delete(oval)
        stickcanvas.create_line(130, 120, 110, 140, width="2")
        stickcanvas.create_line(130, 120, 150, 140, width="2")
        stickcanvas.create_rectangle(124, 65, 138, 70, width="2")


def end():
    global mainlb
    global head
    stickcanvas.delete("all")
    livelb.configure(text="-", fg="white")
    head.configure(fg="#e83d31")
    stickcanvas.create_text(70, 35, text="You Lost\nAnswer:",
                            font=("PenultimateLightItal", 16))
    l1 = currword.split(" ")
    inc = 0
    for i in range(0, len(l1)):
        stickcanvas.create_text(120, 90 + inc, text=f"{l1[i]}",
                                font=("PenultimateLightItal", 23, "bold"))
        inc += 40

    mainlb.configure(text="reset : play again")
    for i in range(0, len(buttons)):
        buttons[i]["state"] = cst.DISABLED
    for i in range(0, len(usedbuttons)):
        btdetails = usedbuttons[i]
        btdetails[0].configure(text=btdetails[1], width="2", relief=cst.RAISED,
                               height="2", font=("Seaside Resort NF", 14, "bold"),
                               bg="#141414", fg="white")


def checker(c1):
    global first
    # disable and empty used button:
    i = ascii_uppercase.index(c1)
    bt1 = buttons[i]
    usedbuttons.append([bt1, bt1.cget("text")])
    bt1.configure(text="", relief=cst.FLAT, bg="#363535", state=cst.DISABLED,
                  font=("Seaside Resort NF", 14))
    # main checking:
    if (first):
        stickcanvas.create_text(205, 65, text="#", font=("PenultimateLight", 14), fill="black")
        stickcanvas.create_text(252, 80, text="  SAVE\nMICHAEL", font=("Seaside Resort NF", 12), fill="black")
        first = False
    if (currword.count(c1) != 0):
        indices = [i for i in range(0, len(currword)) if currword[i] == c1]
        updateMainLabel(indices, c1)
    else:
        global lives
        lives -= 1
        if (lives != 0):
            panelty(lives)
        else:
            # lost
            end()


def updateMainLabel(indices, letter):
    global mainword
    global mainlb
    global usedbuttons
    temp = ""
    c = 0
    flag = True
    for i in range(0, len(mainword)):
        if (flag):
            j = indices[c]
        if (flag and i == j):
            temp += f"{letter}"
            c += 1
            if (c == len(indices)):
                flag = False
        else:
            temp += mainword[i]
    mainword = temp
    mainlb.configure(text=mainword)

    # winner
    if (mainword.count('-') == 0):
        for i in range(0, len(buttons)):
            buttons[i]["state"] = cst.DISABLED
        livelb.configure(text="-", fg="white")
        head.configure(fg="#68b2f2")
        mainlb.configure(fg="#0a7336")
        stickcanvas.delete("all")
        stickcanvas.create_text(120, 50, text="Michael Was Saved\nWell Done!", font=("PenultimateLightItal", 16))
        for i in range(0, len(usedbuttons)):
            btdetails = usedbuttons[i]
            btdetails[0].configure(text=btdetails[1], width="2", relief=cst.RAISED,
                                   height="2", font=("Seaside Resort NF", 14, "bold"),
                                   bg="#141414", fg="white")


def reset():
    global mainword
    global mainlb, livelb
    global usedbuttons
    global lives
    global currword
    global first
    global head
    global catlab
    stickcanvas.delete("all")
    stickcanvas.create_line(20, 170, 300, 170, width="3")
    initiateMichael()
    pickword()
    lives = 5
    first = True
    livelb.configure(text=lives, fg="#0eb538", bg="black")
    head.configure(fg="white")
    for i in range(0, len(buttons)):
        buttons[i]["state"] = cst.NORMAL

    mainword = ""
    for i in range(0, len(currword)):
        if (currword[i] == " "):
            mainword += " "
        else:
            mainword += "-"
    mainlb.configure(text=mainword, font=("PenultimateLightItal", 26), fg="BLACK")
    catlab.configure(text="category: " + category)
    for i in range(0, len(usedbuttons)):
        btdetails = usedbuttons[i]
        btdetails[0].configure(text=btdetails[1], width="2", relief=cst.RAISED,
                               height="2", font=("Seaside Resort NF", 14, "bold"),
                               bg="#141414", fg="white")


# Function dependent:

# Main Label & Category Label:
pickword()
for i in range(0, len(currword)):
    if (currword[i] == " "):
        mainword += " "
    else:
        mainword += "-"

mainlb = Label(window, text=mainword, width="20", height="2", relief=cst.FLAT,
               font=("PenultimateLightItal", 26), justify=cst.CENTER, bg="#ffeab3")
mainlb.place(x=60, y=315)
catlab = Label(window, text="category: " + category, bg="BLACK", fg="WHITE", font=("PenultimateLightItal", 15))
catlab.place(x=60, y=277)

# Letters:
buttons = []  # button store
usedbuttons = []
row = 0
count = 1
limit = 9
update = False
for c in ascii_uppercase:
    mybutton = Button(window, text=f"{c}", width="2", relief=cst.RAISED,
                      height="2", font=("Seaside Resort NF", 14, "bold"),
                      bg="#141414", fg="white", command=partial(checker, f"{c}"))
    buttons.append(mybutton)
    mybutton.place(x=60 * count, y=435 + row)
    count += 1
    if (count == limit):
        count = 1
        row += 100
        update = True
    if (row == 200 and update):
        count = 2
        limit -= 1
        update = False
    if (row == 300 and update):
        count = 3
        limit -= 1
        update = False

# Reset Button:
resetbt = Button(window, text="RESET", font=("PenultimateLightItal", 13, "bold"),
                 width="9", height="1", bg="#ffeab3", command=reset)
resetbt.place(x=400, y=230)

# Credentials:
cred = Label(window, text="Developed By Akshat Joshi",  relief=cst.FLAT,
               font=("PenultimateLightItal", 9), justify=cst.CENTER, bg="black", fg="#666666")
cred.place(x=410, y=827)

# Main:
window.mainloop()