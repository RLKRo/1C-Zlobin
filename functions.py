import numpy as np

MIN_STROKES_IN_LINE = 3


def distance(x, y):
    return ((y - x)[0]**2 + (y - x)[1]**2)**(1/2)


# checks a given pixel
#
# if it is a part of a stroke return 4 points of a stroke (upper left, upper right, lower left, lower right)
# and check all black_pixels
#
# otherwise return None and check all black pixels
def check_black_pixel(x, y, black_color, checked):
    if black_color[x, y]:
        left_up, right_up = vertical_check(x, y, black_color, checked, 'up')
        left_down, right_down = vertical_check(x, y, black_color, checked, 'down')
        return left_down, right_down, left_up, right_up
    return None


# for a given stroke finds two farthest points of the corresponding line
def find_line(left_down, right_down, left_up, right_up, black_color, checked):
    # lines are presented by two points
    first_possible_line = ((left_down + right_down) / 2, (left_up + right_up) / 2)
    second_possible_line = ((left_down + left_up) / 2, (right_down + right_up) / 2)

    answer, x, y = check_line(first_possible_line, black_color, checked)
    if answer == 'Line':
        return x, y

    answer, x, y = check_line(second_possible_line, black_color, checked)
    if answer == 'Line':
        return x, y

    return None, None


# checks a possible line
# returns whether it is a line or not and its farthest points
def check_line(possible_line, black_color, checked):
    if (possible_line[1] - possible_line[0])[0] == 0:  # vertical line
        strokes_counter, highest_point = check_vertically(possible_line, black_color, checked, 'up')
        tmp, lowest_point = check_vertically(possible_line, black_color, checked, 'down')

        strokes_counter += tmp

        if strokes_counter >= MIN_STROKES_IN_LINE:
            return 'Line', lowest_point, highest_point
        else:
            return 'Not a line', None, None
    else:
        strokes_counter, most_right_point = check_direction(possible_line, black_color, checked, 'right')
        tmp, most_left_point = check_direction(possible_line, black_color, checked, 'left')

        strokes_counter += tmp

        if strokes_counter >= MIN_STROKES_IN_LINE:
            return 'Line', most_left_point, most_right_point
        else:
            return 'Not a line', None, None


# counts the amount of other strokes in a given direction
def check_direction(possible_line, black_color, checked, direction):
    strokes_counter = 0

    if direction == 'right':
        x_modifier = 1
    else:
        x_modifier = -1

    inclination = (possible_line[1] - possible_line[0])[1] / (possible_line[1] - possible_line[0])[0]

    y_modifier = inclination * x_modifier

    i, j = possible_line[1]

    last_black_point = np.array([round(i), round(j)])

    while 0 <= i <= black_color.shape[1] and 0 <= j <= black_color.shape[0]:
        x, y = round(i), round(j)
        if black_color[x, y] and not checked[x, y]:
            last_black_point = np.array([x, y])
            strokes_counter += 1
            check_black_pixel(x, y, black_color, checked)   # checks to not count one stroke multiple times for
                                                            # each black point of it
        i += x_modifier
        j += y_modifier

    return strokes_counter, last_black_point


# does the same as what check_direction does but when the direction is vertical
def check_vertically (possible_line, black_color, checked, direction):
    strokes_counter = 0

    if direction == 'up':
        y_modifier = 1
    else:
        y_modifier = -1

    i, j = possible_line[1]

    last_black_point = np.array([round(i), round(j)])

    while 0 <= i <= black_color.shape[1] and 0 <= j <= black_color.shape[0]:
        x, y = round(i), round(j)
        if black_color[x, y] and not checked[x, y]:
            last_black_point = np.array([x, y])
            strokes_counter += 1
            check_black_pixel(x, y, black_color, checked)   # checks to not count one stroke multiple times for
                                                            # each black point of it
        j += y_modifier

    return strokes_counter, last_black_point


# checks all point in the current horizontal line
# if it there are no black pixels in the current direction returns most left and most right point of a current line
# otherwise goes to the next horizontal line and takes its output
#
# Essentially, it returns the most left and most right points of the highest /lowest line containing black pixels
def vertical_check(x, y, black_color, checked, direction):
    checked[x, y] = True
    left_black, next_black, right_black = horizontal_check(x, y, black_color, checked, direction)
    if next_black is None:
        return left_black, right_black
    else:
        return vertical_check(next_black[0], next_black[1], black_color, checked, direction)


def horizontal_check(x, y, black_color, checked, direction):
    next_black_pixel, most_left_black = iterate_horizontally(x, y, black_color, checked, direction, 'left')

    tmp, most_right_black = iterate_horizontally(x, y, black_color, checked, direction, 'right')
    if tmp is not None:
        next_black_pixel = tmp

    return most_left_black, next_black_pixel, most_right_black


def iterate_horizontally(x, y, black_color, checked, direction, horizontal_direction):
    if direction == 'up':
        modifier = 1
    else:
        modifier = -1

    if horizontal_direction == 'left':
        horizontal_modifier = -1
    else:
        horizontal_modifier = 1

    i = x
    next_black_pixel = None  # any black pixel in the current direction

    while black_color[i, y] and 0 <= i <= black_color.shape[1]:
        if black_color[i, y + modifier] and 0 <= y + modifier <= black_color.shape[0]:
            next_black_pixel = np.array([i, y + modifier])
        checked[i, y] = True
        i += horizontal_modifier

    final_black = np.array([i + 1, y])  # last black pixel in the horizontal direction

    return next_black_pixel, final_black
