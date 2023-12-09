import pygame
import os
import random

pygame.mixer.init()
pygame.font.init()

pygame.mixer.music.load(os.path.join("Assets", "Battle of Heroes.ogg"))
pygame.mixer.music.play()

# All Constants
TITLE = "Python Space War"
WIDTH, HEIGHT = 1200, 600
WIN = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED | pygame.NOFRAME
)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
CLOCK = pygame.time.Clock()
# Colors
COLORS = ["blue", "gray", "green", "pink", "purple", "red", "teal", "white", "yellow"]
COLOR_CODES = {
    "blue": (0, 0, 255),
    "gray": (138, 138, 138),
    "green": (0, 255, 0),
    "pink": (255, 0, 255),
    "purple": (75, 0, 130),
    "red": (255, 0, 0),
    "teal": (0, 255, 255),
    "white": (255, 255, 255),
    "yellow": (255, 232, 31),
    "black": (0, 0, 0),
}
# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
WINNER_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Fanfare.mp3"))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Explosion.mp3"))
LASER_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Space_Laser.mp3"))

# Fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 40, bold=False, italic=False)
WINNER_FONT = pygame.font.SysFont("comincsans", 100, bold=True, italic=False)
SMALL_TEXT = pygame.font.SysFont("comincsans", 30, bold=False, italic=True)
# Intensity Metrics
INTENSITIES = [
    {"vel": 5, "bullet_vel": 7.5, "max_bullets": 3, "health": 10},
    {"vel": 7.5, "bullet_vel": 10, "max_bullets": 6, "health": 20},
    {"vel": 10, "bullet_vel": 15, "max_bullets": 10, "health": 30},
    {"vel": 15, "bullet_vel": 25, "max_bullets": 15, "health": 40},
    {"vel": 20, "bullet_vel": 35, "max_bullets": 30, "health": 150},
]
INTENSITY_DESC = [
    "Friendly",
    "Competitive",
    "Champion",
    "Ridiculous",
    "Don't Play This Level!",
]
VEL = INTENSITIES[0]["vel"]
BULLET_VEL = INTENSITIES[0]["bullet_vel"]
MAX_BULLETS = INTENSITIES[0]["max_bullets"]
HEALTH = INTENSITIES[0]["health"]
# Spaceship specifications
SHIP_COLORS = [COLORS[0], COLORS[1]]
SPACESHIP_SIZE = (90, 60)
SPACESHIP_WIDTH = SPACESHIP_SIZE[0]
SPACESHIP_HEIGHT = SPACESHIP_SIZE[1]
SHIP_2_HIT = pygame.USEREVENT + 1
SHIP_1_HIT = pygame.USEREVENT + 2
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", f"space{random.randint(1, 6)}.jpeg")),
    (WIDTH, HEIGHT),
)


# Extend pygame.Rect class to offer customized attributes
class Ship(pygame.Rect):
    angle = 90  # Keep track of the ships rotation

    def __init__(self, x, y, width, height, color, health):
        # Call the constructor of the parent class (pygame.Rect)
        super().__init__(x, y, width, height)
        self.color = color  # Give the ship color
        self.health = health  # Give the ship health
        self.bullets = []  # Initialize bullet list

        # Assign the ship its corresponding image
        self.image = pygame.image.load(os.path.join("Assets", f"spaceship_{color}.png"))

        # Rotate the ship to face the middle
        self.ship = pygame.transform.rotate(
            pygame.transform.scale(self.image, SPACESHIP_SIZE), Ship.angle
        )
        self.angle = Ship.angle

        # Change static variable to reflect rotational changes
        Ship.angle = 270 if Ship.angle == 90 else 90

    def __str__(self):
        return f"{self.color.capitalize()} Wins!"

    def destroyed(self):
        self.image = pygame.image.load(os.path.join("Assets", f"Explosion.png"))
        self.ship = pygame.transform.rotate(
            pygame.transform.scale(self.image, SPACESHIP_SIZE), Ship.angle
        )
        EXPLOSION_SOUND.play()


