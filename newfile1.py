import pandas as pd
import random
from tkinter import * 
from  tkinter import ttk
from functools import partial
import os



def check_file_xls():
     '''
     Функция вытаскивыет название последнего excel файла из папки
     '''
     files = os.listdir()
     files = [file for file in files if ('.xls' in file)]
     
     if len(files)<1:
          return('NaN')

     file = max(files, key=os.path.getctime)
     return(file)
     

def correct_symbols(string):
     '''
     Изменить неккректные символы. Убрать лишние пробелы
     '''
     string = " ".join(string.split())
     string = string.replace('H','Н')
     string = string.replace('a','а')
     string = string.replace('e','е')
     return(string)



#Выбор выгрузки данных
def internet(window,frame):
     '''
     Загрузка файлов игры через гугл таблицы и составление окна с выборлом персонажней
     '''
     #Выгрузка из гугл таблицы
     ##Гугл таблицы
     df_copy = pd.read_csv('https://docs.google.com/spreadsheets/d/1Z6hAlFOlLJa6RBry5vMUHK4jvmIFL0C_Y9Issau2zpY/export?format=csv')

     #Создаем Frame Pack (окно)
     frame.pack_forget()
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     #Создаем начальную запись с персанажами
     text='Загадайте одного из персонажей:\n\n'
     col_pers = list(df_copy.columns)[0]
     for i in range(len(df_copy[col_pers])):
          text = text + str(i+1)+'. '+df_copy[col_pers][i]+'\n'
     #Помщаем нажпись на Frame Pack
     lbl = Label(frame, text= text, justify =LEFT) #отображаем список людей
     lbl.grid(column=0, row=0, padx=10, pady=5)
     #Помещаем кнопку 'начать игру' и переходим к игре (start_game)
     btn3 = Button(frame, text="Начать игру", command=partial(start_game,df_copy,window))  
     btn3.grid(column=0, row=4, padx=10, pady=5)
     
def local(window,frame):
     '''
     Загрузка файлов игры через локальный файл excel в папке и составление окна с выборлом персонажней
     '''
     #Выгрузка из локального файла
     ##Локальный файл
     excel = pd.read_excel(check_file_xls())
     df_copy = pd.DataFrame(excel)
     #Создаем Frame Pack (окно)
     frame.pack_forget()
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     #Создаем начальную запись с персанажами
     text='Загадайте одного из персонажей:\n\n'
     col_pers = list(df_copy.columns)[0]
     for i in range(len(df_copy[col_pers])):
          text = text + str(i+1)+'. '+df_copy[col_pers][i]+'\n'
     #Помщаем нажпись на Frame Pack
     lbl = Label(frame, text= text, justify =LEFT) #отображаем список людей
     lbl.grid(column=0, row=0, padx=10, pady=5)
     #Помещаем кнопку 'начать игру' на pack и переходим к игре (start_game)
     btn3 = Button(frame, text="Начать игру", command=partial(start_game,df_copy,window))
     btn3.grid(column=0, row=4, padx=10, pady=5)




def start_game(df_copy,window):
     '''
     Функция старта игры. Создаемт новое окно, зацикливает игру
     '''
     #делаем копию таблицы для неккоректных ответов
     df = df_copy.copy(deep = False)
     #Ломаем старое окно и составляем новое
     window.destroy()
     window1 = Tk() # создаем само окно винды
     #window1.geometry('800x300')
     window1.resizable(width=False, height=False)
     window1.title("Кто я?")
     incorrect_answers =[]
     #Начинаем ццикл самой игры
     game(window1,df_copy,df,incorrect_answers)
     


 
