from tkinter import *
import os
from PIL import ImageTk, Image
from enum import Enum
import re
from pynput import keyboard
import random
import threading
from time import sleep
from datetime import datetime
from tkinter import messagebox

os.environ.setdefault("ESCDELAY", "0")

homedir = os.path.expanduser('~')
if not os.path.exists(homedir + "/.cache"):
    os.mkdir(homedir + "/.cache")
if not os.path.exists(homedir + "/.cache/screentorch"):
    os.mkdir(homedir + "/.cache/screentorch")
if not os.path.exists(homedir + "/.config/screentorch/config"):
    f = open(homedir + "/.config/screentorch/config", "w+")
    f.write("\n\n")
    f.close()


class QualityButtons(Enum):
    LOW = 0
    MED = 1
    HIGH = 2


class MicButtons(Enum):
    OFF = 0
    ON = 1


class ToggleNVENC(Enum):
    OFF = 0
    ON = 1


class ToggleFeature(Enum):
    OFF = 0
    ON = 1


root = Tk()
root.title("screentorch")
root.resizable(False, False)
root.geometry("520x670")
root.configure(background="#1c1c1c")
root.iconphoto(False, PhotoImage(file=homedir + "/.config/screentorch/assets/logo.png"))

offstate = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/offstate.png"))
onstate = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/onstate.png"))
low = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/low.png"))
medium = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/medium.png"))
high = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/high.png"))
quitButtonImg = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/quit.png"))
saveButtonImg = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/save.png"))
qns = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/quitstart.png"))
clearcache = ImageTk.PhotoImage(Image.open(homedir + "/.config/screentorch/assets/clearcache.png"))

enabledButton = Label(root, image=onstate)
disabledButton = Label(root, image=offstate)
enabledButton2 = Label(root, image=onstate)
disabledButton2 = Label(root, image=offstate)
enabledButton3 = Label(root, image=onstate)
disabledButton3 = Label(root, image=offstate)

disabledButton['bg'] = disabledButton.master['bg']
disabledButton2['bg'] = disabledButton2.master['bg']
disabledButton3['bg'] = disabledButton3.master['bg']

enabledButton['bg'] = disabledButton.master['bg']
enabledButton2['bg'] = disabledButton2.master['bg']
enabledButton3['bg'] = disabledButton3.master['bg']

lowbtn = Label(root, image=low)
mediumbtn = Label(root, image=medium)
highbtn = Label(root, image=high)

lowbtn['bg'] = lowbtn.master['bg']
mediumbtn['bg'] = mediumbtn.master['bg']
highbtn['bg'] = highbtn.master['bg']

