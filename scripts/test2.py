import os
import tkinter as tk
import tkinter.filedialog as filedialog

from PIL import Image, ImageGrab, ImageTk

WIDTH, HEIGHT = 1200, 800
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None
path = "test.jpg"
rect_list = list()
rect_main_data = list()
ImageFilePath = ""
ImgOpen = None
prodDir = ""
ImageFound = False

window = tk.Tk()
window.title("Image Croping Tool")
window.geometry('%sx%s' % (WIDTH, HEIGHT))
window.configure(background='grey')

ImageFrame = tk.Frame(window, width=WIDTH, height=HEIGHT - 70, borderwidth=1)
ImageFrame.pack(expand=True, fill=tk.BOTH)
ImageFrame.place(x=0, y=71)

rawImage = Image.open("../data/download.jpg")
img = ImageTk.PhotoImage(rawImage)

canvasWidth, canvasHeight = rawImage.size
canvas = tk.Canvas(ImageFrame,
                   width=canvasWidth,
                   height=canvasHeight - 70,
                   borderwidth=2,
                   highlightthickness=2,
                   scrollregion=(0, 0, canvasWidth, canvasHeight))


def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y


def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.


def draw_rect(self):
    draw_data = canvas.create_rectangle(topx,
                                        topy,
                                        botx,
                                        boty,
                                        outline="green",
                                        fill="")
    rect_list.append((topx, topy, botx, boty))
    rect_main_data.append(draw_data)


def GetImageFilePath():
    global ImageFilePath
    global ImageFound
    global img
    global canvas
    global ImageFrame
    test = False
    if (ImageFound):
        canvas.destroy()
        canvas = tk.Canvas(ImageFrame,
                           width=canvasWidth,
                           height=canvasHeight - 70,
                           borderwidth=2,
                           highlightthickness=2,
                           scrollregion=(0, 0, canvasWidth, canvasHeight))

    ImageFilePath = filedialog.askopenfilename()

    ImgOpen = Image.open(ImageFilePath)

    if len(ImageFilePath) > 0:
        test = True
        img = ImageTk.PhotoImage(Image.open(ImageFilePath))
        ImageFound = True

        canvas.create_image(0, 0, image=img, anchor=tk.NW)

        canvas.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        rect_id = canvas.create_rectangle(topx,
                                          topy,
                                          topx,
                                          topy,
                                          dash=(2, 2),
                                          fill='',
                                          outline='red')
        canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)
        canvas.bind('<ButtonRelease-1>', draw_rect)
        canvas.update()

    if (test):
        window.mainloop()


def testPrint():
    print("Hello")


def clearRectangles():
    global rect_main_data
    global rect_list

    if (len(rect_main_data) > 0):
        for rect in rect_main_data:
            canvas.delete(rect)
    rect_main_data.clear()
    rect_list.clear()

    canvas.pack()
    window.mainloop()


# TitleBar = tk.LabelFrame(window,width=2000,height=70, borderwidth=1)
# TitleBar.pack(expand = 'yes', fill = 'both')
# TitleBar.place(x=0,y=0)

# tiletest = tk.Label(window,text="Image Cropping Tool", anchor=tk.NE)
# tiletest.pack()

# openFile = tk.Button(TitleBar,text = "Open Image",command = GetImageFilePath,width=10, height=2)
# openFile.place(x=10,y=10)
# cropImages = tk.Button(TitleBar,text = "Crop Images",command = cropImages,width=10, height=2)
# cropImages.place(x=140,y=10)
# clearImages = tk.Button(TitleBar,text = "Clear",command = clearRectangles,width=10, height=2)
# clearImages.place(x=270,y=10)

if (ImageFound):
    canvas.delete(img)
    canvas.update()
canvas.create_image(0, 0, image=img, anchor=tk.NW)
rect_id = canvas.create_rectangle(topx,
                                  topy,
                                  topx,
                                  topy,
                                  dash=(2, 2),
                                  fill='',
                                  outline='red')
canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)
canvas.bind('<ButtonRelease-1>', draw_rect)

hbar = tk.Scrollbar(ImageFrame, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
hbar.config(command=canvas.xview)
vbar = tk.Scrollbar(ImageFrame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)

window.mainloop()
