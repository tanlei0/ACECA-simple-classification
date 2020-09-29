from tkinter import *

width = 600
height = 600
sq_length = 8


class MyDialog:

    def __init__(self, space, parent=None):
        self.root = Tk()
        self.top = Toplevel(self.root)
        self.space = space
        self.cv = None
        self.b = None
        self.drawByRow(space=self.space)
        # Label(self.top, text="Value").pack()
        #
        # self.e = Entry(self.top)
        # self.e.pack(padx=5)
        #
        # b = Button(self.top, text="OK", command=self.ok)
        # b.pack(pady=5)

    def changeSize(self,event):
        global height
        for item in cv.find(ALL):
            cv.move(item, 0, event.height - height)
        height = event.height

    # def changeSize(self, event):
    #     self.b.winfo_geometry()
    #     global height
    #     wh = int(self.top.geometry().split('+')[0].split('x')[1])
    #     offset = int(self.b.winfo_geometry().split('+')[0].split('x')[1])
    #     print(height, wh, offset)
    #     for item in cv.find(ALL):
    #         cv.move(item, 0, wh - height - offset)
    #     height = wh - offset
    #     # cv.config(width=event.width, height=event.height)

    def drawPoints(self, space, cv):
        x1 = 0
        y1 = height - sq_length
        x2 = x1 + sq_length
        y2 = height
        for i, row in enumerate(space):
            for j, char in enumerate(row):
                if char == '1':
                    cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
                                        y2 - sq_length * i, width=None, fill='blue', outline='blue')
                # if char == '0':
                #     cv.create_rectangle(x1 + sq_length * j, y1 - sq_length * i, x2 + sq_length * j,
                #                         y2 - sq_length * i, width=None, fill='white', outline='white')

    def drawByRow(self, space):
        self.top.title = 'CA'
        l = len(space)
        global width, height, cv
        width = l * sq_length
        height = l * sq_length
        self.top.geometry(str(width if width < 800 else 800) + "x" + str(height if height < 800 else 800))
        cv = self.cv = Canvas(self.top, bg='white', width=width, height=height, scrollregion=(0, 0, width, height))
        # cv = Canvas(root, bg='white', width=width, height=height)
        hbar = Scrollbar(self.top, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=cv.xview)
        vbar = Scrollbar(self.top, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=cv.yview)
        cv.config(width=width, height=height)
        cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        cv.pack(side=LEFT, fill=BOTH, expand=YES)
        # cv.pack()
        self.drawPoints(space, cv)
        self.top.bind("<Configure>", self.changeSize)
        # root.mainloop()

    def ok(self):
        self.top.destroy()

    def showImage(self):
        self.root.withdraw()
        self.root.wait_window(self.top)


if __name__ == '__main__':
    space = []
    n = 10
    for i in range(n):
        tm = []
        for j in range(n):
            if i == j or i == j * 2 or i == j * 3:
                tm.append('1')
            else:
                tm.append('0')
        space.append(tm)
    MyDialog(space).showImage()
    MyDialog(space).showImage()
