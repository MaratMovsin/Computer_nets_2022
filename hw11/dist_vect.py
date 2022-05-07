import numpy as np
    

def update_dist(x, y, w):
    not_updated[x] = 1
    while not_updated.sum():
        for i in range(n):
            if not_updated[i]:
                new_vec = np.zeros(n)
                new_vec.fill(np.inf)
                for j in range(n):
                    if i != j and ~np.isinf(adjacency_table[i][j]):
                        not_updated[i]=0
                        for k in range(n):
                            if new_vec[k] > adjacency_table[i][j] + distances[j][k]:
                                new_vec[k] = adjacency_table[i][j] + distances[j][k]
                new_vec[i]=0
                eq = True
                for j in range(n):
                    if distances[i][j] != new_vec[j]:
                        eq=False
                        break
                if not eq:
                    for j in range(n):
                        if i != j and ~np.isinf(adjacency_table[i][j]):
                            not_updated[j]=1
                    distances[i] = new_vec




n = int(input())

adjacency_table = np.zeros((n, n))
adjacency_table.fill(np.inf)
for i in range(n):
    adjacency_table[i][i] = 0

distances = np.copy(adjacency_table)

not_updated = np.zeros(n)

while(1):
    reader = input()
    if reader=='q':
        break
    a, b, c = [int(s) for s in reader.split()]
    if a >= n or b >= n:
        print('Index is out of bounds')
        continue
    adjacency_table[a][b] = c
    adjacency_table[b][a] = c
    update_dist(a, b, c)
    print(distances)


