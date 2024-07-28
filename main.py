import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
empty_background = pygame.image.load("Graphics/empty.jpg")
empty_background = pygame.transform.scale(empty_background, (screen_width, screen_height))
pygame.display.set_caption("MindMaze: The Emotional Odyssey")

# Emojis
emoji_happy = pygame.image.load("Graphics/emoji_happy.png")
emoji_sad = pygame.image.load("Graphics/emoji_sad.png")
emoji_angry = pygame.image.load("Graphics/emoji_angry.png")
emoji_neutral = pygame.image.load("Graphics/emoji_neutral.png")

# Set initial sizes and positions for emojis
emoji_size = (100, 100)
emoji_happy = pygame.transform.scale(emoji_happy, emoji_size)
emoji_sad = pygame.transform.scale(emoji_sad, emoji_size)
emoji_angry = pygame.transform.scale(emoji_angry, emoji_size)
emoji_neutral = pygame.transform.scale(emoji_neutral, emoji_size)

# Set font and size
font = pygame.font.SysFont(None, 65)
font_small = pygame.font.SysFont(None, 40)
font_tiny = pygame.font.SysFont(None, 30)

# Load the back button image
back_button_img = pygame.image.load("Graphics/back_button.png")
back_button_img = pygame.transform.scale(back_button_img, (50, 40))

