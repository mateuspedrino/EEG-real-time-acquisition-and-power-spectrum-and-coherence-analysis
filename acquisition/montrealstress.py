# Author : Rafael Augusto Arone

# -*- coding: utf-8 -*-
import tkinter as tk
import random
import numpy as np
import time
from tkinter import ttk
from collections import deque
from queue import Queue
# information> when the sum of answer time achieves 120s, difficulty is increased
# the file will be in the following format : 
# Hits/mistakes/timeout answering_time initial_time final_time
# mistakes = 0, hits = 1, timeout = 2
class Question():
    def __init__(self, timer,level,levelqueue):
        self.timer = timer
        self.level = level
        self._count = timer
        self._reset_timer = timer
        self._expression = ''
        self._res = 0
        self.savefile = feedback()
        self.savefile.ini()
        self.progress = 0
        self.step = 10.00/timer
        self.levelqueue = levelqueue
    def makequestion(self):
        self.root = tk.Tk()
        self.root.lift()
        self.root.focus_force()
        self.root.wm_attributes('-topmost', 1)
        self._expression, self._res  = self.questionstring(self.level)
        self.msg = tk.Label(self.root, text=self._expression + ' =')
        self.msg.config(bg = 'gray', font = ('times', 100, 'bold'))
        self.msg.pack()
        self.entry = tk.Entry(self.root)
        #self.entry.grid(row=1)
        self.entry.pack()
        self.entry.bind('<Return>', self.get_answer)
        self.entry.focus()
        self.w = tk.Label(self.root)
        self.savefile.ini_question()
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar",  troughcolor ='black', background='red', foreground = 'red')
        self.pb = ttk.Progressbar(self.root, style="red.Horizontal.TProgressbar",variable = self.progress, maximum = 100, length = 500)
        self.pb.pack()
        self.count_progress()
        #self.count_loop()
    def changetimer1(self):
        # When the answer is correct 3 times in a row
        self.timer = np.ceil(0.9 * self.timer)
        self.step = 10/self.timer
    def changetimer2(self):
        # When the answer is correct 3 times in a row
        self.timer = np.ceil(1.1 * self.timer)
        self.step = 10/self.timer
    def changelevel(self):
        self.level += 1
        self.levelqueue.put(self.level)
    def countdown(self):
        self._count = self.timer
        self.progress = 0
    def count_loop(self):
        if self._count > 0:
            self.w.config(text = str(self._count), fg = 'red', font = ('times', 15, 'bold'))
            self.progress += self.step
            self.pb["value"] = self.progress
            self.w.pack()
            self.w.after(1000, self.count_loop)
            self._count -= 1
        else:
            self._message('Tempo Esgotado', 2)
            self.verific_level()
            self.countdown()
    def count_progress(self):
        if self.progress <= 100:
             ### some work to be done
            self.pb["value"] = self.progress
            self.progress += self.step
            time.sleep(0.02)
            self.root.after(100, self.count_progress)
        else:
            self._message('Tempo Esgotado', 2)
            self.verific_level()
            self.countdown()
    def get_answer(self, event):
        self.response = self.entry.get()
        if self.response == '':
                return
        if int(self.response) == self._res:
            self._message("Correto",1)
            self.countdown()
            if self.savefile.correct_answer() == True:
                self.changetimer1()
            else:
                if self.savefile.wrong_answer() == True:
                    self.changetimer2()
        else:
            self._message("Errado",0)
            self.countdown()
        self.verific_level()
    def _message(self, response, int_response):
        self.root.destroy()
        self.root = tk.Tk()
        message = response + "\nAguarde..."
        mes = tk.Label(self.root)
        mes.configure(text = message)
        mes.pack()
        self.savefile.write_answer(int_response,self.level)
        self._count = 2
        self.w = tk.Label(self.root)
        self.internal_loop()
        self.root.mainloop()
    def internal_loop(self):
        self.w.configure(text = str(self._count))
        self.w.pack()
        if self._count > 0:
            self._count -= 1
            self.w.after(1000, self.internal_loop)
        else:
            self.root.destroy()
    def endmessage(self):
        end = "Corretas: " + str(self.savefile.correct) + '\n' + "Erradas: " + str(self.savefile.wrong) + "\n" +"Tempo esgotado: " + str(self.savefile.timeout) + "\n"
        self.root = tk.Tk()
        mes = tk.Label(self.root)
        mes.configure(text=end + "Obrigado pela participação\n")
        mes.pack()
        button = tk.Button(self.root, text = "Ok", command = exit())
        button.pack()
        self.root.mainloop()
    def verific_level(self):
        if self.savefile.verific_level() == True:
            self.changelevel()
            self.timer = self._reset_timer  # reset
            if self.level > 5:
                self.levelqueue.put(self.level)
                self.savefile.close_file()
                # self.endmessage()

    def intro(self):
        global timerh
        message = "Instruções:\nO teste iniciará com um treinamento sobre o funcionamento da captura\n" \
                  "neste teste você deverá digitar no teclado do computador a resposta da expressão matemática\n" \
                  "e após o treinamento, o teste será feito em 5 fases de 2 minutos cada, e cada fase terá um nível de dificuldade diferente"
        root = tk.Tk()
        msg = tk.Message(root, text=message)
        msg.config(font=('times', 15, 'italic'), padx=10)
        msg.pack()
        b2 = tk.Button(root, text='Iniciar', command=root.destroy)
        b2.pack(side=tk.LEFT, padx=5, pady=5)
        root.mainloop()

    def questionstring(self,level):
        random.seed()
        if level == 1:
            a = random.randrange(0, 9)
            b = random.randrange(0, 9)
            c = random.choice('+-')
            res = self.resp(a, b, c)
            quest = str(a) + ' ' + c + ' ' + str(b)
            return quest, res
        if level == 2:
            a = random.randrange(0, 9)
            b = random.randrange(0, 9)
            c = random.randrange(0, 9)
            items = ['+', '-']
            random.shuffle(items)
            quest = str(a) + ' ' + items[0] + ' ' + str(b) + ' ' + items[1] + ' ' + str(c)
            res = self.resp(self.resp(a, b, items[0]), c, items[1])
            return quest, res
        if level == 3:
            a = []
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 9))
            items = ['+', '-', 'x']
            random.shuffle(items)
            quest = str(a[0]) + ' ' + items[0] + ' ' + str(a[1]) + ' ' + items[1] + ' ' + str(a[2])
            res = self.resp2(a, items[0:2])
            if type(res) != int or abs(res) > 100:
                quest, res = self.questionstring(level)
            return quest, res
        if level == 4:
            a = []
            random.seed(time.time())
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 9))
            a.append(random.randrange(0, 9))
            items = ['+', '-', 'x']
            random.shuffle(items)
            random.shuffle(a)
            quest = str(a[0]) + ' ' + items[0] + ' ' + str(a[1]) + ' ' + items[1] + ' ' + str(a[2]) + ' ' + items[
                2] + ' ' + str(a[3])
            res = self.resp2(a, items)
            if type(res) != int or abs(res) > 100:
                quest, res = self.questionstring(level)
            return quest, res
        if level == 5:
            a = []
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 9))
            a.append(random.randrange(0, 99))
            a.append(random.randrange(0, 9))
            items = ['+', '/', 'x', '-']
            random.shuffle(items)
            random.shuffle(a)
            quest = str(a[0]) + ' ' + items[0] + ' ' + str(a[1]) + ' ' + items[1] + ' ' + str(a[2]) + ' ' + items[
                2] + ' ' + str(a[3])
            items2 = items[0:3]
            res = self.resp2(a, items2)
            if type(res) != int or res >100:
                quest, res = self.questionstring(level)
            return quest, res

    def resp(self,number1, number2, operation):
        if operation == '+':
            return number1 + number2
        if operation == '-':
            return number1 - number2

    def resp2(self,numbers, operations):
        if 'x' in operations:
            mult = operations.index('x')
            res1 = numbers[mult] * numbers[mult + 1]
            if (numbers[mult + 1] == 1): return 0.5
            del (numbers[mult + 1])
            numbers[mult] = res1
            if res1 == 0:
                return 0.5
            del operations[mult]
        if '/' in operations:
            div = operations.index('/')
            if numbers[div + 1] > 1:
                res1 = numbers[div] / numbers[div + 1]
                if numbers[div] % numbers[div + 1] != 0:
                     return 0.5
            else:
                return 0.5
            del (numbers[div + 1])
            numbers[div] = int(res1)
            del operations[div]
        qnumbers = len(numbers)
        res = numbers[0]
        for i in range(0, qnumbers - 1):
            res = self.resp(res, numbers[i + 1], operations[i])
        return res
    def loop(self):
        while self.level < 6:
            self.makequestion()
            self.root.mainloop()
        self.savefile.end()