def game(window1,df_copy,df,incorrect_answers):
     '''
     Цикл игры. Здесь реализованы все механики внутри игры
     '''
      
     def check_answer(window1,answer,df_copy,answer_options,table_name,df,incorrect_answers):
          '''
          Функция проверки ответов пользователя. Удаление из первичной таблицы неподходящих ответов.
          '''
          #Проверяем ответы
          #Если ответ не знаю, цикл запуститься по новой, возмуться вопросы по новой
          if answer == 'Не знаю':
               pass
          #Если нет верного ваирианта ответа, то из наших вариантов ответа удаляются все соответсвия предложенным вариантам ответа
          elif answer == 'Нет верного ответа':
               for j in reversed(range(len(df_copy))):
                   not_answer = correct_symbols(df_copy[table_name][j])
                   if not_answer == answer_options[0] or not_answer == answer_options[1] or not_answer == answer_options[2]:
                         df_copy = df_copy.drop(index=j) 
                         df_copy = df_copy.reset_index(drop = True, inplace =False)

          #Если формат вопроса был "Ваш ответ на вопрос : этот вариант ответа?"
          elif count_answer == 1:
               #Если Да, удалить все, что не соответсвует этому варианту ответа
                if answer == 'Да':
                     for j in reversed(range(len(df_copy))):
                          not_answer = correct_symbols(df_copy[table_name][j])
                          if not_answer != answer_options[0]:
                               df_copy = df_copy.drop(index=j) 
                               df_copy = df_copy.reset_index(drop = True, inplace =False)
               #Если Нет, удалить все, что соответсвует этому варианту ответа       
                elif answer == 'Нет':
                     for j in reversed(range(len(df_copy))):
                          not_answer = correct_symbols(df_copy[table_name][j])
                          if not_answer == answer_options[0]:
                               df_copy = df_copy.drop(index=j) 
                               df_copy = df_copy.reset_index(drop = True, inplace =False)
                          
                     
          #Если же это какой-то конкретный вопрос, то удалить все, что не соответсвуют данному ответу на вопрос    
          else:
                for j in reversed(range(len(df_copy))):
                     not_answer = correct_symbols(df_copy[table_name][j])
                     if not_answer != answer:
                          df_copy = df_copy.drop(index=j) 
                          df_copy = df_copy.reset_index(drop = True, inplace =False)
                          
          frame.pack_forget()
          game(window1,df_copy,df,incorrect_answers)

     
     def final_answer(window1,frame,answer,incorrect_answers,df,df_copy):
          '''
          Фунция для ввывода финального ответа.
          Если автомат угадал персонажа: Правильные ответы на вопросы о персонаже. Вариант сыграть ещё или выйти.
          Если не угадал: перезапуск цикл игры, при этом удаляется персонаж из общего списка персонажей.
          '''
          if answer =='Да':

               #Создаение текста правильных ответов на вопросы
               text = 'Правильные ответы на вопросы:\n\n'
               df_col = list(df_copy.columns)
               for i in range(len(df_col)):
                    text = text + str(i+1)+'. '+df_col[i]+'\n'+df_copy[df_col[i]][0]+'\n\n'
               
               #ломаем окно и делаем новое
               window1.destroy()
               window1 = Tk() # создаем само окно винды
               window1.title("Кто я?")
               window1.resizable(width=False, height=False)
               frame = Frame(window1)
               frame.pack(side="top", expand=True, fill="both")
               #Помещаем надпись
               lbl = Label(frame, text= text, justify =LEFT)
               lbl.grid(column=0, row=0, padx=10, pady=5)

               
               #Кнопки - сыграть ещеё или выйти
               btn1 = Button(frame, text='Сыграть ещё раз', command=lambda: [p_quit(window1),start_programm()])
               btn2 = Button(frame, text='Выход', command=lambda: p_quit(window1))

               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)

          else:
               #Добавляем в список некорректных ответов нашего персонажа
               incorrect_answers.append(df_copy[list(df_copy.keys())[0]][0])
               #Из общего DF удаляются все некорректно угаданные персонажи за сессию игры
               df = df[~df[list(df.columns)[0]].isin(incorrect_answers)]
               df = df.reset_index(drop = True, inplace =False)
               df_copy = df.copy(deep = False)
               frame.pack_forget()
               #Перезапуск игры
               game(window1,df_copy,df,incorrect_answers)
                    
     def p_quit(window1):
          '''
          Функция выхода из игры
          '''
          window1.destroy()
          


          
     ###################################
     #создаем фрейм
     frame = Frame(window1)
     frame.pack(side="top", expand=True, fill="both")
     #Если есть ещё какие-либо варианты персонажей, игра продолжается
     if len(df_copy)>1:
          #Составляем перечень вопросов
          names_table=list(df_copy.columns)
          names_table.remove(names_table[0])
          
          answer_options = 'None'
          #Выюираем вопрос и выбираем из него ответы
          answer_options={} 
          table_name = random.choice(names_table) 
          for i in range(len(df_copy[table_name])):
               one_answer = correct_symbols(df_copy[table_name][i])
               answer_options[one_answer] = answer_options.get(one_answer,'Taked')
          #Считаем количество ответов
          count_answer = len(list(answer_options.keys()))
          #Берем лист ответов
          answer_options = list(answer_options.keys())

          #Если ответов меньше 2, запускаем цикл заново
          if count_answer < 2:
               names_table.remove(table_name)
               answer_options == 'None' 
               game(window1,df_copy,df,incorrect_answers)
          #Если ответов больше 3, берем 3 рандомных ответа
          elif count_answer>3:
               answer_options = random.sample(answer_options,3)

          #Если длинна ответов сликшом большая берем только один ответ и состовляем вопрос по особому (Да, Нет, Не знаю)
          if len(max(answer_options,key=len)) > 40:
               answer_options = random.sample(answer_options,1)
               count_answer = len(answer_options)
               #Составление вопроса в виде "Ваш ответ на вопрос : этот вариант ответа?"
               lbl = Label(frame, text= table_name[:-1]+':\n'+answer_options[0][:-1]+'?')
               lbl.grid(column=0, row=0, padx=10, pady=5)
               #Ответы - Да, Нет, Не знаю
               btn1 = Button(frame, text="Да", command= lambda: check_answer(window1,"Да",df_copy,answer_options,table_name,df,incorrect_answers))
               btn2 = Button(frame, text="Нет", command= lambda: check_answer(window1,"Нет",df_copy,answer_options,table_name,df,incorrect_answers))
               btn3 = Button(frame, text="Не знаю", command= lambda: check_answer(window1,"Не знаю",df_copy,answer_options,table_name,df,incorrect_answers))


               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)
               btn3.grid(column=0, row=3, padx=10, pady=5)

           
               window1.mainloop()

          #Для двух вариантов ответа 2 - 3 кнопки варианта ответа (вариант_ответа1, вариант_ответа2, Не знаю)
          elif count_answer == 2:
               lbl = Label(frame, text= table_name)
               lbl.grid(column=0, row=0, padx=10, pady=5)

               btn1 = Button(frame, text= answer_options[0], command= lambda: check_answer(window1,answer_options[0],df_copy,answer_options,table_name,df,incorrect_answers))
               btn2 = Button(frame, text=answer_options[1], command= lambda: check_answer(window1,answer_options[1],df_copy,answer_options,table_name,df,incorrect_answers))
               btn3 = Button(frame, text="Не знаю", command= lambda: check_answer(window1,"Не знаю",df_copy,answer_options,table_name,df,incorrect_answers))


               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)
               btn3.grid(column=0, row=3, padx=10, pady=5)

               window1.mainloop()
          #Для двух вариантов ответа 3 - 4 кнопки варианта ответа (вариант_ответа1, вариант_ответа2, вариант_ответа3, Не знаю)
          elif count_answer == 3:
               lbl = Label(frame, text= table_name)
               lbl.grid(column=0, row=0, padx=10, pady=5)

               btn1 = Button(frame, text= answer_options[0], command= lambda: check_answer(window1,answer_options[0],df_copy,answer_options,table_name,df,incorrect_answers))
               btn2 = Button(frame, text=answer_options[1], command= lambda: check_answer(window1,answer_options[1],df_copy,answer_options,table_name,df,incorrect_answers))
               btn3 = Button(frame, text=answer_options[2], command= lambda: check_answer(window1,answer_options[2],df_copy,answer_options,table_name,df,incorrect_answers))
               btn4 = Button(frame, text="Не знаю", command= lambda: check_answer(window1,"Не знаю",df_copy,answer_options,table_name,df,incorrect_answers))


               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)
               btn3.grid(column=0, row=3, padx=10, pady=5)
               btn4.grid(column=0, row=4, padx=10, pady=5)

               window1.mainloop()
          #Для двух вариантов ответа 4 - 5 кнопки варианта ответа (вариант_ответа1, вариант_ответа2, вариант_ответа3, Нет верного ответа, Не знаю)
          #Если нет верного ответа, то все предложенные варианты не подходят.
          elif count_answer > 3:
               lbl = Label(frame, text= table_name)
               lbl.grid(column=0, row=0)

               btn1 = Button(frame, text= answer_options[0], command= lambda: check_answer(window1,answer_options[0],df_copy,answer_options,table_name,df,incorrect_answers))
               btn2 = Button(frame, text=answer_options[1], command= lambda: check_answer(window1,answer_options[1],df_copy,answer_options,table_name,df,incorrect_answers))
               btn3 = Button(frame, text=answer_options[2], command= lambda: check_answer(window1,answer_options[2],df_copy,answer_options,table_name,df,incorrect_answers))
               btn4 = Button(frame, text="Нет верного ответа", command= lambda: check_answer(window1,"Нет верного ответа",df_copy,answer_options,table_name,df,incorrect_answers))
               btn5 = Button(frame, text="Не знаю", command= lambda: check_answer(window1,"Не знаю",df_copy,answer_options,table_name,df,incorrect_answers))

               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)
               btn3.grid(column=0, row=3, padx=10, pady=5)
               btn4.grid(column=0, row=4, padx=10, pady=5)
               btn5.grid(column=0, row=5, padx=10, pady=5)

               window1.mainloop()
               
     #Если персонад остался один, то вопро, угадал ли автомат
     elif len(df_copy)==1:
          #Надпись
          lbl = Label(frame, text= 'Вы загадали этого персонажа :'+df_copy[list(df_copy.columns)[0]][0]+'?')
          lbl.grid(column=0, row=0)
          #Кнопки вариантов ответов
          btn1 = Button(frame, text='Да', command= lambda: final_answer(window1,frame,'Да',incorrect_answers,df,df_copy))
          btn2 = Button(frame, text='Нет', command= lambda: final_answer(window1,frame,'Нет',incorrect_answers,df,df_copy))
          
          btn1.grid(column=0, row=1, padx=10, pady=5)
          btn2.grid(column=0, row=2, padx=10, pady=5)
     #На случай ошибки, если не осталось вариантов ответа.
     #Такой вариант возможен толлько в случае ошибки программы.
     else:
          #Надпись
          lbl = Label(frame, text= 'Вы загадали персонажа, которого нет в списке')
          lbl.grid(column=0, row=0)
          #Кнопки вариантов ответов
          btn1 = Button(frame, text='Сыграть ещё раз', command=lambda: [p_quit(window1),start_programm()])
          btn2 = Button(frame, text='Выход', command=lambda: p_quit(window1))

          btn1.grid(column=0, row=1, padx=10, pady=5)
          btn2.grid(column=0, row=2, padx=10, pady=5)



def start_programm():
     '''
     Проограмма старта программы с выбором загрузки игры
     '''
     #Создаем окно 
     window = Tk() # создаем само окно винды
     #Называем его
     window.title("Кто я?")
     #window.geometry('240x500')
     #Делаем окно неимзменяемое в размерах
     window.resizable(width=False, height=False)
     #Накладываем Frame Pack на окно
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     #Создаем ориентирующую надпиcь и кнопки выбора загрузок игры (локально или через гугл таблицы) 
     lbl = Label(frame, text="Загрузка через Гугл таблицы/Локально?")
     btn1 = Button(frame, text="Гугл таблицы", command=lambda: internet(window,frame))  
     btn2 = Button(frame, text="Локально", command=lambda: local(window,frame))
     #Помещаем надписи и кнопки на Frame pack
     lbl.grid(column=0, row=0, padx=10, pady=5)
     btn1.grid(column=0, row=2, padx=10, pady=5)
     btn2.grid(column=0, row=3, padx=10, pady=5)
     #Зацикливаем окно
     window.mainloop()

#Старт программы
start_programm()
  
