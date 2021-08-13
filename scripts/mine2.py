import tkinter as tk
from tkinter import *

from PIL import Image, ImageTk


class CanvasEventsDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.topx = 0
        self.topy = 0

        self.botx = 0
        self.boty = 0

        self.rect_id = None

        self.rect_list = list()
        self.rect_main_data = list()

        self.canvas = Canvas(master, width=300, height=300, bg='beige')
        img = ImageTk.PhotoImage(Image.open('./data/download.jpg'))
        self.canvas.image = img
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor=tk.NW)
        self.canvas.pack()

        self.rect_id = self.canvas.create_rectangle(self.topx,
                                                    self.topy,
                                                    self.topx,
                                                    self.topy,
                                                    dash=(2, 2),
                                                    fill='',
                                                    outline='red')

        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)
        self.canvas.bind('<ButtonRelease-1>', self.draw_rect)
        # self.canvas.bind('<Double-3>', self.clearRectangles)
        self.canvas.bind('<Double-3>', self.onClear)

        self.canvas.update()

        b1 = Button(self.master,
                    text='Perform Registration',
                    command=self.perform_registration,
                    bg='brown',
                    fg='white',
                    font=('cambria', 9, 'bold'))

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.canvas.create_window(canvas_width // 2,
                                  canvas_height - 20,
                                  anchor=tk.CENTER,
                                  window=b1)

    def perform_registration(self):
        pass

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx,
                           self.boty)  # Update selection rect.

    def draw_rect(self, event):
        draw_data = self.canvas.create_rectangle(self.topx,
                                                 self.topy,
                                                 self.botx,
                                                 self.boty,
                                                 outline="green",
                                                 fill="")
        self.rect_list.append((self.topx, self.topy, self.botx, self.boty))
        self.rect_main_data.append(draw_data)
        print(self.rect_list)
        print(self.rect_main_data)

    def onClear(self, event):
        # event.widget.delete('all')
        if (len(self.rect_main_data) > 0):
            for rect in self.rect_main_data:
                self.canvas.delete(rect)

        self.rect_main_data.clear()
        self.rect_list.clear()

        self.topx = 0
        self.topy = 0

        self.botx = 0
        self.boty = 0

        self.canvas.create_image(0, 0, image=self.canvas.image, anchor=tk.NW)
        self.rect_id = self.canvas.create_rectangle(self.topx,
                                                    self.topy,
                                                    self.topx,
                                                    self.topy,
                                                    dash=(2, 2),
                                                    fill='',
                                                    outline='red')

    def clearRectangles(self, event):
        if (len(self.rect_main_data) > 0):
            for rect in self.rect_main_data:
                self.canvas.delete(rect)
        self.rect_main_data.clear()
        self.rect_list.clear()


if __name__ == '__main__':
    app = CanvasEventsDemo(Tk())
    app.mainloop()
