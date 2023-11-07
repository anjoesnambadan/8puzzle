import numpy as np
import time
import pygame

initial_state = np.array([[0, 1, 4], [3, 7, 5], [2, 8, 6]])
target_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

depth = 0
moves = []
closed_set = set()

def count_inversions(matrix):
    inversion_count = 0
    puzzle_list = matrix.ravel()

    for i in range(len(puzzle_list)):
        for j in range(i + 1, len(puzzle_list)):
            if puzzle_list[i] > puzzle_list[j] and puzzle_list[i] != 0 and puzzle_list[j] != 0:
                inversion_count += 1

    solvable = True if (inversion_count % 2 == 0) else False
    return solvable

def manhattan(matrix):
    distance = 0
    for i in range(3):
        for j in range(3):
            [[x], [y]]= np.argwhere(target_state == matrix[i][j]).T
            distance += abs(x-i) + abs(y-j)
    return distance
        
def next_best(matrix, depth, max_depth):
    if(np.array_equal(matrix, target_state)):
        print("Solution Found in {0} moves".format(len(closed_set)))
        return True
    
    elif(depth >= max_depth):
        print("Solution not found at given depth")
        return False

    else:
        depth = depth + 1
        up = np.copy(matrix)
        down = np.copy(matrix)
        left = np.copy(matrix)
        right = np.copy(matrix)
        best_option = np.copy(matrix)
        min_manhattan = 99

        [[x], [y]]= np.argwhere(matrix == 0).T
        if(x-1 >= 0):
            up[x, y], up[x-1, y] = up[x-1, y], up[x, y]
            man = manhattan(up)
            if(man < min_manhattan and tuple(up.flatten()) not in closed_set):
                min_manhattan = man
                best_option = up
                last_move = 'U'

        if(x+1 < 3):
            down[x, y], down[x+1, y] = down[x+1, y], down[x, y]
            man = manhattan(down)
            if(man < min_manhattan and tuple(down.flatten()) not in closed_set):
                min_manhattan = man
                best_option = down
                last_move = 'D'

        if(y-1 >= 0):
            left[x, y], left[x, y-1] = left[x, y-1], left[x, y]
            man = manhattan(left)
            if(man < min_manhattan and tuple(left.flatten()) not in closed_set):
                min_manhattan = man
                best_option = left
                last_move = 'L'
    
        if(y+1 < 3):
            right[x, y], right[x, y+1] = right[x, y+1], right[x, y]
            man = manhattan(right)
            if(man < min_manhattan and tuple(right.flatten()) not in closed_set):
                min_manhattan = man
                best_option = right
                last_move = 'R'

        closed_set.add(tuple(best_option.flatten()))

        moves.append(last_move)

        return next_best(best_option, depth, max_depth)    

def render():
    pygame.init()

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    # Create a 3x3 matrix (you can replace this with your matrix)
    matrix = initial_state

    # Define the screen dimensions
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 300
    CELL_SIZE = SCREEN_WIDTH // 3
    BORDER_WIDTH = 2

    # Create a Pygame window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3x3 Matrix")

    # Create a font for rendering the text
    font = pygame.font.SysFont("timesnewroman", 36)

    # Main game loop
    running = True
    move_index = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if(move_index <= len(moves)):
            # Clear the screen
            screen.fill(WHITE)

            # Display the current 3x3 matrix
            for i in range(3):
                for j in range(3):
                    cell_value = matrix[i][j]
                    if(cell_value != 0):
                        text = font.render(str(cell_value), True, BLACK)
                    else:
                        if(move_index == len(moves)):
                            text = font.render("•", True, GREEN)
                        elif(moves[move_index] == 'U'):
                            text = font.render(u'\u2191', True, GREEN)
                        elif(moves[move_index] == 'D'):
                            text = font.render(u'\u2193', True, GREEN)
                        elif(moves[move_index] == 'L'):
                            text = font.render(u'\u2190', True, GREEN)
                        elif(moves[move_index] == 'R'):
                            text = font.render(u'\u2192', True, GREEN)

                    text_rect = text.get_rect()
                    cell_rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
                    # Draw the cell with a border
                    pygame.draw.rect(screen, BLACK, cell_rect, BORDER_WIDTH)
            
                    # Center the text within the cell
                    text_rect.center = cell_rect.center
                    screen.blit(text, text_rect)

            # Update the display
            pygame.display.flip()

            # Apply the current move
            if(move_index < len(moves)):
                current_move = moves[move_index]
                [[x], [y]] = np.argwhere(matrix == 0).T
                if current_move == 'U':
                    matrix[x, y], matrix[x - 1, y] = matrix[x - 1, y], matrix[x, y]
                elif current_move == 'D':
                    matrix[x, y], matrix[x + 1, y] = matrix[x + 1, y], matrix[x, y]
                elif current_move == 'L':
                    matrix[x, y], matrix[x, y - 1] = matrix[x, y - 1], matrix[x, y]
                elif current_move == 'R':
                    matrix[x, y], matrix[x, y + 1] = matrix[x, y + 1], matrix[x, y]

                move_index += 1

            # Sleep for a moment to show the move
            time.sleep(0.2)

    pygame.quit()

def main():
    if(count_inversions(initial_state)):
        max_depth = int(input("Enter the depth limit: "))
        start_time = time.time()
        is_solved = next_best(initial_state, depth, max_depth)
        end_time = time.time()
        print(f"Runtime: {end_time - start_time} seconds")
        if(is_solved):
            render()
    else:
        print("Cannot be solved.")

main()