# Draw all objects onto the window
def draw_window(ship_1: Ship = None, ship_2: Ship = None):
    """Draws the updated window onto the screen. Two main configurations:
    1. Introduction: Activated when Ship args are not passed. This just displays the background and updates the display
    2. Main Gameplay: Activated when Ship args are passed. Displays background, ship health, ships, and bullets


    Args:
        ship_1 (Ship, optional): First ship object. Defaults to None.
        ship_2 (Ship, optional): Second ship object. Defaults to None.
    """
    # Display background
    WIN.blit(SPACE, (0, 0))

    # If called during main gameplay
    if ship_1 != None and ship_2 != None:
        # Display ships' health
        ship_1_health_text = HEALTH_FONT.render(
            f"Health: {ship_1.health}", 1, COLOR_CODES["white"]
        )
        ship_2_health_text = HEALTH_FONT.render(
            f"Health: {ship_2.health}", 1, COLOR_CODES["white"]
        )
        WIN.blit(ship_1_health_text, (30, 10))
        WIN.blit(ship_2_health_text, (WIDTH - ship_2_health_text.get_width() - 30, 10))

        # Display ships and their respective bullets
        for ship in [ship_1, ship_2]:
            WIN.blit(ship.ship, (ship.x, ship.y))
            for bullet in ship.bullets:
                pygame.draw.rect(WIN, ship.color, bullet)

    # Update game display
    pygame.display.update()


# Handle all movement from spaceship 1
def ship_1_handle_movement(ship_1: Ship, keys_pressed: list):
    """Moves the ship dependent upon the keys pressed by the user. Uses W-A-S-D. Checks to make sure ship is within its bounds
    W = Up
    A = Left
    S = Down
    D = Right

    Args:
        ship_1 (Ship): first ship object
        keys_pressed (list): the keys pressed during the most recent iteration of the game program
    """
    # Move ship left
    ship_1.x -= VEL if keys_pressed[pygame.K_a] and ship_1.x > 0 else 0
    # Move ship right
    ship_1.x += (
        VEL
        if keys_pressed[pygame.K_d] and ship_1.x < BORDER.x - ship_1.width / 1.3
        else 0
    )
    # Move ship down
    ship_1.y += (
        VEL
        if keys_pressed[pygame.K_s] and ship_1.y + ship_1.height * 1.5 < HEIGHT
        else 0
    )
    # Move ship up
    ship_1.y -= VEL if keys_pressed[pygame.K_w] and ship_1.y > 0 else 0


# Handle all movement from spaceship 2
def ship_2_handle_movement(ship_2: Ship, keys_pressed: list):
    """Moves the ship dependent upon the keys pressed by the user. Uses UP-LEFT-DOWN-RIGHT keys. Checks to make sure ship is within its bounds.

    Args:
        ship_2 (Ship): second ship object
        keys_pressed (list): the keys pressed during the most recent iteration of the game program
    """
    # Move ship left
    ship_2.x -= (
        VEL
        if keys_pressed[pygame.K_LEFT] and ship_2.x > BORDER.x + BORDER.width * 1.5
        else 0
    )
    # Move ship right
    ship_2.x += (
        VEL
        if keys_pressed[pygame.K_RIGHT] and ship_2.x + ship_2.width / 1.3 < WIDTH
        else 0
    )
    # Move ship down
    ship_2.y += (
        VEL
        if keys_pressed[pygame.K_DOWN] and ship_2.y + ship_2.height * 1.5 < HEIGHT
        else 0
    )
    # Move ship down
    ship_2.y -= VEL if keys_pressed[pygame.K_UP] and ship_2.y > 0 else 0


# Handle all bullet operations
def handle_bullets(ship_1: Ship, ship_2: Ship):
    """Handles all bullet functions for both ships
    1. Moves bullets in the direction they were fired
    2. Checks to see if bullet fired with opposing ship
        a. Posts HIT event
        b. Removes bullet
    3. Checks to see if bullet has gone off screen
        a. Removes bullet

    Args:
        ship_1 (Ship): _description_
        ship_2 (Ship): _description_
    """
    for bullet in ship_1.bullets:
        bullet.x += BULLET_VEL
        if ship_2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SHIP_2_HIT))
            ship_1.bullets.remove(bullet)
        elif bullet.x + bullet.width > WIDTH:
            ship_1.bullets.remove(bullet)

    for bullet in ship_2.bullets:
        bullet.x -= BULLET_VEL
        if ship_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SHIP_1_HIT))
            ship_2.bullets.remove(bullet)
        elif bullet.x < 0:
            ship_2.bullets.remove(bullet)


