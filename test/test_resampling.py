"""
1- Generate a stream with sine waves 
-- Create a mock data stream containing sine waves of known frequency and amplitude.
-- Add markers to the stream
2- Run the stream through synchronisation and resampling
-- use sync/ resampling function 
-- Resampling process should manintains the integrity of the sine waves and markers
3- Verify the output
-- Compare resampled data with the expected results
-- asserions to validate frequencies and markers are preserved

"""
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

# 1- Generate a stream with sine waves
#https://www.quora.com/How-do-you-create-a-sinewave-generator-in-Python
class SineWaveGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sine Wave Generator") 

        # Default val
        self.amplitude = tk.DoubleVar(value=1.0)
        self.frequency = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)

        # Widgets 
        self.amplitude_label = tk.Label(master, text="Amplitude")
        self.amplitude_entry = tk.Entry(master, textvariable= self.amplitude)
        self.frequency_label = tk.Label(master, text="Frequency")
        self.frequency_entry = tk.Entry(master, textvariable= self.frequency)
        self.phase_label = tk.Label(master, text="Phase")
        self.phase_entry = tk.Entry(master, textvariable= self.phase)
        self.execute_button = tk.Button(master, text="Execute", command=self.execute)

        # Grid layout  
        self.amplitude_label.grid(row=0, column=0)
        self.amplitude_entry.grid(row=0, column=1)
        self.frequency_label.grid(row=1, column=0)
        self.frequency_entry.grid(row=1, column=1)
        self.phase_label.grid(row=2, column=0)
        self.phase_entry.grid(row=2, column=1)
        self.execute_button.grid(row=3, column=0, columnspan=2)

    def execute(self):
        t = np.linspace(0, 1, 1000)
        y = self.amplitude.get() * np.sin(2 * np.pi * self.frequency.get() * t - self.phase.get())
        plt.plot(t, y)
        plt.show()  

root = tk.Tk()
my_gui = SineWaveGUI(root)
root.mainloop()