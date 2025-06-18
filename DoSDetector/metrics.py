from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import numpy as np
import time
import netifaces
from detection import AttackDetector
from blacklist import BlacklistManager
from logger import setup_logger
import subprocess
import re
import sys
import argparse
import signal
import threading


class MetricsExtractor:
    def __init__(self, iface=None):
        self.iface = iface
        self._stop_sniff = False
        self.logger = setup_logger('packets.log')
        self.detector = AttackDetector()
        self.flows = {}
        self.blacklist_manager = BlacklistManager(logger='blacklist.log')

        

    def reset_metrics_for_ip(self, ip):
        self.flows[ip] = {
            'start_time': None,
            'end_time': None,
            'dest_ports': [],
            'fin_flag_count': 0,
            'syn_flag_count': 0,
            'rst_flag_count': 0,
            'psh_flag_count': 0,
            'ack_flag_count': 0,
            'fwd_psh_flags': 0,
            'fwd_urg_flags': 0,
            'bwd_psh_flags': 0,
            'bwd_urg_flags': 0,
            'fwd_packet_lengths': [],
            'bwd_packet_lengths': [],
            'fwd_times': [],
            'bwd_times': [],
            'fwd_iat_list': [],
            'bwd_iat_list': []
        }

    def process_packet(self, pkt):
        if IP not in pkt:
            return None

        pkt_time = pkt.time
        src = pkt[IP].src
        dst = pkt[IP].dst

        if src not in self.flows:
            self.reset_metrics_for_ip(src)

        flow = self.flows[src]

        if flow['start_time'] is None:
            flow['start_time'] = pkt_time
        flow['end_time'] = pkt_time

        dport = 0
        if TCP in pkt:
            dport = pkt[TCP].dport
        elif UDP in pkt:
            dport = pkt[UDP].dport

        flow['dest_ports'].append(dport)
       

        pkt_len = len(pkt)
        flags = pkt[TCP].flags if TCP in pkt else 0

        if flags & 0x01: flow['fin_flag_count'] += 1
        if flags & 0x02: flow['syn_flag_count'] += 1
        if flags & 0x04: flow['rst_flag_count'] += 1
        if flags & 0x08: flow['psh_flag_count'] += 1
        if flags & 0x10: flow['ack_flag_count'] += 1

        if pkt[IP].src == src:
            flow['fwd_packet_lengths'].append(pkt_len)
            if flags & 0x08: flow['fwd_psh_flags'] += 1
            if flags & 0x20: flow['fwd_urg_flags'] += 1
            if flow['fwd_times']:
                flow['fwd_iat_list'].append(pkt_time - flow['fwd_times'][-1])
            flow['fwd_times'].append(pkt_time)
        else:
            flow['bwd_packet_lengths'].append(pkt_len)
            if flags & 0x08: flow['bwd_psh_flags'] += 1
            if flags & 0x20: flow['bwd_urg_flags'] += 1
            if flow['bwd_times']:
                flow['bwd_iat_list'].append(pkt_time - flow['bwd_times'][-1])
            flow['bwd_times'].append(pkt_time)

        flow_duration = flow['end_time'] - flow['start_time']
        if flow_duration >= 1:
            metrics = self.get_metrics(flow)
            self.reset_metrics_for_ip(src)
            return src, metrics

        return None

    @staticmethod
    def safe_stats(data):
        return {
            'sum': float(np.sum(data)) if data else 0,
            'mean': float(np.mean(data)) if data else 0,
            'max': float(np.max(data)) if data else 0,
            'min': float(np.min(data)) if data else 0,
            'std': float(np.std(data)) if data else 0,
            'var': float(np.var(data)) if data else 0,
            'count': len(data)
        }

    def get_metrics(self, flow):
        flow_duration = flow['end_time'] - flow['start_time']

        fwd_stats = self.safe_stats(flow['fwd_packet_lengths'])
        bwd_stats = self.safe_stats(flow['bwd_packet_lengths'])

        all_pkt_lengths = flow['fwd_packet_lengths'] + flow['bwd_packet_lengths']
        all_stats = self.safe_stats(all_pkt_lengths)

        flow_bytes_per_s = all_stats['sum'] / flow_duration if flow_duration > 0 else 0
        flow_packets_per_s = all_stats['count'] / flow_duration if flow_duration > 0 else 0
        fwd_packets_per_s = fwd_stats['count'] / flow_duration if flow_duration > 0 else 0
        bwd_packets_per_s = bwd_stats['count'] / flow_duration if flow_duration > 0 else 0

        all_times = sorted(flow['fwd_times'] + flow['bwd_times'])
        flow_iats = [t2 - t1 for t1, t2 in zip(all_times[:-1], all_times[1:])]
        flow_iat_stats = self.safe_stats(flow_iats)
        fwd_iat_stats = self.safe_stats(flow['fwd_iat_list'])
        bwd_iat_stats = self.safe_stats(flow['bwd_iat_list'])

        destination_port = max(set(flow['dest_ports']), key=flow['dest_ports'].count) if flow['dest_ports'] else 0

        return {
            'Destination Port': destination_port,
            'Flow Duration': flow_duration,
            'Total Fwd Packets': fwd_stats['count'],
            'Total Backward Packets': bwd_stats['count'],
            'Total Length of Fwd Packets': fwd_stats['sum'],
            'Total Length of Bwd Packets': bwd_stats['sum'],
            'Fwd Packet Length Max': fwd_stats['max'],
            'Fwd Packet Length Min': fwd_stats['min'],
            'Fwd Packet Length Mean': fwd_stats['mean'],
            'Fwd Packet Length Std': fwd_stats['std'],
            'Bwd Packet Length Max': bwd_stats['max'],
            'Bwd Packet Length Min': bwd_stats['min'],
            'Bwd Packet Length Mean': bwd_stats['mean'],
            'Bwd Packet Length Std': bwd_stats['std'],
            'Flow Bytes/s': flow_bytes_per_s,
            'Flow Packets/s': flow_packets_per_s,
            'Fwd Packets/s': fwd_packets_per_s,
            'Bwd Packets/s': bwd_packets_per_s,
            'Min Packet Length': all_stats['min'],
            'Max Packet Length': all_stats['max'],
            'Packet Length Mean': all_stats['mean'],
            'Packet Length Std': all_stats['std'],
            'Packet Length Variance': all_stats['var'],
            'Flow IAT Mean': flow_iat_stats['mean'],
            'Flow IAT Std': flow_iat_stats['std'],
            'Flow IAT Max': flow_iat_stats['max'],
            'Flow IAT Min': flow_iat_stats['min'],
            'Fwd IAT Total': fwd_iat_stats['sum'],
            'Fwd IAT Mean': fwd_iat_stats['mean'],
            'Fwd IAT Std': fwd_iat_stats['std'],
            'Fwd IAT Max': fwd_iat_stats['max'],
            'Fwd IAT Min': fwd_iat_stats['min'],
            'Bwd IAT Total': bwd_iat_stats['sum'],
            'Bwd IAT Mean': bwd_iat_stats['mean'],
            'Bwd IAT Std': bwd_iat_stats['std'],
            'Bwd IAT Max': bwd_iat_stats['max'],
            'Bwd IAT Min': bwd_iat_stats['min'],
            'FIN Flag Count': flow['fin_flag_count'],
            'SYN Flag Count': flow['syn_flag_count'],
            'RST Flag Count': flow['rst_flag_count'],
            'PSH Flag Count': flow['psh_flag_count'],
            'ACK Flag Count': flow['ack_flag_count'],
            'Fwd PSH Flags': flow['fwd_psh_flags'],
            'Bwd PSH Flags': flow['bwd_psh_flags'],
            'Fwd URG Flags': flow['fwd_urg_flags'],
            'Bwd URG Flags': flow['bwd_urg_flags']
        }

    def packet_callback(self, pkt):
        self.last_packet_time = time.time()
        result = self.process_packet(pkt)
        if result:
            src, metrics = result
            if self.blacklist_manager.is_blacklisted(src):     
                return
            if metrics['Destination Port'] == 8080:
                print(f"[{src}] Flow metrics extracted: {metrics['Destination Port']}, Duration: {metrics['Flow Duration']:.2f}s")
                self.logger.info(f"[{src}] Metrics: {metrics}")
                prediction = self.detector.predict(metrics)
                print(f"Prediction: {prediction}")
                if prediction != "BENIGNO":
                    warnings, blacklisted = self.blacklist_manager.add_warning(src, "DoS " + prediction)
                    print(f"[{prediction}] Warning {warnings} for {src}")
                    print(f"Current blacklist state for {src}: {self.blacklist_manager.blacklist_local[src]}")
                    if blacklisted:
                        print(f"[{src}] Blacklisted after {warnings} warnings.")
                else:
                    print(f"[{src}] Flow is benign, resetting warnings.")
                    self.blacklist_manager.reset_warnings(src)

    def start_sniffing(self, count=0, idle_timeout=5, timeout=300):
        print(f"Starting sniffing on interface: {self.iface}")
        self.reset_metrics()
        self.last_packet_time = None
        self._stop_sniff = False
        self.idle_timeout = idle_timeout

        sniff(
            iface=self.iface,
            prn=self.packet_callback,
            stop_filter=self.stop_filter,
            count=count,
            timeout=timeout
        )
        print("Sniffing finished.")

    def stop_filter(self, pkt):
        if self._stop_sniff:
            return True
    
        current_time = time.time()
        if self.last_packet_time is None:
            self.last_packet_time = current_time
            return False
        elif current_time - self.last_packet_time > self.idle_timeout:
            self._stop_sniff = True
            self.logger.info("Idle timeout reached, resetting metrics")
            self.reset_metrics()
            return True
        else:
            self.last_packet_time = current_time
            return False

    def reset_metrics(self):
        self.flows.clear()
    
    


