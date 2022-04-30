import argparse
import socket
import base64
import numpy as np
import time
import struct
import select
import random
import asyncore



def check_sum(byte_arr):
    byte_list = list()
    for byte in byte_arr:
        byte_list.append(byte)
    np_byte_arr = np.flip(np.array(byte_list))
    if np_byte_arr.shape[0]%2:
        np_byte_arr = np.hstack((np.zeros(1), np_byte_arr))
    byte_mat = np_byte_arr.reshape(-1, 2)
    return int(65535 - ((byte_mat @ np.array([256,1])).sum() % 65536))


def create_packet(packet_id):
    data = bytes(str(time.time()), 'utf-8')
    packet = struct.pack('bbHHbs', 8, 0, 0, packet_id, 1, data)
    return struct.pack('bbHHbs', 8, 0, check_sum(packet), packet_id, 1, data)


def receive_ping(my_socket, packet_id, time_sent, timeout):
    time_left = timeout
    while True:
        started_select = time.time()
        ready = select.select([my_socket], [], [], time_left)
        if ready[0] == []:
            return
        time_received = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        if check_sum(icmp_header) != 0:
            print('Incorrect checksum')
            return
        _, _, _, p_id, _ = struct.unpack(
            'bbHHh', icmp_header)
        if p_id == packet_id:
            return time_received - time_sent
        time_left -= time_received - time_sent
        if time_left <= 0:
            return


def send_packet(dest_addr, timeout=1):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    
    packet_id = int(random.random() % 65535)
    packet = create_packet(packet_id)
    
    while packet:
        sent = my_socket.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]
        
    delay = receive_ping(my_socket, packet_id, time.time(), timeout)
    my_socket.close()
    return delay
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('hostname', type=str)
    args = parser.parse_args()
    
    times = list()
    lost = 0
    n = args.number
    for i in range(n):
        delay = send_packet(args.hostname)
        if delay is None:
            print('Failed')
            lost += 1
        else:
            times.append(delay)
            print(f'{i+1} packets transmitted, {i+1-lost} received, {lost/(i+1)*100 :.3f}% packet loss, rtt min/avg/max = {min(times) :.3f}/{sum(times)/(i+1) :.3f}/{max(times) :.3f} ms')
    
    if lost == n:
        print('lost 100%')


if __name__ == '__main__':
    main()
