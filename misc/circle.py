from tkinter import *
import os
from PIL import ImageTk, Image
trace = 0 

class CanvasEventsDemo: 
    def __init__(self, parent=None):
        canvas = Canvas(width=500, height=500) 
        canvas.pack()

        canvas.bind('<ButtonPress-1>', self.onStart) 
        canvas.bind('<B1-Motion>',     self.onGrow)  
        canvas.bind('<Double-1>',      self.onClear) 
        canvas.bind('<ButtonPress-3>', self.onMove)  

        self.canvas = canvas
        self.drawn  = None
        self.kinds = [canvas.create_oval]

        b = Button(text='Please Click here to upload the reference image', command=self.loadImage)
        b.pack(side=BOTTOM)

    def onStart(self, event):
        self.shape = self.kinds[0]
        # self.kinds = self.kinds[1:] + self.kinds[:1] 
        self.start = event
        self.drawn = None
    
    def onGrow(self, event):                         
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y, outline='red', width=2)
        if trace: print(objectId)
        self.drawn = objectId
    
    def onClear(self, event):
        event.widget.delete('all')                   
    
    def onMove(self, event):
        if self.drawn:                               
            if trace: print(self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

    def loadImage(self):
        img = Image.open(os.path.join(os.getcwd(), 'data', 'template.jpg'))
        img = img.resize((450, 450), Image.ANTIALIAS)
        filename = ImageTk.PhotoImage(img)
        # canvas = Canvas(height=500,width=500)
        self.canvas.image = filename  # <--- keep reference of your image
        self.canvas.create_image(25,0,anchor='nw',image=filename)
        self.canvas.pack()

if __name__ == '__main__':
    CanvasEventsDemo()
    mainloop()