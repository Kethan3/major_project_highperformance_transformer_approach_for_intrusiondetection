import json
import socket
import statistics
import time


def receiver():
    host = '192.168.1.3'
    port = 8000

    forward_packet_lengths = []
    backward_packet_lengths = [150, 200, 250]  # Static example value
    init_win_bytes_fwd = 65535  # Static example value
    inter_arrival_times = []
    flow_start_time = None
    last_packet_time = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("Listening for connection...")
        conn, addr = s.accept()
        print(f"Connection established with {addr}")

        with conn:
            while True:
                data = conn.recv(1024)  # Receive up to 1024 bytes
                if data == b"END":
                    break
                packet_length = len(data)
                forward_packet_lengths.append(packet_length)

                current_time = time.time()
                if flow_start_time is None:
                    flow_start_time = current_time
                else:
                    inter_arrival_times.append(current_time - last_packet_time)

                last_packet_time = current_time
                print(f"Received packet of size: {packet_length} bytes")

    flow_duration = last_packet_time - flow_start_time
    total_length_bwd = sum(backward_packet_lengths)
    bwd_packet_length_mean = statistics.mean(backward_packet_lengths)
    flow_iat_mean = statistics.mean(inter_arrival_times) if inter_arrival_times else 0
    flow_iat_max = max(inter_arrival_times, default=0)
    fwd_iat_max = max(inter_arrival_times, default=0)
    max_packet_length = max(forward_packet_lengths)
    packet_length_mean = statistics.mean(forward_packet_lengths)
    packet_length_std = statistics.stdev(forward_packet_lengths) if len(forward_packet_lengths) > 1 else 0
    packet_length_variance = packet_length_std ** 2
    avg_packet_size = packet_length_mean
    avg_bwd_segment_size = statistics.mean(backward_packet_lengths)
    subflow_bwd_bytes = total_length_bwd

    with open("./../output.txt", "a") as f:
        f.write(json.dumps(["2017", [
            flow_duration,
            statistics.mean(backward_packet_lengths),
            total_length_bwd,
            bwd_packet_length_mean,
            fwd_iat_max,
            flow_iat_mean,
            flow_iat_max,
            max_packet_length,
            statistics.mean(forward_packet_lengths),
            packet_length_mean,
            packet_length_std,
            packet_length_variance,
            avg_packet_size,
            init_win_bytes_fwd,
        ]]) + "\n")


receiver()
