import numpy as np
import sounddevice as sd 
import soundfile as sf 

def ImportAudio(filename):
    audio, fs = sf.read(filename, always_2d=False)
    return audio, fs

def RecordAudio(duration, input_device):
    device_info = sd.query_devices(input_device, 'input')
    fs = device_info['default_samplerate']
    data = sd.rec(int(duration*fs), channels=1, device=input_device, blocking=True)
    return data[:,0], fs

def StoreAudio(filename, audio, fs):
    sf.write(filename, audio, int(fs))

def PlayAudio(audio, output_device):
    # Do we need to extract audo info?
    device_info = sd.query_devices(output_device, 'output')
    fs = device_info['default_samplerate']
    sd.play(audio, device=output_device, blocking=True)
    pass

# assumes symetric positive and negative frequencies when altering nyquist frequency bin
# signal: signal to be offset in the frequency domain
# offset: frequency offset to be added (assumed Hz)
# fs: frequency signal was sampled at
def ShiftFreq(signal, offset, fs):
    # get offset relative to freq_bin size
    n = len(signal)
    # this might not be accurate best would be (fs/2)/
    bin_size = fs/n
    bin_offset = int(offset/bin_size)

    dft = np.fft.fft(signal)
    dft_shifted = np.zeros_like(dft)
    # copy DC
    dft_shifted[0] = dft[0]
    # offset postive frequencies
    pos_limit = int((n+1)/2)-bin_offset
    pos_limit = pos_limit+1 if n % 2 == 0 else pos_limit
    for i in range(1, pos_limit):
        dft_shifted[i+bin_offset] = dft[i]
    # offset negative frequencies
    neg_start = pos_limit + bin_offset 
    for i in range(neg_start, n - bin_offset):
        dft_shifted[i] = dft[i+bin_offset]
    return np.fft.ifft(dft_shifted)



if __name__ == "__main__":
    # Record 5 seconds of audio
    print("Recording")
    audio, fs = RecordAudio(5)
    print(fs)
    shifted_audio = np.real(ShiftFreq(audio[:,0], 1000, fs))
    print("Normal Playing")
    PlayAudio(audio)
    print("Shifted Playing")
    PlayAudio(shifted_audio)
    StoreAudio("test.wav", audio, fs)
    print("Imported Audio")
    imported_audio, fs = ImportAudio("test.wav")
    PlayAudio(imported_audio)