# All operations after game ends
def draw_winner(text: str, ship_1: Ship, ship_2: Ship) -> bool:
    """Handles all window events when the game ends.
    1. Plays winner sound
    2. Draws winner text onto the screen
    3. Prompts user to play again
    4. Handles user input on whether they want to play again

    Args:
        text (str): Text defining which player won.
        ship_1 (Ship): Player 1 Ship object
        ship_2 (Ship): Player 1 Ship object

    Returns:
        bool: Whether user wants to play again
    """
    draw_window(ship_1, ship_2)

    # Make texts
    draw_text = WINNER_FONT.render(text, 1, COLOR_CODES["white"])
    replay_text = HEALTH_FONT.render("Want to play again?", 1, COLOR_CODES["white"])
    yes_or_no = HEALTH_FONT.render("Yes: y           No: n", 1, COLOR_CODES["white"])

    # Post winner text
    WIN.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()

    pygame.time.delay(1000)
    # Play winner fanfare
    WINNER_SOUND.play()
    # Wait 2 seconds
    pygame.time.delay(2000)

    # Post play again text
    WIN.blit(
        replay_text,
        (
            WIDTH / 2 - replay_text.get_width() / 2,
            HEIGHT / 2 + draw_text.get_height(),
        ),
    )
    WIN.blit(
        yes_or_no,
        (
            WIDTH / 2 - replay_text.get_width() / 2,
            HEIGHT / 2 + draw_text.get_height() + replay_text.get_height(),
        ),
    )
    pygame.display.update()

    # Gives user 30 seconds to make a rematch decision or else auto quits
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 30000:
        for event in pygame.event.get():
            # User quit window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                # User clicked 'y' --> Wants to play again
                if event.key == pygame.K_y:
                    return True
                # User clicked 'n' --> Does not want to play again
                elif event.key == pygame.K_n:
                    return False
    # If no decision after 30 sec, assume users do not want to play again
    return False


# Fire bullets
def fire_bullets(ship: Ship):
    """Creates new bullet and adds to ship's bullet list.
    Plays bullet firing sound

    Args:
        ship (Ship): Ship object (can be either player)
    """
    ship.bullets.append(
        pygame.Rect(
            ship.x + ship.width / 1.5 - 5,
            ship.y + ship.height / 1.5 + 3,
            15,
            6,
        )
    )
    if HEALTH != 150:
        BULLET_FIRE_SOUND.play()


# Ops if bullet hits ship
def bullet_hit(health: int) -> int:
    """Plays the bullet collided sound and decrements ship's health by 1

    Args:
        health (int): the ships current health

    Returns:
        int: the ships health decremented by 1
    """
    if HEALTH != 150:
        BULLET_HIT_SOUND.play()
    return health - 1


# Check to see if health is at 0
def is_game_over(ship_1: Ship, ship_2: Ship) -> bool:
    """Check the health of both ships. If either ships' health is 0, end game.

    Args:
        ship_1 (Ship): Player 1 ship
        ship_2 (Ship): Player 2 ship

    Returns:
        bool: Is game over
    """
    if ship_1.health <= 0 or ship_2.health <= 0:
        return True
    return False


# Decides which ship won the game
def decide_winner(ship_1: Ship, ship_2: Ship):
    """Checks to see which ship has been destroyed.
    Destroys the losing ship
    Calls draw_winner() function
    Quits if user decides not to play again

    Args:
        ship_1 (Ship): Player 1 ship
        ship_2 (Ship): Player 2 ship
    """
    # Check health of player 1 ship
    if ship_1.health <= 0:
        winner_text = ship_2.__str__()
        ship_1.destroyed()
    # Check health of player 2 ship
    elif ship_2.health <= 0:
        winner_text = ship_1.__str__()
        ship_2.destroyed()

    # Display endgame text. Prompt user for rematch.
    play_again = draw_winner(
        winner_text,
        ship_1,
        ship_2,
    )
    # If user does not want to play again, quit window.
    if not play_again:
        run = False
        pygame.quit()


