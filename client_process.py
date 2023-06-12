import sys
import socket
import logging
import multiprocessing
import threading
import time
import resource

# Set basic logging
logging.basicConfig(level=logging.INFO)


def kirim_data(counters):
    total_requests, successful_responses = counters  # Unpack counters

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("Membuka socket")

    server_address = ('172.22.0.2', 45001)
    logging.warning(f"Opening socket {server_address}")
    sock.connect(server_address)
    sock.settimeout(20)  # Set a timeout of 20 seconds

    try:
        # Send data
        message = 'TIME Testing\r\n'
        logging.warning(f"[CLIENT] Sending {message}")
        sock.sendall(message.encode('utf-8'))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            try:
                data = sock.recv(1024).decode('utf-8')
            except socket.timeout:
                logging.warning("Timeout occurred. Closing the socket.")
                break

            amount_received += len(data)
            logging.warning(f"[DITERIMA DARI SERVER] {data}")

        logging.info("[CLIENT] Request sent and response received.")
        with total_requests.get_lock():
            total_requests.value += 1  # Increment total requests
        with successful_responses.get_lock():
            successful_responses.value += 1  # Increment successful responses
        return 1  # Return 1 to indicate successful request and response
    except:
        with total_requests.get_lock():
            total_requests.value += 1  # Increment total requests
        return 0  # Return 0 to indicate failed request and response
    finally:
        logging.warning("Testing Done")
        sock.close()


if __name__ == '__main__':
    max_processes = 0
    max_threads = 0
    execution_time = 10  # Set the execution time to 10 seconds

    total_requests = multiprocessing.Value('i', 0)
    successful_responses = multiprocessing.Value('i', 0)

    # Set the maximum number of open files to a large value (e.g., 10000)
    resource.setrlimit(resource.RLIMIT_NOFILE, (10000, 10000))

    start_time = time.time()
    end_time = start_time + execution_time

    processes = []
    while time.time() < end_time:
        process = multiprocessing.Process(target=kirim_data, args=((total_requests, successful_responses),))
        process.start()
        processes.append(process)
        count = len(processes)
        if count > max_processes:
            max_processes = count

        active_threads = threading.active_count()
        if active_threads > max_threads:
            max_threads = active_threads

    for process in processes:
        process.join()

    print(f"Jumlah maksimum proses yang dieksekusi dalam jangka waktu {execution_time} detik adalah {max_processes} proses")
    print(f"Jumlah maksimum thread yang dapat dieksekusi dalam jangka waktu {execution_time} detik adalah {max_threads} thread")
    print(f"Total requests: {total_requests.value}")
    print(f"Successful responses: {successful_responses.value}")
