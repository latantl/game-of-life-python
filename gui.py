from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import *
from src.lifelogic import Life
import os

WIDTH = 641
HEIGHT = 641
BLACK = '#000000'
BLUE = '#003366'
YELLOW = '#FFFF00'
CELLSIZE = 8
DELAY_REF = 1000
DEFAULT_SPEED = 10
MIN_SPEED = 1
MAX_SPEED = 100
GAME = Life(WIDTH // CELLSIZE, HEIGHT // CELLSIZE)

class SettingReminder:
    def __init__(self, value, speedsetter):
        self.value = value
        self.speedsetter = speedsetter
    def set(self, event = None):
        self.speedsetter(self.value)

class LifeApp:
    def __init__(self):
        self.speed = DEFAULT_SPEED
        self.initguielements()
        self.bindkeys()
        self.bindcellrects()
        self.pause()

    def initguielements(self):
        self.tk = Tk()
        self.tk.title('Game of Life')
        self.frame = Frame(self.tk)
        self.frame.grid()
        frame1 = Frame(self.frame)
        frame1.grid()
        self.canvas = Canvas(frame1, width=WIDTH, height=HEIGHT, bg=BLACK)
        self.canvas.grid(columnspan=6)
        self.canvas.focus_set()
        self.canvas.bind('<Button-1>', self.switchcell)
        self.spbutton = Button(frame1, text='Start', command=self.startpause)
        self.spbutton.grid(row=1, column=0, sticky=N + S + E + W)
        self.savebutton = Button(frame1, text='Save', command=self.save)
        self.savebutton.grid(row=1, column=1, sticky=N + S + E + W)
        self.loadbutton = Button(frame1, text='Load', command=self.load)
        self.loadbutton.grid(row=1, column=2, sticky=N + S + E + W)
        self.clearbutton = Button(frame1, text='Clear', command=self.clear)
        self.clearbutton.grid(row=1, column=3, sticky=N + S + E + W)
        self.speedtitlelabel = Label(frame1, text='[↑↓] Speed:')
        self.speedtitlelabel.grid(row=1, column=4, sticky=E)
        self.speedvaluelabel = Label(frame1, text=str(self.speed), width=3)
        self.speedvaluelabel.grid(row=1, column=5, sticky=W)

    def bindcellrects(self):
        for row in GAME.cells:
            for c in row:
                x = 1 + c.j * CELLSIZE
                y = 1 + c.i * CELLSIZE
                c.rect = self.canvas.create_rectangle(x, y, x + CELLSIZE, y + CELLSIZE, tags='cell')
                c.bornevent.sub(self.cellborn)
                c.diedevent.sub(self.celldied)
        self.updatecellrects()

    def updatecellrects(self):
        for row in GAME.cells:
            for c in row:
                if c.isalive:
                    self.cellborn(c)
                else:
                    self.celldied(c)

    def bindkeys(self):
        self.tk.bind('<Return>', self.startpause)
        self.tk.bind('<s>', self.save)
        self.tk.bind('<l>', self.load)
        self.tk.bind('<c>', self.clear)
        self.tk.bind('<Up>', self.increasespeed)
        self.tk.bind('<Down>', self.decreasespeed)
        for i in range(1,10):
            self.tk.bind(i, SettingReminder(i, self.setspeed).set)

    def setspeed(self, value):
        if MIN_SPEED <= value <= MAX_SPEED:
            self.speed = value
            self.speedvaluelabel.configure(text=str(self.speed))

    def increasespeed(self, event = None):
        self.setspeed(self.speed + 1)
    def decreasespeed(self, event = None):
        self.setspeed(self.speed - 1)

    def cellborn(self, cell):
        self.canvas.itemconfigure(cell.rect, fill=YELLOW)
    def celldied(self, cell):
        self.canvas.itemconfigure(cell.rect, fill=BLUE)

    def startpause(self, event = None):
        if GAME.isrunning:
            self.pause()
        else:
            self.start()

    def start(self):
        GAME.isrunning = True
        for row in GAME.cells:
            for c in row:
                self.canvas.itemconfigure(c.rect, outline = BLUE)
        self.spbutton.configure(text='Pause')
        self.runningfunc()

    def pause(self):
        GAME.isrunning = False
        for row in GAME.cells:
            for c in row:
                self.canvas.itemconfigure(c.rect, outline = BLACK)
        self.spbutton.configure(text='Start')

    def runningfunc(self):
        if GAME.isrunning:
            if not GAME.update():
                self.pause()
                return
            self.frame.after(DELAY_REF // self.speed, self.runningfunc)

    def save(self, event = None):
        self.pause()
        filepath = filedialog.asksaveasfilename(initialdir = os.path.join(os.getcwd(), 'saves'),
            title = "Save file as...", filetypes = (("Game of Life states","*.life"),("all files","*.*")))
        if len(filepath) > 0:
            GAME.save(filepath)

    def load(self, event = None):
        self.pause()
        filepath = filedialog.askopenfilename(initialdir = os.path.join(os.getcwd(), 'saves'),
            title = "Load file", filetypes = (("Game of Life states","*.life"),("all files","*.*")))
        if len(filepath) > 0:
            if GAME.load(filepath):
                self.updatecellrects()

    def clear(self, event = None):
        self.pause()
        if messagebox.askokcancel("Clear", "Would you like to kill all cells?"):
            GAME.clear()

    def switchcell(self, event):
        self.pause()
        GAME.cells[(event.y - 1)// CELLSIZE][(event.x - 1) // CELLSIZE].switch()

LifeApp().tk.mainloop()