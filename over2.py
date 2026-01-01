import numpy as np

A = [
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]

B = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

rows_above = 0
rows_below = 0
cols_right = 0

x1, y1 = 1, 2
x2, y2 = 2, 1

if x2-x1 > 0:
    rows_above = x2-x1

if len(B)-x2-1 - (len(A)-x1-1) > 0:
    rows_below = len(B)-x2-1 - (len(A)-x1-1)

cols_right = len(B[0]) - (len(A[0])-y1-1)

h = len(A)
w = len(A[0])

out = [[0] * (w + cols_right) for _ in range(h + rows_above + rows_below)]

for i in range(h):
    for j in range(w):
        out[i + rows_above][j] = A[i][j]


for i in range(len(out)):
    for j in range(len(out[0])):
        print(out[i][j], end="")
    print()

print()

start_x = (x1 + rows_above) - x2
start_y = y1 - y2 + 1

print(start_x)
print(start_y)
print(len(out))
print(len(out[0]))

for i in range(len(B)):
    for j in range(len(B[0])):
        out[start_x + i][start_y + j] = 2
        if i == x2 and j == y2:
            out[start_x + i][start_y + j] = 5


for i in range(len(out)):
    for j in range(len(out[0])):
        print(out[i][j], end="")
    print()




