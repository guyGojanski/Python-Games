import random
import copy

SIZE = 4


# Merge the row to the left and return the new row and the score gained
def merge_row(row):
    # row [0, 2, 2, 4] -> remove_zeros [2, 2, 4]
    remove_zeros = [x for x in row if x != 0]  # Remove zeros
    merged_row = []
    score_increment = 0
    skip = False

    #  remove_zeros [2, 2, 4]
    for i in range(len(remove_zeros)):
        if skip:
            skip = False
            continue
        #  remove_zeros [i-> 2, 2, 4] -> merged_row [4]
        #  we skiped the current element because we merged it with the one before it
        #  remove_zeros [ 2, 2, i-> 4] -> merged_row [4, 4]

        if i + 1 < len(remove_zeros) and remove_zeros[i] == remove_zeros[i + 1]:
            merged_row.append(remove_zeros[i] * 2)  # Merge and double the value
            score_increment += remove_zeros[i] * 2  # Add to the score
            skip = True  # Skip the next element
        else:
            merged_row.append(remove_zeros[i])  # Just move the value

    # merged_row [4, 4] -> merged_row [4, 4, 0, 0]
    while len(merged_row) < len(row):
        merged_row.append(0)  # Fill the rest with zeros

    # merged_row [4, 4, 0, 0]
    return merged_row, score_increment


# Transpose the grid (swap rows and columns) and return as list of lists
def transpose(grid):
    # zip(*grid) produces tuples representing columns; convert each to list
    transposed = zip(*grid)
    result = []
    for row in transposed:
        result.append(list(row))
    return result


# Reverse each row in the grid (useful for right moves)
def reverse(grid):
    # map(reversed, grid) yields reversed iterables for each row; convert to lists
    rows_reversed = map(reversed, grid)
    result = []
    for row in rows_reversed:
        result.append(list(row))
    return result


# Move every row to the left using `merge_row` and return the new grid
def move_left(grid):
    # Move every row to the left using `merge_row` and return the new grid
    # grid -> iterate rows -> apply same merge logic as a single row
    new_grid = []
    score = 0
    for row in grid:
        # row [2, 0, 2, 4] -> merge_row(row) -> [4, 4, 0, 0]
        merged_row, score_increment = merge_row(row)
        new_grid.append(merged_row)
        score += score_increment
    return new_grid, score


# Move right by reversing rows, moving left, then reversing back
def move_right(grid):
    # reverse(grid) -> move_left(...) -> reverse(...) to restore orientation
    new_grid, score = move_left(reverse(grid))
    return reverse(new_grid), score


# Move up by transposing, moving left (which acts like up), then transposing back
def move_up(grid):
    # transpose(grid) turns columns into rows so `move_left` operates on columns
    new_grid, score = move_left(transpose(grid))
    return transpose(new_grid), score


# Move down by transposing, moving right (acts like down), then transposing back
def move_down(grid):
    new_grid, score = move_right(transpose(grid))
    return transpose(new_grid), score


# Find all empty cells (value == 0) and place a new tile (2 or 4)
def add_new_tile(grid):
    # Collect coordinates of empty cells
    empty_cells = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                empty_cells.append((row, col))

    # No empty cell -> nothing to add
    if len(empty_cells) == 0:
        return grid

    # Choose a random empty cell
    row, col = random.choice(empty_cells)

    # Choose a random empty cell and place a 2 (90%) or 4 (10%)
    if random.random() < 0.9:
        grid[row][col] = 2
    else:
        grid[row][col] = 4

    return grid


def get_current_state(grid):
    # Check for win condition (tile 2048)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 2048:
                return "WON"

    # Check for any empty cell (value == 0)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                return "GAME NOT OVER"

    # Check for possible merges horizontally
    for row in range(len(grid)):
        for col in range(len(grid[0]) - 1):
            if grid[row][col] == grid[row][col + 1]:
                return "GAME NOT OVER"

    # Check for possible merges vertically
    for col in range(len(grid[0])):
        for row in range(len(grid) - 1):
            if grid[row][col] == grid[row + 1][col]:
                return "GAME NOT OVER"

    # If no win, no empty cells, and no merges, the game is lost
    return "LOST"


def start_game():
    grid = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid


def move(grid, direction):
    old_grid = copy.deepcopy(grid)

    if direction == "LEFT":
        new_grid, score = move_left(grid)
    elif direction == "RIGHT":
        new_grid, score = move_right(grid)
    elif direction == "UP":
        new_grid, score = move_up(grid)
    elif direction == "DOWN":
        new_grid, score = move_down(grid)
    else:
        raise ValueError("Invalid move direction")

    changed = new_grid != old_grid
    return new_grid, score, changed
