import io
import os
from tkinter import Tk, Button, Label, Canvas, CENTER, Frame, BOTH, HORIZONTAL, Scrollbar, BOTTOM, VERTICAL, \
    RIGHT, X, Y, LEFT, Text, StringVar, OptionMenu
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilenames, askopenfilename
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk, ImageDraw, ImageFont

WIDTH, HEIGHT = 150, 150
H = 1
V = 2
img_width, img_height = 100, 100
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("water marker")
# window.iconbitmap('/home/yassine/PycharmProjects/watermarker/logo.ico')
# window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='watermark.gif'))
window.geometry("1150x630")
window.config(padx=50, pady=50)

img_path = []
img = None
img_logo = None
path = None
canvas = None
canvas_container = None
canvas_container_text = None
frame = None
file = None
x = 0
y = 0
eps_x, eps_y = 0, 0
expended = False
img_logo_txt = None
image_container = None
canvas_text = None
inputtxt = None
background_frame = None
resize_mode = 0
cursor = 'target'
# sb_h_double_arrow sb_v_double_arrow
txt = ''
txt_width = ''
txt_height = ''
# variables contain positions of the final canvas image
x_min_text, y_min_text, x_min_img, y_min_img = 0, 0, 0, 0
final_text_width, final_img_width, final_text_height, final_img_height = 0, 0, 0, 0
canvas_background_path = ''
text_img_data = None
final_img_path = ''
# font dictionary
font_path_dict = {}
# font options menu
drop_family, clicked_family, drop_variants, clicked_variants, drop_size, clicked_size = \
    None, None, None, None, None, None
drop_variants_label, drop_size_label = None, None
color_button = None
colors = ((14, 15, 2), "#0000")
drop_color_label = None
IMAGES_PATH = './images_result'


def all_children(my_window):
    _list = my_window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


def clear():
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()


def add():
    global img_path, background_frame
    paths = askopenfilenames(filetypes=[("Image File", '.jpg .png')])
    if len(paths) > 0:
        img_path = []
        clear()
        column_index = 1
        row_index = 0
        background_frame = Frame(window, width=300, height=300)
        background_frame.pack()
        add_button2 = Button(background_frame, text="Add Images", width=15, command=add)
        add_button2.grid(row=0, column=0)
        add_button2.config(bg='gray')
        edit_button = Button(background_frame, text="Edit Image", width=15, command=lambda: edit(0))
        edit_button.config(bg='green')
        edit_button.grid(row=0, column=2)
        center_frame = Frame(background_frame, width=300, height=300, padx=25, pady=30)
        center_frame.grid(row=1, columnspan=3)

        for pt in range(len(paths)):
            img_path.append(paths[pt])
            if pt % 5 == 0 and pt != 0:
                row_index = pt
                column_index += 1
            image = ImageTk.PhotoImage(Image.open(paths[pt]).resize((WIDTH, HEIGHT), Image.ANTIALIAS).convert("RGBA"))
            btn_label = Button(center_frame, image=image, command=lambda c=pt: edit(c))
            btn_label.photo = image
            btn_label.grid(row=column_index, pady=5, padx=5, column=pt - row_index)


def edit(index):
    print(f'received index image {index}')
    clear()
    global img, img_path, canvas, frame, canvas_container, cursor, canvas_background_path
    canvas_background_path = img_path[index]
    frame = Frame(window, width=900, height=450)
    frame.grid(row=1, column=0)
    resize_img = Image.open(img_path[index])
    print(f'(width: {resize_img.width}, height: {resize_img.height})')
    canvas = Canvas(frame, cursor=cursor, bg='#FFFFFF', width=900, height=450,
                    scrollregion=(0, 0, resize_img.width, resize_img.height))
    h_bar = Scrollbar(frame, orient=HORIZONTAL)
    h_bar.pack(side=BOTTOM, fill=X)
    h_bar.config(command=canvas.xview)
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(xscrollcommand=h_bar.set, yscrollcommand=vbar.set)
    resize_img = ImageTk.PhotoImage(resize_img.convert("RGBA"), Image.ANTIALIAS)
    canvas.create_image(0, 0, image=resize_img, anchor="nw")
    canvas.photo = resize_img
    canvas.pack(side=LEFT, expand=True, fill=BOTH)
    logo = Button(text="Add logo", width=15, command=add_logo)
    logo.grid(row=2, column=0)
    # text = Button(text="Add text", width=15, command=add_text)
    # text.grid(row=3, column=0)
    add_text()
    save_image = Button(text="save image", width=15, bg='green', command=save_img_result)
    save_image.grid(row=0, column=0)


