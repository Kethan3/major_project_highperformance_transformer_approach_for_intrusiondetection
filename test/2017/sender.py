import json
import socket
import time
import random

fwd_packet_lengths = [100, 200, 300, 400, 500]

with open("./2017/run.json", "r") as f:
    data = json.load(f)
# flow_duration, bwd_packet_lengths, total_length_bwd, bwd_packet_length_mean, fwd_iat_max, flow_iat_mean, flow_iat_max, max_packet_length, fwd_packet_lengths, packet_length_mean, packet_length_std, packet_length_variance, avg_packet_size, init_win_bytes_fwd
# USE = [flow_duration, bwd_packet_lengths, total_length_bwd, bwd_packet_length_mean, fwd_iat_max, flow_iat_mean, flow_iat_max, max_packet_length, fwd_packet_lengths, packet_length_mean, packet_length_std, packet_length_variance, avg_packet_size, init_win_bytes_fwd]
USE = data['data']


def sender():
    host = data['IP']
    port = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        start_time = time.time()

        for packet_length in fwd_packet_lengths:
            packet = b"A" * packet_length
            s.sendall(packet)
            print(f"Sent forward packet of size: {packet_length} bytes")
            # time.sleep(random.uniform(0.5, USE[6]))
            time.sleep(0.5)

        s.sendall(b"END")
        end_time = time.time()

        print(f"Flow Duration: {end_time - start_time:.3f} seconds")


sender()