# Load title image
title_image = pygame.image.load("Graphics/title_image.png")
title_image_rect = title_image.get_rect(center=(screen_width // 2, 110))
title_desc = pygame.image.load("Graphics/title_image2.png")
title_desc_rect = title_desc.get_rect(center=(screen_width // 2, 210))

# Feeling image
feeling_image = pygame.image.load("Graphics/feeling_text.png")
feeling_image_rect = feeling_image.get_rect(center=(screen_width // 2, 380))

# Emoji positions
emoji_positions = {
    "happy": (screen_width // 2 - 350, 430),
    "sad": (screen_width // 2 - 150, 430),
    "angry": (screen_width // 2 + 50, 430),
    "neutral": (screen_width // 2 + 250, 430)
}

# Interpolation variables
scaling_factor = 0.1
target_size = (120, 120)
current_sizes = {
    "happy": list(emoji_size),
    "sad": list(emoji_size),
    "angry": list(emoji_size),
    "neutral": list(emoji_size)
}

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Load images
player_img = pygame.image.load("Graphics/player.png")
npc_img = pygame.image.load("Graphics/npc.png")
key_img = pygame.image.load("Graphics/key.png")

# Player settings
player_size = 20
player_pos = [0, 0]
player_speed = 5

# Define walls (list of rects)
walls = []

#npc and key used for the sad level and the angry level
npc_pos = [screen_width // 2, screen_height // 2]
npc_size = 40
key_pos = [screen_width // 2, (screen_height // 2)-20]
key_size = 60
key_acquired = False
npc_rect = pygame.Rect(npc_pos[0], npc_pos[1], npc_size, npc_size)
npc_img = pygame.transform.scale(npc_img, (npc_size, npc_size))
key_rect = pygame.Rect(key_pos[0], key_pos[1], key_size, key_size)
key_img = pygame.transform.scale(key_img, (key_size, key_size))


# Goal position
goal_rect = pygame.Rect(screen_width - 60, screen_height - 60, 30, 30)

def is_over(pos, rect):
    """Check if the mouse is over a given rectangle"""
    return rect.collidepoint(pos)

#function for generating maze walls
def randomize_walls(level):
    """Randomize walls based on difficulty level"""
    walls.clear()
    cell_size = 80 if level == "happy" else 60 if level == "neutral" else 40 if level == "sad" else 30 # Larger cell size for easier maze
    #if level == "sad":

    cols, rows = screen_width // cell_size, screen_height // cell_size

    # Initialize grid and walls
    grid = [[False for _ in range(cols)] for _ in range(rows)]
    cell_walls = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]  # Top, Right, Bottom, Left walls

    #draw the maze walls
    def draw_maze():
        for y in range(rows):
            for x in range(cols):
                if cell_walls[y][x][0]:  # Top
                    walls.append(pygame.Rect(x * cell_size, y * cell_size, cell_size, 3))
                if cell_walls[y][x][1]:  # Right
                    walls.append(pygame.Rect((x + 1) * cell_size, y * cell_size, 3, cell_size))
                if cell_walls[y][x][2]:  # Bottom
                    walls.append(pygame.Rect(x * cell_size, (y + 1) * cell_size, cell_size, 3))
                if cell_walls[y][x][3]:  # Left
                    walls.append(pygame.Rect(x * cell_size, y * cell_size, 3, cell_size))

    def get_neighbors(x, y):
        neighbors = []
        if y > 0:
            neighbors.append((x, y - 1))
        if x < cols - 1:
            neighbors.append((x + 1, y))
        if y < rows - 1:
            neighbors.append((x, y + 1))
        if x > 0:
            neighbors.append((x - 1, y))
        return neighbors

    def remove_walls(current, next):
        cx, cy = current
        nx, ny = next
        dx = cx - nx
        if dx == 1:
            cell_walls[cy][cx][3] = False
            cell_walls[ny][nx][1] = False
        elif dx == -1:
            cell_walls[cy][cx][1] = False
            cell_walls[ny][nx][3] = False
        dy = cy - ny
        if dy == 1:
            cell_walls[cy][cx][0] = False
            cell_walls[ny][nx][2] = False
        elif dy == -1:
            cell_walls[cy][cx][2] = False
            cell_walls[ny][nx][0] = False

    # Maze generation using Recursive Backtracking
    stack = [(0, 0)]
    grid[0][0] = True

    while stack:
        current = stack[-1]
        neighbors = [n for n in get_neighbors(*current) if not grid[n[1]][n[0]]]
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            grid[next_cell[1]][next_cell[0]] = True
            stack.append(next_cell)
        else:
            stack.pop()

    # Draw the maze
    draw_maze()

def main_game(level):
    global back_rect, key_acquired, key_pos
    running = True
    clock = pygame.time.Clock()
    player_pos[:] = [10, 10]  # Reset player position
    randomize_walls(level)  # Randomize walls for the level

    npc_pos = [screen_width // 2 - npc_size // 2, screen_height // 2 - npc_size // 2]
    npc_rect = pygame.Rect(npc_pos[0], npc_pos[1], npc_size, npc_size)
    key_acquired = False  # Track if key is acquired

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(pygame.mouse.get_pos(), back_rect):
                    main_screen()

        # Movement
        keys = pygame.key.get_pressed()
        x_change = 0
        y_change = 0

        if keys[K_a] or keys[K_LEFT]:
            x_change = -player_speed
        if keys[K_d] or keys[K_RIGHT]:
            x_change = player_speed
        if keys[K_w] or keys[K_UP]:
            y_change = -player_speed + 2
        if keys[K_s] or keys[K_DOWN]:
            y_change = player_speed - 2

        # Update player position and handle collisions
        new_pos = player_pos.copy()
        new_pos[0] += x_change
        new_pos[1] += y_change

        player_rect = pygame.Rect(new_pos[0], new_pos[1], player_size, player_size)
        collision = False

        #player collision with wall to stop player from going on
        for wall in walls:
            if player_rect.colliderect(wall):
                collision = True
                break

        if not collision:
            player_pos[:] = new_pos
        else:
            if x_change != 0:
                new_pos = player_pos.copy()
                new_pos[0] += x_change
                player_rect = pygame.Rect(new_pos[0], player_pos[1], player_size, player_size)
                if not any(player_rect.colliderect(wall) for wall in walls):
                    player_pos[0] = new_pos[0]

        if y_change != 0:
            new_pos = player_pos.copy()
            new_pos[1] += y_change
            player_rect = pygame.Rect(player_pos[0], new_pos[1], player_size, player_size)
            if not any(player_rect.colliderect(wall) for wall in walls):
                player_pos[1] = new_pos[1]

        #player collide with NPC (map is either angry or sad)
        if player_rect.colliderect(npc_rect):
            #sad level means they acquire a key and should now head to the exit
            if level == "sad":
                key_acquired = True
                key_pos = [-150, -150]
                screen.blit(key_img, key_pos)
            #angry level means they win, the NPC is the way to exit
            elif level == "angry":
                display_message("Anger is like a storm. Take deep breaths or talk with a trusted adult to help let out some anger!")
                return

        # Check for level completion
        if player_rect.colliderect(goal_rect):
            #sad level but they didn't get the key so they do not complete the level
            if level == "sad" and not key_acquired:
                fail_text = font_small.render("You need a key to pass!", True, black)
                fail_rect = pygame.Rect(300, 50, fail_text.get_width(), fail_text.get_height())
                screen.blit(fail_text, (300, 50))
                pygame.display.flip()
                clock.tick(60)
            #angry level, meaning the exit sign isn't where they should go
            elif level == "angry":
                fail_text = font_small.render("Wrong final destination.", True, black)
                fail_rect = pygame.Rect(300, 50, fail_text.get_width(), fail_text.get_height())
                screen.blit(fail_text, (300, 50))
                pygame.display.flip()
                clock.tick(60)
            #either its happy or neutral levels or its a sad level but they acquired the key
            else:
                if level == "happy":
                    display_message("Happiness is like sunshine, it brightens your day and everyone around you.")
                if level == "sad":
                    display_message("If you're ever unhappy don't be afraid to reach out to a trusted adult!")
                if level == "angry":
                    display_message("Anger is like a storm. Talk with a trusted adult to help let out some anger!")
                if level == "neutral":
                    display_message("Sometimes our feelings are like calm waters, just smooth. That's perfectly okay.")
                return

        # Drawing
        screen.blit(empty_background, (0, 0))
        pygame.draw.rect(screen, blue, player_rect)
        for wall in walls:
            pygame.draw.rect(screen, black, wall)
        pygame.draw.rect(screen, (0, 255, 0), goal_rect)

        if level == "sad":
            screen.blit(npc_img, npc_pos)
            screen.blit(key_img, key_pos)

        if level == "angry":
            screen.blit(npc_img, npc_pos)


        # Draw back button
        back_rect = pygame.Rect(800, 40, 100, 50)
        screen.blit(back_button_img, back_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

def main_screen():
    """Display the main screen with emojis"""
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(mouse_pos, happy_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("happy")
                elif is_over(mouse_pos, sad_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("sad")
                elif is_over(mouse_pos, angry_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("angry")
                elif is_over(mouse_pos, neutral_rect):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    main_game("neutral")
        # Fill the screen with the background image
        background_image = pygame.image.load("Graphics/bg1.png")
        screen.blit(background_image, (0, 0))

        # Draw title image
        screen.blit(title_image, title_image_rect)
        screen.blit(title_desc, title_desc_rect)

        # Draw text img
        screen.blit(feeling_image, feeling_image_rect)

        # Calculate the box dimensions around all emojis
        box_left = emoji_positions["happy"][0] - 50
        box_top = emoji_positions["happy"][1] - 18
        box_width = emoji_positions["neutral"][0] + emoji_size[0] + 50 - box_left
        box_height = emoji_size[1] + 60

        # Draw emojis and get their rectangles
        happy_rect = screen.blit(emoji_happy, emoji_positions["happy"])
        sad_rect = screen.blit(emoji_sad, emoji_positions["sad"])
        angry_rect = screen.blit(emoji_angry, emoji_positions["angry"])
        neutral_rect = screen.blit(emoji_neutral, emoji_positions["neutral"])

        # Draw the filled grey box around all emojis
        pygame.draw.rect(screen, (178, 178, 178), (box_left, box_top, box_width, box_height), border_radius=30)
        # Draw the black border around the grey box
        pygame.draw.rect(screen, "black", (box_left, box_top, box_width, box_height), 3, border_radius=30)

        # Smooth scaling of emojis
        for emoji_key in emoji_positions.keys():
            rect = pygame.Rect(emoji_positions[emoji_key], emoji_size)
            if is_over(mouse_pos, rect):
                current_sizes[emoji_key][0] += (target_size[0] - current_sizes[emoji_key][0]) * scaling_factor
                current_sizes[emoji_key][1] += (target_size[1] - current_sizes[emoji_key][1]) * scaling_factor
            else:
                current_sizes[emoji_key][0] += (emoji_size[0] - current_sizes[emoji_key][0]) * scaling_factor
                current_sizes[emoji_key][1] += (emoji_size[1] - current_sizes[emoji_key][1]) * scaling_factor

            scaled_emoji = pygame.transform.scale(eval(f"emoji_{emoji_key}"), (int(current_sizes[emoji_key][0]), int(current_sizes[emoji_key][1])))
            screen.blit(scaled_emoji, (emoji_positions[emoji_key][0] - (scaled_emoji.get_width() - emoji_size[0]) // 2, emoji_positions[emoji_key][1] - (scaled_emoji.get_height() - emoji_size[1]) // 2))

        # Draw emotion texts under emojis
        screen.blit(font_tiny.render("Happy", True, black), (emoji_positions["happy"][0] + (emoji_size[0] // 2 - font_tiny.render("Happy", True, black).get_width() // 2), emoji_positions["happy"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Sad", True, black), (emoji_positions["sad"][0] + (emoji_size[0] // 2 - font_tiny.render("Sad", True, black).get_width() // 2), emoji_positions["sad"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Angry", True, black), (emoji_positions["angry"][0] + (emoji_size[0] // 2 - font_tiny.render("Angry", True, black).get_width() // 2), emoji_positions["angry"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Neutral", True, black), (emoji_positions["neutral"][0] + (emoji_size[0] // 2 - font_tiny.render("Neutral", True, black).get_width() // 2), emoji_positions["neutral"][1] + emoji_size[1] + 5))

        # Change the cursor to a pointer on hover
        if is_over(mouse_pos, happy_rect) or is_over(mouse_pos, sad_rect) or is_over(mouse_pos, angry_rect) or is_over(mouse_pos, neutral_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

# Define the display_message function
def display_message(message):
    """Display the message screen with a back button"""
    global back_rect
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(mouse_pos, back_rect):
                    main_screen()

        # Background
        screen.fill(white)

        # Display the message in the center of the screen
        font_large = pygame.font.SysFont(None, 30)
        text_surface = font_large.render(message, True, black)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

        # Draw back button
        back_rect = pygame.Rect(800, 50, 100, 50)
        screen.blit(back_button_img, back_rect)

        # Change the cursor to a pointer on back button
        if is_over(mouse_pos, back_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()
