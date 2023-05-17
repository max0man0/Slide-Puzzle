import pygame as pg
import random
import math
from typing import Tuple, List, Any

# For dev purposes only
Never = Any

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
    board = generate_solvable_board()

    while running:
        clock.tick(FPS)  # Make sure to cap the FPS of the game to 60
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_pos = pg.mouse.get_pos()
                # if the mouse clicked in the main board boundry
                if MAIN_BOARD_LEFT <= mouse_pos[0] <= MAIN_BOARD_LEFT + MAIN_BOARD_SIDE_LENGTH and MAIN_BOARD_TOP <= mouse_pos[1] <= MAIN_BOARD_TOP + MAIN_BOARD_SIDE_LENGTH:
                    handle_square_sliding(mouse_pos, board)
                # if reset button was click
                elif RESET_BTN_LEFT <= mouse_pos[0] <= RESET_BTN_LEFT + RESET_BTN_WIDTH and RESET_BTN_TOP <= mouse_pos[1] <= RESET_BTN_TOP + RESET_BTN_HEIGHT:
                    board = generate_solvable_board()

        draw_window(board)

    pg.quit()

def generate_solvable_board(board_length: int) -> List[int]:
    """
    Parameters
    ----------
    `board_length`:
        The number of elements that the returned board should have (must be a perfect square)

    Returns
    -------
    A solveable board of randomly ordered numbers

    Raises
    ------
    ValueError
        If `board_length` is not a perfect square
    """
    # Validate parameter
    if not is_perfect_square(board_length):
        raise ValueError(f"`board_length` {board_length} is not a perfect square")

    board = list(range(1, board_length))
    board.append(0)

    # Perform a random number of valid moves (odd count) to shuffle the board
    num_moves = random.randint(15, 99)
    if num_moves % 2 == 0:
        num_moves += 1
    
    for _ in range(num_moves):
        valid_moves = get_valid_moves(board)
        move = random.choice(valid_moves)
        board[move[0]], board[move[1]] = board[move[1]], board[move[0]]

    return board

def is_perfect_square(num: int) -> bool:
    return num == math.isqrt(num) ** 2

def get_valid_moves(board: List[int]) -> List[Tuple[int, int]]:
    row_count = int(math.sqrt(len(board)))
    empty_index = board.index(0)
    valid_moves = []

    # FIXME check if it works
    if empty_index % row_count != 0: # 
        valid_moves.append((empty_index, empty_index - 1))  # Move empty square to the left
    if empty_index % row_count != 2:
        valid_moves.append((empty_index, empty_index + 1))  # Move empty square to the right
    if empty_index >= 3:
        valid_moves.append((empty_index, empty_index - row_count))  # Move empty square upwards
    if empty_index < 6:
        valid_moves.append((empty_index, empty_index + row_count))  # Move empty square downwards

    return valid_moves

def handle_square_sliding(square_pos: Tuple[int, int], board: List[int]) -> None:
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
    row_count = int(math.sqrt(len(board)))
    column_index = get_partition(
        square_pos[0], MAIN_BOARD_LEFT, MAIN_BOARD_LEFT + MAIN_BOARD_SIDE_LENGTH, row_count)
    row_index = get_partition(
        square_pos[1], MAIN_BOARD_TOP, MAIN_BOARD_TOP + MAIN_BOARD_SIDE_LENGTH, row_count)
    sq_index = row_count * row_index + column_index
    empty_sq_index = board.index(0)

    # Swap the empty square number (0) with the square number gotten from `square_pos`
    if empty_sq_index % row_count == 0:  # if the empty square is at the left-most column
        # Swap if swap is legal
        if sq_index in (empty_sq_index + 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board[empty_sq_index], board[sq_index] = board[sq_index], board[empty_sq_index]
    elif empty_sq_index % row_count == row_count - 1:  # if the empty square is at the right-most column
        # Swap if swap is legal
        if sq_index in (empty_sq_index - 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board[empty_sq_index], board[sq_index] = board[sq_index], board[empty_sq_index]
    else:  # if the empty square is at a column in the middle
        # Swap if swap is legal
        if sq_index in (empty_sq_index - 1, empty_sq_index + 1, empty_sq_index + row_count, empty_sq_index - row_count):
            board[empty_sq_index], board[sq_index] = board[sq_index], board[empty_sq_index]


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


def draw_window(board: List[int]) -> None:
    """
    Parameters
    ----------
    `board`:
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
            What `board` should be:
                [3, 1, 2, 0, 5, 8, 7, 4, 6]

    Returns
    -------
    None.

    Raises
    ------
    TypeError
        If `board` is not a list of integers

    ValueError
        If the number of integers in `board` is not 9
    """

    # Window background color
    WIN.fill(BACKGROUND_COLOR)

    # Validate parameter
    if not isinstance(board, list) or not all([isinstance(element, int) for element in board]):
        raise TypeError("numbered_squares must be a list of integers")

    if len(board) != 9:
        raise ValueError("numbered_squares must have 9 integers")

    # Draw the main board and its background color
    main_board = main_board_color_rect = pg.Rect(
        MAIN_BOARD_LEFT, MAIN_BOARD_TOP, MAIN_BOARD_SIDE_LENGTH, MAIN_BOARD_SIDE_LENGTH)
    pg.draw.rect(WIN, MAIN_BOARD_COLOR, main_board_color_rect)
    pg.draw.rect(WIN, BORDER_COLOR, main_board, 2)

    # Draw squares to slide + determine empty square position
    number_font = pg.font.SysFont("timesnewroman", 36)
    for pos, sq_num in enumerate(board):
        if (sq_num != 0):
            # Draw the slide squares
            slide_square_side_length = MAIN_BOARD_SIDE_LENGTH // math.sqrt(
                len(board))
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

    # Draw the reset button
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
