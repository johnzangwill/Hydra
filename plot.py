from tkinter import *
from tkinter.font import *

class Plot:
    '''
    Thin wrapper around tkinter to make starting plotting easy
    o Converts y coordinate so that bottom left is (0, 0)
    o Provides hooks for mouse click and motion, and for window resize
    o Provides methods for circles and lines and for changing the mouse cursor
    '''
    def __init__(self, motion=None, click=None, resize=None, button=None, width=1000, height=800):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title('Hydra')

        top_frame = Frame(self.root)
        top_frame.pack(fill=BOTH)

        Button(top_frame, text='⏯', command=lambda: self._button('SINGLE')).grid(row=0, column=0)
        Button(top_frame, text='▶', command=lambda: self._button('PLAY')).grid(row=0, column=1)
        Button(top_frame, text='⏩', command=lambda: self._button('FAST')).grid(row=0, column=2)
        Button(top_frame, text='⏸', command=lambda: self._button('PAUSE')).grid(row=0, column=3)
        Button(top_frame, text='⏹', command=lambda: self._button('STOP')).grid(row=0, column=4)
    
        self.canvas = Canvas(self.root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.canvas.bind("<Motion>", self._motion)
        self.canvas.bind("<Button-1>", self._click)
        self.canvas.bind("<Configure>", self._resize)
        self.motion = motion
        self.click = click
        self.resize = resize
        self.button = button

    def _button(self, option):
        if self.button:
            self.button(option)

    def _motion(self, event):
        if self.motion:
            self.motion(event.x, self.height - event.y)

    def _click(self, event):
        if self.click:
            self.click(event.x, self.height - event.y)

    def _resize(self, event):
        self.width = event.width
        self.height = event.height
        self.canvas.config(width=event.width, height=event.height)
        if self.resize:
            self.resize()

    def update(self):
        self.root.update()

    def clear(self):
        self.canvas.delete('all')

    def circle(self, x, y, r, fill='green', outline='brown', width=2):
        self.canvas.create_oval(
            x - r,
            self.height - y + r,
            x + r,
            self.height - y - r,
            fill=fill,
            outline=outline,
            width=width
        )
 
    def line(self, x0, y0, x1, y1, fill='brown', width=2):
        self.canvas.create_line(
            x0,
            self.height - y0,
            x1,
            self.height - y1,
            fill=fill,
            width=width,
        )

    def text(self, x, y, text, size=15):
        self.canvas.create_text(x, self.height - y, text=text, anchor=SW, font=Font(family='courier', size=size), fill='blue')

    def set_cursor(self, name):
        self.canvas.config(cursor=name)
    
    def loop(self):
        self.root.mainloop()
