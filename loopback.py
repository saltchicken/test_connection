import pyaudio

# Constants
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit per sample)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate in Hz

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open input and output streams
input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       frames_per_buffer=CHUNK)

print("Loopback started. Press Ctrl+C to stop.")

try:
    while True:
        # Read data from the microphone
        data = input_stream.read(CHUNK, exception_on_overflow=False)
        # Play the data back through the speakers
        output_stream.write(data)
except KeyboardInterrupt:
    print("\nLoopback stopped.")

# Close the streams
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()

# Terminate PyAudio
p.terminate()
