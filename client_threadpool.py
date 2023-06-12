import sys
import socket
import logging
import threading
import concurrent.futures
import multiprocessing

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

def run_with_threads():
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=kirim_data)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def run_with_threadpool():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10):
            future = executor.submit(kirim_data)
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(str(e))

def run_with_processes():
    with multiprocessing.Pool() as pool:
        results = [pool.apply_async(kirim_data) for _ in range(10)]
        for result in results:
            result.get()

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    run_with_threads()
    run_with_threadpool()
    run_with_processes()
