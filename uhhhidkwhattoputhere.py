import pygame
import random

pygame.init()


#                                          Note for readers who look through the work:
#                    ---TEXT--- == Variable set/more minor things that have less errors, they start at space 100.
#               TEXT WITH NO --- == More major things, class/function creation, start on line 100 so its nicer visually.

#                                    Thank you for your time and patience and help :) <3




# Set display vars and center                                                                      ---DISPLAY VARS---

screen_height = pygame.display.Info().current_h - 30
screen_width = pygame.display.Info().current_w
pygame.display.set_caption("First Game")
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Declare the sprites                                                                              ---SPRITES---

green_coin = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Greencoin.png")
red_coin = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Redcoin.png")
blue_coin = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Bluecoin.png")
yellow_coin = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Yellowcoin.png")
player_sprite = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Dragon.png")
bullet = pygame.image.load(r"C:\\Users\Felix Laptop\Downloads\Bullet.png")

# Set screen bounds                                                                                ---SCREEN VARS---

bottom_of_screen = screen_height
right_side_of_screen = screen_width
left_side_of_screen = 0
top_of_screen = 0
middle_of_screen_x = screen_width / 2
middle_of_screen_y = screen_height / 2
center = screen_width / 2, screen_height / 2

# Set coin variables

player_money = 0
max_coins_on_screen = 40
coins_radius = yellow_coin.get_width()
all_coin_sprites = [yellow_coin, blue_coin, red_coin, green_coin]
regular_coin_chance = 69
blue_coin_chance = 25
red_coin_chance = 5
green_coin_chance = 1
coin_display_chances = (regular_coin_chance, blue_coin_chance, red_coin_chance, green_coin_chance)


# Set color repository                                                                             ---COLORS---

purple = (128, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
gray_ish = (200, 200, 200)
screen_color = black

# Set more player variables                                                                        ---PLAYER VARS---

player_size = 2
movement_speed = 3
player_y = screen_height / 2
player_x = screen_width / 2
player_width = player_sprite.get_width()
player_height = player_sprite.get_height()
player_sprite = pygame.transform.scale(player_sprite, (player_width * player_size, player_height * player_size))

# Set the FPS                                                                                      ---FPS---

FPS = 60
FPS_set = pygame.time.Clock()
FPS_set.tick(FPS)


# Set the circle class                                                                   CLASS TO CREATE THE PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self, surface, rect, image):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.rect = pygame.Rect(rect)
        self.image = image

    # Set the wall collision physics                                                     FUNCTION TO CONTAIN PLAYER

    def game_bounds(self):
        if self.rect[0] >= right_side_of_screen - (self.rect[2] * player_size) + 15:
            self.rect[0] -= movement_speed
        if self.rect[0] <= left_side_of_screen - 15:
            self.rect[0] += movement_speed
        if self.rect[1] <= top_of_screen:
            self.rect[1] += movement_speed
        if self.rect[1] >= bottom_of_screen - (self.rect[3] * player_size) + 10:
            self.rect[1] -= movement_speed

    # Make the the object movable                                                        FUNCTION TO HANDLE MOVEMENT

    def movable(self):
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.rect[0] -= movement_speed
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.rect[0] += movement_speed
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.rect[1] -= movement_speed
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.rect[1] += movement_speed
        return self.rect[0], self.rect[1]

# Set up the class for the coins                                                         CLASS TO CREATE COINS

class Coins_Maker(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)

# Make the groups for me to put the sprites into                                         CREATE SPRITE GROUPS

coinz = pygame.sprite.Group()
player = pygame.sprite.Group()

# Create the player                                                                      CREATE PLAYER

player_display = Player(screen, (player_x, player_y, player_width, player_height), player_sprite)

# Add the player sprite to the sprite group                                              ADD PLAYER TO SPRITE GROUP

player.add(player_display)

# Start the game loop

A = True

while A:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    key = pygame.key.get_pressed()

    screen.fill(screen_color)

    #  Set a termination key                                                                       ---SET TERM KEY---

    if key[pygame.K_DELETE]:
        pygame.quit()
        A = False

    # Create coins until there are enough on screen                                      CREATE COINS

    if len(coinz) <= max_coins_on_screen:
        coin_to_display = random.choices(all_coin_sprites, weights=coin_display_chances, k=1)
        coin = Coins_Maker(coin_to_display[0], random.randint(coins_radius, screen_width - coins_radius), random.randint(coins_radius, screen_height - coins_radius), coins_radius, coins_radius)
        coinz.add(coin)

    # Make the player movable                                                            CALL PLAYER FUNCTIONS THAT NEED CONSTANT INPUT

    player_x, player_y = player_display.movable()
    player_display.game_bounds()


    # Check for collision between Player and Coins                                                 ---PLAYER-COIN COLLISION---

    collision_instances = pygame.sprite.spritecollideany(player_display, coinz)
    if collision_instances is not None:
        if collision_instances.image == yellow_coin:
            player_money += 1
        if collision_instances.image == blue_coin:
            player_money += 5
        if collision_instances.image == red_coin:
            player_money += 25
        if collision_instances.image == green_coin:
            player_money += 100
        coinz.remove(collision_instances)

    # Draw all of the coins                                                              DRAW ALL OF THE COINS

    coinz.draw(screen)

    # Draw player                                                                        DRAW PLAYER

    player.draw(screen)

    # Set text vars                                                                                ---TEXT SETUP---

    font = pygame.font.SysFont('arial', 32)
    text_to_display = f"Score: {player_money}"
    text = font.render(text_to_display, True, white)
    screen.blit(text, (0, 0))

    # Update the screen
    pygame.display.update()