def add_logo():
    global canvas, img_logo,  path, frame, img_width, img_height, canvas_container, \
        final_img_path, final_img_width, final_img_height
    path = askopenfilename(filetypes=[("Image File", '.jpg .png')])
    if len(path) > 0:
        final_img_path = path
        img_logo = Image.open(path)
        img_logo = ImageTk.PhotoImage(img_logo.convert("RGBA"))
        img_width = img_logo.width()
        img_height = img_logo.height()
        final_img_width, final_img_height = img_width, img_height
        canvas_container = canvas.create_image(img_width/2, img_height/2, image=img_logo)
        canvas.bind('<B1-Motion>', move)


def add_logo_txt(fl):
    global canvas, img_logo, img_logo_txt, frame, img_width, img_height,\
        canvas_container_text, path, file, final_text_width, final_text_height
    path = None
    file = fl
    img_logo_txt = ImageTk.PhotoImage(file)
    img_width = img_logo_txt.width()
    img_height = img_logo_txt.height()
    final_text_width, final_text_height = img_width, img_height
    canvas_container_text = canvas.create_image(img_width/2, img_height/2, image=img_logo_txt)

    canvas.bind('<B1-Motion>', move)


def save_img_result():
    global canvas, canvas_background_path, final_img_path, img_logo, img_logo_txt, \
        text_img_data, final_text_width, final_text_height, final_img_width,\
        final_img_height, x_min_img, y_min_img, x_min_text, y_min_text, img_path, IMAGES_PATH, background_frame

    edited_img = Image.open(canvas_background_path)
    edited_w = edited_img.width
    edited_h = edited_img.height
    print(f'image: {(canvas_background_path.split("/")[-1]).split(".")[0]}, '
          f'edited width: {edited_w}, edited height: {edited_h}')
    my_progress = Progressbar(orient=HORIZONTAL, length=300, mode='determinate')
    my_progress.grid(row=3, column=0, pady=5)
    background_frame.update_idletasks()
    step_progress = 0
    for path_item in img_path:
        im = Image.open(path_item)
        w = im.width
        h = im.height
        print(f'image: {(path_item.split("/")[-1]).split(".")[0]}, width: {w}, height: {h}')
        # scale_factor_x = w - edited_w
        # scale_factor_y = h - edited_h
        back_im = im.copy()
        if img_logo is not None:
            im2 = Image.open(final_img_path)
            im2 = im2.resize((final_img_width, final_img_height))
            mask = im2.convert("RGBA")
            back_im.paste(mask, (int(x_min_img), int(y_min_img)), mask)
        if img_logo_txt is not None:
            text_im = Image.open(text_img_data)
            im3 = text_im.resize((final_text_width, final_text_height))
            mask = im3.convert("RGBA")
            back_im.paste(mask, (int(x_min_text), int(y_min_text)), mask)

        back_im.save(f'{IMAGES_PATH}/{(path_item.split("/")[-1]).split(".")[0]}.png', quality=95)
        step_progress += 1
        my_progress['value'] = step_progress * (300 // len(img_path))
        background_frame.update_idletasks()
    Label(text=" saving successfully completed !").grid(row=4, column=0, pady=5)


def check_resize_mode(event_x, event_y, objet):
    global frame, canvas, img_height, img_width, cursor, x_min_text, y_min_text, x_min_img, y_min_img
    print(f'event_x  : {event_x}, width: {img_width} \n '
          f'event_x type : {type(event_x)}, width type: {type(img_height)}')
    mode = 0
    # cursor = 'center_ptr'
    # return coordinates  position for object in canvas
    x_border, y_border, x_min, x_max, y_min, y_max \
        = objet_border_position(canvas_objet=canvas, objet=objet)
    if path is None:
        x_min_text = x_min
        y_min_text = y_min
    else:
        x_min_img = x_min
        y_min_img = y_min
    if x_border+20 > event_x > x_border and y_max > event_y > y_min:
        mode |= H
        # if cursor != 'target':
        #     cursor = 'target'
        #     frame.config(cursor=cursor)
    if y_border+20 > event_y > y_border and x_max > event_x > x_min:
        mode |= V
        # if cursor != 'target':
        #     cursor = 'target'
        #     frame.config(cursor=cursor)
    # if not mode:
        # if cursor != '':
        #     cursor = ''
        #     frame.config(cursor=cursor)
    print(f'mode : {mode}')
    return mode


def start_resize(event, objet):
    global resize_mode
    resize_mode = check_resize_mode(event.x, event.y, objet)


def resize_frame(event):
    global resize_mode, img_width, img_height, img_logo_txt, canvas_container, \
        canvas_container_text, V, H, img_logo, expended, canvas, eps_x, eps_y, \
        cursor, final_text_width, final_img_width, final_text_height, final_img_height
    print(f"resize_mode: {resize_mode}")
    if resize_mode:
        # cursor = ''
        if resize_mode & H:
            img_width = int(event.x - eps_x)
            if path is None:
                img_logo_txt = file
                img_logo_txt = img_logo_txt.resize((img_width, img_height), Image.ANTIALIAS)
                img_logo_txt = ImageTk.PhotoImage(img_logo_txt)
                canvas_container_text = canvas.create_image(eps_x + img_width / 2, eps_y + img_height / 2,
                                                            image=img_logo_txt)
                final_text_width = img_width
            else:
                img_logo = Image.open(path)
                img_logo = img_logo.resize((img_width, img_height), Image.ANTIALIAS).convert("RGBA")
                img_logo = ImageTk.PhotoImage(img_logo)
                canvas_container = canvas.create_image(eps_x + img_width/2, eps_y + img_height/2,
                                                       image=img_logo)
                final_img_width = img_width
        if resize_mode & V:
            img_height = int(event.y - eps_y)
            if path is None:
                img_logo_txt = file
                img_logo_txt = img_logo_txt.resize((img_width, img_height), Image.ANTIALIAS)
                img_logo_txt = ImageTk.PhotoImage(img_logo_txt)
                canvas_container_text = canvas.create_image(eps_x + img_width / 2, eps_y + img_height / 2,
                                                            image=img_logo_txt)
                final_text_height = img_height
            else:
                img_logo = Image.open(path)
                img_logo = img_logo.resize((img_width, img_height), Image.ANTIALIAS).convert("RGBA")
                img_logo = ImageTk.PhotoImage(img_logo)
                canvas_container = canvas.create_image(eps_x + img_width/2, eps_y + img_height/2, image=img_logo)
                final_img_height = img_height
    # else:
    #     cursor = 'size' if check_resize_mode(event.x, event.y, canvas_container) else ''
    #     if cursor != cursor:
    #         frame.config(cursor=cursor)
    #         cursor = cursor


def stop_resize(event):
    global resize_mode
    resize_mode = 0


def add_text():
    global canvas, frame, inputtxt, drop_family, clicked_family,\
        drop_variants, clicked_variants, drop_size, clicked_size, \
        font_path_dict, drop_variants_label, drop_size_label, \
        color_button, drop_color_label
    if inputtxt is None:
        font_path = []
        for root, dirs, files in os.walk("./font"):
            for f in files:
                if f.endswith(".ttf"):
                    font_path.append((os.path.join(root, f).split("/")[2], os.path.join(root, f)))
        for tup in font_path:
            font_path_dict.setdefault(tup[0], {})[(str(tup[1]).split("/")[3]).split(".ttf")[0]] = str(tup[1])
        font_path_item = [key for key in font_path_dict.keys()]
        print(font_path_item)
        print(font_path_dict)
        # menu_width = len(min(font_path_item, key=len))
        inputtxt = Text(frame, height=5, width=15, bg="light yellow")
        inputtxt.pack()
        input_btn = Button(frame, text="Add", width=12, command=add_text_btn)
        input_btn.pack()
        # DropDown Box for font Family
        Label(frame, text=" Family:").pack()
        clicked_family = StringVar()
        clicked_family.set(font_path_item[1])
        drop_family = OptionMenu(frame, clicked_family, *font_path_item, command=font_family)
        drop_family.config(width=12)
        drop_family.pack()
        # DropDown Box for font variants
        drop_variants_label = Label(frame, text=" variants:")
        drop_variants_label.pack()
        clicked_variants = StringVar()
        clicked_variants_values = [key for key in font_path_dict[font_path_item[1]].keys()]
        clicked_variants.set(clicked_variants_values[0])
        drop_variants = OptionMenu(frame, clicked_variants, *clicked_variants_values)
        drop_variants.config(width=12)
        drop_variants.pack()
        # DropDown Box for text Size
        drop_size_label = Label(frame, text=" Size:")
        drop_size_label.pack()
        clicked_size = StringVar()
        clicked_size.set("10")
        drop_size = OptionMenu(frame, clicked_size, "10", "11", "12", "15", "20", "30", "40", "50", "60", "70", "80")
        drop_size.pack()
        drop_color_label = Label(frame, text=" Color:")
        drop_color_label.pack()
        color_button = Button(frame, text='Select a Color', command=change_color)
        color_button.config(width=12)
        color_button.pack()


def font_family(value):
    global drop_family, clicked_family,\
        drop_variants, clicked_variants, \
        drop_size, clicked_size, font_path_dict, \
        drop_variants_label, drop_size_label, color_button, drop_color_label
    family = value
    print(family)
    drop_variants_label.pack_forget()
    drop_variants.pack_forget()
    drop_size_label.pack_forget()
    drop_size.pack_forget()
    color_button.pack_forget()
    drop_color_label.pack_forget()
    drop_variants_label = Label(frame, text=" variants:")
    drop_variants_label.pack()
    clicked_variants_values = [key for key in font_path_dict[value].keys()]
    clicked_variants.set(clicked_variants_values[0])
    drop_variants = OptionMenu(frame, clicked_variants, *clicked_variants_values)
    drop_variants.config(width=12)
    drop_variants.pack()
    # DropDown Box for text Size
    drop_size_label = Label(frame, text=" Size:")
    drop_size_label.pack()
    clicked_size.set(clicked_size.get())
    drop_size = OptionMenu(frame, clicked_size, "10", "11", "12", "15", "20", "30", "40", "50", "60", "70", "80")
    drop_size.pack()
    # color button
    drop_color_label = Label(frame, text=" Color:")
    drop_color_label.pack()
    color_button = Button(frame, text='Select a Color', command=change_color)
    color_button.config(width=12)
    color_button.pack()


def add_text_btn():
    global inputtxt, txt, text_img_data, \
        drop_family, clicked_family,\
        drop_variants, clicked_variants, \
        drop_size, clicked_size, font_path_dict, colors
    txt = inputtxt.get("1.0", "end-1c")
    if txt != '':
        print(clicked_family.get(), clicked_variants.get(), clicked_size.get())
        img_text = Image.new('RGBA', (200, 100), (255, 255, 255, 0))
        d = ImageDraw.Draw(img_text)
        font = ImageFont.truetype(font_path_dict[clicked_family.get()][clicked_variants.get()], int(clicked_size.get()))
        d.text((10, 25), txt, font=font, fill=(255, 0, 0))
        t_width, t_height = d.textsize(txt, font=font)
        img_text = Image.new('RGBA', (t_width, t_height), (255, 255, 255, 0))
        d = ImageDraw.Draw(img_text)
        d.text((0, 0), txt, font=font, fill=colors[0])
        # img_text.save("geeks1.png")
        # add_logo_txt('geeks1.png')
        s = io.BytesIO()
        img_text.save(s, 'png')
        in_memory_file = s.getvalue()
        file_data = io.BytesIO(in_memory_file)
        text_img_data = file_data
        dt = Image.open(file_data)
        add_logo_txt(dt)


def change_color():
    global colors
    colors = askcolor(title="Tkinter Color Chooser")
    # window.configure(bg=colors[1])


def move(e):
    global img_logo, img_logo_txt, canvas, path, x, y, img_width, img_height, \
        eps_x, eps_y, canvas_container, txt, canvas_container_text
    if path is None:
        start_resize(e, canvas_container_text)
        objet = canvas_container_text
    else:
        start_resize(e, canvas_container)
        objet = canvas_container

    resize_frame(e)
    if is_objet_position(canvas_objet=canvas, objet=objet, x_pos=e.x, y_pos=e.y):
        if not resize_mode:
            # frame.config(cursor='fleur')
            x = e.x
            y = e.y
            eps_x = x - img_width/2
            eps_y = y - img_height / 2
            if path is None:
                img_logo_txt = file
                img_logo_txt = img_logo_txt.resize((img_width, img_height))
                img_logo_txt = ImageTk.PhotoImage(img_logo_txt)
                canvas_container_text = canvas.create_image(x, y, image=img_logo_txt)
            else:
                img_logo = Image.open(path)
                img_logo = img_logo.resize((img_width, img_height)).convert("RGBA")
                img_logo = ImageTk.PhotoImage(img_logo)
                canvas_container = canvas.create_image(x, y, image=img_logo)


def is_objet_position(canvas_objet, objet, x_pos, y_pos):
    bounds = canvas_objet.bbox(objet)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    position_canvas_image = canvas_objet.coords(objet)
    x_min_border = position_canvas_image[0] - width/2
    x_max_border = position_canvas_image[0] + width/2
    y_min_border = position_canvas_image[1] - height / 2
    y_max_border = position_canvas_image[1] + height / 2
    # print(f'=================> x, y position image: {position_canvas_image}; width: {width}, {height}')
    # print(f'===========> x_min_border: {x_min_border}; x_max_border: {x_max_border}')
    # print(f'===========> y_min_border: {y_min_border}; y_max_border: {y_max_border}')
    return x_max_border-10 > x_pos > x_min_border+10 and y_max_border-10 > y_pos > y_min_border+10


def objet_border_position(canvas_objet, objet):
    bounds = canvas_objet.bbox(objet)  # returns a tuple like (x1, y1, x2, y2)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    position_canvas_image = canvas_objet.coords(objet)
    x_min_border = position_canvas_image[0] - width/2
    x_max_border = position_canvas_image[0] + width/2
    y_min_border = position_canvas_image[1] - height / 2
    y_max_border = position_canvas_image[1] + height / 2
    return x_max_border-10, y_max_border-10, x_min_border, x_max_border, y_min_border, y_max_border


add_button = Button(text="Add Images", width=15, command=add)
add_button.place(relx=0.5, rely=0.5, anchor=CENTER)

window.mainloop()

