A = [
    [1, 1, 0, 0],
    [1, 1, 1, 0],
    [1, 1, 0, 0]
]

B = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1],
]

# anchors
r1, c1 = 0, 1
r2, c2 = 1, 3

# desired placement of B
target_r, target_c = r1, c1 + 1

row_offset = target_r - r2
col_offset = target_c - c2

# collect all occupied coordinates
coords = []

for i in range(len(A)):
    for j in range(len(A[0])):
        coords.append((i, j))

for i in range(len(B)):
    for j in range(len(B[0])):
        coords.append((i + row_offset, j + col_offset))

min_r = min(r for r, _ in coords)
max_r = max(r for r, _ in coords)
min_c = min(c for _, c in coords)
max_c = max(c for _, c in coords)

H = max_r - min_r + 1
W = max_c - min_c + 1

canvas = [[None for _ in range(W)] for _ in range(H)]


def place(mat, ro, co, do_and):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            r = i + ro - min_r
            c = j + co - min_c
            if canvas[r][c] is None:
                canvas[r][c] = mat[i][j]
            else:
                if do_and:
                    canvas[r][c] |= mat[i][j]


place(A, 0, 0, False)
place(B, row_offset, col_offset, True)

for row in canvas:
    print(row)
