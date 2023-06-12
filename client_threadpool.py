import sys
import socket
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Set basic logging
logging.basicConfig(level=logging.INFO)


def kirim_data():
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
        return 1  # Return 1 to indicate successful request and response
    except:
        return 0  # Return 0 to indicate failed request and response
    finally:
        logging.warning("Testing Done")
        sock.close()


if __name__ == '__main__':
    max_threads = 0
    max_threads2 = 0
    execution_time = 10  # Set the execution time to 20 seconds

    start_time = time.time()
    end_time = start_time + execution_time

    total_requests = 0
    successful_responses = 0

    with ThreadPoolExecutor() as executor:
        while time.time() < end_time:
            future = executor.submit(kirim_data)
            total_requests += 1

            if future.result() == 1:
                successful_responses += 1

            # Sleep for a short time before spawning the next thread
            time.sleep(0.1)

            max_threads = max(max_threads, executor._max_workers)
            # nilai executor._max_workers akan didapatkan dari jumlah cpu yang tersedia
            active_threads = threading.active_count()  
            # Get the number of active threads menggunakan threading

            max_threads2 = max(max_threads2, active_threads)

    print(f"Jumlah maksimum thread yang dapat dieksekusi dalam jangka waktu {execution_time} detik adalah {max_threads} thread - didapat dari executor")
    print(f"Jumlah maksimum thread yang dapat dieksekusi dalam jangka waktu {execution_time} detik adalah {max_threads2} thread - didapat dari threading")
    print(f"Total requests: {total_requests}")
    print(f"Successful responses: {successful_responses}")
