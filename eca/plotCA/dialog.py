from tkinter import *
# 导入ttk
from tkinter import ttk
from tkinter import messagebox



width = 600
height = 600
sq_length = 8
cv = None
space = []
n = 100
for i in range(n):
    tm = []
    for j in range(n):
        if i == j or i == j * 2 or i == j * 3:
            tm.append('1')
        else:
            tm.append('0')
    space.append(tm)

def changeSize(event):
    global height
    for item in cv.find(ALL):
        cv.move(item, 0, event.height - height)
    height = event.height


def drawPoints(space, cv):
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


def drawByRow(space):
    root = Tk()
    root.title = 'CA'
    l = len(space)
    global width, height
    width = l * sq_length
    height = l * sq_length
    root.geometry(str(width if width < 800 else 800) + "x" + str(height if height < 800 else 800))
    global cv
    cv = Canvas(root, bg='white', width=width, height=height, scrollregion=(0, 0, width, height))
    # cv = Canvas(root, bg='white', width=width, height=height)
    hbar = Scrollbar(root, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=cv.xview)
    vbar = Scrollbar(root, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=cv.yview)
    cv.config(width=width, height=height)
    cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    cv.pack(side=LEFT, fill=BOTH, expand=YES)
    # cv.pack()
    drawPoints(space, cv)
    root.bind("<Configure>", changeSize)
    root.mainloop()



# 自定义对话框类，继承Toplevel
class MyDialog(Toplevel):
    # 定义构造方法
    def __init__(self, parent, title=None, modal=True):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        # 设置标题
        if title: self.title(title)
        self.parent = parent
        self.result = None
        # 创建对话框的主体内容
        frame = Frame(self)
        # 调用init_widgets方法来初始化对话框界面
        self.initial_focus = self.init_widgets(frame, parent)
        frame.pack(padx=5, pady=5)
        # # 调用init_buttons方法初始化对话框下方的按钮
        # self.init_buttons()
        # 根据modal选项设置是否为模式对话框
        if modal: self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        # 为"WM_DELETE_WINDOW"协议使用self.cancel_click事件处理方法
        self.protocol("WM_DELETE_WINDOW", self.cancel_click)
        # 根据父窗口来设置对话框的位置
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        print(self.initial_focus)
        # 让对话框获取焦点
        self.initial_focus.focus_set()
        self.wait_window(self)

    # 通过该方法来创建自定义对话框的内容
    def init_widgets(self, root, parent):
        l = len(space)
        global width, height
        width = l * sq_length
        height = l * sq_length
        parent.geometry(str(width if width < 800 else 800) + "x" + str(height if height < 800 else 800))
        global cv
        cv = Canvas(root, bg='white', width=width, height=height, scrollregion=(0, 0, width, height))
        # cv = Canvas(root, bg='white', width=width, height=height)
        hbar = Scrollbar(root, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=cv.xview)
        vbar = Scrollbar(root, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=cv.yview)
        cv.config(width=width, height=height)
        cv.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        cv.pack(side=LEFT, fill=BOTH, expand=YES)
        drawPoints(space, cv)

    # # 通过该方法来创建对话框下方的按钮框
    # def init_buttons(self):
    #     f = Frame(self)
    #     # 创建"确定"按钮,位置绑定self.ok_click处理方法
    #     w = Button(f, text="确定", width=10, command=self.ok_click, default=ACTIVE)
    #     w.pack(side=LEFT, padx=5, pady=5)
    #     # 创建"确定"按钮,位置绑定self.cancel_click处理方法
    #     w = Button(f, text="取消", width=10, command=self.cancel_click)
    #     w.pack(side=LEFT, padx=5, pady=5)
    #     self.bind("<Return>", self.ok_click)
    #     self.bind("<Escape>", self.cancel_click)
    #     f.pack()

    # 该方法可对用户输入的数据进行校验
    def validate(self):
        # 可重写该方法
        return True

    # 该方法可处理用户输入的数据
    def process_input(self):
        user_name = self.name_entry.get()
        user_pass = self.pass_entry.get()
        messagebox.showinfo(message='用户输入的用户名: %s, 密码: %s'
                                    % (user_name, user_pass))

    def ok_click(self, event=None):
        print('确定')
        # 如果不能通过校验，让用户重新输入
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        # 获取用户输入数据
        self.process_input()
        # 将焦点返回给父窗口
        self.parent.focus_set()
        # 销毁自己
        self.destroy()

    def cancel_click(self, event=None):
        print('取消')
        # 将焦点返回给父窗口
        self.parent.focus_set()
        # 销毁自己
        self.destroy()


class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        # 创建2个按钮，并为之绑定事件处理函数
        ttk.Button(self.master, text='模式对话框',
                   command=self.open_modal  # 绑定open_modal方法
                   ).pack(side=LEFT, ipadx=5, ipady=5, padx=10)
        ttk.Button(self.master, text='非模式对话框',
                   command=self.open_none_modal  # 绑定open_none_modal方法
                   ).pack(side=LEFT, ipadx=5, ipady=5, padx=10)

    def open_modal(self):
        d = MyDialog(self.master, title='模式对话框')  # 默认是模式对话框

    def open_none_modal(self):
        d = MyDialog(self.master, title='非模式对话框', modal=False)


root = Tk()
root.title("颜色对话框测试")
App(root)
root.mainloop()