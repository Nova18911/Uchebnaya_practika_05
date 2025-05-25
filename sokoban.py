from tkinter import *
from tkinter import messagebox
import json
from PIL import Image, ImageTk
from threading import Thread
import sounddevice as sd
import soundfile as sf
import numpy as np
from playsound import playsound


class MusicPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data, self.fs = sf.read(file_path, dtype='float32')
        if len(self.data.shape) == 1:
            self.data = np.column_stack((self.data, self.data))
        self.is_playing = False

    def play(self):
        if not self.is_playing:
            self.is_playing = True
            Thread(target=self._play_loop, daemon=True).start()

    def _play_loop(self):
        sd.play(self.data, self.fs, loop=True)
        while self.is_playing:
            sd.sleep(100)

    def stop(self):
        self.is_playing = False
        sd.stop()

def toggle_music():
    if player.is_playing:
        player.stop()
    else:
        player.play()


# Инициализация плеера
player = MusicPlayer("music_for_main.mp3")
player.play()

def play_step_sound():
    Thread(target=lambda: playsound("steps.mp3"), daemon=True).start()

def play_pushing_box():
    Thread(target=lambda: playsound("pushing_box.mp3"), daemon=True).start()

# Обновляем отображение рекордов при открытии окна
def show_records_screen():
    main_root.withdraw()
    records_root.deiconify()
    update_records_display()

