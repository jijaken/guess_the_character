import pandas as pd
import random
from tkinter import * # импорт б-ки
from  tkinter import ttk
from functools import partial
import os



def check_file_xls():
     files = os.listdir()
     files = [file for file in files if ('.xls' in file)]
     
     if len(files)<1:
          return('NaN')

     file = max(files, key=os.path.getctime)
     return(file)
     

def correct_symbols(string):
     string = " ".join(string.split())
     string = string.replace('H','Н')
     string = string.replace('a','а')
     string = string.replace('e','е')
     return(string)



#Выбор выгрузки данных
def internet(window,frame):
     option_export ='Гугл таблица'
     df_copy = pd.read_csv('https://docs.google.com/spreadsheets/d/1Z6hAlFOlLJa6RBry5vMUHK4jvmIFL0C_Y9Issau2zpY/export?format=csv')
     incorrect_answers =[] 
     end_program=False
     frame.pack_forget()
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     #
     text='Загадайте одного из персонажей:\n\n'
     col_pers = list(df_copy.columns)[0]
     for i in range(len(df_copy[col_pers])):
          text = text + str(i+1)+'. '+df_copy[col_pers][i]+'\n'
     #
     lbl = Label(frame, text= text, justify =LEFT) #отображаем список людей
     lbl.grid(column=0, row=0, padx=10, pady=5)
     btn3 = Button(frame, text="Начать игру", command=partial(start_game,df_copy,window))  
     btn3.grid(column=0, row=4, padx=10, pady=5)
def local(window,frame):
     option_export ='Локально' 
     excel = pd.read_excel(check_file_xls())
     df_copy = pd.DataFrame(excel)
     incorrect_answers =[] 
     end_program=False
     frame.pack_forget()
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     #
     text='Загадайте одного из персонажей:\n\n'
     col_pers = list(df_copy.columns)[0]
     for i in range(len(df_copy[col_pers])):
          text = text + str(i+1)+'. '+df_copy[col_pers][i]+'\n'
     #
     lbl = Label(frame, text= text, justify =LEFT) #отображаем список людей
     lbl.grid(column=0, row=0, padx=10, pady=5)
     btn3 = Button(frame, text="Начать игру", command=partial(start_game,df_copy,window))
     btn3.grid(column=0, row=4, padx=10, pady=5)




def start_game(df_copy,window):
     df = df_copy.copy(deep = False)
     window.destroy()
     window1 = Tk() # создаем само окно винды
     #window1.geometry('800x300')
     window1.resizable(width=False, height=False)
     window1.title("Кто я?")
     incorrect_answers =[] 
     game(window1,df_copy,df,incorrect_answers)
     


     
