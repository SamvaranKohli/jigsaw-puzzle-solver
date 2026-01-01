import cv2

offset = 10
R = 100
C = 100
placed = [[None] * C for _ in range(R)]
used = set()
total = 9
pieces = []


def binary_array(name):
    img = cv2.imread(name)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 200, 1, cv2.THRESH_BINARY)

    rows_kept = [row for row in binary if any(row)]

    cols = [j for j in range(len(rows_kept[0]))
            if any(row[j] for row in rows_kept)]

    result = [[row[j] for j in cols] for row in rows_kept]

    def corners(a, b):
        _min = 10000
        x = 0
        y = 0

        for i in range(len(result)):
            for j in range(len(result[i])):
                if result[i][j] == 1:
                    score = a * i + b * j
                    if _min > score:
                        x = i
                        y = j
                        _min = score

        return x, y

    return result, corners(1, 1), corners(1, -1), corners(-1, 1), corners(-1, -1)


def segregate_right(piece, side, top_right_x, bottom_right_x, top_right_y, bottom_right_y):
    if side == "inc":
        _min = 1000

        for i in range(top_right_x, bottom_right_x):
            for j in range(len(piece[i]) - 1, 0, -1):
                if piece[i][j] == 1:
                    _min = min(_min, j)
                    break

        result = piece[top_right_x: bottom_right_x]
        return [row[_min - offset:] for row in result], top_right_y - (min(top_right_y, bottom_right_y) - offset)

    result = piece[top_right_x + 1: bottom_right_x]
    return [row[min(top_right_y, bottom_right_y) - offset:] for row in result], top_right_y - (
            min(top_right_y, bottom_right_y) - offset)


def segregate_bottom(piece, side, bottom_left_y, bottom_right_y, bottom_left_x, bottom_right_x):
    if side == "inc":
        _min = 1000

        for i in range(bottom_left_y, bottom_right_y):
            for j in range(len(piece) - 1, 0, -1):
                if piece[j][i] == 1:
                    _min = min(_min, j)
                    break

        result = piece[_min - offset:]
        return [row[bottom_left_y:bottom_right_y] for row in result], bottom_left_x - (_min - offset)

    result = piece[min(bottom_left_x, bottom_right_x) - offset:]
    return [row[bottom_left_y:bottom_right_y] for row in result], bottom_left_x - (
            min(bottom_left_x, bottom_right_x) - offset)


def segregate_left_top(piece, bottom_left_x, top_right_y):
    result = piece[:bottom_left_x + 1]
    return [row[:top_right_y] for row in result]


def merge_right_bottom(right, bottom, new_top_right_y, new_bottom_left_x):
    rows_to_add = new_bottom_left_x + 1
    rows, cols = len(right), len(right[0])

    new_right = [[0] * cols for _ in range(rows_to_add)] + right

    for i in range(len(bottom)):
        for j in range(len(bottom[0])):
            if new_top_right_y + j >= len(new_right[0]):
                for row in new_right:
                    row.extend([0] * 1)

            new_right[i][new_top_right_y + j] |= bottom[i][j]

    return new_right


def merge(piece_1, piece_2, r1, c1, r2, c2):
    rows_above = 0
    rows_below = 0

    x1, y1 = r1, c1
    x2, y2 = r2, c2

    if x2 - x1 > 0:
        rows_above = x2 - x1

    if len(piece_2) - x2 - 1 - (len(piece_1) - x1 - 1) > 0:
        rows_below = len(piece_2) - x2 - 1 - (len(piece_1) - x1 - 1)

    h = len(piece_1)
    w = len(piece_1[0])

    out = [[0] * w for _ in range(h + rows_above + rows_below)]

    for i in range(h):
        for j in range(w):
            out[i + rows_above][j] = piece_1[i][j]

    start_x = (x1 + rows_above) - x2
    start_y = y1 - y2 + 1

    for i in range(len(piece_2)):
        for j in range(len(piece_2[0])):
            if start_y + j >= len(out[0]):
                for row in out:
                    row.extend([0] * 1)

            out[start_x + i][start_y + j] ^= piece_2[i][j]

    return out


def side_type(piece, r1, r2, c):
    min_ = 1000
    max_ = 0

    for i in range(r1, r2):
        for j in range(0, len(piece[i])):
            if piece[i][j] == 1:
                min_ = min(min_, j)
                max_ = max(max_, j)
                break

    if min_ == 0 and c > 20:
        return "tab"
    elif min_ == 0 and c < 5 and max_ < 10:
        return "st"
    else:
        return "inc"


def rotate_piece(A):
    return list(map(list, zip(*A)))[::-1]


def rotate_piece_point(x, y, W):
    return W - 1 - y, x


def store_piece_type(piece, tlx, tly, trx, try_, blx, bly, brx, bry):
    curA = piece
    TL = (tlx, tly)
    TR = (trx, try_)
    BL = (blx, bly)
    BR = (brx, bry)

    values = []

    for _ in range(4):
        values.append(side_type(curA, TL[0], BL[0], min(TL[1], BL[1])))
        W = len(curA[0])

        TL_r = rotate_piece_point(*TR, W)
        TR_r = rotate_piece_point(*BR, W)
        BR_r = rotate_piece_point(*BL, W)
        BL_r = rotate_piece_point(*TL, W)

        curA = rotate_piece(curA)

        TL, TR, BR, BL = TL_r, TR_r, BR_r, BL_r

    return values


