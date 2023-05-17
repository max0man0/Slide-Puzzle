import pygame as pg
import random
import math
from typing import Never, Tuple, List

pg.init()

WIDTH, HEIGHT = 1000, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Slide Puzzle")

FPS = 60

SLIDE_SQUARE_COLOR = pg.Color("brown1")
BACKGROUND_COLOR = pg.Color("white")
MAIN_BOARD_COLOR = pg.Color("gray80")
BORDER_COLOR = TEXT_COLOR = pg.Color("black")

MAIN_BOARD_SIDE_LENGTH = 600
MAIN_BOARD_CENTER_X = WIDTH//2
MAIN_BOARD_CENTER_Y = HEIGHT//2
MAIN_BOARD_LEFT = MAIN_BOARD_CENTER_X - MAIN_BOARD_SIDE_LENGTH//2
MAIN_BOARD_TOP = MAIN_BOARD_CENTER_Y - MAIN_BOARD_SIDE_LENGTH//2

RESET_BTN_WIDTH, RESET_BTN_HEIGHT = 150, 50
RESET_BTN_CENTER_X = MAIN_BOARD_CENTER_X
RESET_BTN_CENTER_Y = ((MAIN_BOARD_TOP + MAIN_BOARD_SIDE_LENGTH) + HEIGHT) // 2
RESET_BTN_LEFT = RESET_BTN_CENTER_X - RESET_BTN_WIDTH//2
RESET_BTN_TOP = RESET_BTN_CENTER_Y - RESET_BTN_HEIGHT//2


def main() -> None:
    clock = pg.time.Clock()
    running = True
    board_list = random.sample(range(0, 9), 9)
    print(board_list)

    while running:
        clock.tick(FPS)  # Make sure to cap the FPS of the game to 60
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                # if mouse is in the main board boundry
                if MAIN_BOARD_LEFT <= mouse_pos[0] <= MAIN_BOARD_LEFT + MAIN_BOARD_SIDE_LENGTH and MAIN_BOARD_TOP <= mouse_pos[1] <= MAIN_BOARD_TOP + MAIN_BOARD_SIDE_LENGTH:
                    handle_square_sliding(mouse_pos, board_list)
                elif RESET_BTN_LEFT <= mouse_pos[0] <= RESET_BTN_LEFT + RESET_BTN_WIDTH and RESET_BTN_TOP <= mouse_pos[1] <= RESET_BTN_TOP + RESET_BTN_HEIGHT:
                    handle_reset_click()

        draw_window(board_list)

    pg.quit()


def handle_reset_click(arg: Never) -> List[int]:
    # TODO implement this method
    raise NotImplementedError()

