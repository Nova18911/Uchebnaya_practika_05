from tkinter import *


def level_1():
    game_root.withdraw()
    lvl1.deiconify()

def exit_level1():
    lvl1.withdraw()
    game_root.deiconify()

def game_menu():
    root.withdraw()
    game_root.deiconify() # функция открытия окна выбора уровней

def exit_gmenu():
    game_root.withdraw()
    root.deiconify() # закрытие окна выбора уровней

def exit_menu():
    root.destroy()
    root1.destroy()
    game_root.destroy()
    lvl1.destroy() # закрытие игры

def exit_rgames():
    root1.withdraw()
    root.deiconify() # закрытие окна правил

def rules_games():
    root.withdraw()
    root1.deiconify() # открытие окна правил


# главное окно
root = Tk()
root.title("Sokoban")
root.geometry("1000x700+230+20")
root.configure(bg='#d8e6de')
root.resizable(False, False)

titl = Label(root, text='SOKOBAN',
             font=("Arial", 52),
             background="#d8e6de",
             foreground="#1E1E1E")
titl.place(x=320,y=50)

btn1 = Button(root, text="НАЧАТЬ",
              width=80,height=3,
              background='#cc5b3f',
              foreground='#000000',
              command= lambda: game_menu())
btn1.place(x=200,y=270)

btn2 = Button(root, text="ПРАВИЛА ИГРЫ",
              width=80,height=3,
              background='#cc5b3f',
              foreground='#000000',
              command=lambda: rules_games())
btn2.place(x=200,y=340)

btn3 = Button(root, text="РЕКОРДЫ",
              width=80,height=3,
              background='#cc5b3f',
              foreground='#000000')
btn3.place(x=200,y=410)

btn4 = Button(root, text="ВЫХОД",
              width=80,height=3,
              background='#cc5b3f',
              foreground='#000000',
              command=lambda: exit_menu())
btn4.place(x=200,y=480)

# окно правил игры
root1 = Tk()
root1.title('SOKOBAN')
root1.geometry("1000x700+230+20")
root1.configure(bg='#d8e6de')
root1.resizable(False, False)

btn_r = Button(root1, text='НАЗАД',
               width=30,height=2,
                background='#cc5b3f',
              foreground='#000000',
               command=lambda: exit_rgames())
btn_r.place(x=20,y=620)

rules =Label(root1,text='Правила игры',
            font=('Arial', 30),
            background="#d8e6de",
            foreground="#1E1E1E")
