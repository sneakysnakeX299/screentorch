# screentorch
![](assets/demo.png)
## An Instant Replay/ReLive-like program for Linux

# Featuring:
- A GUI written in TKinter
- NVENC encoding
- Microphone use(although somewhat limited and uses a dodgy solution to work)
- Customizable shortcut

# Dependencies:
## PIP:
- Pillow
- pynput
## Programs:
- ffmpeg
- Xorg(because apparently ffmpeg doesn't work on Wayland)
- PulseAudio

# Installation:
- Run "install" with your favourite shell.
- If something goes wrong, run it with your shell's force flag.

# Removal:
- Run "uninstall" with your favourite shell.
- If something goes wrong, run it with your shell's force flag(only tested with bash).
## IMPORTANT!
- If you're running a version of the program released BEFORE adding "uninstall-old" to the repository, use "uninstall-old" instead, as some files are now part of the "assets" directory and said files were previously in "/usr/bin".

# Updating:
- Redownload everything and run "install" with your shell's force flag(only tested with bash).

# TODO:
- Fix dodgy solutions and make code less spaghetti
- Make program as comfortable to use as possible
- Fix the final bit of the code so space could be saved

# Bug reports:
Please, report bugs, so I can fix them. Feel free to pull and rework it, I'd like to learn from better coders than me. Thank you.
