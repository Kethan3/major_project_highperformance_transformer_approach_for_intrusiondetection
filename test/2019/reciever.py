import json
import socket
import statistics


def receiver():
    host = '192.168.1.3'
    port = 8000

    forward_packet_lengths = []
    all_packet_lengths = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("Listening for connection...")
        conn, addr = s.accept()
        print(f"Connection established with {addr}")

        with conn:
            while True:
                data = conn.recv(1024)
                if data == b"END":
                    break
                packet_length = len(data)
                forward_packet_lengths.append(packet_length)
                all_packet_lengths.append(packet_length)
                print(f"Received packet of size: {packet_length} bytes")

    fwd_packet_length_max = max(forward_packet_lengths)
    fwd_packet_length_min = min(forward_packet_lengths)
    fwd_packet_length_mean = statistics.mean(forward_packet_lengths)
    packet_length_min = min(all_packet_lengths)
    packet_length_max = max(all_packet_lengths)
    packet_length_mean = statistics.mean(all_packet_lengths)
    avg_packet_size = packet_length_mean
    avg_fwd_segment_size = fwd_packet_length_mean

    with open("./../output.txt", "a") as f:
        f.write(json.dumps(["2019", [
            fwd_packet_length_max,
            fwd_packet_length_min,
            fwd_packet_length_mean,
            packet_length_min,
            packet_length_max,
            packet_length_mean,
            avg_packet_size,
            avg_fwd_segment_size,
        ]]) + "\n")


receiver()
