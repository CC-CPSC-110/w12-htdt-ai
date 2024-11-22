import random
from collections import deque

#################################################################################
# Generate a grid

def generate_grid_with_characters(n, m):
    """
    Generates an n x m grid with a player ('P') and an opponent ('O') placed at random spots.

    Args:
        n (int): Number of rows in the grid.
        m (int): Number of columns in the grid.

    Returns:
        str: The string representation of the generated grid.
    """
    if n < 2 or m < 2:
        raise ValueError("Grid dimensions must be at least 2x2.")

    # Create an empty grid filled with spaces
    grid = [[' ' for _ in range(m)] for _ in range(n)]

    # Place the boundaries
    for i in range(n):
        grid[i][0] = grid[i][-1] = '#'
    for j in range(m):
        grid[0][j] = grid[-1][j] = '#'

    # Randomly place the player ('P') and opponent ('O') within the grid
    player_x, player_y = random.randint(1, m - 2), random.randint(1, n - 2)
    opponent_x, opponent_y = player_x, player_y

    # Ensure 'O' does not overlap 'P'
    while opponent_x == player_x and opponent_y == player_y:
        opponent_x, opponent_y = random.randint(1, m - 2), random.randint(1, n - 2)

    grid[player_y][player_x] = 'P'
    grid[opponent_y][opponent_x] = 'O'

    # Convert grid to string
    return '\n'.join(''.join(row) for row in grid)


def generate_maze(n, m):
    """
    Generates a valid n x m maze using recursive backtracking.

    Args:
        n (int): Number of rows in the maze.
        m (int): Number of columns in the maze.

    Returns:
        list: A 2D list representing the maze.
    """
    def initialize_grid():
        # Create a grid filled with walls
        return [['#' for _ in range(m)] for _ in range(n)]
    
    def carve_passages(x, y, grid):
        # Shuffle the directions to randomize the maze
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < ny < n - 1 and 0 < nx < m - 1 and grid[ny][nx] == '#':
                # Carve the path
                grid[ny][nx] = ' '
                grid[y + dy // 2][x + dx // 2] = ' '
                # Recurse
                carve_passages(nx, ny, grid)

    # Step 1: Initialize grid
    grid = initialize_grid()

    # Step 2: Start carving from a random cell
    start_x, start_y = random.choice(range(1, m, 2)), random.choice(range(1, n, 2))
    grid[start_y][start_x] = ' '
    carve_passages(start_x, start_y, grid)

    return grid


def place_players(grid):
    """
    Places players ('P' and 'O') at random open spots in the maze.

    Args:
        grid (list): A 2D list representing the maze.

    Returns:
        list: The updated maze with players placed.
    """
    open_spots = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == ' ']
    if len(open_spots) < 2:
        raise ValueError("Maze does not have enough open spots for players.")

    # Randomly place 'P' and 'O' in two different open spots
    p_spot, o_spot = random.sample(open_spots, 2)
    grid[p_spot[1]][p_spot[0]] = 'P'
    grid[o_spot[1]][o_spot[0]] = 'O'

    return grid



def generate_maze_with_players(n, m):
    """
    Generates a valid n x m maze with two players ('P' and 'O') placed at random spots.

    Args:
        n (int): Number of rows in the maze.
        m (int): Number of columns in the maze.

    Returns:
        str: The string representation of the maze with players.
    """
    if n < 5 or m < 5:
        raise ValueError("Maze dimensions must be at least 5x5 to accommodate players.")

    # Generate maze
    maze = generate_maze(n, m)

    # Place players
    maze_with_players = place_players(maze)

    # Convert maze to string
    return '\n'.join(''.join(row) for row in maze_with_players)

#################################################################################




def parse_grid(grid: str):
    """
    Converts a string representation of a grid into a 2D list.

    Args:
        grid_string (str): The grid as a string.

    Returns:
        list: A 2D list representing the grid.
    """
    return [list(line) for line in grid.strip().split('\n')]


def grid_to_string(grid):
    """
    Converts a 2D list representation of a grid back into a string.

    Args:
        grid (list): A 2D list representing the grid.

    Returns:
        str: The string representation of the grid.
    """
    return '\n'.join(''.join(line) for line in grid)


def get_character_coordinates(grid, char):
    """
    Finds the coordinates of a character in the grid.

    Args:
        grid (list): A 2D list representing the grid.
        char (str): The character to locate.

    Returns:
        tuple: (x, y) coordinates of the character, or None if not found.
    """
    for y, row in enumerate(grid):
        if char in row:
            return row.index(char), y
    return None


