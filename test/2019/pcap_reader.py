import json
import pyshark
import numpy as np


def calculate_metrics(pcap_file):
    fwd_lengths = []
    all_lengths = []

    capture = pyshark.FileCapture(pcap_file)
    try:
        for packet in capture:
            try:
                length = int(packet.length)
                all_lengths.append(length)

                if hasattr(packet, 'tcp') and packet.tcp.flags_ack == "True":
                    fwd_lengths.append(length)
            except AttributeError:
                continue
    finally:
        capture.close()

    fwd_packet_length_max = max(fwd_lengths) if fwd_lengths else 0
    fwd_packet_length_min = min(fwd_lengths) if fwd_lengths else 0
    fwd_packet_length_mean = round(np.mean(fwd_lengths)) if fwd_lengths else 0
    packet_length_max = max(all_lengths) if all_lengths else 0
    packet_length_min = min(all_lengths) if all_lengths else 0
    packet_length_mean = round(np.mean(all_lengths)) if all_lengths else 0
    avg_packet_size = round(np.mean(all_lengths)) if all_lengths else 0
    avg_fwd_segment_size = round(np.mean(fwd_lengths)) if fwd_lengths else 0

    return [
        fwd_packet_length_max,
        fwd_packet_length_min,
        fwd_packet_length_mean,
        packet_length_min,
        packet_length_max,
        packet_length_mean,
        avg_packet_size,
        avg_fwd_segment_size,
    ]


if __name__ == "__main__":
    pcap_file = '../test.pcapng'
    metrics = calculate_metrics(pcap_file)
    with open("./../output2.txt", "a") as f:
        f.write(json.dumps(["2019", metrics]) + "\n")
