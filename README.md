# EEG-real-time-data-acquisition-filtering-plotting-and-power-spectrum-coherence-analysis
These files contemplate my scientific initiation project in digital signal processing. In this project I developed a BCI using Ultracortex "Mark IV" EEG system from OpenBCI and I proposed a non-parametric analysis of data during stress tasks through Welch's power spectrum and coherence estimator.

The BCI is composed by acquiring, filtering, plotting data and interacting with user through Montreal stress task.

## BCI
### Acquisition and filtering 
In order to communicate to EEG hardware (Ultracortex Mark IV) from OpenBCI, it was used OpenBCI library for python (acquisitio/open_bci_v3.py). Initializing the program accordingly to OpenBCI specifications, it was created a queue to receive data each sampling period (sampling frequency is 250Hz).  

The data was filtered with a band-pass Hamming linear phase FIR with size 256. As the data arrives the samples are filtered and accumulated in another special list that allows a fast way to manage data, which is deque variable. 

#### Raw files
All filtered data is also saved in a .txt file with 9 collums and X rows where (X=t x 250) and t is the recording time. Each one of the first 8 collums is each of the 8 channels (electrodes) that are pinned to Ultracortex and the last collum is related to recording time (notice that it's created a time reference when the program is initialized). The files at raw_data/ follow this structure and each channel was recorded according to the following electrodes position (10-20 system):

- CH0 : FP2
- CH1 : FPz
- CH2 : F8
- CH3 : Cz
- CH4 : F4
- CH5 : P3
- CH6 : T6
- CH7 : T4

It's important to highlight that all EEG data was recorded with myself.

At raw_data/ there are recordings under normal activity and stress stimulated by Stroop and Montreal tasks. Montreal data was zipped because it was too large to updload to a git repository.

### Plot data
The plot data thread was developed based on pyqtgraph real time interface. It is initialized once in the beggining and then it occurs a loop that rotate the deque of filtered samples and plot them inasmuch as they are filtered. There is a waiting condition that happens if the plot thread runs faster than the receive and filter thread.

### Montreal stress task
This other thread in responsible for displaying the Montreal stress task based on (Dedovic et al., 2005) while EEG data is captured, filtered and displayed. It was developed by my lab partner (it's referenced in the code) using tkinter libreary and appended to a thread in the main program. 

## Simulations
The porpose of simulations (at simulations/) is to observe the behavior of processing tools that will be used to analyse EEG raw data in frequency domain. So, in these files some examples are performed to:

- Compare Welch's method with classic periodogram (noise and frequency resolution);
- Study coherence dynamics between pairs of sine signals with different amplitudes, frequencies and phases;
- Study the frequency domain effect of random inserted peaks (this simulate muscular contractions that add noise in EEG data);

## Data analysis
Considering the recordings at raw_data/, each data channels was fitted into 50s windows and the channels power spectrum for each raw data were estimated through Welch's method. Average power bands were calculated for each channel window (inside 50 seconds) and displayed in radar plots. 


## References
Dedovic, K., Renwick, R., Mahani, N. K., Engert, V., Lupien, S. J., and Pruessner, J. C.
(2005). The montreal imaging stress task: using functional imaging to investigate the
effects of perceiving and processing psychosocial stress in the human brain. Journal of
Psychiatry and Neuroscience, 30(5):319.
