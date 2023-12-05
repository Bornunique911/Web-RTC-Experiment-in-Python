import cv2
import socket
import pickle
import struct
import pyaudio

# Video streaming function
def receive_video():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    connection = client_socket.makefile('rb')
    
    while True:
        size = struct.unpack('>L', connection.read(struct.calcsize('>L')))[0]
        data = connection.read(size)
        frame = pickle.loads(data)
        cv2.imshow('Received', frame)
        cv2.waitKey(1)

# Audio streaming function
def receive_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.connect(('127.0.0.1', 8888))
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    
    while True:
        audio_data = audio_socket.recv(CHUNK)
        stream.write(audio_data)

# Start video and audio streaming functions
receive_video()
receive_audio()
