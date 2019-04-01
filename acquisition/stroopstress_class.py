# Author : Mateus C. Pedrino - University of Sao Paulo

# Stroop test 

import matplotlib.pyplot as plt
import time as tm
import random as rn

class Stroop():
    def __init__(self):

        # Color words and respectively hex numbers
        self.words=['verde','azul','amarelo','vermelho','preto','cinza','marrom','rosa','roxo','laranja']
        self.colors=['#00ff11','#0004ff','#f0ff00','#ff0000','#000000','#878787','#673412','#ff00db','#58004b','#ffa500']

        # The second while is to ensure contradiction between word color and word name
        # and ensure that the new plot will not match nor color or word from previous plot

        # Just for initialization porposes
        self.c_aux=rn.randint(0,len(self.colors)-1) 
        self.w_aux=rn.randint(0,len(self.words)-1)
    def loop(self):
        plt.figure()
        while True:
            plt.axis('off')
            self.c_idx=rn.randint(0,len(self.colors)-1) 
            self.w_idx=rn.randint(0,len(self.words)-1)
            while self.c_idx==self.w_idx or self.c_idx==self.c_aux or self.w_idx==self.w_aux: 
                self.c_idx=rn.randint(0,len(self.colors)-1)
                self.w_idx=rn.randint(0,len(self.words)-1)
            self.c_aux=self.c_idx
            self.w_aux=self.w_idx
            self.c_rand=self.colors[self.c_idx]
            self.w_rand=self.words[self.w_idx]
            plt.text(0.5,0.5,self.w_rand,ha="center",va="center",size=75,color=self.c_rand)
            plt.pause(3) # Time in seconds to change plot
            plt.clf()
        plt.show()