def handle_square_sliding(square_pos: Tuple[int, int], board_list: List[int]) -> None:
    """
    Parameters
    ----------
    `mouse_pos`:
        The current coordinates of the square to slide.

    `board_list`:
        The integers that each represent the number of the slide square. The list will modified if there was a square that slid.

    Returns
    -------
    None.
    """
    row_count = int(math.sqrt(len(board_list)))
    column_index = get_partition(
        square_pos[0], MAIN_BOARD_LEFT, MAIN_BOARD_LEFT + MAIN_BOARD_SIDE_LENGTH, row_count)
    row_index = get_partition(
        square_pos[1], MAIN_BOARD_TOP, MAIN_BOARD_TOP + MAIN_BOARD_SIDE_LENGTH, row_count)
    sq_index = row_count * row_index + column_index
    empty_sq_index = board_list.index(0)

    # Swap the empty square number (0) with the square number gotten from `square_pos`
    if empty_sq_index % row_count == 0:  # if the empty square is at the left-most column
        # Swap if swap is legal
        if sq_index in (empty_sq_index + 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board_list[empty_sq_index], board_list[sq_index] = board_list[sq_index], board_list[empty_sq_index]
    elif empty_sq_index % row_count == row_count - 1:  # if the empty square is at the right-most column
        # Swap if swap is legal
        if sq_index in (empty_sq_index - 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board_list[empty_sq_index], board_list[sq_index] = board_list[sq_index], board_list[empty_sq_index]
    else:  # if the empty square is at a column in the middle
        # Swap if swap is legal
        if sq_index in (empty_sq_index - 1, empty_sq_index + 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board_list[empty_sq_index], board_list[sq_index] = board_list[sq_index], board_list[empty_sq_index]


def get_partition(x: int, min_number: int, max_number: int, partition_count: int) -> int:
    """
    Divide the range `min_number`-`max_number` (both ends excluded) to `partition_count` partitions and find in the index of the partition that `x` is in

    Parameters
    ----------
    `x`:
        The number to find in which partition it is in.

    `min_number`:
        The minimum number in the range that x is expected to be in (excluded from the range).

    `max_number`:
        The max number in the range that x is expected to be in (excluded from the range).

    `partition_count`:
        The number partitions to divide the range into.

    Returns
    -------
    The index of the partition that `x` is in.

    Raises
    ------
    ValueError
        If `x` is not the interval (`min_number`, `max_number`)
    """
    if x < min_number or x > max_number:
        raise ValueError(
            f"x ({x}) is outside the range ({min_number}, {max_number}).")
    range_size = max_number - min_number
    partition_size = range_size / partition_count
    x_relative = x - min_number
    partition_index = int(x_relative // partition_size)
    return partition_index


def draw_window(numbered_squares: List[int]) -> None:
    """
    Parameters
    ----------
    `numbered_squares`:
        List of 9 numbers corresponding to the order of the squares in the board
        where the number is the index that the square should be in after solving the puzzle + 1.
        - The list should be considered a flattened matrix.
        - The place that the empty square resides in should be annotated with 0 in the given list.

        Example:
            Board:
            ```
            | 3 | 1 | 2 |
            |   | 5 | 8 |
            | 7 | 4 | 6 |
            ```
            What numbered_squares should be:
                [3, 1, 2, 0, 5, 8, 7, 4, 6]

    Returns
    -------
    None.

    Raises
    ------
    TypeError
        If `numbered_squares` is not a list of integers

    ValueError
        If the number of integers in `numbered_squares` is not 9
    """

    # Window background color
    WIN.fill(BACKGROUND_COLOR)

    # Validate parameter
    if not isinstance(numbered_squares, list) or not all([isinstance(element, int) for element in numbered_squares]):
        raise TypeError("numbered_squares must be a list of integers")

    if len(numbered_squares) != 9:
        raise ValueError("numbered_squares must have 9 integers")

    # Draw the main board and its background color
    main_board = main_board_color_rect = pg.Rect(
        MAIN_BOARD_LEFT, MAIN_BOARD_TOP, MAIN_BOARD_SIDE_LENGTH, MAIN_BOARD_SIDE_LENGTH)
    pg.draw.rect(WIN, MAIN_BOARD_COLOR, main_board_color_rect)
    pg.draw.rect(WIN, BORDER_COLOR, main_board, 2)

    # Draw squares to slide + determine empty square position
    number_font = pg.font.SysFont("timesnewroman", 36)
    for pos, sq_num in enumerate(numbered_squares):
        if (sq_num != 0):
            # Draw the slide squares
            slide_square_side_length = MAIN_BOARD_SIDE_LENGTH // math.sqrt(
                len(numbered_squares))
            slide_square = slide_square_color_rect = pg.Rect(main_board.left+((pos % 3)*slide_square_side_length), main_board.top+(
                (pos//3)*slide_square_side_length), slide_square_side_length, slide_square_side_length)
            pg.draw.rect(WIN, SLIDE_SQUARE_COLOR, slide_square_color_rect)
            pg.draw.rect(WIN, BORDER_COLOR, slide_square, 1)

            # Draw the numbers of the squares
            slide_square_number = number_font.render(
                str(sq_num), True, TEXT_COLOR)
            slide_square_number_rect = slide_square_number.get_rect()
            slide_square_number_rect.center = slide_square.center
            WIN.blit(slide_square_number, slide_square_number_rect)

    # TODO Draw the reset button
    reset_btn = pg.Rect(RESET_BTN_LEFT, RESET_BTN_TOP, RESET_BTN_WIDTH, RESET_BTN_HEIGHT)
    pg.draw.rect(WIN, BORDER_COLOR, reset_btn, 2)

    reset_label_font = pg.font.SysFont("timesnewroman", 30)
    reset_btn_label = reset_label_font.render("Reset", True, TEXT_COLOR)
    reset_btn_label_rect = reset_btn_label.get_rect()
    reset_btn_label_rect.center = reset_btn.center
    WIN.blit(reset_btn_label, reset_btn_label_rect)


    pg.display.update()


if __name__ == "__main__":
    main()
