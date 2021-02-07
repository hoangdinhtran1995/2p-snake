# snage
import pygame
import random

# initialize
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height + 20))
clock = pygame.time.Clock()
pygame.display.set_caption("snake box")
big_font = pygame.font.Font("freesansbold.ttf", 80)
small_font = pygame.font.Font("freesansbold.ttf", 32)
smallest_font = pygame.font.Font("freesansbold.ttf", 16)
box_width = 25
screen_width_boxes = int(screen_width / box_width)
screen_height_boxes = int(screen_height / box_width)


def drawboxes():
    for i in range(screen_width_boxes):
        for j in range(screen_height_boxes):
            pygame.draw.rect(screen, (0, 0, 0), (i * box_width + 1, j * box_width + 1, box_width - 2, box_width - 2))


class head:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.col = col

    def vel_update(self, xvel, yvel):
        self.x_vel = xvel
        self.y_vel = yvel

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        pygame.draw.rect(screen, self.col,
                         (self.x * box_width + 1, self.y * box_width + 1, box_width - 2, box_width - 2))


class tail:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col

    def draw(self):
        if game_over_state:
            self.col = (200, 100, 100)
        pygame.draw.rect(screen, self.col,
                         (self.x * box_width + 1, self.y * box_width + 1, box_width - 2, box_width - 2))


class food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.eaten = False

    def draw(self):
        pygame.draw.rect(screen, (230, 230, 230),
                         (self.x * box_width + 10, self.y * box_width + 10, 5, 5))


def draw_tail(tailList):
    for i in tailList:
        tailList[i].draw()


def make_food(head, tailList, head2, tailList2):
    box_occupied = True
    while box_occupied:
        box_occupied = False
        rand_x = random.randint(0, screen_width_boxes - 1)
        rand_y = random.randint(0, screen_height_boxes - 1)
        if head.x == rand_x and head.y == rand_y:
            box_occupied = True
        for i in range(len(tailList)):
            if tailList[i].x == rand_x and tailList[i].y == rand_y:
                box_occupied = True
        if head2.x == rand_x and head2.y == rand_y:
            box_occupied = True
        for i in range(len(tailList2)):
            if tailList2[i].x == rand_x and tailList2[i].y == rand_y:
                box_occupied = True
    Food = food(rand_x, rand_y)
    food_list.append(Food)


def update_tail(head, tailList, col):
    tailList.append(tail(head.x, head.y, col))
    del tailList[0]
    return tailList


def game_over():
    global game_over_state
    game_over_state = True
    Head.vel_update(0, 0)
    Head2.vel_update(0, 0)


def game_over_text(x, y):
    if loser[0] is Head:
        winner = "Player 2"
    else:
        winner = "Player 1"

    over_text = big_font.render("Winner is " + winner, True, (200, 0, 0))
    screen.blit(over_text, (x - 100, y))
    restart_text = small_font.render("Press R to restart", True, (200, 0, 0))
    screen.blit(restart_text, (x + 100, y + 100))
    score_text = small_font.render("Final scores:", True, (200, 200, 200))
    screen.blit(score_text, (x + 130, y + 200))
    score1_text = small_font.render("Player 1:    " + str(score), True, (200, 200, 200))
    score2_text = small_font.render("Player 2:    " + str(score2), True, (200, 200, 200))
    screen.blit(score1_text, (x + 130, y + 250))
    screen.blit(score2_text, (x + 130, y + 300))


def check_tail_collision(head, tailList, tailListopp):
    global game_over_state
    global loser
    for i in range(1, len(tailList) - 1):
        if head.x == tailList[i].x and head.y == tailList[i].y:
            game_over_state = True
    for i in range(len(tailListopp)):
        if head.x == tailListopp[i].x and head.y == tailListopp[i].y:
            game_over_state = True
    if game_over_state:
        loser.append(head)


def check_direction_ok(head, direction):
    direction_ok = True
    if len(tail_list) > 1:
        if head.y_vel == 1 and direction == (0, -1):
            direction_ok = False
        if head.y_vel == -1 and direction == (0, 1):
            direction_ok = False
        if head.x_vel == 1 and direction == (-1, 0):
            direction_ok = False
        if head.x_vel == -1 and direction == (1, 0):
            direction_ok = False
    return direction_ok


