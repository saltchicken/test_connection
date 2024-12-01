import socket

def run_server(host='0.0.0.0', port=12345, buffer_size=4096):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")
    
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    
    try:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            # Simulate processing
            conn.sendall(b'ACK')  # Acknowledge receipt
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    try:
        print("Running... Press Ctrl+C to stop.")
        while True:
            run_server()
            
    except KeyboardInterrupt:
        print("\nTerminated by user.")
    
