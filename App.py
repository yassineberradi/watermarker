from tkinter import *

HORIZONTAL = 1
VERTICAL = 2

# filename = r'watermark.png'
# img = Image.open(filename)
# img.save('logo.ico')
# def save_as_png(c, file_name):
#     # save postscript image
#     c.postscript(file=file_name + '.eps')
#     # use PIL to convert to PNG
#     im = Image.open(file_name + '.eps')
#     im.save(file_name + '.png', 'png')
#
#
# def getter(widget):
#     global window
#     xx = window.winfo_rootx() + widget.winfo_x()
#     yy = window.winfo_rooty() + widget.winfo_y()
#     xx1 = xx + widget.winfo_width()
#     yy1 = yy + widget.winfo_height()
#     ImageGrab.grab().crop((xx, yy, xx1, yy1)).save("image_canvas.png")

class App:
    def __init__(self, top):
        self.Frame1 = Frame(top, bd=5, relief='raised', width=100, height=100)
        self.Frame1.place(x=10, y=10)
        self.Frame1.bind("<ButtonPress-1>", self.start_resize)
        self.Frame1.bind("<ButtonRelease-1>", self.stop_resize)
        self.Frame1.bind("<Motion>", self.resize_frame)
        self.resize_mode = 0
        self.cursor = ''

    def check_resize_mode(self, x, y):
        width, height = self.Frame1.cget('width'), self.Frame1.cget('height')
        mode = 0
        if x > width-10:
            mode |= HORIZONTAL
        if y > height-10:
            mode |= VERTICAL
        return mode

    def start_resize(self, event):
        self.resize_mode = self.check_resize_mode(event.x, event.y)

    def resize_frame(self, event):
        if self.resize_mode:
            if self.resize_mode & HORIZONTAL:
                self.Frame1.config(width=event.x)
            if self.resize_mode & VERTICAL:
                self.Frame1.config(height=event.y)
        else:
            cursor = 'size' if self.check_resize_mode(event.x, event.y) else ''
            if cursor != self.cursor:
                self.Frame1.config(cursor=cursor)
                self.cursor = cursor

    def stop_resize(self, event):
        self.resize_mode = 0
