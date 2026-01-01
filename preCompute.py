def segregateRight(A, type, top_right_x, bottom_right_x, top_right_y, bottom_right_y):
    if type == "inc":
        min_ = 1000

        for i in range(top_right_x, bottom_right_x):
            for j in range(len(A[i])-1, 0, -1):
                if A[i][j] == 1:
                    min_ = min(min_, j)
                    break

        print(min_)

        result = A[top_right_x + 1: bottom_right_x]
        return [row[min_ - 10:] for row in result]

    result = A[top_right_x + 1: bottom_right_x]
    return [row[min(top_right_y, bottom_right_y) - 10:] for row in result]


def segregateBottom(A, type, bottom_left_y, bottom_right_y, bottom_left_x, bottom_right_x):
    if type == "inc":
        min_ = 1000

        for i in range(bottom_left_y, bottom_right_y):
            for j in range(len(A)-1, 0, -1):
                if A[j][i] == 1:
                    min_ = min(min_, j)
                    break

        print(min_)

        result = A[min_ - 15:]
        return [row[bottom_left_y:bottom_right_y] for row in result]

    result = A[min(bottom_left_x, bottom_right_x) - 10:]
    return [row[bottom_left_y:bottom_right_y] for row in result]


def mergeRightBottom(right, bottom, bottom_original_length, bottom_left_x):
    new_bottom_left_x = bottom_left_x - (bottom_original_length-len(bottom))
    rows_to_add = len(bottom)-new_bottom_left_x
    cols_to_add = len(bottom[0])

    rows, cols = len(right), len(right[0])

    new_right = [[0] * (cols + cols_to_add) for _ in range(rows_to_add)] + [row + [0] * cols_to_add for row in right]

    overlap_y = len(right[0])-1

    for i in range(len(bottom)):
        for j in range(len(bottom[0])):
            new_right[i][overlap_y+j] = bottom[i][j]

    return new_right


def segregateLeftTop(A,bottom_left_x, top_right_y):
    result = A[:bottom_left_x+1]
    return [row[:top_right_y + 10] for row in result]