class feedback():
    def __init__(self):
        showtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        self.name = 'Coleta_de_Dados_' + showtime + '.txt'
        self._feedbackfile = open(self.name,'w')
        self._buffertimer = 0
        self.ncorrect = 0
        self.nwrong = 0
        self.correct = 0
        self.wrong = 0
        self.timeout = 0
    def ini(self):
        start_time  = time.strftime("%H-%M-%S", time.localtime())
        self._feedbackfile.write('início:' + start_time +'\n')
    def write_answer(self, result, level):
        total_time = float(time.time()) - float(self.floatstart_time) + 2.0 # Somado 2 pelo tempo de espera
        self._buffertimer += total_time
        self.end_time =  time.strftime("%H-%M-%S", time.localtime())
        if result == 1:
            self.correct += 1
            self.ncorrect += 1
            self.wrong += 0
        if result == 0:
            self.wrong += 1
            self.nwrong += 1
            self.ncorrect = 0
        if result == 2:
            self.timeout += 1
            self.nwrong += 1
            self.ncorrect = 0
        self._feedbackfile.write(str(level) + ' ' + str(result) + ' ' + str(total_time) +
                                 ' ' + str(self.start_time) + ' ' + str(self.end_time) + '\n')
    def verific_level(self):
        if self._buffertimer >= 120:
            self._buffertimer = 0
            return True
        return False
    def ini_question(self):
        self.start_time =  time.strftime("%H-%M-%S", time.localtime())
        self.floatstart_time = time.time()
    def correct_answer(self):
        if self.ncorrect == 3:
            self.ncorrect = 0
            return True
        return False
    def wrong_answer(self):
        if self.nwrong == 3:
            self.wrong = 0
            return True
        return False
    def close_file(self):
        self._feedbackfile.close()
    def end(self):
        end = "Corretas: " + str(self.correct) + '\n' + "Erradas: " + str(
            self.wrong) + "\n" + "Tempo esgotado: " + str(self.timeout) + "\n"
        root = tk.Tk()
        mes = tk.Label(root)
        mes.configure(text=end + "Obrigado pela participação\n")
        mes.pack()
        button = tk.Button(root, text="Ok", command=exit)
        button.pack()
        root.mainloop()
#começa o questionário
# level = 1
# timelimit = 17#seconds
# question = Question(timelimit,level)
# question.intro()
# while question.level<6:
#     question.makequestion()
#     question.root.mainloop()
# question.savefile.end()