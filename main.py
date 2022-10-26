# Библиотеки математики
import matplotlib.pyplot as plt
# Библиотека для создания приложения
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar, Combobox
from tkinter import messagebox
# Библиотека для считывания таблиц
import pandas as pd
# Библиотека для нахождения директории файла
from tkinter import filedialog as fd
# Импорт для изображения
from PIL import Image, ImageTk
# Для машинного эпсилона
import sys
# Для удаления файла
import os
import math as m

# Основное окно
def main():

    # основа
    root = Tk()
    root.title("Интерполяция")
    root.geometry(f'{int(root.winfo_screenwidth() * 0.8)}x{int(root.winfo_screenheight() * 0.8)}')
    root.resizable(width=False, height=False)

    # определение оптимальных размеров
    size_screen = root.winfo_screenheight() * 0.8
    size_font = int(size_screen / 95)
    font_lower = f"family {size_font}"

    # необходимые функции

    # вывод ошибки
    def mistake(x="неизвестная ошибка"):
        messagebox.showwarning(title="Ошибка", message=f'Возникла ошибка: {x}.')

    # считывание директории
    def direction():
        name = fd.askopenfilename()
        direct.delete(0, END)
        direct.insert(0, name)

    # считывание таблицы
    def read_xlsx(name):
        try:
            excel_data_df = pd.read_excel(name, sheet_name='точки')
            try:
                x, y = excel_data_df['x'].tolist(), excel_data_df['y'].tolist()
                try:
                    x = [float(i) for i in x]
                    y = [float(i) for i in y]
                    return x, y
                except:
                    mistake(x=f"неверный тип данных")
                    return wrong
            except:
                mistake(x=f"неверное наименование или расположение столбцов данных")
                return wrong
        except:
            mistake(x='в таблице не нашлось необходимого листа')
            return wrong

    # считывание текстового файла
    def read_txt(name):
        x = []
        y = []
        f = open(name, "r")
        try:
            for i in f:
                x_i, y_i = i.split()
                x.append(float(x_i))
                y.append(float(y_i))
            return x, y
        except:
            mistake(x='ошибка считывания данных')
            return wrong

    # считывание файлов и определение типа
    def read_file():
        name_file = direct.get()
        expansion = name_file.split(".")[-1].lower()
        if not(expansion in ["txt", "xlsx"]):
            mistake(x="директория или формат файла не соответствует требованиям")
            return wrong
        else:
            if expansion == "txt":
                x, y = read_txt(name_file)
            else:
                x, y = read_xlsx(name_file)

            return x, y

    # создание таблицы
    def create_table():

        global table

        frame = Frame(canvas)
        frame.place(relx=0.075, rely=0.4)

        table = Treeview(frame)
        table["columns"] = ("i", "X", "Y")

        scroll = Scrollbar(frame)
        scroll.config(command=table.yview)
        scroll.pack(side=RIGHT, fill=Y)

        table.column("#0", width=0, stretch=NO)
        table.column("i", anchor=CENTER, width=40)
        table.column("X", anchor=CENTER, width=80)
        table.column("Y", anchor=CENTER, width=80)

        table.heading("#0", text="", anchor=CENTER)
        table.heading("i", text="i", anchor=CENTER)
        table.heading("X", text="X", anchor=CENTER)
        table.heading("Y", text="Y", anchor=CENTER)

    # очистка таблицы
    def clear_table():
        for i in table.get_children():
            table.delete(i)

    # сортировка таблиц + удаление повторяющихся элементов
    def sort_table():

        global x_basic
        global y_basic

        x_basic = ([float((table.set(k, "X"))) for k in table.get_children('')])
        y_basic = ([float((table.set(k, "Y"))) for k in table.get_children('')])
        # print(x_basic)
        # print(y_basic)
        d = {x_basic[i]: y_basic[i] for i in range(len(x_basic))}

        sorted_tuple = sorted(d.items(), key=lambda x: x[0])

        d = dict(sorted_tuple)
        # print(d)

        clear_table()

        cnt = 1
        for index in d:
            table.insert(parent='', index='end', text='', values=(f'{cnt}', f'{index}', f'{d[index]}'))
            cnt += 1
        x_basic = [i for i in d.keys()]
        y_basic = [d[i] for i in d.keys()]
        # print(y_basic)
        # print(x_basic)

    # отлов ошибок ручного ввода
    def check_input():
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            input_record()
        except:
            mistake(x="неверно введены точки")

    # занесение данных в таблицу
    def input_record():

        global count
        # global x_element
        # global y_element

        count += 1
        # table.insert(parent='', index='end', text='', values=(i_entry.get(), x_entry.get(), y_entry.get()))
        table.insert(parent='', index='end', text='', values=(count, x_entry.get(), y_entry.get()))

        # sort_table()

        # i_entry.delete(0, END)

        x_entry.delete(0, END)
        y_entry.delete(0, END)

        sort_table()

    # ручной ввод
    def write():

        Label(canvas, text="Введите данные ниже:", font=font_lower).place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.05)
        create_table()
        table.pack()

        global Input_frame

        Input_frame = Frame(canvas)
        Input_frame.place(relx=0.05, rely=0.7)

        # i_element = Label(Input_frame, text="i")
        # i_element.grid(row=0, column=0)

        global x_entry
        global y_entry

        x_element = Label(Input_frame, text="X")
        x_element.grid(row=0, column=1)

        y_element = Label(Input_frame, text="Y")
        y_element.grid(row=0, column=2)

        # i_entry = Entry(Input_frame)
        # i_entry.grid(row=1, column=0)

        x_entry = Entry(Input_frame)
        x_entry.grid(row=1, column=1)

        y_entry = Entry(Input_frame)
        y_entry.grid(row=1, column=2)

        global count
        count = 0

        global btn_add
        global btn_clear

        btn_add = Button(canvas, text="Внести точку", command=check_input, font=font_lower)
        btn_add.place(relx=0.05, rely=0.8, relwidth=0.09, relheight=0.05)

        btn_clear = Button(canvas, text="Очистить таблицу", command=clear_table, font=font_lower)
        btn_clear.place(relx=0.15, rely=0.8, relwidth=0.09, relheight=0.05)

    # считывание и отображение
    def read():

        try:
            btn_add.destroy()
            btn_clear.destroy()
            Input_frame.destroy()
        except:
            pass

        x, y = read_file()

        if x == None or y == None:
            pass
        else:

            Label(canvas, text="Считанные данные представлены ниже:", font=font_lower).place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.05)

            # Button(canvas, text="Построить график", command=graph, font=font_lower).place(relx=0.05, rely=0.9, relwidth=0.09, relheight=0.05)

            create_table()

            for i in range(len(x)):
                table.insert(parent='', index='end', text='', values=(f'{i + 1}', f'{x[i]}', f'{y[i]}'))

            sort_table()

            table.pack()

            # print(x)
            # print(y)
            # frame = Frame(canvas, width=220)
            # frame.place(relx=0.05, rely=0.35, relheight=0.4)
            # data = Canvas(frame, bg="cornsilk")
            # data.place(relx=0, rely=0, relheight=1, relwidth=1)

            # w = 15
            # Label(data, text="X", font=font_lower, relief="sunken", width=w).grid(column=0, row=0)
            # Label(data, text="Y", font=font_lower, relief="sunken", width=w).grid(column=1, row=0)
            #
            # for index in range(len(x)):
            #     Label(data, text=f"{x[index]}", font=font_lower, relief="sunken", width=w).grid(column=0, row=index + 1)
            #     Label(data, text=f"{y[index]}", font=font_lower, relief="sunken", width=w).grid(column=1, row=index + 1)

            # scroll_bar = Scrollbar(frame, orient="vertical", command=data.yview)
            # scroll_bar.grid(row=0, column=1, sticky=NS)
            # data.configure(yscrollcommand=scroll_bar.set)

            # frame.config(width=2 + scroll_bar.winfo_width())

    # округление до заданного знака
    def round_to(x):
        return round(x, 5)

    # создание новой таблицы для результатов (правая часть)
    def create_table_res():

        global table_res

        frame = Frame(canvas)
        frame.place(relx=0.75, rely=0.4)

        table_res = Treeview(frame)
        table_res["columns"] = ("n", "Y*", "Y* - Y")

        scroll = Scrollbar(frame)
        scroll.config(command=table_res.yview)
        scroll.pack(side=RIGHT, fill=Y)

        table_res.column("#0", width=0, stretch=NO)
        table_res.column("n", anchor=CENTER, width=40)
        table_res.column("Y*", anchor=CENTER, width=80)
        table_res.column("Y* - Y", anchor=CENTER, width=80)

        table_res.heading("#0", text="", anchor=CENTER)
        table_res.heading("n", text="n", anchor=CENTER)
        table_res.heading("Y*", text="Y*", anchor=CENTER)
        table_res.heading("Y* - Y", text="|Y* - Y|", anchor=CENTER)

        try:
            mist = "неверно введены данные для рассчитываемой функции"
            entry_func = str(fun_entry.get())

            def f(x):
                result = eval(entry_func)
                return result
        except:
            mistake(x=mist)
            return

        y = f(x_lag)
        for i in range(len(y_ans)):

            table_res.insert(parent='', index='end', text='', values=(i + 1, y_ans[i], round_to(abs(y - y_ans[i]))))
            # print(i + 1, y_ans[i], y)

        sort_table()

    # отображение точек на графике
    def graph():
        plt.plot(x_basic, y_basic, f"{line_colour[colour1]}o", label="Исходные точки")
        plt.plot(x_lag, y_lag, f"{line_colour[colour2]}o", label="Лагранж")
        # plt.plot(points_lagr_x, points_lagr_y, f"c^", label="Узловые точки", markersize=15)

    # создание графика
    def graph_create():

        try:
            global frame_graph

            frame_graph.destroy()

            frame_graph = Canvas(canvas, bg=main_colour)
            frame_graph.place(relx=0.3, rely=0.4, width=width_graph, height=height_graph)

        except:
            pass

        global colour1
        global colour2

        colour1 = choiceVar1.get()
        colour2 = choiceVar2.get()

        while colour1 == colour2:
            messagebox.showwarning("Внимание!", "Одинаковый цвет исходных и полученных точек может "
                                                "помешать реальному восприятию. Цвет поменян.")

            var_colour = [i for i in range(len(line_colour))]
            i = 2
            while colour1 == colour2:
                i -= 1
                colour1 = choiceVar1.get()
                combo_box_2.current(var_colour[i])
                colour2 = choiceVar2.get()
                # print(colour1, colour2, colour1 == colour2)

            combo_box_2.current(var_colour[i])

        try:
            os.remove("saved_figure.png")
        except:
            pass

        plt.figure()

    # отображение графика
    def graph_save(f=False):

        plt.xlabel("Ось X")
        plt.ylabel("Ось Y")
        # plt.legend()
        plt.savefig(f'saved_figure.png')

        img = Image.open(f'saved_figure.png')
        img = img.resize((width_graph, height_graph))
        img = ImageTk.PhotoImage(img)

        picture = Label(frame_graph, image=img)
        picture.grid(column=0, row=0)

        #print(choiceVar1.get(), choiceVar2.get())

    # функция интерполяции (расчет)
    def interpolation_res(x, y, r):

        # print(f"x = {x}")
        # print(f"y = {y}")
        # print()

        sum_lagr = 0

        for i in range(len(x)):
            ans_above = y[i]
            ans_under = 1
            for j in range(len(x)):
                if i == j:
                    continue
                ans_above *= (r - x[j])
                ans_under *= (x[i] - x[j])
            sum_lagr += ans_above / ans_under

        # print(sum_lagr)
        return sum_lagr

    # функция интерполяции (формальная часть)
    def interpolation():

        try:
            m_eps = sys.float_info.epsilon
            raznica = round_to(x_basic[0] - x_basic[1])
            for i in range(len(x_basic) - 1):
                if round_to(x_basic[i] - x_basic[i + 1]) < raznica * (1 + m_eps):
                    # print(x_basic[i] - x_basic[i + 1])
                    # print(x_basic[i], x_basic[i + 1])
                    # print(raznica)
                    mistake(x=f"точки по оси Х не равноудалены i = {i + 1, i + 2}")
                    return
        except:
            pass

        # x_test = x_basic

        #print(x_basic)

        try:
            x_check = x_basic
        except:
            mistake(x="нет данных")
            return

        #
        # file_result.write("\n\nКонечные разности:\n")
        #
        # # print(x_basic, 1)
        # # print(y_basic, 2)
        #
        # a = [y_basic]
        #
        # t = a[-1][:]
        # b = []
        # for i in range(len(t) - 1):
        #     b.append(t[i] - t[i + 1])
        # a.append(b)
        #
        # while len(a[-1]) != 1:
        #     t = a[-1][:]
        #     b = []
        #     for i in range(len(a[-1]) - 1):
        #         t = a[-1]
        #         b.append(t[i + 1] - t[i])
        #     a.append(b)
        #
        # #print(*a, sep='\n')
        #
        # file_result.write(f"\nY              ")
        # for i in range(len(x_basic) - 1):
        #     file_result.write(f"{str(i + 1):15s}")
        #
        # file_result.write(f"\n\n")
        #
        # dif_min = [min(i) for i in a]
        # dif_max = [max(i) for i in a]
        #
        # for i in range(len(a)):
        #     file_result.write(f"{str(round_to(y_basic[i])):15s}")
        #     for j in range(len(a[0])):
        #         try:
        #             file_result.write(f"{str(round_to(a[j + 1][i])):15s}")
        #         except:
        #             pass
        #     file_result.write("\n\n")
        #
        # file_result.write(f"\nmin            ")
        #
        # for i in dif_min[1:-1]:
        #     # print(i)
        #     file_result.write(f"{str(round_to(i)):15s}")
        # file_result.write("\n")
        #
        # file_result.write(f"\nmax            ")
        #
        # for i in dif_max[1:-1]:
        #     # print(i)
        #     file_result.write(f"{str(round_to(i)):15s}")
        # file_result.write("\n")
        #
        # file_result.write(f"\ndif            ")
        #
        # dif = []
        #
        # for i in range(len(dif_max[1:-1])):
        #     dif.append(dif_max[i + 1] - dif_min[i + 1])
        #     # print(i)
        #     file_result.write(f"{str(round_to(dif[i])):15s}")
        # file_result.write("\n")
        #
        # normal_value = dif.index(min(dif)) + 1
        #
        # file_result.write(f"\nОптимальная степень полинома: {normal_value}\n")
        #
        # file_result.write(f"\nДля составления интерполяционного полинома Лагранжа {normal_value} степени "
        #                   f"будет использованы следующие точки:\n\n")
        #



        global points_lagr_x
        global points_lagr_y
        global x_lag
        global y_lag
        global y_ans
        global mat_func

        y_ans = []

        try:
            x_lag = float(point_entry.get())
        except:
            mistake(x="неверно введены данные для интерполируемой точки")
            return

        mist = "функция неопределена"
        entry_func = str(fun_entry.get())

        if entry_func == "":
            mistake(x=mist)
            return

        graph_create()

        # for normal_value in range(5, ):
        for n in range(1, len(x_basic)):

            normal_value = n + 1

            h = len(x_basic) / normal_value

            a = x_basic[:]
            b = []
            b.append(a[0])

            for i in range(n - 2):
                b.append(a[int(i * h + round(h))])
                # print(b)

            if n != 1:
                b.append(a[-1])

            # print(normal_value - 1, "h =", h)
            points_lagr_x = x_basic[::round(h)]
            points_lagr_x = b[:]
            #
            #
            # for i in range(normal_value + 1):
            #     points_lagr_x.append(x_basic[round(h * i)])

            points_lagr_y = [y_basic[x_basic.index(i)] for i in points_lagr_x]

            print(points_lagr_x, len(points_lagr_x))
            print(points_lagr_y, len(points_lagr_y))


            #
            # file_result.write(f"\n{'X':15s}{'Y':15s}\n\n")
            # for i in range(len(points_lagr_x)):
            #     file_result.write(f"\n{str(points_lagr_x[i]):15s}{str(points_lagr_y[i]):15s}\n")

            # print(points_lagr_x, "x")
            # print(points_lagr_y, "y")
            # print(points_lagr_y[0])


            #
            # func_global = ''
            # for i in range(len(points_lagr_x)):
            #     func = f"({points_lagr_y[i]} * "
            #     for j in range(len(points_lagr_x)):
            #         if i != j:
            #             func += f"(x - ({points_lagr_x[j]}))"
            #     func += " / ("
            #     for j in range(len(points_lagr_x)):
            #         if i != j:
            #             func += f"({points_lagr_x[i]} - ({points_lagr_x[j]}))"
            #     func += ")) + "
            #     func_global += func
            #
            # func = func_global.replace(")(", ") * (")[:-4] + ")"




            # for i in range(len(points_lagr_x)):
            #     func = f"({points_lagr_y[i]} * "
            #     for j in range(len(points_lagr_x)):
            #         if i != j:
            #             func += f"(x - ({points_lagr_x[j]}))"
            #     func += " / ("
            #     for j in range(len(points_lagr_x)):
            #         if i != j:
            #             func += f"({points_lagr_x[i]} - ({points_lagr_x[j]}))"
            #     func += ")) + "
            #     func_global += func


            # file_result.write(f"Получившийся полином: {func}\n\n")

            # print(func.count("("))
            #
            # print(func.count(")"))
            #
            # print(func, normal_value)


            # print(-2)



            # print(f(-2.2))
            # print(-1)
            # x_lag = x_basic[:]
            # y_lag = []
            # print(-1)
            # print("x =", x_lag)

            # x_lag = 0

            try:
                y_lag = interpolation_res(points_lagr_x, points_lagr_y, x_lag)
                y_ans.append(y_lag)
            except:
                mistake(x="данные не определены")
                return



            # print(y_ans)

            # for i in x_lag:
            #     # print("y =", y_lag)
            #     y_lag.append(round_to(f(i)))


            # print(x_lag)
            # print(y_lag)
            # print(1)

            graph()

            # graph()
            # graph()
            # print(2)

            create_table_res()

            # print(3)

            table_res.pack()

            # print(4)
        graph_save()

        file_result.write("------------------------------\n")
        file_result.write(f"\n\ni              ")
        for i in range(len(x_basic)):
            file_result.write(f"{str(i + 1):30s}")

        file_result.write(f"\n\nx              ")
        for i in x_basic:
            file_result.write(f"{str(i):30s}")

        file_result.write(f"\n\ny              ")
        for i in y_basic:
            file_result.write(f"{str(i):30s}")

        file_result.write(f"\n\ny*             ")
        for i in y_ans:
            file_result.write(f"{str(i):30s}")
        # except:
        #     mistake(x=f"неверный ввод параметров")

    # создание фона
    canvas = Canvas(root, background=main_colour)
    canvas.place(rely=0.02, relx=0.02, relheight=0.96, relwidth=0.96)

    # создание интерфейса
    txt = Label(canvas, text="Задайте путь файла с расширением .txt или .xlsx,\nгде находятся необходимые значения", font=font_lower)
    txt.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.05)

    # путь файла
    direct = Entry(canvas, font=font_lower)
    direct.place(relx=0.3, rely=0.05, relwidth=0.5, relheight=0.05)

    direct.insert(0, "C:/Users/Egor/Desktop/Учеба/4 семестр/Технологии программирования/Курсовая работа/test.xlsx")

    # найти файл
    btn = Button(canvas, text='Найти файл', command=direction, font=font_lower)
    btn.place(relx=0.85, rely=0.05, relwidth=0.1, relheight=0.05)

    # кнопка, открывающая инструкцию
    btn = Button(canvas, text='Инструкция пользования программой', command=rules, font=font_lower)
    btn.place(relx=0.05, rely=0.15, relwidth=0.2, relheight=0.05)

    # считывание файла
    btn = Button(canvas, text='Считать данные с файла', command=read, font=font_lower, background="lawngreen")
    btn.place(relx=0.3, rely=0.15, relwidth=0.5, relheight=0.05)

    # ввод значений вручную
    btn = Button(canvas, text='Ввести вручную', command=write, font=font_lower)
    btn.place(relx=0.85, rely=0.15, relwidth=0.1, relheight=0.05)

    # поле для интерполируемой точки
    Label(canvas, text="Укажите рассчитываемую точку:", font=font_lower).place(relx=0.05, rely=0.9, relwidth=0.15, relheight=0.05)
    point_entry = Entry(canvas, font=font_lower)
    point_entry.insert(0, "0")
    point_entry.place(relx=0.25, rely=0.9, relwidth=0.05, relheight=0.05)

    # поле для математической функции
    Label(canvas, text="Укажите рассчитываемую функцию:", font=font_lower).place(relx=0.35, rely=0.9, relwidth=0.15, relheight=0.05)
    fun_entry = Entry(canvas, font=font_lower)
    fun_entry.insert(0, "x ** 2")
    fun_entry.place(relx=0.55, rely=0.9, relwidth=0.15, relheight=0.05)

    # кнопка для запуска интерполяции
    btn = Button(canvas, text="Интерполировать и построить график", command=interpolation, font=font_lower, background="lawngreen")
    btn.place(relx=0.75, rely=0.9, relwidth=0.2, relheight=0.05)

    global frame_graph

    # область для графика
    frame_graph = Canvas(canvas, bg=main_colour)
    frame_graph.place(relx=0.3, rely=0.4, width=width_graph, height=height_graph)
    #frame_graph.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.4)

    global choiceVar1
    global choiceVar2

    # блок выбора цвета для точек на графике
    choiceVar1 = StringVar()
    choiceVar2 = StringVar()

    txt = Label(canvas, text="Цвет исходных точек: ", font=font_lower)
    txt.place(relx=0.3, rely=0.3, relwidth=0.15, relheight=0.05)

    global combo_box_1
    global combo_box_2

    combo_box_1 = Combobox(canvas, font=font_lower, values=[i for i in line_colour.keys()], textvariable=choiceVar1, justify=CENTER)
    combo_box_1.current(0)
    combo_box_1.place(relx=0.5, rely=0.3, relwidth=0.1, relheight=0.05)

    txt = Label(canvas, text="Цвет полученных точек: ", font=font_lower)
    txt.place(relx=0.65, rely=0.3, relwidth=0.15, relheight=0.05)

    combo_box_2 = Combobox(canvas, font=font_lower, values=[i for i in line_colour.keys()], textvariable=choiceVar2, justify=CENTER)
    combo_box_2.current(1)
    combo_box_2.place(relx=0.85, rely=0.3, relwidth=0.1, relheight=0.05)

    root.mainloop()