def calculate_distance(grid, char1, char2):
    """
    Calculates the Manhattan distance between two characters in the grid.

    Args:
        grid: The grid.
        char1 (str): The first character.
        char2 (str): The second character.

    Returns:
        int: The Manhattan distance between the two characters.
             Returns 0 if the characters overlap.
    """
    # Parse the grid and find the coordinates of both characters
    coord1 = get_character_coordinates(grid, char1)
    coord2 = get_character_coordinates(grid, char2)

    if coord1 is None or coord2 is None:
        raise ValueError(f"One or both characters ('{char1}', '{char2}') not found in the grid.")

    # Calculate the Manhattan distance
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2)




def generate_possible_moves(grid, char):
    """
    Generates all possible grids for a character's valid moves in the grid.

    Args:
        grid (list): A 2D list representing the grid.
        char (str): The character to move.

    Returns:
        list: A list of grids, where each grid represents a valid move of the character.
    """
    current_position = get_character_coordinates(grid, char)
    if not current_position:
        raise ValueError(f"Character '{char}' not found in the grid.")

    x, y = current_position
    possible_moves = [
        (x, y - 1),  # Up
        (x, y + 1),  # Down
        (x - 1, y),  # Left
        (x + 1, y)   # Right
    ]

    # Filter moves that are out of bounds or blocked
    valid_moves = [
        (new_x, new_y)
        for new_x, new_y in possible_moves
        if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]) and grid[new_y][new_x] == ' '
    ]

    # Generate new grids for each valid move
    new_grids = []
    for new_x, new_y in valid_moves:
        new_grid = [row[:] for row in grid]  # Create a deep copy of the grid
        new_grid[y][x] = ' '  # Clear the current position of the character
        new_grid[new_y][new_x] = char  # Move the character to the new position
        new_grids.append(new_grid)

    return new_grids


def find_best_move(distances):
    """
    Finds the move with the shortest distance to the target.

    Args:
        distances (list): A list of tuples containing moves and their distances.

    Returns:
        tuple: The coordinates of the best move.
    """
    if not distances:
        return None  # No valid moves
    return min(distances, key=lambda x: x[1])[0]  # Return the move with the smallest distance


def calculate_distances(grids, char1, char2):
    return map(lambda grid: (grid, calculate_distance(grid, char1, char2)), grids)


def make_move(grid_string, char1, char2):
    """
    Calculates and performs the best move for char1 to get closer to char2.

    Args:
        grid_string (str): The string representation of the grid.
        char1 (str): The character to move.
        char2 (str): The target character.

    Returns:
        str: Updated grid string after moving char1.
    """
    grid = parse_grid(grid_string)

    # Generate possible moves
    possible_moves = generate_possible_moves(grid, char1)

    # Calculate distances
    distances = calculate_distances(possible_moves, char1, char2)

    # Find the best move
    best_move = find_best_move(distances)

    return grid_to_string(best_move)


def calculate_path_distance(grid, char1, char2):
    """
    Calculates the shortest path length between two characters in the grid, considering obstacles.

    Args:
        grid_string (str): The string representation of the grid.
        char1 (str): The starting character.
        char2 (str): The target character.

    Returns:
        int: The shortest path length between the two characters, or -1 if no path exists.
    """


    start = get_character_coordinates(grid, char1)
    target = get_character_coordinates(grid, char2)

    if not start or not target:
        raise ValueError(f"One or both characters ('{char1}', '{char2}') not found in the grid.")

    # Directions for moving: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # BFS setup
    queue = deque([(start, 0)])  # (current_position, path_length)
    visited = set()
    visited.add(start)

    while queue:
        (x, y), path_length = queue.popleft()

        # Check if we reached the target
        if (x, y) == target:
            return path_length

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check boundaries and obstacles
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and (nx, ny) not in visited:
                if grid[ny][nx] == ' ' or (nx, ny) == target:  # Allow moving into the target
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path_length + 1))

    # If no path is found
    return -1


def calculate_path_distances(grids, char1, char2):
    return map(lambda grid: (grid, calculate_path_distance(grid, char1, char2)), grids)


def make_smart_move(grid_string, char1, char2):
    """
    Calculates and performs the best move for char1 to get closer to char2.

    Args:
        grid_string (str): The string representation of the grid.
        char1 (str): The character to move.
        char2 (str): The target character.

    Returns:
        str: Updated grid string after moving char1.
    """
    grid = parse_grid(grid_string)

    # Generate possible moves
    possible_moves = generate_possible_moves(grid, char1)

    # Calculate distances
    distances = calculate_path_distances(possible_moves, char1, char2)

    # Find the best move
    best_move = find_best_move(distances)

    return grid_to_string(best_move)


# Example usage
n, m = 10, 15
# grid = generate_grid_with_characters(n, m)
grid = generate_maze_with_players(10,10)
print("Generated Grid:")
print(grid)

def play():
    global grid
    grid = make_move(grid, 'P', 'O')
    print("\nGrid After One Move:")
    print(grid)
    
play()

def smart_play():
    global grid
    grid = make_smart_move(grid, 'P', 'O')
    print("\nGrid After One Move:")
    print(grid)