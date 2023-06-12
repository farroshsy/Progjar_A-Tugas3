import sys
import socket
import logging
import threading
import time

def kirim_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.22.0.2', 45000)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        message = 'TIME Testing\r\n'
        logging.warning(f"[CLIENT] sending {message}")
        sock.sendall(message.encode('utf-8'))
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(1024).decode('utf-8')
            amount_received += len(data)
            logging.warning(f"[DITERIMA DARI SERVER] {data}")
    finally:
        logging.warning("closing")
        sock.close()

def print_thread_count():
    count = 0
    max_count = 0
    start_time = time.time()
    end_time = start_time + 5  # Run for 5 seconds

    while time.time() < end_time:
        count = threading.active_count()
        if count > max_count:
            max_count = count
        print(f"Total thread count: {count}")
        time.sleep(0.01)  # Print thread count every 0.01 second

    print(f"Maximum thread count: {max_count}")

if __name__ == '__main__':
    # Disable logging temporarily
    logging.disable(logging.CRITICAL)

    # Start the thread count monitoring thread
    thread = threading.Thread(target=print_thread_count)
    thread.start()

    # Start a large number of client threads
    threads = []
    for i in range(1000):
        thread = threading.Thread(target=kirim_data)
        thread.start()
        threads.append(thread)

    # Wait for all client threads to finish
    for thread in threads:
        thread.join()

    # Re-enable logging
    logging.disable(logging.NOTSET)

    # Wait for the monitoring thread to complete
    thread.join()