# дополнительное окно инструкции
def rules():
    global root_1
    try:
        if 'normal' == root_1.state():
            pass
        else:
            root_1.mainloop()
    except:
        root_1 = Tk()
        root_1.title("Инструкция")
        root_1.geometry(f'{height_root_1}x{width_root_1}')
        root_1.resizable(width=False, height=False)

        # определение оптимальных размеров
        size_screen = root_1.winfo_screenheight() * 0.8
        size_font = int(size_screen / 95)
        font_lower = f"family {size_font}"

        canvas = Canvas(root_1, background=main_colour)
        canvas.place(rely=0.02, relx=0.02, relheight=0.96, relwidth=0.96)

        global line
        line = 0

        n = 10
        height_label = height_root_1 // n
        height_label_proc = 1 / n

        # ввод правил в окно
        def label_it(x_2, x_3, main_t=False):

            global line
            if main_t:
                bg_t = "lawngreen"
            else:
                bg_t = "lightgray"

            Label(canvas, text=f"{line}", font=font_lower, borderwidth=2, relief="ridge", bg=bg_t).grid(column=0, row=line)
            Label(canvas, text=f"{x_2}", font=font_lower, borderwidth=2, relief="ridge", bg=bg_t).grid(column=1, row=line)
            Label(canvas, text=f"{x_3}", font=font_lower, borderwidth=2, relief="ridge", bg=bg_t).grid(column=2, row=line)
            line += 1

        label_it("Тема", "Комментарий", main_t=True)
        label_it("Порядок действий", '1. Считывание данных (можно бить данные вручную или считать с предложенных файлов);\n'
                                     '2. Выбор параметров для будущего графика;\n'
                                     '3. Построение графика + интерполяция данных;\n'
                                     '4. Получение результата в виде текстового файла и сохраненного графика.')
        label_it("Путь к файлу", "Если нужно достать какой-нибудь файл с ПК, то необходимо прописать полный путь через "
                                 "\"/\". Например:\nC:/Users/Egor/Desktop/Учеба/4 семестр/Технологии программирования/"
                                 "Курсовая работа/test.xlsx")
        label_it("Таблица Excel", 'Если нужно считать данные с файла с расширением .xlsx, то нужно:\n'
                                  '-- Завести отдельный лист с названием "точки". Регистр важен;\n'
                                  '-- В верхней строчке завести два столбца с именами "x" и "y" (англ.);\n'
                                  '-- В каждом столбце указать точки. Обратите внимание, что количество элементов\n'
                                  'обоих столбцов должно быть равно. Также важно помнить, что точки в столбце "x"\n'
                                  'должны быть равноудалены друг от друга.')
        label_it("Текстовый файл", 'Если нужно считать данные с файла с расширением .txt, то нужно:\n'
                                  '-- Через пробел (или табуляцию) на каждой строке написать по 2 значения -- x и y;\n'
                                  '-- Каждая точка должна иметь свою пару;\n'
                                   '-- Каждая точка первого столбика должна быть равноудалена от соседней нижней.\n')
        label_it("Ошибка", 'Просим соблюдать вышеупомянутые инструкции. Если вышла такая ситуация, что возникла\n '
                           'неизвестная ошибка, то просим перезапустить приложение.\n '
                           'Если возникла ситуация, что какая-то кнопка не работает, то просим нажать еще раз. ')


        """

        table = Treeview(frame)
        table["columns"] = ("№", "", "Комментарий")

        scroll = Scrollbar(frame)
        scroll.config(command=table.yview)
        scroll.pack(side=RIGHT, fill=Y)

        table.column("#0", width=0, stretch=NO)
        table.column("№", anchor=CENTER, width=height_root_1 // 5)
        table.column("Тема", anchor=CENTER, width=height_root_1 // 5)
        table.column("Комментарий", anchor=CENTER, width=height_root_1 // 5 * 3 - 10)

        table.heading("#0", text="", anchor=CENTER)
        table.heading("№", text="№", anchor=CENTER)
        table.heading("Тема", text="Тема", anchor=CENTER)
        table.heading("Комментарий", text="Комментарий", anchor=CENTER)

        table.insert(parent='', index='end', text='', values=(1, "", "Если нужно достать какой-нибудь "
                                                                                 "файл с ПК,\n то необходимо прописать "
                                                                                 "полный путь через \"/\". Например:\n"
                                                                                 "C:/Users/Egor/Desktop/Учеба/4 семестр/"
                                                                                 "Технологии программирования/Курсовая "
                                                                                 "работа/test.xlsx"))"""

# дополнительные параметры
main_colour = "honeydew"

wrong = (None, None)

height_graph = 350
width_graph = 600

height_root_1 = 1000
width_root_1 = 600

line_colour = {
    "Красный": "r",
    "Зеленый": "g",
    "Синий": "b",
    "Желтый": "y"
}

file_result = open("result.txt", "w")
file_result.close()

# файл для результатов
file_result = open("result.txt", "a")

# запуск программы
if __name__ == "__main__":
    main()

# файл для результатов
file_result.close()

