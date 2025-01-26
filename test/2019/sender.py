import json
import socket
import time

with open("./2019/run.json", "r") as f:
    data = json.load(f)

# fwd_packet_length_max, fwd_packet_length_min, fwd_packet_length_mean, packet_length_min, packet_length_max, packet_length_mean, avg_packet_size, avg_fwd_segment_size
# USE = [fwd_packet_length_max, fwd_packet_length_min, fwd_packet_length_mean, packet_length_min, packet_length_max, packet_length_mean, avg_packet_size, avg_fwd_segment_size]
USE = data['data']


def sender():
    host = data['IP']
    port = 8000

    forward_packet_lengths = [
        USE[1],
        USE[0],
        int(USE[2]),
    ]

    while len(forward_packet_lengths) < 5:
        forward_packet_lengths.append(USE[2])

    print("Forward Packet Lengths:", forward_packet_lengths)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for packet_length in forward_packet_lengths:
            packet = b"A" * packet_length
            s.sendall(packet)
            print(f"Sent forward packet of size: {packet_length} bytes")
            time.sleep(0.5)

        s.sendall(b"END")


sender()
