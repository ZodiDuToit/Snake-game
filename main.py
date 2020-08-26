import pygame, random

WIDTH = 500
CUBE_SIZE = 20

FOOD_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)


class Cube:
    def __init__(self, position, color=SNAKE_COLOR, cubeSize=CUBE_SIZE):
        self.x, self.y = position
        self.position = [self.x, self.y]

        self.cubeSize = cubeSize
        self.width, self.height = self.cubeSize, self.cubeSize

        self.color = color

    def show(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width - 1, self.height - 1))


class Snake:
    def __init__(self, headPosition, dir):
        self.head = Cube(headPosition)
        self.body = [self.head]

        self.previousPosition = None

        self.dir = dir

    def move(self, dir):
        dirX, dirY = dir

        self.body.insert(
            0,
            Cube((self.body[0].x + CUBE_SIZE * dirX,
                  self.body[0].y + CUBE_SIZE * dirY)))
        self.body.pop()

        self.head = self.body[0]

    def show(self, screen):
        for cube in self.body:
            cube.show(screen)

    def addCube(self):
        self.body.insert(-1, Cube(snake.previousPosition))

    def inBody(self, currentPosition, dir):
        xDir, yDir = dir
        x, y = currentPosition

        if len(self.body) >= 2 and (x + (CUBE_SIZE * xDir), y +
                                    (CUBE_SIZE * yDir)) == (snake.body[1].x,
                                                            snake.body[1].y):
            return True
        return False


def getEvents():
    global currentFood
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and snake.inBody(snake.body[0].position,
                                            (-1, 0)) is False:
        snake.dir = (-1, 0)

    elif keys[pygame.K_RIGHT] and snake.inBody(snake.body[0].position,
                                               (1, 0)) is False:
        snake.dir = (1, 0)

    elif keys[pygame.K_UP] and snake.inBody(snake.body[0].position,
                                            (0, -1)) is False:
        snake.dir = (0, -1)

    elif keys[pygame.K_DOWN] and snake.inBody(snake.body[0].position,
                                              (0, 1)) is False:
        snake.dir = (0, 1)

    if snake.head.position == currentFood.position:
        currentFood = generateFood()
        snake.addCube()

    if snake.head.x < 0 or snake.head.x >= WIDTH or snake.head.y < 0 or snake.head.y > WIDTH:
        reset()

    xDir, yDir = snake.dir

    for cube in snake.body:
        if len(snake.body) >= 2 and (snake.head.x + (CUBE_SIZE * xDir),
                                     snake.head.y +
                                     (CUBE_SIZE * yDir)) == (cube.x, cube.y):

            reset()
            break


def redrawScreen(screen):
    screen.fill((0, 0, 0))

    snake.show(screen)
    currentFood.show(screen)
    pygame.display.update()


def reset():
    global snake, currentFood

    snake = Snake((240, 240), (1, 0))
    currentFood = generateFood()


def generateFood():
    while True:
        x, y = random.randint(
            0, (WIDTH - CUBE_SIZE) // CUBE_SIZE) * CUBE_SIZE, random.randint(
                0, (WIDTH - CUBE_SIZE) // CUBE_SIZE) * CUBE_SIZE

        if (x, y) not in snake.body:
            return Cube((x, y), FOOD_COLOR)

        else:
            continue


screen = pygame.display.set_mode((WIDTH, WIDTH))
snake = Snake((240, 240), (1, 0))


def main():
    global currentFood

    clock = pygame.time.Clock()
    currentFood = generateFood()

    while True:
        clock.tick(60)
        pygame.time.delay(100)

        getEvents()

        snake.move(snake.dir)
        snake.previousPosition = snake.body[-1].position

        redrawScreen(screen)


main()
