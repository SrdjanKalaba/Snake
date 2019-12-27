import pygame as py
import menu
from random import randint
from time import localtime

py.init()

with open("settings.txt") as file:
    settings = file.read()
    settings = settings.split("\n")

windowSize = int(settings[3][12:])
GridSize = int(settings[4][10:])
FPS = int(settings[1][5:])
DELAY = int(settings[2][6:])
PLAYERNAME = settings[5][12:]
font = py.font.SysFont("Arial", 85)
_TITLE_TEXT_ = font.render("SNAKE GAME", True, (255, 255, 255))
_TITLE_TEXT_POS = _TITLE_TEXT_.get_rect()
_TITLE_TEXT_POS.center = (windowSize // 2, 85 // 2)
_PLAY_BUTTON_ = menu.Button(150, 225, 450, 100, "Play", 56, (50, 50, 50))


class Fruit:
    def __init__(self):
        self.x = randint(0, windowSize // GridSize - 1)
        self.y = randint(0, windowSize // GridSize - 1)


class Snake:
    def __init__(self):
        self.x, self.y = (10, 10)
        self.direct: list = [0, 0]  # [x, y]
        self.body = [(self.x, self.y), (self.x, self.y + 1)]
        self.len: int = len(self.body)

    def AddBlock(self):
        self.body.append((-1, -1))
        self.len = len(self.body)

    def UpdatePos(self):
        for i in range(1, len(self.body)):
            self.body[len(self.body) - i] = self.body[len(self.body) - i - 1]
        self.body[0] = (self.x, self.y)

    def BlockCheck(self, x=0, y=1, uslov=windowSize // GridSize - 1, p="y"):
        if p == "y":
            for i, block in enumerate(self.body):
                if block[x] == uslov and block[y] == self.y:
                    Game0ver()
        else:
            for i, block in enumerate(self.body):
                if block[x] == uslov and block[y] == self.x:
                    Game0ver()

    def Move(self):
        keys = py.key.get_pressed()
        if keys[py.K_UP] and self.direct[1] != 1:  # KEY UP
            self.direct = [0, -1]
        elif keys[py.K_DOWN] and self.direct[1] != -1:  # KEY DOWN
            self.direct = [0, 1]
        elif keys[py.K_RIGHT] and self.direct[0] != -1:  # KEY RIGHT
            self.direct = [1, 0]
        elif keys[py.K_LEFT] and self.direct[0] != 1:  # KEY LEFT
            self.direct = [-1, 0]
        self.y += self.direct[1]
        self.x += self.direct[0]
        if self.x < 0:
            self.BlockCheck()
            self.x = windowSize // GridSize - 1
        elif self.x > windowSize // GridSize - 1:
            self.BlockCheck(0, 1, 0)
            self.x = 0
        if self.y < 0:
            self.BlockCheck(1, 0, windowSize // GridSize, "x")
            self.y = windowSize // GridSize
        elif self.y > windowSize // GridSize - 1:
            self.BlockCheck(1, 0, 0, "x")
            self.y = 0
        self.UpdatePos()


class Game:
    def __init__(self):
        self.menu: bool = True
        self.active: bool = True
        self.winS: int = windowSize
        self.win: py.Surface = py.display.set_mode((self.winS, self.winS))
        self.GridSize: int = GridSize
        self.snake = Snake()
        self.fruit = Fruit()
        self.score: int = 0
        self.font = py.font.SysFont("Arial", 60)
        self.GameoverText = self.font.render("Game0ver", True, (255, 255, 255))
        self.FPS = FPS
        self.DELAY = DELAY
        self.PlAYER = PLAYERNAME
        py.display.set_caption(f"FAKE SNAKE Score: {self.score}")


global var
var = Game()


def Menu():
    var.win.fill((0, 0, 0))
    py.time.delay(var.DELAY)
    var.win.blit(_TITLE_TEXT_, _TITLE_TEXT_POS)
    _PLAY_BUTTON_.Draw(var.win)
    py.display.update()
    if _PLAY_BUTTON_.OnClick():
        var.menu = False


def Close():
    for e in py.event.get():
        if e.type == py.QUIT:
            var.active = not var.active


def Game0ver():
    global var
    Gameover = var.GameoverText.get_rect()
    Gameover.center = (var.winS // 2, var.winS // 2)
    var.win.blit(var.GameoverText, Gameover)
    py.display.set_caption("Game0ver")
    py.display.update()
    with open("scores.txt", "a") as f:
        f.write(
            f" Player \"{var.PlAYER}\" Scored {var.score} at {localtime()[3]}:{localtime()[4]} {localtime()[1]}. {localtime()[2]}. {localtime()[0]}. \n")
    py.time.wait(2000)
    var = Game()


def FruitInBody():
    IsIt = False
    for i in range(0, len(var.snake.body)):
        if var.snake.body[i][0] == var.fruit.x or var.snake.body[i][1] == var.fruit.y:
            IsIt = True
            break
    return IsIt


def Fruitf():
    if var.snake.x == var.fruit.x and var.snake.y == var.fruit.y:
        var.fruit = Fruit()
        while FruitInBody():
            var.fruit = Fruit()
        var.snake.AddBlock()
        var.score += 10 * FPS
        py.display.set_caption(f"FAKE SNAKE Score: {var.score}")


def DrawFruit():
    py.draw.circle(var.win, (0, 255, 0), (var.fruit.x * var.GridSize + var.GridSize // 2 + 1, var.fruit.y * var.GridSize
                                          + var.GridSize // 2 + 1), GridSize // 2)


def DrawSnake():
    for i, p in enumerate(var.snake.body):
        if i != 0:
            py.draw.rect(var.win, (255, 0, 0),
                         (p[0] * var.GridSize + 1, p[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))
        else:
            py.draw.rect(var.win, (0, 0, 255),
                         (p[0] * var.GridSize + 1, p[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))


def logic():
    Fruitf()
    var.snake.Move()
    for i in range(1, len(var.snake.body)):
        if (var.snake.body[0][0] == var.snake.body[i][0] and var.snake.body[0][1] == var.snake.body[i][1]) and len(
                var.snake.body) != 2:
            Game0ver()
            break

def DrawGrid():
    for i in range(var.winS // var.GridSize + 1):
        py.draw.line(var.win, (255, 255, 255), (i * var.GridSize, 0), (i * var.GridSize, var.winS))
        py.draw.line(var.win, (255, 255, 255), (0, i * var.GridSize), (var.winS, i * var.GridSize))


def Draw():
    var.win.fill((0, 0, 0))
    # DrawGrid()
    DrawFruit()
    DrawSnake()
    py.display.update()


def Main():
    Clock = py.time.Clock()
    while var.active:
        if not var.menu:
            py.time.delay(var.DELAY)
            Close()
            logic()
            Draw()
            Clock.tick(var.FPS)
        else:
            Close()
            Menu()
            Clock.tick(30)


if __name__ == "__main__":
    Main()
py.quit()