def game(window1,df_copy,df,incorrect_answers):
      
     def check_answer(window1,answer,df_copy,answer_options,table_name,df,incorrect_answers):
          
          #Удаляем не подходящие варианты ответа
          if answer == 'Не знаю':
               pass
          elif answer == 'Нет верного ответа':
               for j in reversed(range(len(df_copy))):
                   not_answer = correct_symbols(df_copy[table_name][j])
                   if not_answer == answer_options[0] or not_answer == answer_options[1] or not_answer == answer_options[2]:
                         df_copy = df_copy.drop(index=j) 
                         df_copy = df_copy.reset_index(drop = True, inplace =False)

          elif count_answer == 1:
                if answer == 'Да':
                     for j in reversed(range(len(df_copy))):
                          not_answer = correct_symbols(df_copy[table_name][j])
                          if not_answer != answer_options[0]:
                               df_copy = df_copy.drop(index=j) 
                               df_copy = df_copy.reset_index(drop = True, inplace =False)
                elif answer == 'Нет':
                     for j in reversed(range(len(df_copy))):
                          not_answer = correct_symbols(df_copy[table_name][j])
                          if not_answer == answer_options[0]:
                               df_copy = df_copy.drop(index=j) 
                               df_copy = df_copy.reset_index(drop = True, inplace =False)
                          
                     
                
          else:
                for j in reversed(range(len(df_copy))):
                     not_answer = correct_symbols(df_copy[table_name][j])
                     if not_answer != answer:
                          df_copy = df_copy.drop(index=j) 
                          df_copy = df_copy.reset_index(drop = True, inplace =False)
                          
          frame.pack_forget()
          game(window1,df_copy,df,incorrect_answers)

     
     def final_answer(window1,frame,answer,incorrect_answers,df,df_copy):
          if answer =='Да':

               
               window1.destroy()

               text = 'Правильные ответы на вопросы:\n\n'
               df_col = list(df_copy.columns)
               for i in range(len(df_col)):
                    text = text + str(i+1)+'. '+df_col[i]+'\n'+df_copy[df_col[i]][0]+'\n\n'
                    
               window1 = Tk() # создаем само окно винды
               window1.title("Кто я?")
               window1.resizable(width=False, height=False)
               frame = Frame(window1)
               frame.pack(side="top", expand=True, fill="both")
               lbl = Label(frame, text= text, justify =LEFT)
               lbl.grid(column=0, row=0, padx=10, pady=5)

               

               btn1 = Button(frame, text='Сыграть ещё раз', command=lambda: [p_quit(window1),start_programm()])
               btn2 = Button(frame, text='Выход', command=lambda: p_quit(window1))

               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)

          else:
               incorrect_answers.append(df_copy[list(df_copy.keys())[0]][0])
               df = df[~df[list(df.columns)[0]].isin(incorrect_answers)]
               df = df.reset_index(drop = True, inplace =False)
               df_copy = df.copy(deep = False)
               frame.pack_forget()
               game(window1,df_copy,df,incorrect_answers)
                    
     def p_quit(window1):
          window1.destroy()
          
          
     ###################################
     #создаем фрейм
     frame = Frame(window1)
     frame.pack(side="top", expand=True, fill="both")
     
     end_program=False
     if len(df_copy)>1:
          
          names_table=list(df_copy.columns)
          names_table.remove(names_table[0])
          
          answer_options = 'None' 
          while answer_options == 'None':
               answer_options={} 
               table_name = random.choice(names_table) 
               for i in range(len(df_copy[table_name])):
                    one_answer = correct_symbols(df_copy[table_name][i])
                    answer_options[one_answer] = answer_options.get(one_answer,'Taked')
               count_answer = len(list(answer_options.keys()))
               answer_options = list(answer_options.keys())

           
          if count_answer < 2:
               names_table.remove(table_name)
               answer_options == 'None' 
               game(window1,df_copy,df,incorrect_answers)
               
          elif count_answer>3:
               answer_options = random.sample(answer_options,3)


          if len(max(answer_options,key=len)) > 40:
               answer_options = random.sample(answer_options,1)
               count_answer = len(answer_options)
           
          if count_answer == 1:
               lbl = Label(frame, text= table_name[:-1]+':\n'+answer_options[0][:-1]+'?')
               lbl.grid(column=0, row=0, padx=10, pady=5)

               btn1 = Button(frame, text="Да", command= lambda: check_answer(window1,"Да",df_copy,answer_options,table_name,df,incorrect_answers))
               btn2 = Button(frame, text="Нет", command= lambda: check_answer(window1,"Нет",df_copy,answer_options,table_name,df,incorrect_answers))
               btn3 = Button(frame, text="Не знаю", command= lambda: check_answer(window1,"Не знаю",df_copy,answer_options,table_name,df,incorrect_answers))


               btn1.grid(column=0, row=1, padx=10, pady=5)
               btn2.grid(column=0, row=2, padx=10, pady=5)
               btn3.grid(column=0, row=3, padx=10, pady=5)

           
               window1.mainloop()
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

     elif len(df_copy)==1:
          lbl = Label(frame, text= 'Вы загадали этого персонажа :'+df_copy[list(df_copy.columns)[0]][0]+'?')
          lbl.grid(column=0, row=0)

          btn1 = Button(frame, text='Да', command= lambda: final_answer(window1,frame,'Да',incorrect_answers,df,df_copy))
          btn2 = Button(frame, text='Нет', command= lambda: final_answer(window1,frame,'Нет',incorrect_answers,df,df_copy))

          btn1.grid(column=0, row=1, padx=10, pady=5)
          btn2.grid(column=0, row=2, padx=10, pady=5)
     else:
          lbl = Label(frame, text= 'Вы загадали персонажа, которого нет в списке')
          lbl.grid(column=0, row=0)

          btn1 = Button(frame, text='Сыграть ещё раз', command=lambda: [p_quit(window1),start_programm()])
          btn2 = Button(frame, text='Выход', command=lambda: p_quit(window1))

          btn1.grid(column=0, row=1, padx=10, pady=5)
          btn2.grid(column=0, row=2, padx=10, pady=5)



def start_programm():
     window = Tk() # создаем само окно винды
     window.title("Кто я?")
     #window.geometry('240x500')
     window.resizable(width=False, height=False)
     frame = Frame(window)
     frame.pack(side="top", expand=True, fill="both")
     
     lbl = Label(frame, text="Загрузка через Гугл таблицы/Локально?")
     btn1 = Button(frame, text="Гугл таблицы", command=lambda: internet(window,frame))  
     btn2 = Button(frame, text="Локально", command=lambda: local(window,frame))

     lbl.grid(column=0, row=0, padx=10, pady=5)
     btn1.grid(column=0, row=2, padx=10, pady=5)
     btn2.grid(column=0, row=3, padx=10, pady=5)
     window.mainloop()

start_programm()
  