if __name__ == "__main__":
    def signal_handler(sig, frame):
        print("\n[!] Ctrl+C detected. Stopping sniffing...")
        extractor._stop_sniff = True
        sys.exit(0)

    interfaces = netifaces.interfaces()
    interfaz = None
    
    parser = argparse.ArgumentParser(description="DoS Detector Metrics Extractor and Traffic Monitorer")
    parser.add_argument('--ip', type=str, help="Server's IP or partial IP")
    parser.add_argument('--port', type=str, help="Server's Port")
    args = parser.parse_args()

    # If the user provides 'help' as an argument, show usage and exit
    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help") or (args.ip and args.ip.lower() == "help") or (args.port and args.port.lower() == "help"):
        parser.print_help()
        sys.exit(0)

    if args.ip:
        src = args.ip
    else:
        src = input("Indicate the Server's IP or partial IP: ")

    if args.port:
        port = args.port
    else:
        port = input("Indicate Server's Port: ")

    # Check if src is a valid IP using regex
    ip_regex = r"^([0-9]{1,3}\.?){1,4}$"
    if not re.match(ip_regex, src):
        src = "192.168.1."

    # Check if port is a valid TCP/UDP port (0-65535)
    port_regex = r"^([0-9]{1,5})$"
    if not (re.match(port_regex, port) and 0 <= int(port) <= 65535):
        port = "8080"

    for interface in interfaces:
        try:
            ip_address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            if ip_address.startswith(src):
                interfaz = interface
                print(f"Interface: {interface}, IP: {ip_address}")
                interfaz = r"\Device\NPF_" + interfaz
                break
        except Exception:
            continue

    if not interfaz:
        raise RuntimeError(f"No se encontró una interfaz con IP '{src}'")

    extractor = MetricsExtractor(iface=interfaz)



    signal.signal(signal.SIGINT, signal_handler)

    extractor.start_sniffing(timeout=900)