enabledLabel = Label(root, text="Enabled?", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
enabledLabel.grid(row=0, column=0, padx=16, pady=15, sticky=W)

enabled = ""
nvenc = ""
quality = ""
microphone = ""
bitrate = ""
output = ""
temp = ""
fps = ""
cliplength = ""
shortcut = ""
screen = ""
pshortcut = ""
kshortcut = ""
fqcheck = 0


def statusIf():
    global enabled
    with open(homedir + "/.xprofile") as xprofile_check:
        xpline = xprofile_check.readlines()
        if len(xpline) == 0:
            with open(homedir + "/.xprofile", "r+") as xprofile_fix:
                xprofile_fix.write("\n\n")
            xprofile_fix.close()
        for line in xpline:
            if "screentorch &".strip() not in line:
                enabledButton.grid_remove()
                enabled = 0
                disabledButton.grid(row=0, column=1, sticky=E)
            else:
                disabledButton.grid_remove()
                enabledButton.grid(row=0, column=1, sticky=E)
                enabled = 1
                break
    xprofile_check.close()


def statusElse():
    global enabled
    with open(homedir + "/.xprofile") as xprofile_check:
        xpline = xprofile_check.readlines()
        for line in xpline:
            if "screentorch &".strip() in line:
                disabledButton.grid_remove()
                enabled = 1
                enabledButton.grid(row=0, column=1, sticky=E)
                break
            else:
                enabledButton.grid_remove()
                disabledButton.grid(row=0, column=1, sticky=E)
                enabled = 0
    xprofile_check.close()


def nvencIf():
    global nvenc
    enabledButton2.grid(row=5, column=1, sticky=E)
    nvenc = "h264_nvenc"


def nvencElse():
    global nvenc
    disabledButton2.grid(row=5, column=1, sticky=E)
    nvenc = "libx264"


def micIf():
    global microphone
    microphone = 1
    enabledButton3.grid(row=6, column=1, sticky=E)


def micElse():
    global microphone
    microphone = 0
    disabledButton3.grid(row=6, column=1, sticky=E)


for checkpass in range(3):
    tocheck = "enabled"
    togrid = disabledButton
    toset = enabled
    rownum = 0
    if checkpass == 1:
        tocheck = "nvenc"
        togrid = disabledButton2
        toset = nvenc
        rownum = 5
    if checkpass == 2:
        tocheck = "mic"
        toset = microphone
        togrid = disabledButton3
        rownum = 6
    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^' + tocheck + '\W+=\W+[0-1]$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
    else:
        pass

        if re.match('^' + tocheck + '\W+=\W+' + str(re.match('[0-1]$', conline[line].strip())) + '$', conline[line].strip()):
            pass

        conline[line] = str(conline[line]) + "\n"
    try:
        if re.match('^' + tocheck + '\W+=\W+1', conline[line].strip()):
            if checkpass == 0:
                statusIf()
            if checkpass == 1:
                nvencIf()
            if checkpass == 2:
                micIf()
        else:
            if checkpass == 0:
                statusElse()
            if checkpass == 1:
                nvencElse()
            if checkpass == 2:
                micElse()
    except IndexError:
        togrid.grid(row=rownum, column=1, sticky=E)
        toset = 0
        if checkpass == 0:
            enabled = toset
        if checkpass == 1:
            nvenc = "libx264"
        if checkpass == 2:
            microphone = toset
        with open(homedir + "/.config/screentorch/config", "a") as configfile:
            configfile.writelines(tocheck + " = 0\n")


setLength = Label(root, text="Length(in seconds, max value is 3600):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
setLength.grid(row=1, column=0, sticky=W, padx=16, pady=5)

setQuality = Label(root, text="Quality:", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
setQuality.grid(row=2, column=0, sticky=W, padx=16, pady=15)

lowbtn.grid(row=2, column=0, sticky=W, columnspan=3, padx=193)
mediumbtn.grid(row=2, column=0, sticky=E, columnspan=1, padx=50)
highbtn.grid(row=2, column=0, sticky=E, columnspan=3)


setFPS = Label(root, text="Framerate(max value is 2147483648):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
setFPS.grid(row=3, column=0, sticky=W, padx=16, pady=5)

bitrate = Label(root, text="Bitrate(kbps):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
bitrate.grid(row=4, column=0, padx=16, pady=15, sticky=W)

toggleNVENC = Label(root, text="Use NVENC hardware encoding? (Recommended, NVIDIA only)", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
toggleNVENC.grid(row=5, column=0, padx=16, sticky=W)


with open(homedir + "/.config/screentorch/config", "r") as configfile:
    conline = configfile.readlines()

line = 0
while line < len(conline) and not re.match('^quality\W+=\W+[0-2]$', conline[line].strip()):
    line += 1

if not line < len(conline) and len(conline) > 0:
    if not conline[-1][-1] == "\n":
        conline[-1] = conline[-1] + "\n"
else:
    pass

    if re.match('^quality\W+=\W+' + str(re.match('[0-2]$', conline[line].strip())) + '$', conline[line].strip()):
        pass

    conline[line] = str(conline[line]) + "\n"
try:
    if re.match('^quality\W+=\W+0', conline[line].strip()):
        lowbtn['bg'] = 'green'
        mediumbtn['bg'] = mediumbtn.master['bg']
        highbtn['bg'] = highbtn.master['bg']
        if nvenc == "libx264":
            quality = "ultrafast"
        if nvenc == "h264_nvenc":
            quality = "llhp"
    elif re.match('^quality\W+=\W+1', conline[line].strip()):
        lowbtn['bg'] = lowbtn.master['bg']
        mediumbtn['bg'] = 'green'
        highbtn['bg'] = highbtn.master['bg']
        if nvenc == "libx264":
            quality = "faster"
        if nvenc == "h264_nvenc":
            quality = "ll"
    elif re.match('^quality\W+=\W+2', conline[line].strip()):
        lowbtn['bg'] = lowbtn.master['bg']
        mediumbtn['bg'] = mediumbtn.master['bg']
        highbtn['bg'] = 'green'
        if nvenc == "libx264":
            quality = "slow"
        if nvenc == "h264_nvenc":
            quality = "llhq"
except IndexError:
    lowbtn['bg'] = lowbtn.master['bg']
    mediumbtn['bg'] = 'green'
    highbtn['bg'] = highbtn.master['bg']
    if nvenc == "libx264":
        quality = "faster"
    if nvenc == "h264_nvenc":
        quality = "ll"
    with open(homedir + "/.config/screentorch/config", "a") as configfile:
        configfile.writelines("quality = 1\n")


toggleMic = Label(root, text="Use microphone:", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
toggleMic.grid(row=6, column=0, padx=16, pady=13, sticky=W)


def typeCheck(event):
    if event.char in '[0123456789]':
        pass
    elif event.keysym not in ('Delete', 'BackSpace'):
        return 'break'


screenLabel = Label(root, text="Screen(in numbers, starting from 0):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
screenLabel.grid(row=7, column=0, padx=16, sticky=W, pady=7)

screenTextbox = Entry(root, width=30, bg="#2c2c2c", fg="white")
setFramerate = Entry(root, width=22, bg="#2c2c2c", fg="white")
setBitrate = Entry(root, width=22, bg="#2c2c2c", fg="white")

checkpass = 0

for checkpass in range(3):
    if checkpass == 0:
        tocheck = "screen"
        toinsert = screenTextbox
        toset = screen
        defaultval = "0"
    if checkpass == 1:
        tocheck = "fps"
        toinsert = setFramerate
        toset = fps
        defaultval = "60"
    if checkpass == 2:
        tocheck = "bitrate"
        toinsert = setBitrate
        toset = bitrate
        defaultval = "15000"
    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^' + tocheck + '\W+=\W+[0-9][0-9]{0,9}|2147483648$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
    else:
        pass

        if re.match('^' + tocheck + '\W+=\W+' + str(conline[line]) + '$', conline[line].strip()):
            pass

        conline[line] = tocheck + " = " + str(conline[line]) + "\n"
    try:
        toinsert.insert(0, conline[line].strip(tocheck + " =\n"))
        toset = conline[line].strip(tocheck + " =\n")
        if checkpass == 0:
            screen = toset
        if checkpass == 1:
            fps = toset
        if checkpass == 2:
            bitrate = toset
    except IndexError:
        toinsert.insert(0, defaultval)
        toset = defaultval
        if checkpass == 0:
            screen = toset
        if checkpass == 1:
            fps = toset
        if checkpass == 2:
            bitrate = toset
        with open(homedir + "/.config/screentorch/config", "a") as configfile:
            configfile.writelines(tocheck + " = " + toset + "\n")

screenTextbox.grid(row=7, column=0, columnspan=2, sticky=E)
screenTextbox.bind("<KeyPress>", typeCheck)

keyShort = Label(root, text="Highlight shortcut(Esc when done):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
keyShort.grid(row=8, column=0, padx=16, sticky=W, pady=13)

keys = []


def on_press(key):
    try:
        selection = root.focus_get()
        if str(selection) != ".!entry4":
            keyShortSet.delete(0, END)
            keys.clear()
            return False
        if str(key).strip("'") not in keys:
            keys.append(str(key).strip("'"))
        else:
            keylocation = keys.index(key.strip("'"))
            keys.remove(keylocation)
        if key == keyboard.Key.esc:
            boxlength = keyShortSet.get()
            keyShortSet.delete(len(boxlength)-1, END)
            keys.remove(str(keyboard.Key.esc)) # Causes ValueError, but that's good, because I don't have to add code to remove the Escape key from the list. Not a bug, but a feature!
            keys.clear()
            root.focus()
        if keys.index(str(key).strip("'")) != len(keys):
            keyShortSet.insert(END, str(key).strip("'") + "+")
        else:
            keyShortSet.insert(END, str(key).strip("'"))
    except AttributeError:
        selection = root.focus_get()
        if str(selection) != ".!entry4":
            keyShortSet.delete(0, END)
            keys.clear()
            return False


def on_release(key):
    if key == key:
        keys.remove(str(key).strip("'"))
        keyShortSet.delete(0, END)
        lastkey = 0
        while lastkey < len(keys) and len(keys) > 0:
            lastkey += 1
            if lastkey > len(keys):
                lastkey = 0
            else:
                keyShortSet.insert(0, str(keys[lastkey-2]) + "+")
    if key == keyboard.Key.esc:
        keys.clear()
        return False
    selection = root.focus_get()
    if str(selection) != ".!entry4":
        keyShortSet.delete(0, END)
        keys.clear()
        return False


def keyListen(event):
    keyShortSet.delete(0, END)
    keys.clear()
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()


def disableBox(event):
    return 'break'


keyShortSet = Entry(root, width=30, bg="#2c2c2c", fg="white", textvariable=on_release)
keyShortSet.bind('<KeyPress>', disableBox)
keyShortSet.bind('<Button-1>', keyListen)

pauseShort = Label(root, text="Pause shortcut(Esc when done):", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
pauseShort.grid(row=9, column=0, padx=16, sticky=W, pady=7)


def on_pressp(key):
    try:
        selection = root.focus_get()
        if str(selection) != ".!entry5":
            pauseShortSet.delete(0, END)
            keys.clear()
            return False
        if str(key).strip("'") not in keys:
            keys.append(str(key).strip("'"))
        else:
            keylocation = keys.index(key.strip("'"))
            keys.remove(keylocation)
        if key == keyboard.Key.esc:
            boxlength = pauseShortSet.get()
            pauseShortSet.delete(len(boxlength)-1, END)
            keys.remove(str(keyboard.Key.esc))  # Causes ValueError, but that's good, because I don't have to add code to remove the Escape key from the list. Not a bug, but a feature!
            keys.clear()
            root.focus()
        if keys.index(str(key).strip("'")) != len(keys):
            pauseShortSet.insert(END, str(key).strip("'") + "+")
        else:
            pauseShortSet.insert(END, str(key).strip("'"))
    except AttributeError:
        selection = root.focus_get()
        if str(selection) != ".!entry5":
            pauseShortSet.delete(0, END)
            keys.clear()
            return False


def on_releasep(key):
    if key == key:
        keys.remove(str(key).strip("'"))
        pauseShortSet.delete(0, END)
        lastkey = 0
        while lastkey < len(keys) and len(keys) > 0:
            lastkey += 1
            if lastkey > len(keys):
                lastkey = 0
            else:
                pauseShortSet.insert(0, str(keys[lastkey-2]) + "+")
    if key == keyboard.Key.esc:
        keys.clear()
        return False
    selection = root.focus_get()
    if str(selection) != ".!entry5":
        pauseShortSet.delete(0, END)
        keys.clear()
        return False


def keyListenp(event):
    pauseShortSet.delete(0, END)
    keys.clear()
    listener = keyboard.Listener(
        on_press=on_pressp,
        on_release=on_releasep)
    listener.start()


pauseShortSet = Entry(root, width=30, bg="#2c2c2c", fg="white", textvariable=on_releasep)
pauseShortSet.bind('<KeyPress>', disableBox)
pauseShortSet.bind('<Button-1>', keyListenp)


killShort = Label(root, text="Kill shortcut:", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
killShort.grid(row=10, column=0, padx=16, sticky=W, pady=13)


def on_pressk(key):
    try:
        selection = root.focus_get()
        if str(selection) != ".!entry6":
            killShortSet.delete(0, END)
            keys.clear()
            return False
        if str(key).strip("'") not in keys:
            keys.append(str(key).strip("'"))
        else:
            keylocation = keys.index(key.strip("'"))
            keys.remove(keylocation)
        if key == keyboard.Key.esc:
            boxlength = killShortSet.get()
            killShortSet.delete(len(boxlength)-1, END)
            keys.remove(str(keyboard.Key.esc))  # Causes ValueError, but that's good, because I don't have to add code to remove the Escape key from the list. Not a bug, but a feature!
            keys.clear()
            root.focus()
        if keys.index(str(key).strip("'")) != len(keys):
            killShortSet.insert(END, str(key).strip("'") + "+")
        else:
            killShortSet.insert(END, str(key).strip("'"))
    except AttributeError:
        selection = root.focus_get()
        if str(selection) != ".!entry6":
            killShortSet.delete(0, END)
            keys.clear()
            return False


def on_releasek(key):
    if key == key:
        keys.remove(str(key).strip("'"))
        killShortSet.delete(0, END)
        lastkey = 0
        while lastkey < len(keys) and len(keys) > 0:
            lastkey += 1
            if lastkey > len(keys):
                lastkey = 0
            else:
                killShortSet.insert(0, str(keys[lastkey-2]) + "+")
    if key == keyboard.Key.esc:
        keys.clear()
        return False
    selection = root.focus_get()
    if str(selection) != ".!entry6":
        killShortSet.delete(0, END)
        keys.clear()
        return False


def keyListenk(event):
    killShortSet.delete(0, END)
    keys.clear()
    listener = keyboard.Listener(
        on_press=on_pressk,
        on_release=on_releasek)
    listener.start()


killShortSet = Entry(root, width=30, bg="#2c2c2c", fg="white", textvariable=on_releasek)
killShortSet.bind('<KeyPress>', disableBox)
killShortSet.bind('<Button-1>', keyListenk)


for checkpass in range(3):
    tocheck = "shortcut"
    toinsert = keyShortSet
    defaultval = "Key.alt+c"
    if checkpass == 1:
        tocheck = "pshortcut"
        toinsert = pauseShortSet
        toset = pshortcut
        defaultval = "Key.alt+h"
    if checkpass == 2:
        tocheck = "kshortcut"
        toinsert = killShortSet
        toset = kshortcut
        defaultval = "Key.alt+k"
    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match("^" + tocheck + "\W+=\W+\S*$", conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
    else:
        pass

        if re.match('^' + tocheck + '\W+=\W+' + str(conline[line]) + '$', conline[line].strip()):
            pass

        conline[line] = tocheck + " = " + str(conline[line]) + "\n"
    try:
        brokentext = conline[line].strip(str(re.match('^' + tocheck + '\W+=\W+\S', conline[line])))
        toinsert.insert(0, brokentext.strip("\n"))
        if checkpass == 0:
            shortcut = brokentext
        if checkpass == 1:
            pshortcut = brokentext
        if checkpass == 2:
            kshortcut = brokentext
    except IndexError:
        toinsert.insert(0, defaultval)
        if checkpass == 0:
            shortcut = defaultval
        if checkpass == 1:
            pshortcut = defaultval
        if checkpass == 2:
            kshortcut = defaultval
        with open(homedir + "/.config/screentorch/config", "a") as configfile:
            configfile.writelines(tocheck + " = " + defaultval + "\n")


keyShortSet.grid(row=8, column=0, columnspan=2, sticky=E)
pauseShortSet.grid(row=9, column=0, columnspan=2, sticky=E)
killShortSet.grid(row=10, column=0, columnspan=2, sticky=E)

fileOutput = Label(root, text="Output:", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
fileOutput.grid(row=11, column=0, padx=16, sticky=W, pady=7)

fileOutputTextbox = Entry(root, width=54, bg="#2c2c2c", fg="white")
tmpOutputTextbox = Entry(root, width=35, bg="#2c2c2c", fg="white")

for checkpass in range(2):
    tocheck = "output"
    toinsert = fileOutputTextbox
    defaultval = homedir
    if checkpass == 1:
        tocheck = "temp"
        toinsert = tmpOutputTextbox
        defaultval = homedir + "/.cache/screentorch"
    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match("^" + tocheck + "\W+=\W+\S*$", conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
    else:
        pass

        if re.match("^" + tocheck + "\W+=\W+" + str(conline[line]) + '$', conline[line].strip()):
            pass

        conline[line] = tocheck + " = " + str(conline[line]) + "\n"
    try:
        brokentext = conline[line].strip(str(re.match('^' + tocheck + '\W+=\W+', conline[line])))
        toinsert.insert(0, brokentext.strip("\n"))
        if checkpass == 0:
            output = brokentext.strip()
        if checkpass == 1:
            temp = brokentext.strip()
    except IndexError:
        toinsert.insert(0, defaultval)
        if checkpass == 0:
            output = defaultval
        if checkpass == 1:
            temp = defaultval
        with open(homedir + "/.config/screentorch/config", "a") as configfile:
            configfile.writelines("output = " + homedir + "\n")


fileOutputTextbox.grid(row=11, column=0, columnspan=2, sticky=E)


length = Entry(root, width=22, bg="#2c2c2c", fg="white")

with open(homedir + "/.config/screentorch/config", "r") as configfile:
    conline = configfile.readlines()

line = 0
while line < len(conline) and not re.match('^length\W+=\W+[0-9][0-9]{0,2}|3600$', conline[line].strip()):
    line += 1

if not line < len(conline) and len(conline) > 0:
    if not conline[-1][-1] == "\n":
        conline[-1] = conline[-1] + "\n"
else:
    pass

    if re.match('^length\W+=\W+' + str(conline[line]) + '$', conline[line].strip()):
        pass

    conline[line] = "length = " + str(conline[line]) + "\n"
try:
    length.insert(0, conline[line].strip("length =\n"))
    cliplength = conline[line].strip("length =\n")
except IndexError:
    length.insert(0, "60")
    cliplength = "60"
    with open(homedir + "/.config/screentorch/config", "a") as configfile:
        configfile.writelines("length = 60\n")

length.grid(row=1, column=0, columnspan=2, sticky=E)
length.bind('<KeyPress>', typeCheck)


setFramerate.grid(row=3, column=0, columnspan=2, sticky=E)
setFramerate.bind('<KeyPress>', typeCheck)


setBitrate.grid(row=4, column=0, columnspan=2, sticky=E)
setBitrate.bind('<KeyPress>', typeCheck)


tmpOutput = Label(root, text="Temp directory:", font=("Helvetica", 10), bg="#1c1c1c", fg="white")
tmpOutput.grid(row=12, column=0, padx=16, sticky=W, pady=13)


tmpOutputTextbox.grid(row=12, column=0, columnspan=2, sticky=E, padx=103)


def saveClick(clicksavebutton):
    lengthbox = length.get()
    fpsbox = setFramerate.get()
    bitratebox = setBitrate.get()
    outputbox = fileOutputTextbox.get()
    tempbox = tmpOutputTextbox.get()
    shortbox = keyShortSet.get()
    screenbox = screenTextbox.get()
    pBox = pauseShortSet.get()
    kBox = killShortSet.get()

    def saveLength():
        global cliplength
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match('^length\W+=\W+[0-9][0-9]{0,9}|2147483648$', conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("length = " + str(lengthbox) + "\n")
        else:
            pass

            if re.match('^length\W+=\W+' + str(lengthbox) + '$', conline[line].strip()):
                return

            conline[line] = "length = " + str(lengthbox) + "\n"
        if int(lengthbox) <= 3600 and int(fpsbox) <= 2147483648 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            cliplength = conline[line].strip("length =\n")
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveFPS():
        global fps
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match('^fps\W+=\W+[0-9][0-9]{0,9}|2147483648$', conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("fps = " + str(fpsbox) + "\n")
        else:
            pass

            if re.match('^fps\W+=\W+' + str(fpsbox) + '$', conline[line].strip()):
                return

            conline[line] = "fps = " + str(fpsbox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            fps = conline[line].strip("fps =\n")
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveBitrate():
        global bitrate
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match('^bitrate\W+=\W+[0-9][0-9]{0,9}|2147483648$', conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("bitrate = " + str(bitratebox) + "\n")
        else:
            pass

            if re.match('^bitrate\W+=\W+' + str(bitratebox) + '$', conline[line].strip()):
                return

            conline[line] = "bitrate = " + str(bitratebox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            bitrate = conline[line].strip("bitrate =\n")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveScreen():
        global screen
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match('^screen\W+=\W+[0-9][0-9]{0,9}|2147483648$', conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("screen = " + str(screenbox) + "\n")
        else:
            pass

            if re.match('^screen\W+=\W+' + str(screenbox) + '$', conline[line].strip()):
                return

            conline[line] = "screen = " + str(screenbox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            screen = conline[line].strip("screen =\n")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveLocation():
        global output
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match("^output\W+=\W+\S*$", conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("output = " + str(outputbox) + "\n")
        else:
            pass

            if re.match('^output\W+=\W+' + str(outputbox) + '$', conline[line].strip()):
                return

            conline[line] = "output = " + str(outputbox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            output = conline[line].strip("output =\n")
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveShortcut():
        global shortcut
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match("^shortcut\W+=\W+\S*$", conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("shortcut = " + str(shortbox) + "\n")
        else:
            pass

            if re.match('^shortcut\W+=\W+' + str(shortbox) + '$', conline[line].strip()):
                return

            conline[line] = "shortcut = " + str(shortbox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            shortcut = keyShortSet.get()
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def saveTemp():
        global temp
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match("^temp\W+=\W+\S*$", conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("temp = " + str(tempbox) + "\n")
        else:
            pass

            if re.match('^temp\W+=\W+' + str(tempbox) + '$', conline[line].strip()):
                return

            conline[line] = "temp = " + str(tempbox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            temp = conline[line].strip("temp =\n")
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def savepShortcut():
        global pshortcut
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match("^pshortcut\W+=\W+\S*$", conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("pshortcut = " + str(pBox) + "\n")
        else:
            pass

            if re.match('^pshortcut\W+=\W+' + str(pBox) + '$', conline[line].strip()):
                return

            conline[line] = "pshortcut = " + str(pBox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            pshortcut = pauseShortSet.get()
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    def savekShortcut():
        global kshortcut
        with open(homedir + "/.config/screentorch/config", "r") as configfile:
            conline = configfile.readlines()

        line = 0
        while line < len(conline) and not re.match("^kshortcut\W+=\W+\S*$", conline[line].strip()):
            line += 1

        if not line < len(conline) and len(conline) > 0:
            if not conline[-1][-1] == "\n":
                conline[-1] = conline[-1] + "\n"
            conline.append("kshortcut = " + str(kBox) + "\n")
        else:
            pass

            if re.match('^kshortcut\W+=\W+' + str(kBox) + '$', conline[line].strip()):
                return

            conline[line] = "kshortcut = " + str(kBox) + "\n"
        if int(fpsbox) <= 2147483648 and int(lengthbox) <= 3600 and int(bitratebox) <= 2147483648 and int(screenbox) <= 2147483648:
            with open(homedir + "/.config/screentorch/config", "w") as configfile:
                configfile.writelines(conline)
            kshortcut = killShortSet.get()
            saveLabel = Label(root, text="Saved!", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(1000, saveLabel.destroy)
        else:
            saveLabel = Label(root, text="Save failed", bg="#1c1c1c", fg="white")
            saveLabel.place(relx=0.5, rely=0.98, anchor=CENTER)
            saveLabel.after(3500, saveLabel.destroy)

    saveLength()
    saveBitrate()
    saveFPS()
    saveLocation()
    saveTemp()
    saveShortcut()
    saveScreen()
    savepShortcut()
    savekShortcut()
    tmpsl = tmpOutputTextbox.get()
    if tmpsl == "Tomo chan best girl":
        os.popen("xdg-open " + homedir + "/.config/screentorch/assets/test.jpg")
        os.popen("pacat " + homedir + "/.config/screentorch/assets/test.wav")


def clrcache(cachefiles):
    if len(os.listdir(temp)) == 0:
        pass
    else:
        filelist = [f for f in os.listdir(temp) if f.endswith(".mkv")]
        for f in filelist:
            os.remove(os.path.join(temp, f))


clearCacheBtn = Label(root, image=clearcache)
clearCacheBtn.grid(row=12, column=0, columnspan=2, sticky=E)
clearCacheBtn.bind('<Button-1>', clrcache)


def selectall(event):
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')
    return 'break'


def toggleFeature(button):
    if not os.path.exists(homedir + "/.xprofile"):
        xprofile = open(homedir + "/.xprofile", "w+")
        xprofile.write("\n\n")
        xprofile.close()
    global enabled
    if button == ToggleFeature.OFF:
        disabledButton.grid(row=0, column=1, sticky=E)
        enabled = 0
        with open(homedir + "/.xprofile", "r") as xprofile:
            lines = xprofile.readlines()
        with open(homedir + "/.xprofile", "w") as xprofile:
            for line in lines:
                if line.strip("\n") != "screentorch &":
                    xprofile.write(line)
    elif button == ToggleFeature.ON:
        enabled = 1
        disabledButton.grid_remove()
        enabledButton.grid(row=0, column=1, sticky=E)
        xprofile = open(homedir + "/.xprofile", "a")
        xprofile.write("screentorch &\n")
        xprofile.close()

    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^enabled\W+=\W+[0-1]$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
        conline.append("enabled = " + str(button.value) + "\n")
    else:
        pass

        if re.match('^enabled\W+=\W+' + str(button.value) + '$', conline[line].strip()):
            return

        conline[line] = "enabled = " + str(button.value) + "\n"

    with open(homedir + "/.config/screentorch/config", "w") as configfile:
        configfile.writelines(conline)


def toggleNVENC(button):
    global nvenc
    if button == ToggleNVENC.OFF:
        disabledButton2.grid(row=5, column=1, sticky=E)
        nvenc = "libx264"
    elif button == ToggleNVENC.ON:
        disabledButton2.grid_remove()
        nvenc = "h264_nvenc"
        enabledButton2.grid(row=5, column=1, sticky=E)
    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^nvenc\W+=\W+[0-1]$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
        conline.append("nvenc = " + str(button.value) + "\n")
    else:
        pass

        if re.match('^nvenc\W+=\W+' + str(button.value) + '$', conline[line].strip()):
            return

        conline[line] = "nvenc = " + str(button.value) + "\n"

    with open(homedir + "/.config/screentorch/config", "w") as configfile:
        configfile.writelines(conline)


def micToggle(button):
    global microphone
    if button == MicButtons.OFF:
        microphone = 0
        disabledButton3.grid(row=6, column=1, sticky=E)
    elif button == MicButtons.ON:
        microphone = 1
        disabledButton3.grid_remove()
        enabledButton3.grid(row=6, column=1, sticky=E)

    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^mic\W+=\W+[0-1]$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
        conline.append("mic = " + str(button.value) + "\n")
    else:
        pass

        if re.match('^mic\W+=\W+' + str(button.value) + '$', conline[line].strip()):
            return

        conline[line] = "mic = " + str(button.value) + "\n"

    with open(homedir + "/.config/screentorch/config", "w") as configfile:
        configfile.writelines(conline)


def qualityOptions(button):
    global quality
    lowbtn['bg'] = lowbtn.master['bg']
    mediumbtn['bg'] = lowbtn.master['bg']
    highbtn['bg'] = highbtn.master['bg']
    if button == QualityButtons.LOW:
        lowbtn['bg'] = 'green'
        if nvenc == "libx264":
            quality = "ultrafast"
        if nvenc == "h264_nvenc":
            quality = "llhp"
    elif button == QualityButtons.MED:
        mediumbtn['bg'] = 'green'
        if nvenc == "libx264":
            quality = "faster"
        if nvenc == "h264_nvenc":
            quality = "ll"
    elif button == QualityButtons.HIGH:
        highbtn['bg'] = 'green'
        if nvenc == "libx264":
            quality = "slow"
        if nvenc == "h264_nvenc":
            quality = "llhq"

    with open(homedir + "/.config/screentorch/config", "r") as configfile:
        conline = configfile.readlines()

    line = 0
    while line < len(conline) and not re.match('^quality\W+=\W+[0-2]$', conline[line].strip()):
        line += 1

    if not line < len(conline) and len(conline) > 0:
        if not conline[-1][-1] == "\n":
            conline[-1] = conline[-1] + "\n"
        conline.append("quality = " + str(button.value) + "\n")
    else:
        pass

        if re.match('^quality\W+=\W+' + str(button.value) + '$', conline[line].strip()):
            return

        conline[line] = "quality = " + str(button.value) + "\n"

    with open(homedir + "/.config/screentorch/config", "w") as configfile:
        configfile.writelines(conline)


lowbtn.bind("<Button-1>", lambda event: qualityOptions(QualityButtons.LOW))
mediumbtn.bind("<Button-1>", lambda event: qualityOptions(QualityButtons.MED))
highbtn.bind("<Button-1>", lambda event: qualityOptions(QualityButtons.HIGH))


disabledButton.bind("<Button-1>", lambda event: toggleFeature(ToggleFeature.ON))
enabledButton.bind("<Button-1>", lambda event: toggleFeature(ToggleFeature.OFF))

disabledButton2.bind("<Button-1>", lambda event: toggleNVENC(ToggleNVENC.ON))
enabledButton2.bind("<Button-1>", lambda event: toggleNVENC(ToggleNVENC.OFF))

disabledButton3.bind("<Button-1>", lambda event: micToggle(MicButtons.ON))
enabledButton3.bind("<Button-1>", lambda event: micToggle(MicButtons.OFF))


tmpOutputTextbox.bind('<Control-a>', selectall)
fileOutputTextbox.bind('<Control-a>', selectall)
tmpOutputTextbox.bind('<Control-A>', selectall)
fileOutputTextbox.bind('<Control-A>', selectall)

length.bind('<Control-a>', selectall)
length.bind('<Control-A>', selectall)


def destroyUI(destroy):
    global fqcheck
    fqcheck += 1
    root.destroy()


save = Label(root, image=saveButtonImg)
save.place(relx=0.25, rely=0.83, anchor=CENTER)
save.bind("<Button-1>", saveClick)

quitButton = Label(root, image=quitButtonImg)
quitButton.place(relx=0.75, rely=0.83, anchor=CENTER)
quitButton.bind("<Button-1>", destroyUI)

quitNoStart = Label(root, image=qns)
quitNoStart.place(relx=0.5, rely=0.92, anchor=CENTER)
quitNoStart.bind("<Button-1>", exit)

root.mainloop()

if enabled == 1 and fqcheck == 1:
    deactivated = 0
    os.popen("killall recorder")
    buttons = []
    for num, word in enumerate(shortcut.split("+")):
        if len(word) > 3 and word.strip("Key."):
            buttons.append("<" + word.strip("Key.\n") + ">")
        else:
            buttons.append(word.strip())
    wordcount = 0
    shortcut = ""
    while wordcount < len(buttons):
        if wordcount == len(buttons)-1:
            shortcut = shortcut + str(buttons[wordcount])
        else:
            shortcut = shortcut + str(buttons[wordcount]) + "+"
        wordcount += 1
    buttons2 = []
    for num, word in enumerate(pshortcut.split("+")):
        if len(word) > 3 and word.strip("Key."):
            buttons2.append("<" + word.strip("Key.\n") + ">")
        else:
            buttons2.append(word.strip())
    wordcount2 = 0
    pshortcut = ""
    while wordcount2 < len(buttons2):
        if wordcount2 == len(buttons2)-1:
            pshortcut = pshortcut + str(buttons2[wordcount2])
        else:
            pshortcut = pshortcut + str(buttons2[wordcount2]) + "+"
        wordcount2 += 1
    buttons3 = []
    for num, word in enumerate(kshortcut.split("+")):
        if len(word) > 3 and word.strip("Key."):
            buttons3.append("<" + word.strip("Key.\n") + ">")
        else:
            buttons3.append(word.strip())
    wordcount3 = 0
    kshortcut = ""
    while wordcount3 < len(buttons3):
        if wordcount3 == len(buttons3)-1:
            kshortcut = kshortcut + str(buttons3[wordcount3])
        else:
            kshortcut = kshortcut + str(buttons3[wordcount3]) + "+"
        wordcount3 += 1
    filename = str(random.randrange(10000000000)) + ".mkv"
    filename2 = str(random.randrange(10000000000)) + ".mkv"
    rescmd = os.popen("xrandr | grep \* | cut -d' ' -f4").read().strip()
    if screen == "0":
        offset = ['0']
    elif int(screen) == 1:
        offset = rescmd.split("\n")[0].split("x")
    elif int(screen) > 1:
        recscreen = 0
        screenlist = rescmd.split("\n")
        offset = 0
        while recscreen != len(screenlist):
            screenres = []
            screenres = rescmd.split("\n")[recscreen].split("x")
            recscreen += 1
            offset = int(offset) + int(screenres[0])
        offset = [str(offset)]
    res = rescmd.split("\n")

    def ffmpeg():
        if len(res) > 1 and offset[0] != str(offset):
            os.popen(homedir + "/.config/screentorch/assets/recorder -hwaccel auto -f pulse -i default -f x11grab -s " + str(res[int(screen)]) + " -framerate " + str(fps) + " -i :0.0+" + offset[0] + ",0 -pix_fmt yuv420p -c:v " + str(nvenc) + " -preset " + str(quality) + " -b:v " + str(bitrate) + "K -maxrate " + str(bitrate) + "K -y " + str(temp) + "/" + filename).read()
        else:
            os.popen(homedir + "/.config/screentorch/assets/recorder -hwaccel auto -f pulse -i default -f x11grab -s " + str(res[int(screen)]) + " -framerate " + str(fps) + " -i :0.0 -pix_fmt yuv420p -c:v " + str(nvenc) + " -preset " + str(quality) + " -b:v " + str(bitrate) + "K -maxrate " + str(bitrate) + "K -y " + str(temp) + "/" + filename).read()

    class RecordingThread(threading.Thread):
        daemon = True

        def __init__(self, *args, **kwargs):
            super(RecordingThread, self).__init__(*args, **kwargs)
            self._stop_event = threading.Event()

        def stop(self):
            self._stop_event.set()

        def stopped(self):
            return self._stop_event.is_set()


    RecordingThread(target=ffmpeg, name="recording").start()
    sleep(1)
    if microphone == 1:
        os.popen('pacmd list-source-outputs|tr "\n" " "| awk ' + "'" + 'BEGIN {RS="index:"};/application.process.binary = "recorder"/ {print $0 }' + "'" + ' |awk ' + "'" + '{print"pacmd move-source-output " $1 " " (NR+1)}' + "'" + '|bash')
    else:
        os.popen('pacmd list-source-outputs|tr "\n" " "| awk ' + "'" + 'BEGIN {RS="index:"};/application.process.binary = "recorder"/ {print $0 }' + "'" + ' |awk ' + "'" + '{print"pacmd move-source-output " $1 " " (NR-0)}' + "'" + '|bash')


    def highlight():
        global filename
        global deactivated
        if deactivated == 1:
            deactivated = 0
            os.popen("notify-send 'Recording unpaused, highlighting last " + str(cliplength) + " seconds of paused footage...'")
        os.popen("killall recorder")
        RecordingThread(target=ffmpeg, name="recording").stop()
        sleep(2)
        filelength = os.popen("ffprobe -i " + "'" + str(temp) + "/" + str(filename) + "'" + " -show_entries format=duration -v quiet -of csv='p=0'").read().strip()
        currtime = str(datetime.now())
        tod = currtime.split(":")
        fname = "screentorch_"
        currtime = 0
        while currtime != len(tod):
            if currtime == len(tod) - 1:
                fname = fname + tod[currtime]
            else:
                fname = fname + tod[currtime] + "-"
            currtime += 1
        if float(filelength) < float(cliplength):
            os.popen("mv " + "'" + str(temp) + "/" + str(filename) + "' '" + str(output) + "/" + str(fname) + ".mkv" + "'")
        else:
            duration = float(filelength) - float(cliplength)
            os.popen("ffmpeg -ss " + str(duration) + " -i " + "'" + str(temp) + "/" + str(filename) + "'" + " -t " + str(filelength) + " -c copy " + "'" + str(output) + "/" + str(fname) + ".mkv" + "'")
        sleep(2)
        os.popen("rm " + "'" + str(temp) + "/" + str(filename) + "'")
        os.popen("notify-send 'Highlight saved to " + str(output) + "/" + str(fname) + ".mkv" + "'")
        RecordingThread(target=ffmpeg, name="recording").start()

    def pause():
        global deactivated
        deactivated += 1
        if deactivated == 1:
            os.popen("killall recorder")
            RecordingThread(target=ffmpeg, name="recording").stop()
            os.popen("notify-send 'Recording paused'")
        if deactivated > 1:
            deactivated = 0
            os.popen("notify-send 'Recording unpaused'")
            RecordingThread(target=ffmpeg, name="recording").start()

    def kill():
        askme = Tk()
        askme.withdraw()
        confirmation = messagebox.askyesno(title="Kill combination pressed", message="Are you sure you want to kill screentorch?")
        if confirmation:
            RecordingThread(target=ffmpeg, name="recording").stop()
            os.popen("killall recorder")
            exit()
        else:
            askme.destroy()
            pass

    with keyboard.GlobalHotKeys({
        str(shortcut): highlight,
        str(pshortcut): pause,
        str(kshortcut): kill}) as l:
        l.join()
else:
    exit()
