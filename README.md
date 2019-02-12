# EEG-real-time-data-acquisition-filtering-plotting-and-power-spectrum-coherence-analysis
These files contemplate my scientific initiation project in digital signal processing. In this project I developed a BCI using Ultracortex "Mark IV" EEG system from OpenBCI and I proposed a non-parametric analysis of data during stress tasks through Welch's power spectrum and coherence estimator.

The BCI is composed by acquiring, filtering, plotting data and interacting with user through Montreal stress task.

# BCI
## Acquisition
In order to communicate to EEG hardware (Ultracortex Mark IV) from OpenBCI, it was used OpenBCI library for python (acquisitio/open_bci_v3.py). There are three threads 
