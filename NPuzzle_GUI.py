import search
import state as st
import pygame
from arcade import sound as arcade

pygame.init()

# Constants
N = 3
WINDOW_WIDTH = N * 100
WINDOW_HEIGHT = N * 100
MARGIN = N * 10
table_width = WINDOW_WIDTH - 2 * MARGIN
table_height = WINDOW_HEIGHT - 2 * MARGIN

FPS = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (240, 247, 250)
BLUE_GRAY = (213, 227, 232)
BLUE = (104, 185, 222)
LIGHT_RED = (179, 64, 76)

FONT = pygame.font.Font(None, 40)

# Initialize the pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + 100))
screen.fill(WHITE)
pygame.display.set_caption("N-Puzzle")
clock = pygame.time.Clock()


# Draw the board
def draw_board(state):
    # Fill the screen with white and draw the table
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE_GRAY, (MARGIN, MARGIN, table_width, table_height))

    for i in range(N):
        for j in range(N):
            # Draw the numbers if they are not 0
            if state[0][i * N + j] != 0:

                # Draw the numbers
                text = FONT.render(str(state[0][i * N + j]), True, LIGHT_RED)
                screen.blit(text, (MARGIN + j * table_width // N + table_width // N // 2 - text.get_width() // 2,
                                   MARGIN + i * table_height // N + table_height // N // 2 - text.get_height() // 2))

            else:
                # Draw the empty cell
                pygame.draw.rect(screen, LIGHT_BLUE, (
                    MARGIN + j * table_width // N, MARGIN + i * table_height // N, table_width // N,
                    table_height // N))

            # Draw the grid which is a table of N x N with Margin
            pygame.draw.rect(screen, BLACK, (
                MARGIN + j * table_width // N, MARGIN + i * table_height // N, table_width // N, table_height // N), 1)

    pygame.draw.rect(screen, BLACK, (MARGIN, MARGIN, table_width, table_height), N)
    pygame.display.update(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    clock.tick(FPS)


# Draw the solve button
def draw_solve_button():
    pygame.draw.rect(screen, BLUE_GRAY, (MARGIN, WINDOW_HEIGHT + 20, table_width, 50), 0, 10)
    text = FONT.render("Solve", True, BLACK)
    screen.blit(text, (MARGIN + table_width // 2 - text.get_width() // 2, WINDOW_HEIGHT + 45 - text.get_height() // 2))
    pygame.display.flip()


# Solve the puzzle
def solve_puzzle(moves, state):
    # Write "Solving..." on the screen
    # Show that we are in solution
    text = FONT.render("Solving...", True, BLACK)

    draw_board(state)
    pygame.display.flip()

    screen.blit(text, (MARGIN + table_width // 2 - text.get_width() // 2, WINDOW_HEIGHT + 45 - text.get_height() // 2))
    pygame.display.flip()

    for move in moves:
        print(move)
        # move_empty_cell(state[0], move)
        st.if_legal(state[0], move)

        # Make sound when the cell is moving
        sound = arcade.Sound("moving_box_sound.wav", True)
        arcade.Sound.play(sound, 0.1, 0, False, 2)
        draw_board(state)

    draw_solve_button()
    draw_board(state)


# Main function
def main():
    state = st.create(N)
    draw_board(state)
    draw_solve_button()

    while True:
        # Go through all the events (for any click or key press)
        for event in pygame.event.get():

            # Quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Check if the key is pressed
            if event.type == pygame.KEYDOWN:

                # The arrow is the opposite of the movement because the 0 is moving
                last_pos = state[0].index(0)

                if event.key == pygame.K_UP:
                    st.if_legal(state[0], "v")
                elif event.key == pygame.K_DOWN:
                    st.if_legal(state[0], "^")
                elif event.key == pygame.K_LEFT:
                    st.if_legal(state[0], ">")
                elif event.key == pygame.K_RIGHT:
                    st.if_legal(state[0], "<")

                if last_pos != state[0].index(0):
                    # Make sound when the user moves the cell
                    sound = arcade.Sound("moving_box_sound.wav", True)
                    arcade.Sound.play(sound, 0.1, 0, False, 2)

                # Draw the board after any movement
                draw_board(state)

            # Check if the mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # if the solve button is clicked
                if MARGIN <= x <= MARGIN + table_width and WINDOW_HEIGHT + 20 <= y <= WINDOW_HEIGHT + 80:
                    # Solve the puzzle
                    solution = state.copy()
                    state = search.search(state)
                    solve_puzzle(state[1], solution)
                    state[1] = ""

                # if the board is clicked
                elif MARGIN <= x <= MARGIN + table_width and MARGIN <= y <= MARGIN + table_height:
                    # Get index of the pressed cell
                    x = (x - MARGIN) // (table_width // N)
                    y = (y - MARGIN) // (table_height // N)
                    index = y * N + x

                    # Get the way to move the cell
                    if index-state[0].index(0) == 1:
                        st.if_legal(state[0], ">")
                    elif index-state[0].index(0) == -1:
                        st.if_legal(state[0], "<")
                    elif index-state[0].index(0) == N:
                        st.if_legal(state[0], "v")
                    elif index-state[0].index(0) == -N:
                        st.if_legal(state[0], "^")

                    # Make sound when the user moves the cell
                    sound = arcade.Sound("moving_box_sound.wav", True)
                    arcade.Sound.play(sound, 0.1, 0, False, 2)
                    draw_board(state)


if __name__ == "__main__":
    main()
