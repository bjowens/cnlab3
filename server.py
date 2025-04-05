import random
import socket
import os
import sys
import threading

IP = '127.0.0.1'  # default IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_info(data: bytes):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')


def upload_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data
    file_name += '.temp'
    # please do not change the above line!
    with open(file_name, 'wb') as file:
        retrieved_size = 0
        try:
            while retrieved_size < file_size:
                # Section 1 step 6a (receive a chunk of data)
                chunk = conn_socket.recv(BUFFER_SIZE)
                # Section 1 stop 6b (update number of bytes received)
                retrieved_size += len(chunk)
                # Section 1 stop 6c (write data to file)
                file.write(chunk)
        except OSError as oe:
            print(oe)
            os.remove(file_name)


def service_client_connection(conn_socket: socket):
    try:
        # Step 2: Receive the message from the client
        data = conn_socket.recv(1024)  # Adjust buffer size as needed

        # Step 3: Extract file size and file name
        file_name, file_size = get_file_info(data)
        print(f'Received: {file_name} with size = {file_size}')

        # Step 4: Send 'go ahead' message to the client
        conn_socket.sendall(b'go ahead')

        upload_file(conn_socket, file_name, file_size)
    except Exception as e:
        print(e)
    finally:
        conn_socket.close()


def start_server(ip, port):
    # create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))  # section 3 and 4 step 1
    server_socket.listen(5)  # section 4 step 2
    print(f'Server ready and listening on {ip}:{port}')
    try:
        while True:  # section 4 step 6
            (conn_socket, addr) = server_socket.accept()  # section 4 step 3
            thread = threading.Thread(target=service_client_connection, args=(conn_socket,))  # section 4 step 4
            thread.start()  # section 4 step 5
    except KeyboardInterrupt as ki:
        pass
    finally:
        server_socket.close()


if __name__ == "__main__":
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    try:
        # if port is provided on cmdline, then use it
        if len(sys.argv) > 2:
            PORT = int(sys.argv[2])
    except ValueError as ve:
        print(ve)

    start_server(IP, PORT)