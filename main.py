from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import a_star as search
from time import sleep

class Dialog(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grab_set()

    def moveToCenter(self):
        self.update()
        self.geometry(f"+{self.master.winfo_width() // 2 + self.master.winfo_x() - self.winfo_width() // 2}+{self.master.winfo_height() // 2 + self.master.winfo_y() - self.winfo_height() // 2}")
        self.update()

    def close(self):
        self.destroy()

class Waiting(Dialog):
    def __init__(self, master, maximum):
        super().__init__(master)

        self.title("waiting")

        self.label = Label(self, text="loading...")
        self.label.pack()

        self.progressbar = Progressbar(self, maximum = maximum, length = 200)
        self.progressbar.pack()

        self.moveToCenter()

    def set_value(self, value):
        self.progressbar['value'] = value
        self.update()

    def add(self):
        self.progressbar['value'] = self.progressbar['value'] + 1
        self.update()

class Searching(Dialog):
    def __init__(self, master):
        super().__init__(master)
        self.step = 0

        self.title("searching")

        self.label1 = Label(self, text = "searching...")
        self.label1.pack()

        self.label2 = Label(self, text = "searching layer: " + str(self.step))
        self.label2.pack()

        self.moveToCenter()

    def add(self):
        self.step += 1
        self.label2['text'] = "searching layer: " + str(self.step)
        self.update()


class NewPic(Dialog):
    def __init__(self, master, default, callableFunction):
        super().__init__(master)
        self.callable = callableFunction

        self.picPath = StringVar()
        self.width = StringVar()
        self.height = StringVar()

        self.picPath.set(default['path'])
        self.width.set(str(default['shape'][0]))
        self.height.set(str(default['shape'][1]))

        self.title("select picture")

        self.line1 = Frame(self)
        self.line2 = Frame(self)

        self.label1 = Label(self.line1, text="Picture Path:")
        self.label2 = Label(self.line2, text="width")
        self.label3 = Label(self.line2, text="height")

        self.picPathEntry = Entry(self.line1,
            textvariable = self.picPath
        )
        
        self.picSelectButton = Button(self.line1,
            text="...",
            command = self.getPath
        )

        self.widthSpin = Spinbox(self.line2, from_ = 3, to_ = 10, textvariable=self.width)
        self.heightSpin = Spinbox(self.line2, from_ = 3, to_ = 10, textvariable=self.height)

        self.okButton = Button(self,
            text="OK",
            command = self.ok
        )

        self.label1.pack(side = LEFT, padx = 10)
        self.picPathEntry.pack(side = LEFT, fill = X, expand = 1, padx = 10)
        self.picSelectButton.pack(side = LEFT, padx = 10)
        self.label2.pack(side = LEFT, padx = 10)
        self.widthSpin.pack(side = LEFT, padx = 10, fill = X, expand = 1)
        self.label3.pack(side = LEFT, padx = 10)
        self.heightSpin.pack(side = LEFT, padx = 10, fill = X, expand = 1)
        self.line1.pack(fill = X, expand = 1, pady = 5)
        self.line2.pack(fill = X, expand = 1, pady = 5)
        self.okButton.pack(pady = 5)

        self.moveToCenter()

    def ok(self):
        self.destroy()
        self.callable({'path' : self.picPath.get(), "shape": (int(self.width.get()), int(self.height.get()))})

    def getPath(self):
        path = askopenfilename()
        self.picPath.set(path)


class APP(Tk):
    def __init__(self):
        super().__init__()
        self.last_data = {
            "path": "image.png",
            "shape": (3, 3)
        }
        self.first_run = True
        self.selectPic()

    def init_window(self):
        self.geometry("800x500")

        self.title("Jigsaw puzzle")

        self.buttonFrame = Frame(self)
        self.buttonFrame.pack()

        self.selectPicButton = Button(self.buttonFrame,
            text="new picture",
            command = self.selectPic
        )
        self.selectPicButton.pack(side=LEFT, padx = 13, pady = 13)

        self.label1 = Label(self.buttonFrame, text = "step:")
        self.label1.pack(side = LEFT, padx = 13, pady = 13)

        self.stepString = StringVar()
        self.stepString.set("13")
        self.stepSpinBox = Spinbox(self.buttonFrame, from_ = 1, to_ = 20, textvariable = self.stepString)
        self.stepSpinBox.pack(side = LEFT)

        self.randomPicButton = Button(self.buttonFrame,
            text="random",
            command = self.random
        )
        self.randomPicButton.pack(side=LEFT, padx = 13, pady = 13)

        self.solvePicButton = Button(self.buttonFrame, 
            text="solve",
            command=self.solve
        )
        self.solvePicButton.pack(side=LEFT, padx = 13, pady = 13)

        self.canvas = Canvas(self)

        self.canvas.pack(fill = BOTH, expand = 1)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Configure>", self.draw)
        self.canvas.bind("<Key>", self.canvas_keyDown)

    def selectPic(self):
        NewPic(self, self.last_data, self.selectPicCallback)

    def selectPicCallback(self, data):
        if self.first_run:
            self.first_run = False
            self.init_window()
            self.init_picture(data)
        else:
            self.init_picture(data)
            self.draw("all")

    def random(self):
        step = int(self.stepString.get())
        self.data = search.get_random(self.shape, step)
        self.foreach_all_with_pos(lambda pos : self.draw(pos))

    def solve(self):
        waiting = Searching(self)
        way = search.search(self.data, self.shape)[1:]
        waiting.close()
        for data in way:
            sleep(0.3)
            self.data = data
            self.foreach_all_with_pos(lambda pos : self.draw(pos))
            self.update()

    def format_pos(self, pos):
        return pos[0] * self.shape[1] + pos[1]


    def foreach_all_with_pos(self, fun):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                fun((i, j))

    def draw_sub_pic(self, canvas_index, image_index):
        self.canvas.itemconfig(self.canvas_image[canvas_index], image = self.tk_images[image_index])

    def draw(self, e):
        def draw_one_pic(pos):
            self.draw_sub_pic(self.format_pos(pos), self.data[self.format_pos(pos)])
        if isinstance(e, Event) or e == "all":
            if isinstance(e, Event):
                self.canvas_size = (e.width, e.height)
            waiting = Waiting(self, self.shape[0] * self.shape[1])
            self.sub_size = (self.canvas_size[0] // self.shape[0], self.canvas_size[1] // self.shape[1])
            self.tk_images = []
            for image in self.images:
                self.tk_images.append(ImageTk.PhotoImage(image.resize(self.sub_size)))
            self.foreach_all_with_pos(lambda pos : self.canvas.moveto(self.canvas_image[self.format_pos(pos)], self.sub_size[0] * pos[0], self.sub_size[1] * pos[1]))
            self.foreach_all_with_pos(lambda pos : (draw_one_pic(pos), waiting.add()))
            waiting.close()
        else:
            draw_one_pic(e)

    def init_picture(self, data):
        self.last_data = data
        self.shape = data['shape']
        image = Image.open(data['path'])
        subsize = (image.size[0] // self.shape[0], image.size[1] // self.shape[1])

        self.images = [Image.new("RGB", (1, 1))]
        self.foreach_all_with_pos(lambda pos : self.images.append(image.crop((subsize[0] * pos[0], subsize[1] * pos[1], subsize[0] * (pos[0] + 1), subsize[1] * (pos[1] + 1)))))

        self.canvas.delete("all")
        self.canvas_image = []
        self.foreach_all_with_pos(lambda pos : self.canvas_image.append(self.canvas.create_image(0, 0, anchor = NW)))

        self.data = search.get_answer(self.shape)

    def move(self, firstBlock, secondBlock):
        self.data = search.swap(self.data, self.shape, firstBlock, secondBlock)
        self.draw(firstBlock)
        self.draw(secondBlock)

    def canvas_click(self, e):
        pos = (e.x // self.sub_size[0], e.y // self.sub_size[1])
        space_pos = search.get_space_pos(self.data, self.shape)
        if search.get_distance(pos, space_pos) == 1:
            self.move(pos, space_pos)

    def canvas_keyDown(self, e):
        print(e)
        
app = APP()

mainloop()
