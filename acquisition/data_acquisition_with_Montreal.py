# Data acquisition from EEG source - OpenBCI Ultracortex IV (8 channels)
# Author : Mateus Camargo Pedrino
# Digital Signal Processing laboratory : University of São Paulo (SEL/EESC/USP)
# Montreal stress program author : Rafael Augusto Arone

from open_bci_v3 import OpenBCIBoard
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from queue import Queue 
from threading import Thread
import time as tm
import scipy.signal as sg
from collections import deque
import random as rn
from montrealstress import Question

global eegque, curve, Xm, eeg_list, filtered, file_EEG, w, numberofchannels, ptr, eegdeque, t0
eegdeque = deque(maxlen=1024)
ptr=0

# Creates time reference for appending in EEG rawdata
t0=tm.time()

# # Recieve data from electrodes
def handle_sample(sample):
    eegqueue.put(sample.channel_data)
    buffer=eegqueue.get()
    for j in range(0,8):
        eeg_list[j].pop(0) # Remove sample that was last received
        eeg_list[j].append(buffer[j])
    filter_signal()

def save_file(aux):
    for item in aux:
        file_EEG.write("%s\t" % item)
    file_EEG.write("\n")

# Real time filtering
def filter_signal():
    aux=[]
    for j in range(0,8):
        filtered[j].append(np.dot(eeg_list[j],w))
        aux.append(np.dot(eeg_list[j],w))
    aux.append(tm.time()-t0)
    eegdeque.append(aux)
    save_file(aux)


# Real time plot
def plotdata_mateus():
        ### START QtApp #####
    #################### 
    app = pg.QtGui.QApplication([])            # you MUST do this once (initialize things)
    win = pg.GraphicsWindow(title="Sinais dos eletrodos filtrados em tempo real") # creates a window
    p = [win.addPlot(row=i, col=1) for i in range(numberofchannels)] # creates empty space for the plot in the window
    curve = [p[i].plot(pen='r') for i in range(numberofchannels)]  # create an empty "plot" (a curve to plot)
    [p[i].setLabels(left=('Ch ' + str(i + 1), 'uV'), bottom=('time', 's')) for i in range(numberofchannels)] # Insert labels
    windowWidth = 250 
    Xm=[]
    for i in range(numberofchannels):
        Xm.append(np.linspace(0,0,windowWidth))
    global ptr
    ptr=0
    def update(): 
        a = [list(i) for i in zip(*eegdeque)]  # EEG data
        if len(a) == 0: return
        [curve[i].setData(a[8], a[i]) for i in range(numberofchannels)]  # set the curve with this data
        pg.QtGui.QApplication.processEvents()  # you MUST process the plot now

    
    ### MAIN PROGRAM #####    
    # this is a brutal infinite loop calling your realtime data plot
    while True: update()
    
    ### END QtApp ####
    pg.QtGui.QApplication.exec_() # you MUST put this at the end
    ##################

# Read serial information related to the electrodes
board = OpenBCIBoard()
board.print_register_settings()

numberofchannels=8

# Montreal task
levelqueue=Queue()
question  = Question(level=1, timer = 20,levelqueue = levelqueue)

# Filtering setup
w = sg.firwin(256, [5, 50], pass_zero=False, fs = 250, window="hann")
w=np.flip(w) # Change w0 to last position in order to multiply that last sample that came from queue

# File to save recordings in time domain
showtime_rec = tm.strftime("%Y-%m-%d_%H-%M-%S", tm.localtime()) # Extract data info about time and date
name_rec = 'EEG_Dados_' + showtime_rec + '.txt' # File name
file_EEG = open(name_rec, 'w') # Create a file to save data

# Initialize lists and queue
eegqueue = Queue()
filtered=[[],[],[],[],[],[],[],[]] # Receive filtered data
eeg_list=[[],[],[],[],[],[],[],[]] # Initialize list with 8 spaces to allocate data that are poped from queue

for i in range(0,8):  # Initialize each one of the 256 first elements (filter size) of each queue position with zero
    for j in range(0,256):
        eeg_list[i].append(0)


# Receive, process and plot data in a parallel manner
procs = []
procs.append(Thread(name = "streaming",target = board.start_streaming, args = (handle_sample,)))
procs.append(Thread(name="test", target=question.loop, args=()))
procs.append(Thread(name="plot", target=plotdata_mateus, args=()))
procs[1].daemon = True
[v.start()for v in procs]
[v.join() for v in procs]