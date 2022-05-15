import argparse
import numpy as np

routers = dict()
ips = set()

class Table():
    def __init__(self):
        self.dists = dict()
        self.next = dict()

class Router():
    def __init__(self, ip):
        self.ip = ip
        self.neighbours = set()
        self.table = Table()
        self.neighbours_tables = dict()
        
    def make_link(self, ip):
        self.neighbours.add(ip)
        self.table.dists[ip] = 1
        self.table.next[ip] = ip
        
    def init_with_inf(self):
        for neighbour in self.neighbours:
            self.neighbours_tables[neighbour] = Table()
            for ip in ips:
                self.neighbours_tables[neighbour].dists[ip] = np.inf
                self.neighbours_tables[neighbour].next[ip] = 'None'
        for ip in ips:
            self.table.dists[ip] = np.inf
            self.table.next[ip] = 'None'
        self.table.dists[self.ip] = 0
        self.table.next[self.ip] = 0
        
    def update_neighbours_tables(self):
        for neighbour in self.neighbours:
            for ip in ips:
                self.neighbours_tables[neighbour].dists[ip] = routers[neighbour].table.dists[ip]
                self.neighbours_tables[neighbour].next[ip] = routers[neighbour].table.next[ip]
        
    def update_table(self):
        for ip in ips:
            self.table.dists[ip] = np.inf
        for ip1 in self.neighbours:
            if ip1 == self.ip:
                continue
            for ip2 in ips:
                ww = self.neighbours_tables[ip1].dists[ip2]
                if self.table.dists[ip2] > self.neighbours_tables[ip1].dists[ip2]+1:
                    self.table.dists[ip2] = self.neighbours_tables[ip1].dists[ip2]+1
                    self.table.next[ip2] = ip1
        self.table.dists[self.ip] = 0
        self.table.next[self.ip] = 0
    
    def print_table(self, it):
        if it == -1:
            epoch = 'Final state'
        else:
            epoch = f'Simulation step {it}'
        print(f'{epoch} of router {self.ip} table:')
        print('[Source IP]          [Destination IP]     [Next Hop]      [Metric]')
        for ip in ips:
            if ip != self.ip and not np.isinf(self.table.dists[ip]):
                print(f'{self.ip:20} {ip:20} {self.table.next[ip]:20} {self.table.dists[ip]:3}')
        print('')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    
    with open(args.filename, 'r') as file:
        n = int(file.readline())
        for i in range(n):
            ip = file.readline()[:-1]
            ips.add(ip)
            routers[ip] = Router(ip)
        m = int(file.readline())
        for i in range(m):
            ip1, ip2 = file.readline().split()
            routers[ip1].make_link(ip2)
            routers[ip2].make_link(ip1)
        for ip in ips:
            routers[ip].init_with_inf()
        for it in range(n):
            for ip in ips:
                routers[ip].update_neighbours_tables()
            for ip in ips:
                routers[ip].update_table()
            for ip in ips:
                routers[ip].print_table(it)
    for ip in ips:
        routers[ip].print_table(-1)


if __name__ == '__main__':
    main()