def resize_window(event: pygame.event.Event, ship_1: Ship, ship_2: Ship):
    global WIDTH, HEIGHT, BORDER, SPACE
    new_size = event.size
    WIDTH, HEIGHT = new_size
    new_win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
    SPACE = pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
    )
    ship_1.ship = pygame.transform.rotate(
        pygame.transform.scale(ship_1.image, SPACESHIP_SIZE), ship_1.angle
    )
    ship_2.ship = pygame.transform.rotate(
        pygame.transform.scale(ship_2.image, SPACESHIP_SIZE), ship_2.angle
    )
    return new_win


# Check to see if user quit or resized window
def check_universal_events(event: pygame.event.Event):
    """Checks to see if user quit or resized window and runs different functions respectively

    Args:
        event (pygame.event.Event): most recent event

    Returns:
        bool: quits game and breaks loop is user closes window
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        return False
    elif event.type == pygame.VIDEORESIZE:
        # Handle window resize event
        WIN = resize_window(event, ship_1, ship_2)
        pygame.display.flip()


# Runs the main game loop
def main_game_loop(ship_1: Ship, ship_2: Ship) -> bool:
    """Handles the general operations for the main game play
    1. Iterates through all game events to check different conditions
        a. Fires bullets and posts collision events
    2. Checks to see if game is over
        a. Exit main game play
    3. Else
        a. gets all pressed keys
        b. moves ships

    Args:
        ship_1 (Ship): Player 1 ship
        ship_2 (Ship): Player 2 ship

    Returns:
        bool: Whether or not the game is still running
    """
    for event in pygame.event.get():
        check_universal_events(event)
        if event.type == pygame.KEYDOWN and HEALTH != 150:
            # Check bullets fire
            if event.key == pygame.K_LALT and len(ship_1.bullets) < MAX_BULLETS:
                fire_bullets(ship_1)
            if event.key == pygame.K_RALT and len(ship_2.bullets) < MAX_BULLETS:
                fire_bullets(ship_2)

        # Check bullet collisions
        if event.type == SHIP_1_HIT:
            ship_1.health = bullet_hit(ship_1.health)
        if event.type == SHIP_2_HIT:
            ship_2.health = bullet_hit(ship_2.health)

    # Check for winning condition
    if is_game_over(ship_1, ship_2):
        return False
    else:
        # Check for pressed keys
        keys_pressed = pygame.key.get_pressed()

        # Run main game loop
        if HEALTH == 150 and (
            keys_pressed[pygame.K_LALT] or keys_pressed[pygame.K_RALT]
        ):
            LASER_SOUND.play()
            if keys_pressed[pygame.K_LALT]:
                fire_bullets(ship_1)
            if keys_pressed[pygame.K_RALT]:
                fire_bullets(ship_2)
        ship_1_handle_movement(ship_1, keys_pressed)
        ship_2_handle_movement(ship_2, keys_pressed)
        handle_bullets(ship_1, ship_2)
        draw_window(
            ship_1,
            ship_2,
        )

    return True


# Opening game sequence
def intro() -> bool:
    """Handles opening sequence: title slide and enter prompt
    1. Builds animated title sequence
    2. Prompts user to press 'Return' to enter main game


    Returns:
        bool: _description_
    """
    draw_window()

    # Make texts
    # title = WINNER_FONT.render(f"Welcome to {TITLE}", 1, COLOR_CODES["white"])
    title = WINNER_FONT.render(f"Welcome to {TITLE}", 1, COLOR_CODES["yellow"])
    prompt = HEALTH_FONT.render("Press Enter to Play!", 1, COLOR_CODES["white"])

    start_time = pygame.time.get_ticks()

    # Opening title text
    while pygame.time.get_ticks() - start_time < 900:
        for event in pygame.event.get():
            check_universal_events(event)
        # Scale the texts
        elapsed_time = pygame.time.get_ticks() - start_time
        scale_factor = 4.0 - (elapsed_time / 300)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * scale_factor),
                int(title.get_height() * scale_factor),
            ),
        )

        # Post opening title text
        WIN.blit(SPACE, (0, 0))
        WIN.blit(
            scaled_title,
            (
                WIDTH / 2 - scaled_title.get_width() / 2,
                HEIGHT / 2 - title.get_height() / 2,
            ),
        )
        pygame.display.update()
        CLOCK.tick(FPS)

    # Wait
    pygame.time.delay(1500)

    # Post 'Enter' prompt text
    WIN.blit(
        prompt,
        (
            WIDTH / 2 - prompt.get_width() / 2,
            HEIGHT / 2 + title.get_height(),
        ),
    )
    pygame.display.update()
    # Give user 30 seconds to enter game
    while pygame.time.get_ticks() - start_time < 30000:
        for event in pygame.event.get():
            check_universal_events(event)
            # If user presses Return key, enter game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return False
    # If no decision after 30 sec, assume users do not want to play again
    pygame.quit()


# Prompts user to select their desired intensity level
def choose_intensity() -> dict:
    """Prompts players to select their desired intensity level for the game.
    Users have 5 choices. Based on their key input, set the conditions for the various intensity levels as defined in the constant INTENSITIES

    Returns:
        dict: the attributes of the selected intensity
    """
    draw_window()
    start_time = pygame.time.get_ticks()

    # Create the texts
    title = WINNER_FONT.render(f"Choose Your Intensity", 1, COLOR_CODES["yellow"])
    subtitle = SMALL_TEXT.render(
        f"Press Number For Corresponding Intensity Level", 1, COLOR_CODES["white"]
    )
    option_1 = HEALTH_FONT.render("Press Enter to Play!", 1, COLOR_CODES["white"])

    # Post the title text
    WIN.blit(
        title,
        (
            WIDTH / 2 - title.get_width() / 2,
            HEIGHT / 3 - title.get_height(),
        ),
    )

    pygame.display.update()
    pygame.time.delay(300)

    # Post the subtitle text
    WIN.blit(
        subtitle,
        (
            WIDTH / 2 - subtitle.get_width() / 2,
            HEIGHT / 3,
        ),
    )

    pygame.display.update()
    pygame.time.delay(300)

    # Show user different intensity options
    for i in range(4):
        option = HEALTH_FONT.render(
            f"{i}: {INTENSITY_DESC[i]}", 1, COLOR_CODES["white"]
        )
        if i % 2 == 0:
            WIN.blit(
                option,
                (
                    2.5 * WIDTH / 10,
                    HEIGHT / 3 + title.get_height() + option.get_height() * (i // 2),
                ),
            )
        else:
            WIN.blit(
                option,
                (
                    5.5 * WIDTH / 10,
                    HEIGHT / 3 + title.get_height() + option.get_height() * (i // 2),
                ),
            )
        option = HEALTH_FONT.render(f"4: {INTENSITY_DESC[4]}", 1, COLOR_CODES["white"])
        WIN.blit(
            option,
            (
                WIDTH / 2 - option.get_width() / 2,
                HEIGHT / 3 + title.get_height() + option.get_height() * 2,
            ),
        )

    pygame.display.update()

    # Give user 30 seconds to make a decision. Select intensity based on key input.
    while pygame.time.get_ticks() - start_time < 30000:
        for event in pygame.event.get():
            check_universal_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    return INTENSITIES[0]
                if event.key == pygame.K_1:
                    return INTENSITIES[1]
                if event.key == pygame.K_2:
                    return INTENSITIES[2]
                if event.key == pygame.K_3:
                    return INTENSITIES[3]
                if event.key == pygame.K_4:
                    return INTENSITIES[4]

        CLOCK.tick(FPS)


# Prompts both players to choose their desired ship characters
def choose_characters(i: int) -> str:
    """Asks the 'i' player for his/her desired color for his/her ship.
    If no color is selected within 10 seconds. Randomly assign a color

    Args:
        i (int): Player

    Returns:
        str: The color of the player's character
    """
    draw_window()
    start_time = pygame.time.get_ticks()

    # Create text
    title = WINNER_FONT.render(f"Player {i} Choose Your Ship", 1, COLOR_CODES["yellow"])
    subtitle = SMALL_TEXT.render(
        f"Press Number For Corresponding Color", 1, COLOR_CODES["white"]
    )
    option_last = HEALTH_FONT.render(
        f"8: {COLORS[8].capitalize()}", 1, COLOR_CODES["white"]
    )

    # Post title text
    WIN.blit(
        title,
        (
            WIDTH / 2 - title.get_width() / 2,
            HEIGHT / 3 - title.get_height(),
        ),
    )

    pygame.display.update()
    pygame.time.delay(300)

    # Post subtitle text
    WIN.blit(
        subtitle,
        (
            WIDTH / 2 - subtitle.get_width() / 2,
            HEIGHT / 3,
        ),
    )

    pygame.display.update()
    pygame.time.delay(300)

    # Show all color options to choose from
    for i in range(8):
        option = HEALTH_FONT.render(
            f"{i}: {COLORS[i].capitalize()}", 1, COLOR_CODES["white"]
        )
        if i % 2 == 0:
            WIN.blit(
                option,
                (
                    WIDTH / 2 - option_last.get_width() * 1.5,
                    HEIGHT / 3 + subtitle.get_height() + option.get_height() * (i // 2),
                ),
            )
        else:
            WIN.blit(
                option,
                (
                    WIDTH / 2 + option_last.get_width() * 0.5,
                    HEIGHT / 3 + subtitle.get_height() + option.get_height() * (i // 2),
                ),
            )
    WIN.blit(
        option_last,
        (
            WIDTH / 2 - option_last.get_width() / 2,
            HEIGHT / 3
            + title.get_height()
            + option.get_height() * (len(COLORS) // 2 - 1),
        ),
    )

    pygame.display.update()

    # Give user 10 seconds to select character
    while pygame.time.get_ticks() - start_time < 10000:
        for event in pygame.event.get():
            check_universal_events(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    return COLORS[0]
                if event.key == pygame.K_1:
                    return COLORS[1]
                if event.key == pygame.K_2:
                    return COLORS[2]
                if event.key == pygame.K_3:
                    return COLORS[3]
                if event.key == pygame.K_4:
                    return COLORS[4]
                if event.key == pygame.K_5:
                    return COLORS[5]
                if event.key == pygame.K_6:
                    return COLORS[6]
                if event.key == pygame.K_7:
                    return COLORS[7]
                if event.key == pygame.K_8:
                    return COLORS[8]

        CLOCK.tick(FPS)
    # If user does not pick a ship, randomly assign them one
    return COLORS[random.randint(0, 9)]


# Main game loop
def main(first_time: bool):
    global VEL, BULLET_VEL, MAX_BULLETS, HEALTH, SHIP_COLORS, SPACE
    pygame.display.set_caption(TITLE)
    SPACE = pygame.transform.scale(
        pygame.image.load(os.path.join("Assets", f"space{random.randint(1, 6)}.jpeg")),
        (WIDTH, HEIGHT),
    )
    if first_time:
        first_time = intro()
    intesity = choose_intensity()
    {"vel": 5, "bulllet_vel": 7.5, "max_bullets": 3, "health": 10}
    VEL = intesity["vel"]
    BULLET_VEL = intesity["bullet_vel"]
    MAX_BULLETS = intesity["max_bullets"]
    HEALTH = intesity["health"]

    SHIP_COLORS[0] = choose_characters(1)
    SHIP_COLORS[1] = choose_characters(2)

    ship_1 = Ship(
        300,
        HEIGHT / 2 - SPACESHIP_HEIGHT,
        SPACESHIP_WIDTH,
        SPACESHIP_HEIGHT,
        SHIP_COLORS[0],
        HEALTH,
    )
    ship_2 = Ship(
        900,
        HEIGHT / 2 - SPACESHIP_HEIGHT,
        SPACESHIP_HEIGHT,
        SPACESHIP_HEIGHT,
        SHIP_COLORS[1],
        HEALTH,
    )

    winner_text = ""

    run = True
    main_game = True
    while run:
        CLOCK.tick(FPS)
        # Run main game loop
        if main_game:
            main_game = main_game_loop(ship_1, ship_2)
        else:
            decide_winner(ship_1, ship_2)
            break

    main(False)


# Only run main if file is explicitly called
if __name__ == "__main__":
    main(True)
