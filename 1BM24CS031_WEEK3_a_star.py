import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board        # Flat tuple of length 9 representing 3x3 grid
        self.parent = parent      # Link to parent state to reconstruct path
        self.move = move          # Direction taken to reach this state
        self.g = g                # Cost from start to current node
        self.h = h                # Estimated cost from current node to goal
        self.f = g + h            # Total evaluation function: f(n) = g(n) + h(n)

    def __lt__(self, other):
        return self.f < other.f

def get_misplaced_tiles(board, goal):
    """Heuristic function: Counts how many tiles are not in their target positions."""
    count = 0
    for i in range(9):
        # Ignore the blank space (0) per standard 8-puzzle heuristic rules
        if board[i] != 0 and board[i] != goal[i]:
            count += 1
    return count

def get_neighbors(state, goal):
    """Generates all valid next states by shifting the blank tile (0)."""
    neighbors = []
    zero_idx = state.board.index(0)
    row, col = divmod(zero_idx, 3)
    
    # Valid directional moves for the blank tile: (row_offset, col_offset, move_name)
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
    
    for dr, dc, move_name in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_idx = new_row * 3 + new_col
            
            # Create a new board layout by swapping the tiles
            new_board = list(state.board)
            new_board[zero_idx], new_board[new_zero_idx] = new_board[new_zero_idx], new_board[zero_idx]
            new_board_tuple = tuple(new_board)
            
            g_score = state.g + 1
            h_score = get_misplaced_tiles(new_board_tuple, goal)
            
            neighbors.append(PuzzleState(new_board_tuple, state, move_name, g_score, h_score))
            
    return neighbors

def solve_8_puzzle(start_board, goal_board):
    """Solves the 8-puzzle using the A* Search Algorithm with Misplaced Tiles heuristic."""
    start_tuple = tuple(start_board)
    goal_tuple = tuple(goal_board)
    
    initial_state = PuzzleState(start_tuple, g=0, h=get_misplaced_tiles(start_tuple, goal_tuple))
    open_list = [initial_state]
    closed_set = set()
    
    while open_list:
        current_state = heapq.heappop(open_list)
        
        if current_state.board == goal_tuple:
            return current_state
            
        closed_set.add(current_state.board)
        
        for neighbor in get_neighbors(current_state, goal_tuple):
            if neighbor.board in closed_set:
                continue
                
            heapq.heappush(open_list, neighbor)
            
    return None

def get_user_input(prompt_name):
    """Helper function to read a 3x3 board arrangement from the user row by row."""
    print(f"\nEnter the {prompt_name} grid configuration row by row.")
    print("Use numbers 1-8 for tiles, and 0 for the blank space. Separate numbers with spaces.")
    board = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").split()))
                if len(row) != 3:
                    print("Error: Each row must contain exactly 3 numbers.")
                    continue
                board.extend(row)
                break
            except ValueError:
                print("Error: Please enter numbers only.")
                
    # Validate entire board structure
    if sorted(board) != list(range(9)):
        print("Warning: The grid configuration must contain all numbers from 0 to 8 exactly once.")
        return get_user_input(prompt_name) # Retry input on error
        
    return board

def print_solution(solution_state):
    """Traces and visually prints the moves from start to goal layout."""
    path = []
    current = solution_state
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    
    print(f"\nTotal steps required: {len(path) - 1}\n")
    for step, state in enumerate(path):
        if step == 0:
            print("Initial State:")
        else:
            print(f"Step {step} — Move Blank: {state.move}")
            
        for i in range(0, 9, 3):
            print(f" {state.board[i]} {state.board[i+1]} {state.board[i+2]} ")
        print("-" * 15)

if __name__ == "__main__":
    print("--- 8-Puzzle Solver ---")
    initial_puzzle = get_user_input("STARTING")
    target_puzzle = get_user_input("GOAL")
    
    print("\nCalculating path...")
    solution = solve_8_puzzle(initial_puzzle, target_puzzle)
    
    if solution:
        print_solution(solution)
    else:
        print("\nThis specific puzzle configuration cannot be solved.")
