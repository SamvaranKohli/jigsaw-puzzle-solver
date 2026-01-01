import main

pieces = []

for i in range(1, 9):
    name = str(i) + ".png"
    piece = {}
    A, (top_left_x, top_left_y), (top_right_x, top_right_y), (bottom_left_x, bottom_left_y), (
        bottom_right_x, bottom_right_y) = main.binary_array(name)
    values = main.store_piece_type(A, top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y,
                                   bottom_right_x,
                                   bottom_right_y)

    piece["array"] = A
    piece["coord"] = [top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y, bottom_right_x,
                      bottom_right_y]
    piece["sides"] = [values]

    pieces.append(piece)
