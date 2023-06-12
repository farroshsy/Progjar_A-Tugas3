import sys
import socket
import logging
import threading
import time

# Set basic logging
logging.basicConfig(level=logging.INFO)


def kirim_data(counters):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.warning("membuka socket")

    server_address = ('172.22.0.2', 45001)
    logging.warning(f"opening socket {server_address}")
    sock.connect(server_address)
    sock.settimeout(20)  # Set a timeout of 20 seconds

    try:
        # Send data
        message = 'TIME Testing\r\n'
        logging.warning(f"[CLIENT] sending {message}")
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
        counters[0] += 1  # Increment total requests
        counters[1] += 1  # Increment successful responses
    except:
        logging.warning("[CLIENT] Failed to send request or receive response.")
        counters[0] += 1  # Increment total requests
    finally:
        logging.warning("Testing Done")
        sock.close()


if __name__ == '__main__':
    time_test = 10
    threads = []
    max_threads = 0
    counters = [0, 0]  # [total_requests, successful_responses]

    start = time.perf_counter()

    while time.perf_counter() - start < time_test:
        thread = threading.Thread(target=kirim_data, args=(counters,))
        thread.start()
        threads.append(thread)
        count = threading.active_count()
        if count > max_threads:
            max_threads = count

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    total_requests = counters[0]
    successful_responses = counters[1]

    print(f"Jumlah maksimum thread yang dapat dieksekusi dalam jangka waktu {time_test} detik adalah {max_threads} thread")
    print(f"Total requests: {total_requests}")
    print(f"Successful responses: {successful_responses}")