def pre_processing():
    for i in range(1, total + 1):
        folder = "Puzzle3/"
        name = str(i) + ".png"
        piece = {}
        A, (top_left_x, top_left_y), (top_right_x, top_right_y), (bottom_left_x, bottom_left_y), (
            bottom_right_x, bottom_right_y) = binary_array(folder + name)
        piece["sides"] = store_piece_type(A, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x,
                                          bottom_left_y,
                                          bottom_right_x,
                                          bottom_right_y)

        piece["array"] = A
        piece["coord"] = [top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y,
                          bottom_right_x,
                          bottom_right_y]
        piece["name"] = name
        pieces.append(piece)


def number_of_zero(piece):
    count = 0
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if piece[i][j] == 0:
                count += 1

    return count


def merge_final(top_piece, left_piece, piece):
    right = None
    bottom = None

    merge_x = None
    merge_y = None

    if left_piece is not None:
        right, merge_y = segregate_right(left_piece["array"], left_piece["sides"][2], left_piece["coord"][2],
                                         left_piece["coord"][6], left_piece["coord"][3], left_piece["coord"][7])

    if top_piece is not None:
        bottom, merge_x = segregate_bottom(top_piece["array"], top_piece["sides"][3], top_piece["coord"][5],
                                           top_piece["coord"][7], top_piece["coord"][4], top_piece["coord"][6])

    if right is not None and bottom is not None:
        m1 = merge_right_bottom(right, bottom, merge_y, merge_x)
    elif right is not None:
        m1 = right
        merge_x = 0
    elif bottom is not None:
        m1 = bottom
        merge_y = 0
    else:
        return 100

    m2 = segregate_left_top(piece["array"], piece["coord"][4], piece["coord"][3])
    m3 = merge(m1, m2, merge_x, merge_y, piece["coord"][0], piece["coord"][1])

    return ((number_of_zero(m1) - number_of_zero(m3)) / number_of_zero(m1)) * 100


def required_side(side):
    if side == "st":
        return "st"
    elif side == "tab":
        return "inc"

    return "tab"


def print_solution():
    for i in range(len(placed)):
        for j in range(len(placed[0])):
            if placed[i][j] is not None:
                print(placed[i][j]["name"], end=" ")

        print()


def solve(i):
    if i == R * C:
        print_solution()
        return True

    r = i // C
    c = i % C

    required_top_side = "st"
    required_left_side = "st"

    required_bottom_side = "NA"
    required_right_side = "NA"

    top_piece = None
    left_piece = None

    if r != 0:
        top_piece = placed[r - 1][c]
        bottom_side = top_piece["sides"][3]
        required_top_side = required_side(bottom_side)

    if c != 0:
        left_piece = placed[r][c - 1]
        right_side = left_piece["sides"][2]
        required_left_side = required_side(right_side)

    if r == R - 1:
        required_bottom_side = "st"

    if c == C - 1:
        required_right_side = "st"

    allPiecesThatFit = []

    for j in range(len(pieces)):

        if j in used:
            continue

        left_side = pieces[j]["sides"][0]
        top_side = pieces[j]["sides"][1]
        right_side = pieces[j]["sides"][2]
        bottom_side = pieces[j]["sides"][3]

        if required_bottom_side == "st" and required_bottom_side != bottom_side:
            continue

        if required_right_side == "st" and required_right_side != right_side:
            continue

        if required_left_side == left_side and required_top_side == top_side:
            fitValue = merge_final(top_piece, left_piece, pieces[i])
            allPiecesThatFit.append([fitValue, j])

    allPiecesThatFit.sort(reverse=True)

    for j in range(len(allPiecesThatFit)):
        fitValue, piece_index = allPiecesThatFit[j]
        placed[r][c] = pieces[piece_index]
        used.add(piece_index)
        if solve(i + 1):
            return True

        used.remove(piece_index)
        placed[r][c] = None

    return False


def solve2(i, r, c):
    if i == total:
        print_solution()
        return True

    required_top_side = "st"
    required_left_side = "st"

    required_bottom_side = "NA"
    required_right_side = "NA"

    top_piece = None
    left_piece = None

    if r != 0:
        top_piece = placed[r - 1][c]
        bottom_side = top_piece["sides"][3]
        required_top_side = required_side(bottom_side)

    if c != 0:
        left_piece = placed[r][c - 1]
        right_side = left_piece["sides"][2]
        required_left_side = required_side(right_side)

    if r == R - 1:
        required_bottom_side = "st"

    if c == C - 1:
        required_right_side = "st"

    allPiecesThatFit = []

    for j in range(len(pieces)):

        if j in used:
            continue

        left_side = pieces[j]["sides"][0]
        top_side = pieces[j]["sides"][1]
        right_side = pieces[j]["sides"][2]
        bottom_side = pieces[j]["sides"][3]

        if required_bottom_side == "st" and required_bottom_side != bottom_side:
            continue

        if required_right_side == "st" and required_right_side != right_side:
            continue

        if required_left_side == left_side and required_top_side == top_side:
            fitValue = merge_final(top_piece, left_piece, pieces[i])
            allPiecesThatFit.append([fitValue, j])

    allPiecesThatFit.sort(reverse=True)

    for j in range(len(allPiecesThatFit)):
        fitValue, piece_index = allPiecesThatFit[j]
        placed[r][c] = pieces[piece_index]
        used.add(piece_index)

        if placed[r][c]["sides"][2] == "st":
            if solve2(i + 1, r + 1, 0):
                return True
        else:
            if solve2(i + 1, r, c + 1):
                return True

        used.remove(piece_index)
        placed[r][c] = None

    return False


if __name__ == '__main__':
    pre_processing()
    # solve(0)
    solve2(0, 0, 0)
