import tkinter
import random


fnt1 = ("Times New Roman", 24)
fnt2 = ("Times New Roman", 50)
index = 0
timer = 0

score = 0
bg_pos = 0
px = 240
py = 540
METEO_MAX = 30
mx = [0] * METEO_MAX
my = [0] * METEO_MAX


key = ""
koff = False
def key_down(e):
    global key, koff
    key = e.keysym #현재 누른 키 넣음
    koff = False #키 누르면 거짓

def key_up(e):
    global koff
    koff = True #키 떼면 참


def main():
    global index, timer, score, bg_pos, px, key, koff
    timer = timer + 1

    bg_pos = (bg_pos + 1) % 640
    canvas.delete("SCREEN")

    canvas.create_image(240, bg_pos - 320, image = img_bg, tag = "SCREEN")
    canvas.create_image(240, bg_pos + 320, image = img_bg, tag = "SCREEN")
    
    if index == 0:
        canvas.create_text(240, 240, text="METEOR", fill="gold", font=fnt2, tag="SCREEN")
        canvas.create_text(240, 480, text="Press [SPACE] key", fill="lime", font=fnt1, tag="SCREEN")
        if key == "space":
            score = 0
            px = 240
            init_enemy()
            index = 1

    if index == 1:
        score = score + 1
        move_player()
        move_enemy()

    if index == 2:
        move_enemy()
        canvas.create_text(240, timer * 4, text="GAME OVER", fill="red", font=fnt2, tag="SCREEN")
        if timer == 60:
            canvas.delete("OVER")
            index = 0
            timer = 0

    canvas.create_text(240, 30, text="SCORE "+str(score), fill="white", font=fnt1, tag="SCREEN")

    if koff == True: #키 뗀게 참이면 다시 거짓으로 만듦
        key = ""
        koff = False

    root.after(50, main)


def hit_check(x1, y1, x2, y2):
    if ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2) < 36 * 36):
        return True
    return False

def init_enemy():
    for i in range(METEO_MAX):
        mx[i] = random.randint(0, 480)
        my[i] = random.randint(-640, 0)

def move_enemy():
    global index, timer
    for i in range(METEO_MAX):
        my[i] = my[i] + 6 + i / 5
        if my[i] > 660:
            mx[i] = random.randint(0, 480)
            my[i] = random.randint(-640, 0)
        if index == 1 and hit_check(px, py, mx[i], my[i]) == True:
            index = 2
            timer = 0
        canvas.create_image(mx[i], my[i], image=img_enemy, tag="SCREEN")


def move_player(): #누른 키가 상하좌우일 경우
    global px
    global py
    
    if key == "Left" and px > 30:
        px = px - 10
    if key == "Right" and px < 450:
        px = px + 10
    if key == "Up" and py > 30:
        py = py - 10
    if key == "Down" and py < 610:
        py = py + 10
        
    canvas.create_image(px, py, image=img_player[timer%2], tag="SCREEN")
    

root = tkinter.Tk()
root.title("mini game")

root.bind("<KeyPress>", key_down) #키 누른거 입력받음
root.bind("<KeyRelease>", key_up) #키 뗀거 입력받음

canvas = tkinter.Canvas(width = 480, height = 640)
canvas.pack()

img_player = [tkinter.PhotoImage(file="starship0.png"), tkinter.PhotoImage(file="starship1.png")]
img_enemy = tkinter.PhotoImage(file="meteo.png")
img_bg = tkinter.PhotoImage(file="cosmo.png")

main()

root.mainloop()