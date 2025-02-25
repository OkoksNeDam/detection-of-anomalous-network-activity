from abc import ABC, abstractmethod
import numpy as np

from scapy.all import *
from scapy.contrib.mpls import MPLS
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether, Dot1Q

from exceptions.file_exceptions import FileExtensionException


class FlowFileProcessorService(ABC):
    FILE_EXTENSION = None
    FEATURE_LIST = None

    def __init__(self, filepath: str):
        self.__filepath = filepath

    @abstractmethod
    def process(self): pass


class FlowPCAPProcessorService(FlowFileProcessorService):
    """
    Обработка и извлченение данных из файлов расширения pcap.
    """

    __FILE_EXTENSION = ".pcap"
    FEATURE_LIST = ['packets_number', 'total_packets_len', 'flow_duration', 'max_packet_len',
                    'min_packet_len', 'mean_packet_len', 'std_packet_len', 'flow_IAT_mean', 'flow_IAT_std',
                    'flow_IAT_max', 'flow_IAT_min', 'flow_IAT_total', 'total_headers_len',
                    'packets/s', 'FIN_flag_count', 'SYN_flag_count', 'RST_flag_count', 'PUSH_flag_count',
                    'ACK_flag_count']

    def __init__(self, filepath: str):
        super().__init__(filepath)
        _, file_extension = os.path.splitext(filepath)
        if file_extension != self.__FILE_EXTENSION:
            raise FileExtensionException(message=f"Файлы расширения {file_extension} не поддерживаются.")
        self.__packets = rdpcap(filepath)

    def __get_packets_number(self) -> tuple:
        """
        Считает количество пакетов в файле.
        """
        return len(self.__packets),

    def __get_total_packets_length(self) -> tuple:
        """
        Считает суммарную длину пакетов в файле.
        """
        return np.sum(list(map(len, self.__packets))),

    def __get_flow_duration(self) -> tuple:
        """
        Считает длительность потока в микросекундах.
        """
        first_packet_time = self.__packets[0].time
        last_packet_time = self.__packets[-1].time

        flow_duration = float((last_packet_time - first_packet_time) * 1_000_000)
        return flow_duration,

    def __get_max_packet_length(self) -> tuple:
        """
        Считает максимальный размер пакета в потоке.
        """
        return np.max(list(map(len, self.__packets))),

    def __get_min_packet_length(self) -> tuple:
        """
        Считает минимальный размер пакета в потоке.
        """
        return np.max(list(map(len, self.__packets))),

    def __get_mean_packet_length(self) -> tuple:
        """
        Считает средний размер пакета в потоке.
        """
        return np.mean(list(map(len, self.__packets))),

    def __get_std_packet_length(self) -> tuple:
        """
        Считает стандартное отклонение размера пакетов в потоке.
        """
        return np.std(list(map(len, self.__packets))),

    def __get_flow_IAT_info(self) -> tuple:
        """
        Считает среднее, стандартное отклонение, максимум, минимум и сумму времени
        между двумя пакетами в потоке.
        :return: tuple из посчитанных значений:
        (mean_time_diff, std_time_diff, max_time_diff, min_time_diff, total_time_diff)
        """
        if len(self.__packets) < 2:
            return 0,

        time_diffs = []
        prev_time = self.__packets[0].time

        for packet in self.__packets[1:]:
            current_time = packet.time
            time_diff = float((current_time - prev_time) * 1_000_000)
            time_diffs.append(time_diff)
            prev_time = current_time

        mean_time_diff = np.mean(time_diffs)
        std_time_diff = np.std(time_diffs)
        max_time_diff = np.max(time_diffs)
        min_time_diff = np.min(time_diffs)
        total_time_diff = np.sum(time_diffs)

        return mean_time_diff, std_time_diff, max_time_diff, min_time_diff, total_time_diff

    def __get_total_headers_length(self) -> tuple:
        """
        Считает общее количество байт, которые используются для заголовков.
        """
        HEADER_SIZES = {
            Ether: 14,  # Ethernet header
            IP: 20,  # IPv4 header
            IPv6: 40,  # IPv6 header
            TCP: 20,  # TCP header
            UDP: 8,  # UDP header
            ICMP: 8,  # ICMP header
            Dot1Q: 4,  # VLAN (802.1Q) header
            MPLS: 4,  # MPLS header (per label)
        }
        total_bytes = 0

        for packet in self.__packets:
            for layer, size in HEADER_SIZES.items():
                if layer in packet:
                    # Для MPLS учитываем количество labels
                    if layer == MPLS:
                        total_bytes += size * len(packet[layer])
                    else:
                        total_bytes += size

        return total_bytes,

    def __get_packets_per_second(self) -> tuple:
        """
        Считает среднее число пакетов за каждую секунду.
        """
        packets_per_second = defaultdict(int)

        for packet in self.__packets:
            second = int(packet.time)
            packets_per_second[second] += 1

        if not packets_per_second:
            return 0,

        total_packets = sum(packets_per_second.values())
        total_seconds = len(packets_per_second)
        return total_packets / total_seconds,

    def __get_number_of_flags(self) -> tuple:
        """
        Считает количество пакетов с флагами FIN, SYN, RST, PUSH, ACK.
        """
        FLAGS = {
            'FIN': 0x01,
            'SYN': 0x02,
            'RST': 0x04,
            'PUSH': 0x08,
            'ACK': 0x10,
        }
        flag_counts = {flag: 0 for flag in FLAGS}

        for packet in self.__packets:
            if TCP in packet:
                tcp_flags = packet[TCP].flags
                for flag, value in FLAGS.items():
                    if tcp_flags & value:
                        flag_counts[flag] += 1

        return tuple(flag_counts.values())

    def process(self) -> tuple:
        """
        Ивзлечение данных из файла pcap.
        :return: tuple с данными, ивзлеченными из файла.
        """
        processed_flow = ()
        processed_flow += self.__get_packets_number()
        processed_flow += self.__get_total_packets_length()
        processed_flow += self.__get_flow_duration()
        processed_flow += self.__get_max_packet_length()
        processed_flow += self.__get_min_packet_length()
        processed_flow += self.__get_mean_packet_length()
        processed_flow += self.__get_std_packet_length()
        processed_flow += self.__get_flow_IAT_info()
        processed_flow += self.__get_total_headers_length()
        processed_flow += self.__get_packets_per_second()
        processed_flow += self.__get_number_of_flags()
        return processed_flow
