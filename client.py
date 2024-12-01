import socket
import time

def run_client(server_host='127.0.0.1', server_port=12345, buffer_size=1024 * 4, data_size_mb=1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    print(f"Connected to server at {server_host}:{server_port}")
    
    data = b'a' * buffer_size  # Sending dummy data
    total_data = data_size_mb * 1024 * 1024
    sent_data = 0
    
    start_time = time.perf_counter()
    try:
        while sent_data < total_data:
            client_socket.sendall(data)
            sent_data += len(data)
            ack = client_socket.recv(1024)  # Wait for server acknowledgment
            if ack != b'ACK':
                print("Acknowledgment mismatch.")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        end_time = time.perf_counter()
        client_socket.close()
        
        duration = end_time - start_time
        speed_mbps = (sent_data * 8) / (duration * 1_000_000)
        
        print(f"Sent {sent_data / (1024 * 1024):.2f} MB and received acknowledgment in {duration:.8f} seconds.")
        print(f"Transfer speed (round trip): {speed_mbps:.2f} Mbps")

if __name__ == "__main__":
    run_client(data_size_mb=0.000976562 * 4)