rules.place(x=350,y=50)
rul1 = Label(root1, text='На складе, представленном в игре в виде плана,находится кладовщик и',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul1.place(x=140,y=150)
rul2 = Label(root1, text='ящики. Задача состоит в перемещении ящиков по лабиринту (складу) с',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul2.place(x=143,y=190)
rul3 = Label(root1, text='целью поставить их на заданные конечные места. Ящики можно толкать, но',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul3.place(x=122,y=230)
rul4 = Label(root1, text='нельзя тянуть. Кроме того, нельзя перемещать более одного ящика за',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul4.place(x=140,y=270)
rul5 = Label(root1, text='раз. Кладовщик может свободно перемещаться по складу, но не может',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul5.place(x=140,y=310)
rul6 = Label(root1, text='проходить через ящики и стены.',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul6.place(x=320,y=350)
rul7 = Label(root1, text='Головоломка решена, когда все коробки занимают места для хранения.',
             font=('Arial', 16),
             background="#d8e6de",
             foreground="#1E1E1E")
rul7.place(x=140,y=400)


# окно выбора уровня
game_root = Tk()
game_root.title('SOKOBAN')
game_root.geometry('1000x700+230+20')
game_root.configure(bg='#d8e6de')
game_root.resizable(False, False)

title1 = Label(game_root, text='ВЫБОР УРОВНЯ',
              font=("Arial", 52),
              background="#d8e6de",
              foreground="#1E1E1E")
title1.place(x=220,y=50)

lvl1 = Button(game_root, text='1',
              width=13,height=6,
              background='#cc5b3f',
              foreground='#000000',
              command= lambda: level_1())
lvl1.place(x=100,y=350)

lvl2 = Button(game_root, text='2',
              width=13,height=6,
              background='#cc5b3f',
              foreground='#000000')
lvl2.place(x=280,y=350)

lvl3 = Button(game_root, text='3',
              width=13,height=6,
              background='#cc5b3f',
              foreground='#000000')
lvl3.place(x=460,y=350)

lvl4 = Button(game_root, text='4',
              width=13,height=6,
              background='#cc5b3f',
              foreground='#000000')
lvl4.place(x=640,y=350)

lvl5 = Button(game_root, text='5',
              width=13,height=6,
              background='#cc5b3f',
              foreground='#000000')
lvl5.place(x=820,y=350)

btn = Button(game_root, text='НАЗАД',
             width=30,height=2,
             background='#cc5b3f',
             foreground='#000000',
             command= lambda: exit_gmenu())
btn.place(x=20,y=620)

# уровень 1
class Level1:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, bg='#fff0d8',
                    width=400, height=400)
        self.canvas.place(x=50, y=170)
        self.pers_size = 50
        self.x1 = 200
        self.y1 = 150
        self.x2 = self.x1 - self.pers_size
        self.y2 = self.y1 + self.pers_size


        self.static_objects = [self.canvas.create_rectangle(0,50,50,0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0,100,50,50, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0,150,50,100, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0, 200, 50, 150, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0, 250, 50, 200, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0, 300, 50, 250, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0, 350, 50, 300, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(0, 400, 50, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(50, 50, 100, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(100, 50, 150, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(150, 50, 200, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(200, 50, 250, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 50, 300, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(300, 50, 350, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 50, 400, 0, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 100, 400, 50, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 150, 400, 100, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 200, 400, 150, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 250, 400, 200, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 300, 400, 250, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 350, 400, 300, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(350, 400, 400, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(300, 400, 350, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 400, 300, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(200, 400, 250, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(150, 400, 200, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(100, 400, 150, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(50, 400, 100, 350, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 350, 300, 300, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 300, 300, 250, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 250, 300, 200, fill='#cc7c3f', outline='#843900'),
                              self.canvas.create_rectangle(250, 200, 300, 150, fill='#cc7c3f', outline='#843900')
                              ]

        self.move_object = [self.canvas.create_rectangle(200,200,250,150, fill='#6b6b6b', outline='#464645')]


        self.pers = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2,
                                            fill='#3fcc65', outline='#29a84b')


        repl = Button(self.master, text='ЗАНОВО',
                      width=20, height=2,
                      background='#cc5b3f',
                      foreground='#000000')
        repl.place(x=50, y=40)

        repl = Button(self.master, text='ШАГ НАЗАД',
                      width=20, height=2,
                      background='#cc5b3f',
                      foreground='#000000')
        repl.place(x=230, y=40)

        back = Button(self.master, text='НАЗАД',
                      width=30, height=2,
                      background='#cc5b3f',
                      foreground='#000000',
                      command= lambda: exit_level1())
        back.place(x=20, y=620)

        self.canvas.focus_set()

        self.master.bind("<KeyPress>", self.move)

    # обработка клавиш для передвижения
    def move(self, event):
        dx, dy = 0, 0
        if event.keysym == 'Left':
            dx = -50
        elif event.keysym == 'Right':
            dx = 50
        elif event.keysym == 'Up':
            dy = -50
        elif event.keysym == 'Down':
            dy = 50


        x_1, y_1, x_2, y_2 = self.canvas.coords(self.pers)
        new_x1 = x_1 + dx
        new_y1 = y_1 + dy
        new_x2 = x_2 + dx
        new_y2 = y_2 + dy

        if not self.check_collision(new_x1, new_y1, new_x2, new_y2):
                self.canvas.move(self.pers, dx, dy)


    def check_collision(self, new_x1, new_y1, new_x2, new_y2):
        # Проверяем пересечение с каждым статическим объектом
        for obj in self.static_objects:
            x1, y1, x2, y2 = self.canvas.coords(obj)
            if not (new_x2 - 50 < x1 or new_x1 + 50 > x2 or new_y2 - 50 < y1 or new_y1 + 50 > y2):
                return True  # Есть пересечение
        return False  # Пересечений нет



# окно уровня 1
lvl1 = Tk()
lvl1.title('SOKOBAN')
lvl1.geometry('1000x700+230+20')
lvl1.configure(bg='#d8e6de')
lvl1.resizable(False, False)

lvl_name = Label(lvl1, text='Уровень 1',
                    font=('Arial', 24),
                    background='#d8e6de',
                    foreground='#000000')
lvl_name.place(x=50,  y=110)
app = Level1(lvl1)




lvl1.withdraw()
game_root.withdraw()
root1.withdraw()
root.mainloop()
