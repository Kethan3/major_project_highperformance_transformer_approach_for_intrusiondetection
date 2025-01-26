import json
import pyshark
import numpy as np


def calculate_metrics(pcap_file):
    timestamps = []
    packet_lengths = []
    forward_directions = []
    backward_directions = []
    fwd_iat_times = []
    max_packet_length = 0
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    init_win_bytes_fwd = None
    forward_timestamps = []
    backward_timestamps = []

    capture = pyshark.FileCapture(pcap_file)
    try:
        for packet in capture:
            try:
                timestamp = float(packet.sniff_timestamp)
                timestamps.append(timestamp)

                length = int(packet.length)
                packet_lengths.append(length)
                max_packet_length = max(max_packet_length, length)

                if hasattr(packet, 'ip'):
                    src = packet.ip.src
                    dst = packet.ip.dst
                    if not forward_directions and not backward_directions:
                        forward_directions.append(src)
                    if src in forward_directions:
                        fwd_packet_lengths.append(length)
                        forward_timestamps.append(timestamp)
                    else:
                        bwd_packet_lengths.append(length)
                        backward_timestamps.append(timestamp)

                    if "TCP" in packet:
                        if init_win_bytes_fwd is None:
                            init_win_bytes_fwd = int(packet.tcp.window_size)

            except AttributeError:
                continue
    finally:
        capture.close()

    flow_duration = max(timestamps) - min(timestamps)
    timestamps = sorted(timestamps)
    iat_times = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
    flow_iat_mean = np.mean(iat_times)
    flow_iat_max = max(iat_times)

    forward_timestamps = sorted(forward_timestamps)
    fwd_iat_times = [forward_timestamps[i + 1] - forward_timestamps[i] for i in range(len(forward_timestamps) - 1)]
    fwd_iat_max = max(fwd_iat_times) if fwd_iat_times else 0

    return [
        flow_duration,
        np.mean(bwd_packet_lengths),
        sum(bwd_packet_lengths),
        np.mean(bwd_packet_lengths),
        fwd_iat_max,
        flow_iat_mean,
        flow_iat_max,
        max_packet_length,
        np.mean(fwd_packet_lengths),
        np.mean(packet_lengths),
        np.std(packet_lengths),
        np.var(packet_lengths),
        np.mean(packet_lengths),
        init_win_bytes_fwd,
    ]


if __name__ == "__main__":
    pcap_file = '../test.pcapng'
    metrics = calculate_metrics(pcap_file)
    with open("./../output2.txt", "a") as f:
        f.write(json.dumps(["2017", metrics]) + "\n")
