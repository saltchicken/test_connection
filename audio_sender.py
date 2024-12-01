import socket
import pyaudio
import zlib
import time

stats = {"sends_per_chunk" : 0,
         "acks_recieved" : 0}

CHUNK = 44100 # Will retrieve 2048 bytes due to each sample being 2 bytes - FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

HOST = "127.0.0.1"
PORT = 12345

p = pyaudio.PyAudio()
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
# NOTE: Needed for realtime. First read takes longer, this "primes" the stream, remove if the first sample is important for recording.
_ = input_stream.read(CHUNK, exception_on_overflow=False)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"Connected to server at {HOST}:{PORT}")

buffer = b""

audio_data = input_stream.read(CHUNK, exception_on_overflow=False)

buffer += audio_data

SEND_BYTES = 2048

start_time = time.perf_counter()
while len(buffer) >= SEND_BYTES:
    stats["sends_per_chunk"] += 1
    client_socket.sendall(buffer[:SEND_BYTES])
    buffer = buffer[SEND_BYTES:]
    ack = client_socket.recv(1024)  # Wait for server acknowledgment
    if ack != b'ACK':
        print("Acknowledgment mismatch.")
        break
    else:
        stats["acks_recieved"] += 1

if buffer:
    client_socket.sendall(buffer.ljust(SEND_BYTES, b'\x00'))


end_time = time.perf_counter()
stats['total_time'] = end_time - start_time

print(stats)

client_socket.close()
input_stream.stop_stream()
input_stream.close()
p.terminate()