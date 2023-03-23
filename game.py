import pygame
from sys import exit
import random


# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x = round(random.randrange(25, dis_width - snake_block_size) / 25.0) * 25.0
        self.y = round(random.randrange(25, dis_height - snake_block_size) / 25.0) * 25.0

        self.image = pygame.image.load('graphics/Food.png').convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def destroy(self):
        if self.rect.colliderect(snake_rect):
            self.kill()

    def update(self):
        self.destroy()


# Menu Screen
def main_menu():
    # game name
    game_name_surf = text_font.render('Snake', False, (255, 255, 255))
    game_name_surf = pygame.transform.rotozoom(game_name_surf, 0, 3)
    game_name_rect = game_name_surf.get_rect(center=(dis_width/2, 150))

    # press play
    press_play_surf = text_font.render('Press space to play', False, (255, 255, 255))
    press_play_surf = pygame.transform.rotozoom(press_play_surf, 0, 1.5)
    press_play_rect = press_play_surf.get_rect(center = (dis_width/2, 650))

    # display
    screen.blit(game_name_surf, game_name_rect)
    screen.blit(press_play_surf, press_play_rect)


# Show description
def show_description():
    # description
    description1_surf = text_font.render('Use arrow keys to move.', False, (255, 255, 255))
    description1_rect = description1_surf.get_rect(center=(dis_width/2, 350))
    description2_surf = text_font.render('Eat as many apples without hitting', False, (255, 255, 255))
    description2_rect = description2_surf.get_rect(center=(dis_width/2, 400))
    description3_surf = text_font.render('the walls or your own snake.', False, (255, 255, 255))
    description3_rect = description3_surf.get_rect(center=(dis_width/2, 450))

    screen.blit(description1_surf, description1_rect)
    screen.blit(description2_surf, description2_rect)
    screen.blit(description3_surf, description3_rect)


# Show Score at the end
def show_score():
    score_surf = text_font.render(f'Score: {score}', False, (255, 255, 255))
    score_surf = pygame.transform.rotozoom(score_surf, 0, 2)
    score_rect = score_surf.get_rect(center = (dis_width/2, 400))

    screen.blit(score_surf, score_rect)


# Display list of snake blocks (tail)
def extension(snakes):
    for obj in snakes:
        surf = pygame.image.load('graphics/SnakeNode.png').convert_alpha()
        rect = surf.get_rect(center=(obj[0] + 13, obj[1] + 13))

        screen.blit(surf, rect)


# Initialize pygame
pygame.init()
dis_width = 800
dis_height = 800
screen = pygame.display.set_mode((dis_width, dis_height))
border_color = '#B4EB46'
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False

# Score
score = -1

# Snake
snake_block_size = 25
snake_list = []
length = 1

x_change = 0
y_change = 0

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # start game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                score = 0
                game_active = True

        # snake movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -snake_block_size
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = snake_block_size
                y_change = 0
            elif event.key == pygame.K_UP:
                y_change = -snake_block_size
                x_change = 0
            elif event.key == pygame.K_DOWN:
                y_change = snake_block_size
                x_change = 0

    # screen will always be black
    screen.fill(border_color)
    pygame.draw.rect(screen, 'Black', [13, 13, 776, 776])

    if game_active:
        # update food
        if not food.sprites():
            food.add(Food())
            length += 1
            score += 1

        food.update()
        food.draw(screen)

        # out of bounds for snake
        if snake_rect.x < 13 or snake_rect.y < 13 or snake_rect.x > dis_width - 13 or snake_rect.y > dis_height - 13:
            game_active = False

        # snake movement
        snake_rect.x += x_change
        snake_rect.y += y_change
        screen.blit(snake_surf, snake_rect)

        snake_head = []
        snake_head.append(snake_rect.x)
        snake_head.append(snake_rect.y)
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_active = False

        extension(snake_list)

    else:
        main_menu()

        if score == -1:
            show_description()
        else:
            show_score()

        # initialize snake
        snake_surf = pygame.image.load('graphics/SnakeNode.png').convert_alpha()
        snake_rect = snake_surf.get_rect(center=(dis_width/2, dis_height/2))
        x_change = 0
        y_change = 0

        # initialize food
        food = pygame.sprite.GroupSingle()
        food.add(Food())

        # empty list and reset length to 1
        snake_list.clear()
        length = 1

    pygame.display.update()
    clock.tick(10)
