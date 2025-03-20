# -*- coding: utf-8 -*-
"""Untitled8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BzJIl6-c4opOEtHEfq6-S1KcgjUVZ3rB
"""

import random
import time
from IPython.display import display, HTML, clear_output

# Emojis and visual representations
MONKEY = "\U0001F412"  # Red circle for monkey
TABLE_BLUE = "\U0001F535"  # Blue circle for table
TABLE_VIOLET = "\U0001F7E3"  # Violet circle for table after monkey arrives
BANANA_GREEN = "\U0001F7E9"  # Green square for banana initially
BANANA_YELLOW = "\U0001F34C"  # Banana emoji after eaten
EMPTY = "\u2B1C"  # White square

# Grid dimensions
GRID_SIZE = 5

def initialize_grid(grid_size, table_pos, num_bananas):
    """Initialize the grid with a table and bananas."""
    grid = [[EMPTY for _ in range(grid_size)] for _ in range(grid_size)]

    # Place table at the given position
    grid[table_pos[0]][table_pos[1]] = TABLE_BLUE

    # Place bananas randomly on the grid, avoiding the table position
    banana_positions = set()
    while len(banana_positions) < num_bananas:
        pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
        if pos != table_pos:
            banana_positions.add(pos)

    for pos in banana_positions:
        grid[pos[0]][pos[1]] = BANANA_GREEN

    return grid, banana_positions

def display_grid(grid, monkey_pos, commentary):
    """Display the grid with the monkey's current position and keep commentary persistent."""
    clear_output(wait=True)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            # Special case: Monkey + Table
            if (i, j) == monkey_pos and (cell == TABLE_BLUE or cell == TABLE_VIOLET):
                print(f"{MONKEY}/{cell}", end=" ")
            # Case: Monkey in any other position
            elif (i, j) == monkey_pos:
                print(MONKEY, end=" ")
            # Case: Normal cell
            else:
                print(cell, end=" ")
        print()  # New line after each row
    print("\n".join(commentary))  # Keep commentary persistent
    display(HTML("<br>"))

def move_monkey(grid, start, end):
    """Move the monkey step-by-step to the target position."""
    path = []
    x, y = start
    ex, ey = end

    while x != ex or y != ey:
        if x < ex:
            x += 1
        elif x > ex:
            x -= 1
        elif y < ey:
            y += 1
        elif y > ey:
            y -= 1
        path.append((x, y))

    return path

def get_adjacent_cell(grid, position):
    """Get an adjacent empty cell for the monkey to move after eating the last banana."""
    x, y = position
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == EMPTY:
            return (nx, ny)
    return position  # If no adjacent cell is empty, stay in place

def monkey_simulation(grid_size, monkey_pos, table_pos, num_bananas):
    """Run the simulation."""
    grid, banana_positions = initialize_grid(grid_size, table_pos, num_bananas)
    commentary = [f"Monkey is initially at {monkey_pos[0] + 1},{monkey_pos[1] + 1}"]
    obtained_table = False  # Track if the monkey has obtained the table

    # Show initial grid
    display_grid(grid, monkey_pos, commentary)
    time.sleep(2.5)

    # Move monkey to the table
    path_to_table = move_monkey(grid, monkey_pos, table_pos)
    for pos in path_to_table:
        monkey_pos = pos
        commentary.append(f"Monkey moved to {monkey_pos[0] + 1},{monkey_pos[1] + 1}")
        display_grid(grid, monkey_pos, commentary)
        time.sleep(0.5)

    # Change table color to violet after reaching
    grid[table_pos[0]][table_pos[1]] = TABLE_VIOLET
    obtained_table = True
    commentary.append(f"Monkey obtained the table at {table_pos[0] + 1},{table_pos[1] + 1}")
    display_grid(grid, monkey_pos, commentary)
    time.sleep(1)

    # Collect bananas optimally (one by one)
    while banana_positions:
        closest_banana = min(banana_positions, key=lambda b: abs(b[0] - monkey_pos[0]) + abs(b[1] - monkey_pos[1]))
        path_to_banana = move_monkey(grid, monkey_pos, closest_banana)

        for pos in path_to_banana:
            monkey_pos = pos
            commentary.append(f"Monkey moved to {monkey_pos[0] + 1},{monkey_pos[1] + 1}")
            display_grid(grid, monkey_pos, commentary)
            time.sleep(0.5)

        # Check if the banana is reached and the table is obtained
        if obtained_table:
            banana_positions.remove(closest_banana)
            grid[closest_banana[0]][closest_banana[1]] = BANANA_YELLOW
            commentary.append(f"Monkey obtained banana at {closest_banana[0] + 1},{closest_banana[1] + 1}")
        else:
            commentary.append(f"Monkey moved to a banana position at {closest_banana[0] + 1},{closest_banana[1] + 1}, but did not obtain it (table not reached).")

        display_grid(grid, monkey_pos, commentary)
        time.sleep(1)

    # After eating the last banana, move to an adjacent cell and stop
    final_position = get_adjacent_cell(grid, monkey_pos)
    path_to_final = move_monkey(grid, monkey_pos, final_position)

    for pos in path_to_final:
        monkey_pos = pos
        commentary.append(f"Monkey moved to {monkey_pos[0] + 1},{monkey_pos[1] + 1} (final position).")
        display_grid(grid, monkey_pos, commentary)
        time.sleep(0.5)

# User input for monkey, table, and banana positions
monkey_start = (int(input("Enter monkey's starting row: ")) - 1, int(input("Enter monkey's starting column: ")) - 1)
table_position = (int(input("Enter table's row: ")) - 1, int(input("Enter table's column: ")) - 1)
number_of_bananas = int(input("Enter number of bananas: "))

# Run the simulation
monkey_simulation(GRID_SIZE, monkey_start, table_position, number_of_bananas)