# Добавляем в начало кода (после импортов) функцию для работы с рекордами
def load_records():
    with open('records.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"level1": [], "level2": [], "level3": []}


def save_records(records):
    with open('records.json', 'w') as rec:
        json.dump(records, rec, indent=4)


def add_record(level, nickname, steps):
    records = load_records()
    level_key = f"level{level}"

    # Добавляем новый рекорд
    records[level_key].append({"nickname": nickname, "steps": steps})

    # Сортируем по количеству шагов (чем меньше, тем лучше)
    records[level_key].sort(key=lambda x: x["steps"])

    # Оставляем только топ-3
    records[level_key] = records[level_key][:3]

    save_records(records)
    update_records_display()


def update_records_display():
    records = load_records()

    # Очищаем старые записи
    for i in range(1, 4):
        for j in range(1, 4):
            canvas_r.delete(f"record_level{i}_pos{j}")

    # Добавляем новые записи
    for level in range(1, 4):
        level_key = f"level{level}"
        level_records = records.get(level_key, [])

        for i, record in enumerate(level_records):
            nickname = record["nickname"]
            steps = record["steps"]

            # Позиционирование зависит от уровня
            if level == 1:
                x_pos = 190
            elif level == 2:
                x_pos = 520
            else:
                x_pos = 840

            y_pos = 220 + i * 100

            # Отображаем запись
            canvas_r.create_text(
                x_pos, y_pos + 25,
                text=f"{nickname}: {steps} шагов",
                font=('Arial', 12),
                fill='#000000',
                tags=f"record_level{level}_pos{i + 1}"
            )

# Основные функции игры
def level_1():
    global nick_level1
    game_root.withdraw()
    lvl1.deiconify()
    if nick_level1 is None:  # Если ник еще не введен
        input_nick(1)
    if nick_level1:  # Если ник введен (не None и не пустая строка)
        nick_label1.config(text=f"Игрок: {nick_level1}")
        app1.replace()

def exit_level1():
    global nick_level1
    lvl1.withdraw()
    game_root.deiconify()
    nick_level1 = None  # Сбрасываем ник для уровня 1
    nick_label1.config(text="Игрок: ")  # Очищаем поле отображения

def level_2():
    global nick_level2
    game_root.withdraw()
    lvl2.deiconify()
    if nick_level2 is None:
        input_nick(2)
    if nick_level2:
        nick_label2.config(text=f"Игрок: {nick_level2}")
        app2.replace()


def exit_level2():
    global nick_level2
    lvl2.withdraw()
    game_root.deiconify()
    nick_level2 = None  # Сбрасываем ник для уровня 2
    nick_label2.config(text="Игрок: ")  # Очищаем поле отображения

def level_3():
    global nick_level3
    game_root.withdraw()
    lvl3.deiconify()
    if nick_level3 is None:
        input_nick(3)
    if nick_level3:
        nick_label3.config(text=f"Игрок: {nick_level3}")

def exit_lvl3():
    global nick_level3
    lvl3.withdraw()
    game_root.deiconify()
    nick_level3 = None  # Сбрасываем ник для уровня 3
    nick_label3.config(text="Игрок: ")  # Очищаем поле отображения

def game_menu():
    main_root.withdraw()
    game_root.deiconify()


def exit_gmenu():
    game_root.withdraw()
    main_root.deiconify()


def exit_menu():
    main_root.destroy()
    for window in [rules_root, game_root, records_root, nick_root, lvl1, lvl2, lvl3]:
        try:
            window.destroy()
        except:
            continue


def exit_rgames():
    rules_root.withdraw()
    main_root.deiconify()


def rules_games():
    main_root.withdraw()
    rules_root.deiconify()


def exit_records():
    records_root.withdraw()
    main_root.deiconify()

nick_level1 = None
nick_level2 = None
nick_level3 = None


def input_nick(level):

    def save_nick():
        nonlocal level
        nickname = nick.get().strip()

        if not nickname:
            messagebox.showerror("Ошибка", "Необходимо ввести никнейм!")
            return

        if len(nickname) >= 10:
            messagebox.showerror("Ошибка", "Никнейм не должен превышать 10 символов!")
            return

        # Сохраняем ник для соответствующего уровня
        if level == 1:
            global nick_level1
            nick_level1 = nickname
            nick_label1.config(text=f"Игрок: {nickname}")
        elif level == 2:
            global nick_level2
            nick_level2 = nickname
            nick_label2.config(text=f"Игрок: {nickname}")
        elif level == 3:
            global nick_level3
            nick_level3 = nickname
            nick_label3.config(text=f"Игрок: {nickname}")

        nick_root.destroy()

    nick_root = Toplevel()
    nick_root.geometry('400x200+500+300')
    nick_root.configure(bg='#d8e6de')
    nick_root.resizable(False, False)
    nick_root.overrideredirect(True)

    # Блокируем закрытие окна через Alt+F4
    nick_root.protocol("WM_DELETE_WINDOW", lambda: None)



    border_frame = Frame(nick_root, bg='#000000', bd=1)
    border_frame.pack(fill='both', expand=True)
    main_frame = Frame(border_frame, bg='#d8e6de')
    main_frame.pack(fill='both', expand=True, padx=2, pady=2)

    Label(nick_root, text='Введите имя',
          background='#d8e6de',
          foreground='#000000',
          font=('Arial', 20)).place(x=115, y=10)

    nick = Entry(nick_root, width=50)
    nick.place(x=50, y=100)

    Button(nick_root, text='OK',
           width=10,
           background='#cc5b3f',
           foreground='#000000',
           command=save_nick).place(x=165, y=150)

    nick_root.grab_set()
    nick_root.focus_set()  # Устанавливаем фокус на окно
    nick_root.wait_window()


# Главное окно
main_root = Tk()
main_root.title("Sokoban")
main_root.geometry("1000x700+230+20")
main_root.configure(bg='#d8e6de')
main_root.resizable(False, False)

SOKOBAN = Label(main_root, text='SOKOBAN',
                font=("Arial", 52),
                background="#d8e6de",
                foreground="#1E1E1E")
SOKOBAN.place(x=320, y=50)

Button(main_root, text="НАЧАТЬ",
       width=80, height=3,
       background='#cc5b3f',
       foreground='#000000',
       command=game_menu).place(x=200, y=270)

Button(main_root, text="ПРАВИЛА ИГРЫ",
       width=80, height=3,
       background='#cc5b3f',
       foreground='#000000',
       command=rules_games).place(x=200, y=340)

Button(main_root, text="РЕКОРДЫ",
       width=80, height=3,
       background='#cc5b3f',
       foreground='#000000',
       command=show_records_screen).place(x=200, y=410)

Button(main_root, text="ВЫХОД",
       width=80, height=3,
       background='#cc5b3f',
       foreground='#000000',
       command=exit_menu).place(x=200, y=480)

Button(main_root, text='🔊',
       font=('Arial, 20'),
       command=toggle_music,
       background='#cc5b3f').place(x=706, y=600)

# Окно правил игры
rules_root = Toplevel()
rules_root.title('SOKOBAN')
rules_root.geometry("1000x700+230+20")
rules_root.configure(bg='#d8e6de')
rules_root.resizable(False, False)

Button(rules_root, text='НАЗАД',
       width=30, height=2,
       background='#cc5b3f',
       foreground='#000000',
       command=exit_rgames).place(x=20, y=620)

Label(rules_root, text='Правила игры',
      font=('Arial', 30),
      background="#d8e6de",
      foreground="#1E1E1E").place(x=350, y=50)

rules_text = [
    '   Цель игры: необходимо поставить все ящики в отмеченные точки.   ',
    '    Игровое поле представляет собой склад, на котором находится    ',
    '                  кладовщик, стены (препятствия) и ящики.           ',
    ' Головоломка решена, когда все коробки занимают места для хранения. ',
    'Игрок оказывается в безвыходной ситуации (ситуации поражения), если',
    'ящик задвинут в угол, два ящика располагаются рядом друг с другом у',
    '         стены, если четыре ящика образуют квадрат 2 на 2.         '
]

for i, text in enumerate(rules_text):
    Label(rules_root, text=text,
          font=('Arial', 16),
          background="#d8e6de",
          foreground="#1E1E1E").place(x=140, y=150 + i * 40)

# Окно рекордов
records_root = Toplevel()
records_root.title('SOKOBAN')
records_root.geometry('1000x700+230+20')
records_root.configure(bg='#d8e6de')
records_root.resizable(False, False)

canvas_r = Canvas(records_root, width=1000, height=700, bg='#d8e6de')
canvas_r.place(x=0, y=0)
canvas_r.create_text(500, 50, text='РЕКОРДЫ', font=('Arial', 42), fill ='#000000')
canvas_r.create_text(220, 150, text='Уровень 1', font=('Arial', 16), fill = '#000000')
canvas_r.create_text(500, 150, text='Уровень 2', font=('Arial', 16), fill = '#000000')
canvas_r.create_text(800, 150, text='Уровень 3', font=('Arial', 16), fill = '#000000')
canvas_r.create_rectangle(30,220,70,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(30,320,70,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(30,420,70,470, fill='#d8e6de', outline='#843900')
canvas_r.create_text(50,250, text='1', font=('Arial', 12), fill='#000000')
canvas_r.create_text(50,350, text='2', font=('Arial', 12), fill='#000000')
canvas_r.create_text(50,450, text='3', font=('Arial', 12), fill='#000000')
canvas_r.create_rectangle(90,220,310,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(90,320,310,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(90,420,310,470, fill='#d8e6de', outline='#843900')

canvas_r.create_rectangle(360,220,400,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(360,320,400,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(360,420,400,470, fill='#d8e6de', outline='#843900')
canvas_r.create_text(380,250, text='1', font=('Arial', 12), fill='#000000')
canvas_r.create_text(380,350, text='2', font=('Arial', 12), fill='#000000')
canvas_r.create_text(380,450, text='3', font=('Arial', 12), fill='#000000')
canvas_r.create_rectangle(420,220,640,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(420,320,640,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(420,420,640,470, fill='#d8e6de', outline='#843900')

canvas_r.create_rectangle(690,220,730,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(690,320,730,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(690,420,730,470, fill='#d8e6de', outline='#843900')
canvas_r.create_text(710,250, text='1', font=('Arial', 12), fill='#000000')
canvas_r.create_text(710,350, text='2', font=('Arial', 12), fill='#000000')
canvas_r.create_text(710,450, text='3', font=('Arial', 12), fill='#000000')
canvas_r.create_rectangle(750,220,970,270, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(750,320,970,370, fill='#d8e6de', outline='#843900')
canvas_r.create_rectangle(750,420,970,470, fill='#d8e6de', outline='#843900')


Button(records_root, text='НАЗАД',
       width=30, height=2,
       background='#cc5b3f',
       foreground='#000000',
       command=exit_records).place(x=20, y=620)


texture1 = Image.open("box1.jpg")
texture1 = texture1.resize((100, 100))
texture_photo1 = ImageTk.PhotoImage(texture1)

texture2 = Image.open("box2.jpg")
texture2 = texture2.resize((100, 100))
texture_photo2 = ImageTk.PhotoImage(texture2)

texture3 = Image.open("box3.jpg")
texture3 = texture3.resize((100, 100))
texture_photo3 = ImageTk.PhotoImage(texture3)

# Окно выбора уровня
game_root = Toplevel()
game_root.title('SOKOBAN')
game_root.geometry('1000x700+230+20')
game_root.configure(bg='#d8e6de')
game_root.resizable(False, False)

Label(game_root, text='ВЫБОР УРОВНЯ',
      font=("Arial", 52),
      background="#d8e6de",
      foreground="#1E1E1E").place(x=220, y=50)

Button(game_root,
       width=100, height=100,
       image=texture_photo1,
       foreground='#000000',
       command=lambda: level_1()).place(x=250, y=350)


Button(game_root, text='2',
       width=100, height=100,
       image=texture_photo2,
       foreground='#000000',
       command=lambda: level_2()).place(x=430, y=350)

Button(game_root,
       width=100, height=100,
       image=texture_photo3,
       foreground='#000000',
       command= lambda: level_3()).place(x=610, y=350)

Button(game_root, text='НАЗАД',
       width=30, height=2,
       background='#cc5b3f',
       foreground='#000000',
       command=exit_gmenu).place(x=20, y=620)

def load_person_image():
    image_pers = Image.open("person.jpg")
    image_pers = image_pers.resize((50, 50))
    return ImageTk.PhotoImage(image_pers)

def load_stat_obj_image():
    image_stat_obj = Image.open("static_obj.jpg")
    image_stat_obj = image_stat_obj.resize((50, 50))
    return ImageTk.PhotoImage(image_stat_obj)

def load_move_obj_image():
    image_move_obj = Image.open("box.jpg")
    image_move_obj = image_move_obj.resize((50, 50))
    return ImageTk.PhotoImage(image_move_obj)


class Basic_lvl:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, bg='#fff0d8', width=400, height=400)
        self.canvas.place(x=50, y=170)
        self.pers_image = load_person_image()
        self.static_obj_t = load_stat_obj_image()
        self.move_obj_t = load_move_obj_image()

        self.steps = 0
        self.steps_l = Label(master, text='Шаги', font=('Arial', 24),
                             bg='#d8e6de', fg='#000000')
        self.steps_l.place(x=700, y=100)

        self.steps_label = Label(master, text=f"{self.steps}",
                                 font=('Arial', 24),
                                 bg='#cc5b3f',
                                 fg='#000000')
        self.steps_label.place(x=800, y=100)

        # Кнопки
        repl = Button(self.master, text='ЗАНОВО', width=20, height=2,
                      background='#cc5b3f', foreground='#000000',
                      command=self.replace)
        repl.place(x=50, y=40)

        back = Button(self.master, text='НАЗАД', width=30, height=2,
                      background='#cc5b3f', foreground='#000000',
                      command=lambda: (self.exit_level(), self.replace()))
        back.place(x=20, y=620)

        self.master.bind("<KeyPress>", self.move)
        self.level_completed = False
        self.static_objects = []

    def show_win_window(self, level_num, nick_var):
        # Отключаем кнопки
        for child in self.master.winfo_children():
            if isinstance(child, Button):
                child.config(state=DISABLED)

        self.master.unbind("<KeyPress>")

        self.win_root = Toplevel()
        self.win_root.title('SOKOBAN')
        self.win_root.geometry('400x250+500+300')
        self.win_root.resizable(False, False)
        self.win_root.configure(bg='#d8e6de')
        self.win_root.overrideredirect(True)

        # Создаем рамку с тенью
        border_frame = Frame(self.win_root, bg='black', bd=3)
        border_frame.pack(fill='both', expand=True, padx=3, pady=3)

        main_frame = Frame(border_frame, bg='#d8e6de')
        main_frame.pack(fill='both', expand=True, padx=1, pady=1)

        content = Frame(main_frame, bg='#d8e6de')
        content.pack(fill='both', expand=True, padx=20, pady=20)

        Label(content, text='ВЫ ВЫИГРАЛИ!', font=('Arial', 24, 'bold'),
              bg='#d8e6de', fg='#000000').pack(pady=(10, 20))

        Label(content, text=f"{self.steps} шагов", font=('Arial', 16),
              bg='#d8e6de', fg='#000000').pack()

        Button(content, text='OK', width=10, height=1,
               bg='#cc5b3f', fg='white', font=('Arial', 10, 'bold'),
               command=lambda: (
                   add_record(level_num, nick_var, self.steps),
                   self.exit_level(),
                   self.win_root.destroy(),
                   self.replace()
               )).pack(pady=20)

    # проверка столкновения со стенами
    def check_collision(self, x1, y1, x2, y2):
        for obj in self.static_objects:
            wall_x1, wall_y1, wall_x2, wall_y2 = self.canvas.bbox(obj)
            if not (x2 <= wall_x1 or x1 >= wall_x2 or y2 <= wall_y1 or y1 >= wall_y2):
                return True
        return False

    # проверка столкновения с ящиками
    def check_box_collision(self, current_box, x1, y1, all_boxes):
        for box in all_boxes:
            if box == current_box:
                continue
            box_x1, box_y1, box_x2, box_y2 = self.canvas.bbox(box)
            if not (x1 + 50 <= box_x1 or x1 >= box_x2 or y1 + 50 <= box_y1 or y1 >= box_y2):
                return True
        return False

    #сброс уровня
    def replace(self):
        self.steps = 0
        self.steps_label.config(text=f"{self.steps}")
        self.level_completed = False

        # Включение кнопок и привязка клавиш
        for child in self.master.winfo_children():
            if isinstance(child, Button):
                child.config(state=NORMAL)

        self.master.bind("<KeyPress>", self.move)

    #Метод для выхода с уровня, должен быть переопределен в дочерних классах
    def exit_level(self):
        pass

    #Метод для движения, должен быть переопределен в дочерних классах
    def move(self, event):
        pass

    #Метод для проверки победы, должен быть переопределен в дочерних классах
    def win_check(self):
        pass


class Level1(Basic_lvl):
    def __init__(self, master):
        super().__init__(master)
        self.x1 = 150
        self.y1 = 150

        self.pers = self.canvas.create_image(self.x1, self.y1, image=self.pers_image, anchor='nw')

        # Создание статических объектов (стен)
        wall_positions = [
            (0, 0), (50, 0), (100, 0), (150, 0), (200, 0), (250, 0), (300, 0), (350, 0),
            (0, 50), (0, 100), (0, 150), (0, 200), (0, 250), (0, 300), (0, 350),
            (350, 50), (350, 100), (350, 150), (350, 200), (350, 250), (350, 300), (350, 350),
            (50, 350), (100, 350), (150, 350), (200, 350), (250, 350), (300, 350), (250, 300),
            (250, 250), (250, 200), (250, 150), (150, 50), (100, 50), (50, 50), (50, 100)
        ]

        for x, y in wall_positions:
            obj = self.canvas.create_image(x, y, image=self.static_obj_t, anchor='nw')
            self.static_objects.append(obj)

        # Создание подвижных объектов
        self.move_object1 = self.canvas.create_image(200, 150, image=self.move_obj_t, anchor='nw')
        self.move_object2 = self.canvas.create_image(100, 200, image=self.move_obj_t, anchor='nw')
        self.move_object3 = self.canvas.create_image(100, 250, image=self.move_obj_t, anchor='nw')

        # Позиции для ящиков (целевые точки)
        self.position1 = self.canvas.create_rectangle(50, 150, 100, 200, dash=2)
        self.position2 = self.canvas.create_rectangle(50, 250, 100, 300, dash=2)
        self.position3 = self.canvas.create_rectangle(300, 300, 350, 350, dash=2)

    def exit_level(self):
        exit_level1()

    def win_check(self):
        if self.level_completed:
            return

        # Получаем координаты всех ящиков и позиций
        boxes = [
            self.canvas.coords(self.move_object1),
            self.canvas.coords(self.move_object2),
            self.canvas.coords(self.move_object3)
        ]

        positions = [
            self.canvas.coords(self.position1),
            self.canvas.coords(self.position2),
            self.canvas.coords(self.position3)
        ]

        # Проверяем, находится ли каждый ящик на какой-либо позиции
        boxes_on_spot = [False] * 3

        for i, box in enumerate(boxes):
            box_x, box_y = box[0], box[1]
            for pos in positions:
                pos_x, pos_y = pos[0], pos[1]
                if abs(box_x - pos_x) < 5 and abs(box_y - pos_y) < 5:
                    boxes_on_spot[i] = True
                    break

        # Если все три ящика на своих местах
        if all(boxes_on_spot):
            self.level_completed = True
            self.show_win_window(1, nick_level1)

    def move(self, event):
        global nick_level1
        if nick_level1 is None or nick_level1 == "":
            messagebox.showwarning('Внимание', 'Введите сначала никнейм!')
            return

        dx, dy = 0, 0
        if event.keysym == 'Left':
            dx = -50
        elif event.keysym == 'Right':
            dx = 50
        elif event.keysym == 'Up':
            dy = -50
        elif event.keysym == 'Down':
            dy = 50

        # Новая позиция игрока
        x, y = self.canvas.coords(self.pers)
        new_x = x + dx
        new_y = y + dy

        # Проверяем столкновение со стенами
        if self.check_collision(new_x, new_y, new_x + 50, new_y + 50):
            return

        # Проверяем возможность движения ящиков
        moved_boxes = []
        boxes = [self.move_object1, self.move_object2, self.move_object3]

        for box in boxes:
            box_x, box_y = self.canvas.coords(box)[:2]
            if abs(box_x - new_x) < 5 and abs(box_y - new_y) < 5:
                new_box_x = box_x + dx
                new_box_y = box_y + dy

                if (not self.check_collision(new_box_x, new_box_y, new_box_x + 50, new_box_y + 50) and
                        not self.check_box_collision(box, new_box_x, new_box_y, boxes)):
                    self.canvas.move(box, dx, dy)
                    if dx != 0 or dy != 0:
                        play_pushing_box()
                    moved_boxes.append(box)
                else:
                    return

        # Двигаем персонажа и одновременно воспроизводим звук
        self.canvas.move(self.pers, dx, dy)
        if dx != 0 or dy != 0:
            play_step_sound()
            self.steps += 1
            self.steps_label.config(text=f"{self.steps}")

        self.win_check()

    def replace(self):
        super().replace()
        # Сброс позиции персонажа
        self.canvas.coords(self.pers, self.x1, self.y1)

        # Сброс позиций ящиков
        self.canvas.coords(self.move_object1, 200, 150)
        self.canvas.coords(self.move_object2, 100, 200)
        self.canvas.coords(self.move_object3, 100, 250)


class Level2(Basic_lvl):
    def __init__(self, master):
        super().__init__(master)
        self.x1 = 150
        self.y1 = 150

        self.pers = self.canvas.create_image(self.x1, self.y1, image=self.pers_image, anchor='nw')

        wall_positions = [(0, 0), (50, 0), (100, 0), (150, 0), (200, 0),
                          (250, 0), (300, 0), (350, 0), (350, 50), (350, 100),
                          (350, 150), (350, 200), (350, 250), (350, 300), (350, 350),
                          (250, 350), (300, 350), (150, 350), (200, 350), (50, 350),
                          (100, 350), (0, 350), (0, 300), (0, 250), (0, 200), (0, 150),
                          (0, 100), (0, 50), (150, 50), (200, 50), (250, 50), (300, 50),
                          (200, 150), (200, 200), (150, 200), (250, 300), (300, 300)]

        for x, y in wall_positions:
            obj = self.canvas.create_image(x, y, image=self.static_obj_t, anchor='nw')
            self.static_objects.append(obj)

        self.move_block1 = self.canvas.create_image(150, 100, image=self.move_obj_t, anchor='nw')
        self.move_block2 = self.canvas.create_image(250, 150, image=self.move_obj_t, anchor='nw')
        self.move_block3 = self.canvas.create_image(100, 150, image=self.move_obj_t, anchor='nw')
        self.move_block4 = self.canvas.create_image(150, 250, image=self.move_obj_t, anchor='nw')

        self.position1 = self.canvas.create_rectangle(300, 100, 350, 150, outline='#464645', dash=2)
        self.position2 = self.canvas.create_rectangle(50, 50, 100, 100, outline='#464645', dash=2)
        self.position3 = self.canvas.create_rectangle(250, 100, 300, 150, outline='#464645', dash=2)
        self.position4 = self.canvas.create_rectangle(150, 300, 200, 350, outline='#464645', dash=2)

    def exit_level(self):
        exit_level2()

    def win_check(self):
        if self.level_completed:
            return
        # Получаем координаты всех позиций для ящиков
        positions = [
            self.canvas.coords(self.position1),
            self.canvas.coords(self.position2),
            self.canvas.coords(self.position3),
            self.canvas.coords(self.position4)
        ]

        # Получаем координаты всех ящиков
        boxes = [
            self.canvas.coords(self.move_block1),
            self.canvas.coords(self.move_block2),
            self.canvas.coords(self.move_block3),
            self.canvas.coords(self.move_block4)
        ]

        boxes_on_spot = [False] * 4

        for i, box in enumerate(boxes):
            box_x, box_y = box[0], box[1]
            for pos in positions:
                pos_x, pos_y = pos[0], pos[1]
                if abs(box_x - pos_x) < 5 and abs(box_y - pos_y) < 5:
                    boxes_on_spot[i] = True
                    break

        # Если все 4 ящика на своих местах
        if all(boxes_on_spot):
            self.level_completed = True
            self.show_win_window(2, nick_level2)

    def move(self, event):
        global nick_level2
        if nick_level2 is None or nick_level2 == "":
            messagebox.showwarning('Внимание', 'Введите сначала никнейм!')
            return
        dx, dy = 0, 0
        if event.keysym == 'Left':
            dx = -50
        elif event.keysym == 'Right':
            dx = 50
        elif event.keysym == 'Up':
            dy = -50
        elif event.keysym == 'Down':
            dy = 50

        # Новая позиция игрока
        x, y = self.canvas.coords(self.pers)
        new_x = x + dx
        new_y = y + dy

        # Проверяем столкновение со стенами
        if self.check_collision(new_x, new_y, new_x + 50, new_y + 50):
            return

        moved_boxes = []
        boxes = [self.move_block1, self.move_block2, self.move_block3, self.move_block4]

        for box in boxes:
            box_x, box_y = self.canvas.coords(box)[:2]
            if abs(box_x - new_x) < 5 and abs(box_y - new_y) < 5:
                new_box_x = box_x + dx
                new_box_y = box_y + dy

                # Проверяем, может ли ящик двигаться
                if (not self.check_collision(new_box_x, new_box_y, new_box_x + 50, new_box_y + 50) and
                        not self.check_box_collision(box, new_box_x, new_box_y, boxes)):
                    self.canvas.move(box, dx, dy)
                    moved_boxes.append(box)
                    if dx != 0 or dy != 0:
                        play_pushing_box()
                else:
                    return  # Не можем двигать ящик, значит и персонаж не двигается

        # Двигаем персонажа
        self.canvas.move(self.pers, dx, dy)
        if dx != 0 or dy != 0:
            play_step_sound()
            self.steps += 1
            self.steps_label.config(text=f"{self.steps}")

        self.win_check()

    def replace(self):
        super().replace()
        # Сброс позиции персонажа
        self.canvas.coords(self.pers, self.x1, self.y1)

        # Сброс позиций ящиков
        self.canvas.coords(self.move_block1, 150, 100)
        self.canvas.coords(self.move_block2, 250, 150)
        self.canvas.coords(self.move_block3, 100, 150)
        self.canvas.coords(self.move_block4, 150, 250)


class Level3(Basic_lvl):
    def __init__(self, master):
        super().__init__(master)
        self.x1 = 50
        self.y1 = 50

        self.pers = self.canvas.create_image(self.x1, self.y1, image=self.pers_image, anchor='nw')

        wall_positions = [(0, 0), (50, 0), (100, 0), (150, 0), (200, 0),
                          (250, 0), (300, 0), (350, 0), (350, 50), (350, 100),
                          (350, 150), (350, 200), (350, 250), (350, 300), (350, 350),
                          (250, 350), (300, 350), (150, 350), (200, 350), (50, 350),
                          (100, 350), (0, 350), (0, 300), (0, 250), (0, 200), (0, 150),
                          (0, 100), (0, 50), (0, 100), (100, 300), (100, 250)]

        for x, y in wall_positions:
            obj = self.canvas.create_image(x, y, image=self.static_obj_t, anchor='nw')
            self.static_objects.append(obj)

        self.move_block1 = self.canvas.create_image(100, 100, image=self.move_obj_t, anchor='nw')
        self.move_block2 = self.canvas.create_image(100, 150, image=self.move_obj_t, anchor='nw')
        self.move_block3 = self.canvas.create_image(150, 100, image=self.move_obj_t, anchor='nw')
        self.move_block4 = self.canvas.create_image(200, 200, image=self.move_obj_t, anchor='nw')
        self.move_block5 = self.canvas.create_image(200, 250, image=self.move_obj_t, anchor='nw')
        self.move_block6 = self.canvas.create_image(250, 250, image=self.move_obj_t, anchor='nw')

        self.position1 = self.canvas.create_rectangle(50, 300, 100, 350, outline='#464645', dash=2)
        self.position2 = self.canvas.create_rectangle(150, 150, 200, 200, outline='#464645', dash=2)
        self.position3 = self.canvas.create_rectangle(200, 150, 250, 200, outline='#464645', dash=2)
        self.position4 = self.canvas.create_rectangle(150, 300, 200, 350, outline='#464645', dash=2)
        self.position5 = self.canvas.create_rectangle(300, 200, 350, 250, outline='#464645', dash=2)
        self.position6 = self.canvas.create_rectangle(300, 250, 350, 300, outline='#464645', dash=2)

    def exit_level(self):
        exit_lvl3()

    def win_check(self):
        if self.level_completed:
            return
        # Получаем координаты всех позиций для ящиков
        positions = [
            self.canvas.coords(self.position1),
            self.canvas.coords(self.position2),
            self.canvas.coords(self.position3),
            self.canvas.coords(self.position4),
            self.canvas.coords(self.position5),
            self.canvas.coords(self.position6)
        ]

        # Получаем координаты всех ящиков
        boxes = [
            self.canvas.coords(self.move_block1),
            self.canvas.coords(self.move_block2),
            self.canvas.coords(self.move_block3),
            self.canvas.coords(self.move_block4),
            self.canvas.coords(self.move_block5),
            self.canvas.coords(self.move_block6)
        ]

        # Проверяем, сколько ящиков находятся на своих местах
        correct_boxes = 0

        for box in boxes:
            box_x, box_y = box[0], box[1]
            for pos in positions:
                pos_x, pos_y = pos[0], pos[1]
                if abs(box_x - pos_x) < 5 and abs(box_y - pos_y) < 5:
                    correct_boxes += 1
                    break

        # Если все 6 ящиков на своих местах
        if correct_boxes == 6:
            self.level_completed = True
            self.show_win_window(3, nick_level3)

    def move(self, event):
        global nick_level3
        if nick_level3 is None or nick_level3 == "":
            messagebox.showwarning('Внимание', 'Введите сначала никнейм!')
            return
        dx, dy = 0, 0
        if event.keysym == 'Left':
            dx = -50
        elif event.keysym == 'Right':
            dx = 50
        elif event.keysym == 'Up':
            dy = -50
        elif event.keysym == 'Down':
            dy = 50

        # Новая позиция игрока
        x, y = self.canvas.coords(self.pers)
        new_x = x + dx
        new_y = y + dy

        # Проверяем столкновение со стенами
        if self.check_collision(new_x, new_y, new_x + 50, new_y + 50):
            return

        moved_boxes = []
        boxes = [self.move_block1, self.move_block2, self.move_block3,
                 self.move_block4, self.move_block5, self.move_block6]

        for box in boxes:
            box_x, box_y = self.canvas.coords(box)[:2]
            if abs(box_x - new_x) < 5 and abs(box_y - new_y) < 5:
                new_box_x = box_x + dx
                new_box_y = box_y + dy

                # Проверяем, может ли ящик двигаться
                if (not self.check_collision(new_box_x, new_box_y, new_box_x + 50, new_box_y + 50) and
                        not self.check_box_collision(box, new_box_x, new_box_y, boxes)):
                    self.canvas.move(box, dx, dy)
                    if dx != 0 or dy != 0:
                        play_pushing_box()
                    moved_boxes.append(box)
                else:
                    return  # Не можем двигать ящик, значит и персонаж не двигается

        # Двигаем персонажа
        self.canvas.move(self.pers, dx, dy)
        if dx != 0 or dy != 0:
            play_step_sound()
            self.steps += 1
            self.steps_label.config(text=f"{self.steps}")

        self.win_check()

    def replace(self):
        super().replace()
        # Сброс позиции персонажа
        self.canvas.coords(self.pers, self.x1, self.y1)

        # Сброс позиций ящиков
        self.canvas.coords(self.move_block1, 100, 100)
        self.canvas.coords(self.move_block2, 100, 150)
        self.canvas.coords(self.move_block3, 150, 100)
        self.canvas.coords(self.move_block4, 200, 200)
        self.canvas.coords(self.move_block5, 200, 250)
        self.canvas.coords(self.move_block6, 250, 250)

# Уровень 1
lvl1 = Toplevel()
lvl1.title('SOKOBAN')
lvl1.geometry('1000x700+230+20')
lvl1.configure(bg='#d8e6de')
lvl1.resizable(False, False)

Label(lvl1, text='Уровень 1',
      font=('Arial', 24),
      background='#d8e6de',
      foreground='#000000').place(x=50, y=110)

nick_label1 = Label(lvl1, text='Игрок: ',
                   font=('Arial', 24),
                   background='#cc5b3f',
                   foreground='#000000')
nick_label1.place(x=700, y=150)

# Уровень 2
lvl2 = Toplevel()
lvl2.title('SOKOBAN')
lvl2.geometry('1000x700+230+20')
lvl2.configure(bg='#d8e6de')
lvl2.resizable(False, False)

Label(lvl2, text='Уровень 2',
      font=('Arial', 24),
      background='#d8e6de',
      foreground='#000000').place(x=50, y=110)

nick_label2 = Label(lvl2, text='Игрок: ',
                   font=('Arial', 24),
                   background='#cc5b3f',
                   foreground='#000000')
nick_label2.place(x=700, y=150)

# Уровень 3
lvl3 = Toplevel()
lvl3.title('SOKOBAN')
lvl3.geometry('1000x700+230+20')
lvl3.configure(bg='#d8e6de')
lvl3.resizable(False, False)
Label(lvl3, text='Уровень 3',
      font=('Arial', 24),
      background='#d8e6de',
      foreground='#000000').place(x=50, y=110)

nick_label3 = Label(lvl3, text='Игрок: ',
                   font=('Arial', 24),
                   background='#cc5b3f',
                   foreground='#000000')
nick_label3.place(x=700, y=150)

app1 = Level1(lvl1)
app2 = Level2(lvl2)
app3 = Level3(lvl3)

# Скрытие всех окон кроме главного
nick_root = Toplevel()
nick_root.withdraw()
lvl3.withdraw()
lvl2.withdraw()
lvl1.withdraw()
game_root.withdraw()
rules_root.withdraw()
records_root.withdraw()
main_root.mainloop()