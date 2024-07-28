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

# Player settings
player_size = 40
player_pos = [50, 50]
player_speed = 5

# Define walls (list of rects)
walls = []

# Goal position
goal_rect = pygame.Rect(screen_width-60, screen_height-60, 50, 50)

def is_over(pos, rect):
    """Check if the mouse is over a given rectangle"""
    return rect.collidepoint(pos)

def randomize_walls(level):
    """Randomize walls based on difficulty level"""
    walls.clear()
    # Outer walls
    walls.extend([
        pygame.Rect(0, 0, screen_width, 10),
        pygame.Rect(0, 0, 10, screen_height),
        pygame.Rect(0, screen_height-10, screen_width, 10),
        pygame.Rect(screen_width-10, 0, 10, screen_height),
    ])

    # Add inner walls
    wall_count = { "happy": 5, "sad": 10, "angry": 15, "neutral": 20 }
    for _ in range(wall_count[level]):
        x = random.randint(50, screen_width - 100)
        y = random.randint(50, screen_height - 100)
        width = random.choice([10, 200])
        height = random.choice([10, 200])
        walls.append(pygame.Rect(x, y, width, height))

def main_game(level):
    global back_rect
    running = True
    clock = pygame.time.Clock()
    player_pos[:] = [50, 50]  # Reset player position
    randomize_walls(level)  # Randomize walls for the level

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if is_over(pygame.mouse.get_pos(), back_rect):
                    main_screen()
                    return

        # Movement
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            player_pos[0] -= player_speed
        if keys[K_d] or keys[K_RIGHT]:
            player_pos[0] += player_speed
        if keys[K_w] or keys[K_UP]:
            player_pos[1] -= player_speed
        if keys[K_s] or keys[K_DOWN]:
            player_pos[1] += player_speed

        # Collision detection with walls
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[K_a] or keys[K_LEFT]:
                    player_pos[0] += player_speed
                if keys[K_d] or keys[K_RIGHT]:
                    player_pos[0] -= player_speed
                if keys[K_w] or keys[K_UP]:
                    player_pos[1] += player_speed
                if keys[K_s] or keys[K_DOWN]:
                    player_pos[1] -= player_speed

        # Check for level completion
        if player_rect.colliderect(goal_rect):
            display_message("You Win!")
            return

        # Drawing
        screen.fill(white)
        pygame.draw.rect(screen, blue, player_rect)
        for wall in walls:
            pygame.draw.rect(screen, black, wall)
        pygame.draw.rect(screen, (0, 255, 0), goal_rect)

        # Draw back button
        back_text = font_small.render("Back", True, black)
        back_rect = pygame.Rect(50, 50, back_text.get_width(), back_text.get_height())
        pygame.draw.rect(screen, white, back_rect)
        screen.blit(back_text, (50, 50))

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
                    main_game("happy")
                elif is_over(mouse_pos, sad_rect):
                    main_game("sad")
                elif is_over(mouse_pos, angry_rect):
                    main_game("angry")
                elif is_over(mouse_pos, neutral_rect):
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
        if any(is_over(mouse_pos, pygame.Rect(emoji_positions[emoji_key], emoji_size)) for emoji_key in emoji_positions.keys()):
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
                    running = False
                    main_screen()

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
