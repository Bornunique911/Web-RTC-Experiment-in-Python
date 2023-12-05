import cv2
import socket
import pickle
import struct
import pyaudio
import threading

# Video streaming function
def send_video():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(10)
    
    while True:
        client_socket, client_addr = server_socket.accept()
        connection = client_socket.makefile('wb')
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 480))
            data = pickle.dumps(frame)
            size = struct.pack('>L', len(data))
            connection.write(size + data)
        connection.close()

# Audio streaming function
def send_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.bind(('0.0.0.0', 8888))
    audio_socket.listen(10)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    while True:
        client_socket, client_addr = audio_socket.accept()
        while True:
            audio_data = stream.read(CHUNK)
            client_socket.sendall(audio_data)

# Start video and audio streaming threads
video_thread = threading.Thread(target=send_video)
audio_thread = threading.Thread(target=send_audio)

video_thread.start()
audio_thread.start()
