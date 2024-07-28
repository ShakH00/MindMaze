import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MindMaze: The Emotional Odyssey")

white = (255, 255, 255)
black = (0, 0, 0)
TILE_SIZE = 64
WIDTH = TILE_SIZE*10
HEIGHT = TILE_SIZE*10
player = pygame.image.load("Graphics/player.png")
player = pygame.transform.scale(player, (64,64))
playerX = (1*TILE_SIZE)+125
playerY = (1*TILE_SIZE)-20
x_change = 0
y_change = 0
tile_options = ['empty','wall','endgoal','npc']
rows, cols = (10, 10)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Emojis
emoji_happy = pygame.image.load("Graphics/emoji_happy.png")
emoji_sad = pygame.image.load("Graphics/emoji_sad.png")
emoji_angry = pygame.image.load("Graphics/emoji_angry.png")
emoji_neutral = pygame.image.load("Graphics/emoji_neutral.png")

# Scale emojis
emoji_size = (100, 100)
emoji_happy = pygame.transform.scale(emoji_happy, emoji_size)
emoji_sad = pygame.transform.scale(emoji_sad, emoji_size)
emoji_angry = pygame.transform.scale(emoji_angry, emoji_size)
emoji_neutral = pygame.transform.scale(emoji_neutral, emoji_size)

# Set font and size
font = pygame.font.SysFont(None, 65)
font_small = pygame.font.SysFont(None, 40)
font_tiny = pygame.font.SysFont(None, 30)

# Render text
# feeling_text = font_small.render("How are you feeling today?", True, black)

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

def is_over(pos, rect):
    """Check if the mouse is over a given rectangle"""
    return rect.collidepoint(pos)

def get_player_position():
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            if maze[row][column] == 4:
                return [row,column]

#algorithm used for generating maze levels
def create_maze(emotion):
    global x_change, y_change, cur_row, cur_col
    running = True
    while running:
        screen.fill(white)
        for row in range(len(maze)):
            for column in range(len(maze[row])):
                x = (column * TILE_SIZE) + 125
                y = (row * TILE_SIZE) - 20
                if maze[row][column] == 4:
                    chosen_tile = pygame.image.load(f"Graphics/empty.png")
                    chosen_tile = pygame.transform.scale(chosen_tile, (64, 64))
                    screen.blit(chosen_tile, (x, y))
                else:
                    tile = tile_options[maze[row][column]]
                    chosen_tile = pygame.image.load(f"Graphics/{tile}.png")
                    chosen_tile = pygame.transform.scale(chosen_tile, (64, 64))
                    screen.blit(chosen_tile, (x, y))
        global playerX, playerY
        cur_row = int(get_player_position()[0])
        cur_col = int(get_player_position()[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:


                if(event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    playerX += 64
                    cur_col += 1
                elif(event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    x_change = -64
                    cur_col -= 1
                elif(event.key == pygame.K_UP or event.key == pygame.K_w):
                    y_change = -64
                    row -= 1
                elif(event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    y_change = 64
                    row += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_d or event.key == pygame.K_a:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    y_change = 0
        playerX += x_change
        playerY += y_change
        tileChosen = tile_options[maze[cur_row,cur_col]]
        if tileChosen == 'empty':
            screen.blit(player, (playerX, playerY))
        elif tileChosen == 'endgoal':
            print("COMPLETED!")


        pygame.display.flip()


        #screen.blit(player,(playerX,playerY))




    #if emotion == "happy":

    #elif emotion == "sad":

    #elif emotion == "angry":

    #elif emotion == "neutral":


#function to display the maze on the screen
def display_maze(maze_txt):
    running = True

def main_screen():
    """Display the main screen with emojis"""
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        cursor_changed = False

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(mouse_pos, happy_rect):
                    #display_message("Happy")
                    create_maze("happy")
                elif is_over(mouse_pos, sad_rect):
                    display_message("Sad")
                    #create_maze("sad")
                elif is_over(mouse_pos, angry_rect):
                    display_message("Angry")
                    #create_maze("angry")
                elif is_over(mouse_pos, neutral_rect):
                    display_message("Neutral")
                    #create_maze("neutral")

        # Fill the screen with the background image
        background_image = pygame.image.load("Graphics/bg.jpg")
        screen.blit(background_image, (0, 0))

        # Draw title image
        screen.blit(title_image, title_image_rect)
        screen.blit(title_desc, title_desc_rect)

        # Draw text img
        screen.blit(feeling_image, feeling_image_rect)

        # Draw emojis and get their rectangles
        happy_rect = screen.blit(emoji_happy, emoji_positions["happy"])
        sad_rect = screen.blit(emoji_sad, emoji_positions["sad"])
        angry_rect = screen.blit(emoji_angry, emoji_positions["angry"])
        neutral_rect = screen.blit(emoji_neutral, emoji_positions["neutral"])

        # Calculate the box dimensions around all emojis
        box_left = emoji_positions["happy"][0] - 50
        box_top = emoji_positions["happy"][1] - 18
        box_width = emoji_positions["neutral"][0] + emoji_size[0] + 50 - box_left
        box_height = emoji_size[1] + 60

        # Draw the big box around all emojis
        pygame.draw.rect(screen, black, (box_left, box_top, box_width, box_height), 3, border_radius=30)

        # Draw emotion texts under emojis
        screen.blit(font_tiny.render("Happy", True, black), (emoji_positions["happy"][0] + (emoji_size[0] // 2 - font_tiny.render("Happy", True, black).get_width() // 2), emoji_positions["happy"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Sad", True, black), (emoji_positions["sad"][0] + (emoji_size[0] // 2 - font_tiny.render("Sad", True, black).get_width() // 2), emoji_positions["sad"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Angry", True, black), (emoji_positions["angry"][0] + (emoji_size[0] // 2 - font_tiny.render("Angry", True, black).get_width() // 2), emoji_positions["angry"][1] + emoji_size[1] + 5))
        screen.blit(font_tiny.render("Neutral", True, black), (emoji_positions["neutral"][0] + (emoji_size[0] // 2 - font_tiny.render("Neutral", True, black).get_width() // 2), emoji_positions["neutral"][1] + emoji_size[1] + 5))


        # Check if the mouse is over any emoji and change the cursor to a pointer
        if is_over(mouse_pos, happy_rect) or is_over(mouse_pos, sad_rect) or is_over(mouse_pos, angry_rect) or is_over(mouse_pos, neutral_rect):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            cursor_changed = True

        if not cursor_changed:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Update the display
        pygame.display.flip()

def display_message(message):
    """Display the message screen with a back button"""
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
                    running = False

        # Background
        screen.fill(white)

        # Display message
        message_text = font.render(message, True, black)
        screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2 - message_text.get_height() // 2))

        # Draw back button
        back_text = font_small.render("Back", True, black)
        back_rect = pygame.Rect(50, 50, back_text.get_width(), back_text.get_height())
        pygame.draw.rect(screen, white, back_rect)
        screen.blit(back_text, (50, 50))

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