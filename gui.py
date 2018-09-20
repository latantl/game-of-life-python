from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import *
from lifelogic import *
import os

WIDTH: int = 641
HEIGHT: int = 641
BLACK: str = '#000000'
BLUE: str = '#003366'
YELLOW: str = '#FFFF00'
CELL_SIZE: int = 8
DELAY_REF: int = 1000
DEFAULT_SPEED = 10
MIN_SPEED = 1
MAX_SPEED = 100
GAME = Life(WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE)


class SettingReminder:

    def __init__(self, value: int, speed_setter):
        self.value = value
        self.speed_setter = speed_setter

    def set(self, event=None):
        self.speed_setter(self.value)


class LifeApp:

    def __init__(self):
        self.speed: int = DEFAULT_SPEED
        # create gui elements
        self.tk = Tk()
        self.frame = Frame(self.tk)
        self.canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT, bg=BLACK)
        self.start_pause_btn = Button(self.frame, text='Start', command=self.start_pause)
        self.step_btn = Button(self.frame, text='Step', command=self.step)
        self.save_btn = Button(self.frame, text='Save', command=self.save)
        self.load_btn = Button(self.frame, text='Load', command=self.load)
        self.clear_btn = Button(self.frame, text='Clear', command=self.clear)
        self.speed_title_lbl = Label(self.frame, text='[↑↓] Speed:')
        self.speed_value_lbl = Label(self.frame, text=str(self.speed), width=3)
        # setting up gui
        self.setup_gui()
        self.bind_gui_events()
        self.bind_cell_rectangles()
        # game is paused at the beginning
        self.pause()

    def setup_gui(self) -> None:
        self.tk.title('Game of Life')
        self.frame.grid()
        self.canvas.grid(columnspan=7)
        self.start_pause_btn.grid(row=1, column=0, sticky=N + S + E + W)
        self.step_btn.grid(row=1, column=1, sticky=N + S + E + W)
        self.save_btn.grid(row=1, column=2, sticky=N + S + E + W)
        self.load_btn.grid(row=1, column=3, sticky=N + S + E + W)
        self.clear_btn.grid(row=1, column=4, sticky=N + S + E + W)
        self.speed_title_lbl.grid(row=1, column=5, sticky=E)
        self.speed_value_lbl.grid(row=1, column=6, sticky=W)

    def bind_cell_rectangles(self) -> None:
        for row in GAME.cells:
            for c in row:
                x = 1 + c.j * CELL_SIZE
                y = 1 + c.i * CELL_SIZE
                c.rectangle = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, tags='cell')
                c.born_event.sub(self.cell_born)
                c.died_event.sub(self.cell_died)
        self.update_cell_rectangles()

    def update_cell_rectangles(self) -> None:
        for row in GAME.cells:
            for c in row:
                if c.is_alive:
                    self.cell_born(c)
                else:
                    self.cell_died(c)

    def bind_gui_events(self) -> None:
        self.canvas.bind('<Button-1>', self.switch_cell)
        self.tk.bind('<Return>', self.start_pause)
        self.tk.bind('<space>', self.step)
        self.tk.bind('<s>', self.save)
        self.tk.bind('<l>', self.load)
        self.tk.bind('<c>', self.clear)
        self.tk.bind('<Up>', self.increase_speed)
        self.tk.bind('<Down>', self.decrease_speed)
        for i in range(1, 10):
            self.tk.bind(i, SettingReminder(i, self.set_speed).set)

    def set_speed(self, value: int) -> None:
        if MIN_SPEED <= value <= MAX_SPEED:
            self.speed = value
            self.speed_value_lbl.configure(text=str(self.speed))

    def increase_speed(self, event=None) -> None:
        self.set_speed(self.speed + 1)

    def decrease_speed(self, event=None) -> None:
        self.set_speed(self.speed - 1)

    def cell_born(self, cell: Cell) -> None:
        self.canvas.itemconfigure(cell.rectangle, fill=YELLOW)

    def cell_died(self, cell: Cell) -> None:
        self.canvas.itemconfigure(cell.rectangle, fill=BLUE)

    def set_grid_color(self, color) -> None:
        for row in GAME.cells:
            for c in row:
                self.canvas.itemconfigure(c.rectangle, outline=color)

    def start_pause(self, event=None) -> None:
        if GAME.is_running:
            self.pause()
        else:
            self.start()

    def start(self) -> None:
        GAME.is_running = True
        self.set_grid_color(BLUE)
        self.start_pause_btn.configure(text='Pause')
        self.running_func()

    def pause(self):
        GAME.is_running = False
        self.set_grid_color(BLACK)
        self.start_pause_btn.configure(text='Start')

    def running_func(self) -> None:
        if GAME.is_running:
            if not GAME.update():
                self.pause()
                return
            self.frame.after(DELAY_REF // self.speed, self.running_func)

    def step(self, event=None) -> None:
        if GAME.is_running:
            self.pause()
        GAME.update()

    def save(self, event=None) -> None:
        self.pause()
        filepath = filedialog.asksaveasfilename(initialdir=os.path.join(os.getcwd(), 'saves'), title="Save file as...",
                                                filetypes=(("Game of Life states", "*.life"), ("all files", "*.*")))
        if len(filepath) > 0:
            GAME.save(filepath)

    def load(self, event=None) -> None:
        self.pause()
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), 'saves'), title="Load file",
                                               filetypes=(("Game of Life states", "*.life"), ("all files", "*.*")))
        if len(file_path) > 0:
            if GAME.load(file_path):
                self.update_cell_rectangles()

    def clear(self, event=None) -> None:
        self.pause()
        if messagebox.askokcancel("Clear", "Would you like to kill all cells?"):
            GAME.clear()

    def switch_cell(self, event) -> None:
        self.pause()
        GAME.cells[(event.y - 1) // CELL_SIZE][(event.x - 1) // CELL_SIZE].switch()


LifeApp().tk.mainloop()