def display_score(score, x, y, player):
    level_text = smallest_font.render(player + " Score: " + str(score), True, (255, 255, 255))
    screen.blit(level_text, (x, y))


def display_time(cur_time):
    time_text = smallest_font.render("Time: " + str(round(cur_time, 1)), True, (200, 200, 200))
    screen.blit(time_text, (350, 600))


initiated = False
running = True
# game loop
while running:

    if not initiated:
        foods = 10
        tickrate = 10
        tickadd = 0.5
        time = 0
        score = 0
        score2 = 0
        Head = head(x=10, y=10, col=(50, 200, 50))
        Head2 = head(x=20, y=20, col=(140, 60, 160))
        tail_list = [tail(Head.x, Head.y, (150, 200, 150))]
        tail_list2 = [tail(Head2.x, Head2.y, (230, 180, 230))]
        loser = []

        food_list = []
        # Food = make_food(Head, [])
        while len(food_list) < foods:
            make_food(Head, tail_list, Head2, tail_list2)

        game_over_state = False
        initiated = True

    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and check_direction_ok(Head, (0, -1)):
                Head.vel_update(0, -1)
            if event.key == pygame.K_DOWN and check_direction_ok(Head, (0, 1)):
                Head.vel_update(0, 1)
            if event.key == pygame.K_LEFT and check_direction_ok(Head, (-1, 0)):
                Head.vel_update(-1, 0)
            if event.key == pygame.K_RIGHT and check_direction_ok(Head, (1, 0)):
                Head.vel_update(1, 0)
            if event.key == pygame.K_w and check_direction_ok(Head2, (0, -1)):
                Head2.vel_update(0, -1)
            if event.key == pygame.K_s and check_direction_ok(Head2, (0, 1)):
                Head2.vel_update(0, 1)
            if event.key == pygame.K_a and check_direction_ok(Head2, (-1, 0)):
                Head2.vel_update(-1, 0)
            if event.key == pygame.K_d and check_direction_ok(Head2, (1, 0)):
                Head2.vel_update(1, 0)
            if event.key == pygame.K_r:
                initiated = False
                break

    drawboxes()

    if not game_over_state:
        Head.move()
        Head2.move()
        check_tail_collision(Head, tail_list, tail_list2)
        check_tail_collision(Head2, tail_list2, tail_list)

    # # wall collision
    # if not -1 < Head.x < 32 or not -1 < Head.y < 24:
    #     game_over()

    if not -1 < Head.x < 32:
        Head.x = Head.x % 32
    if not -1 < Head.y < 24:
        Head.y = Head.y % 24
    if not -1 < Head2.x < 32:
        Head2.x = Head2.x % 32
    if not -1 < Head2.y < 24:
        Head2.y = Head2.y % 24

    for i in range(len(food_list)):
        if Head.x == food_list[i].x and Head.y == food_list[i].y:
            del food_list[i]
            make_food(Head, tail_list, Head2, tail_list2)
            tail_list.append(tail(x=Head.x, y=Head.y, col=(150, 200, 150)))
            tickrate += tickadd
            score += 1
    for i in range(len(food_list)):
        if Head2.x == food_list[i].x and Head2.y == food_list[i].y:
            del food_list[i]
            make_food(Head, tail_list, Head2, tail_list2)
            tail_list2.append(tail(x=Head2.x, y=Head2.y, col=(230, 180, 230)))
            tickrate += tickadd
            score2 += 1

    if not game_over_state:
        update_tail(Head, tail_list, (150, 200, 150))
        update_tail(Head2, tail_list2, (230, 180, 230))

    for i in range(len(tail_list)):
        tail_list[i].draw()
    for i in range(len(tail_list2)):
        tail_list2[i].draw()

    if game_over_state:
        game_over_text(150, 10)
    Head.draw()
    Head2.draw()

    for i in food_list:
        i.draw()

    display_score(score, 10, 600, "Player 1")
    display_score(score2, 650, 600, "Player 2")

    clock.tick(tickrate)
    if not game_over_state:
        time += 1 / tickrate
    display_time(time)

    pygame.display.update()
