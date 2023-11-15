from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import get_window
from scipy.fft import fft
from Soundfile import SoundFile

filename = askopenfilename()

def applyHammingWindow(soundfile_obj, timeFrameStart, timeFrameEnd):
    start_time_sec = timeFrameStart / 1000
    end_time_sec = timeFrameEnd / 1000

    start_frame = int(start_time_sec * soundfile_obj.frame_rate)
    end_frame = int(end_time_sec * soundfile_obj.frame_rate)

    if start_frame < 0:
        start_frame = 0
    if end_frame > len(soundfile_obj.audio_data):
        end_frame = len(soundfile_obj.audio_data)

    time_frame_data = soundfile_obj.audio_data[start_frame:end_frame]

    hamming_window = get_window('hamming', len(time_frame_data))
    windowed_data = time_frame_data * hamming_window

    return windowed_data

def calculateModulus(windowed_data):
    fft_result = fft(windowed_data)

    modulus = np.abs(fft_result)

    return modulus

def arraySizeEven(size):
    if size & 2 == 0:
        return True
    else:
        return False
    
def trimArray(modulusResult, size):
    if arraySizeEven(size):
        modulusResult = np.delete(modulusResult, [int(modulusResult.size/2), int(modulusResult.size/2 + 1)])
    else:
        modulusResult = np.delete(modulusResult, [int((modulusResult.size-1)/2)])
    return modulusResult

def applyCoefficient(modulusResult, size):
    if arraySizeEven(size):
        for i, element in enumerate(modulusResult):
            if i != 0 and i != modulusResult.size - 1:
                modulusResult[i] = element * 2
    else:
        for i, element in enumerate(modulusResult):
            if i != 0:
                modulusResult[i] = element * 2
    return modulusResult

def generateFrequencyValues(samplingRate, numberOfValues):
    return np.linspace(0, samplingRate/2, numberOfValues)

def plotResult(modulusResult, frequencyValues, numberOfChannels):
    plt.figure(figsize=(10, 6))

    if numberOfChannels == 1:
        plt.plot(frequencyValues, modulusResult)
    else:
        for channel in range(numberOfChannels):
            plt.plot(frequencyValues, modulusResult)

    plt.title("Modulus Result as a Function of Frequency")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Modulus")
    plt.legend()
    plt.show()


soundfile_obj = SoundFile(filename)
soundfile_obj.plotSignal(filename)

timeFrameStart = -1
timeFrameEnd = -1

while timeFrameStart <= 0 :
    timeFrameStart = int(input("the beginning of the frame in miliseconds: "))

while timeFrameEnd <= timeFrameStart and timeFrameEnd<= soundfile_obj.duration :
    timeFrameEnd = int(input("Enter frame length for calculations in miliseconds: "))

soundfile_obj.plotTimeFrame(timeFrameStart, timeFrameEnd)
windowedData = applyHammingWindow(soundfile_obj, timeFrameStart, timeFrameEnd)

modulusResult = calculateModulus(windowedData)

originalSize = modulusResult.size

modulusResult = trimArray(modulusResult, originalSize)
modulusResult = applyCoefficient(modulusResult, originalSize)
frequencyValues = generateFrequencyValues(soundfile_obj.frame_rate, modulusResult.size)
timeValues = np.arange(len(modulusResult)) / soundfile_obj.frame_rate

plotResult(modulusResult, timeValues, soundfile_obj.num_channels)