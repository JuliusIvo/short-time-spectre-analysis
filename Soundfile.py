import wave
import matplotlib.pyplot as plt
import numpy as np

class SoundFile:
    def __init__(self, filename):
        self.filename = filename
        self.audio_data, self.num_channels, self.frame_rate, self.num_frames, self.duration = self.readSoundFile()

    def readSoundFile(self):
        with wave.open(self.filename, 'rb') as soundfile:
            num_channels = soundfile.getnchannels()
            sample_width = soundfile.getsampwidth()
            frame_rate = soundfile.getframerate()
            num_frames = soundfile.getnframes()

            duration = num_frames / frame_rate

            audio_data = np.frombuffer(soundfile.readframes(num_frames), dtype=np.int16)

            if num_channels == 2:
                left_channel = audio_data[::2]
                right_channel = audio_data[1::2]
                left_channel = left_channel.reshape(-1, 1)
                right_channel = right_channel.reshape(-1, 1)
                audio_data = np.column_stack((left_channel, right_channel)).flatten()

        return audio_data, num_channels, frame_rate, num_frames, duration

    def plotSignal(self, filename):
        time = np.arange(len(self.audio_data)) / self.frame_rate

        if self.num_channels == 1:
            plt.title(f"Original audio (Mono) of {filename.split('/')[-1]}")
            plt.plot(time, self.audio_data)
        else:
            left_channel = self.audio_data[::2]
            right_channel = self.audio_data[1::2]

            time_stereo = np.arange(len(left_channel)) / self.frame_rate

            plt.figure(figsize=(10, 6))

            plt.subplot(2, 1, 1)
            plt.plot(time_stereo, left_channel, label="Left channel")
            plt.title(f"Left channel of {filename.split('/')[-1]}")
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(time_stereo, right_channel, label="Right channel")
            plt.title(f"Right channel of {filename.split('/')[-1]}")
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.legend()

            plt.tight_layout()

        plt.show()

    def plotTimeFrame(self, timeFrameStart, timeFrameEnd):
        start_time_sec = timeFrameStart / 1000
        end_time_sec = timeFrameEnd / 1000

        start_frame = int(start_time_sec * self.frame_rate)
        end_frame = int(end_time_sec * self.frame_rate)

        if start_frame < 0:
            start_frame = 0
        if end_frame > len(self.audio_data):
            end_frame = len(self.audio_data)

        time_frame_data = self.audio_data[start_frame:end_frame]
        time_frame_time = np.arange(start_frame, end_frame) / self.frame_rate

        if self.num_channels == 1:
            plt.title(f"Time Frame ({start_time_sec}s - {end_time_sec}s) of {self.filename.split('/')[-1]} (Mono)")
            plt.plot(time_frame_time, time_frame_data)
        else:
            left_channel = time_frame_data[::2]
            right_channel = time_frame_data[1::2]

            time_stereo = np.arange(len(left_channel)) / self.frame_rate

            plt.title(f"Time Frame ({start_time_sec}s - {end_time_sec}s) of {self.filename.split('/')[-1]} (Stereo)")
            plt.subplot(2, 1, 1)
            plt.plot(time_stereo, left_channel, label="Left channel")
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(time_stereo, right_channel, label="Right channel")
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.legend()

            plt.tight_layout()

        plt.show()