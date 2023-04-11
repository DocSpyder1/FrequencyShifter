import streamlit as st
import numpy as np
import sounddevice as sd
import holoviews as hv
from holoviews import opts
hv.extension('bokeh', logo=False)
from core import *

# App Pipeline:
# Record Audio or Import Audio
# Shift the Frequency
# Play or Store the Audio
# Maybe recording is silly

st.write("Frequency Shifter App")

audio_data = None
audio_fs = None

devices = sd.query_devices()
device_names = [device['name']  for device in devices]
device_ids = [device['index']  for device in devices]
devices = [(device['name'], device['index'])  for device in devices]

# Import Audio
with st.container():
    upload_tab, record_tab = st.tabs(["Upload", "Record"])
    file_uploaded= False
    with upload_tab:
        audio_file = st.file_uploader("Upload an Audio File")
        # Check is an accepted data format?
        if audio_file is not None:
            audio_data, audio_fs = ImportAudio(audio_file) 
            file_uploaded= True
        
    with record_tab:
        submitted = False
        with st.form("Record Audio", clear_on_submit=False):
            duration = st.number_input("Recording Duration", min_value=0)
            input_device = st.selectbox('Input Device', devices)
            submitted = st.form_submit_button("Record")
            if submitted and duration != 0.0:
                st.write("Recording")
                audio_data, audio_fs = RecordAudio(duration, input_device[1])
                st.session_state['recorded_audio']=(audio_data,audio_fs)
                #StoreAudio("temp.wav", audio_data, audio_fs)
                st.write("Done")
        
    # audio_data, audio_fs = ImportAudio("temp.wav") 

if 'recorded_audio' in st.session_state.keys():
    audio_data, audio_fs = st.session_state.recorded_audio

def DisplayAudio(audio_data, fs):
    st.audio(audio_data, sample_rate=int(audio_fs))
    freq_x = np.linspace(0,audio_fs, len(audio_data))
    dft = np.real(np.fft.rfft(audio_data))

    time_domain_plt = hv.Curve(audio_data).opts(title="Time Domain of Audio", width=700, xlabel="Samples", ylabel="Amplitude")
    freq_domain_plt = hv.Curve(zip(freq_x,dft)).opts(title="Frequency Domain of Audio", width=700, xlabel="Frequency Bins", ylabel="Amplitude")
    st.write(hv.render(time_domain_plt, backend='bokeh'))
    st.write(hv.render(freq_domain_plt, backend='bokeh'))

# Play Audio
if audio_data is not None:
    with st.container():
        DisplayAudio(audio_data, audio_fs)

    with st.container():
        with st.form("Offset Audio", clear_on_submit=False):
            offset = st.number_input("Frequency Offset", min_value=0)
            submitted = st.form_submit_button("Submit")
            if submitted:
                shifted_data = np.real(ShiftFreq(audio_data, offset, audio_fs))
                DisplayAudio(shifted_data, audio_fs)
else:
    st.write("No Audio to Play")
