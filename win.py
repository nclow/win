#!/usr/bin/env python3
import subprocess
import os
import sys

wfile = os.environ["HOME"]+"/.windowlist"
arg = sys.argv[1]

def get(command):
    return subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")

def check_window(w_id):
    w_type = get("xprop -id "+w_id)
    if " _NET_WM_WINDOW_TYPE_NORMAL" in w_type:
        return True
    else:
        return False

def read_windows():
    w_list =  [l.split()[:6] for l in get("wmctrl -lG").splitlines()]
    relevant = [(" ").join(w) for w in w_list if check_window(w[0]) == True]
    with open(wfile, "wt") as out:
        for item in relevant:
            out.write(item+"\n")

def restore_windows():
    try:
        wlist = [l.split() for l in open(wfile).read().splitlines()]
    except FileNotFoundError:
        pass
    else:
        for w in wlist:
            try:
                cmd = "wmctrl -ir "+w[0]+" -e 0,"+(",").join(w[2:])
                subprocess.Popen(["/bin/bash", "-c", cmd])
            except:
                pass

def default():
    height=1920
    width=1080
    cmds = [
        # g,x,y,w,h
        "wmctrl -e 0,3840,0,-1,-1 -r Firefox",
        #"wmctrl -e 0,3840,0,-1,-1 -r Chrome",
        "wmctrl -e 0,1920,0,-1,-1 -r Sublime",
        "wmctrl -e 0,0,0,-1,-1 -r Slack",
        #"wmctrl -e 0,0,540,900,540 -r 'Toggl Desktop'",
        #"wmctrl -e 0,3840,0,-1,-1 -r mysql",
        #"wmctrl -e 0,3840,0,-1,-1 -r DBeaver",
        #"wmctrl -e 0,3840,0,-1,-1 -r Postman",
    ]

    popen = subprocess.Popen(["/bin/bash", "-c", "wmctrl -l | grep -i 'nclow@perseus'"], stdout=subprocess.PIPE)
    ret = str(popen.communicate()[0], encoding='UTF-8')
    #print(ret)
    lines = ret.split("\n")[:-1]
    #print(lines)

    y_buffer = 30
    tiled_height = int(1080 / len(lines)) - y_buffer
    tile = 0

    for line in lines:
        attrs = line.split(" ")
        win_id = attrs[0]
        print(win_id)

        y = int((tiled_height + y_buffer) * tile)
        cmds.append("wmctrl -e 0,0,{0},1920,{1} -r {2} -i".format(y, tiled_height, win_id))
        tile += 1

    for cmd in cmds:
        print(cmd)
        subprocess.Popen(["/bin/bash", "-c", cmd])

if arg == "restore":
    restore_windows()
elif arg == "get":
    read_windows()
elif arg == "default":
    default()
else:
    print("Unknown command")
