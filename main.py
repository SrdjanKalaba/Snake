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
settings_fonts = py.font.SysFont("Arial", 45)
_TITLE_TEXT_ = font.render("SNAKE GAME", True, (255, 255, 255))
_TITLE_TEXT_POS = _TITLE_TEXT_.get_rect()
_TITLE_TEXT_POS.center = (windowSize // 2, 85 // 2)
_PLAY_BUTTON_ = menu.Button(windowSize // 2 - 225, 150, 450, 100, "Play", 56, (50, 50, 50))
_SETTING_BUTTON_ = menu.Button(windowSize // 2 - 225, 300, 450, 100, "Settings", 56, (50, 50, 50))
_FPS_TEXT_ = settings_fonts.render(f"FPS: {FPS}", True, (255, 255, 255))
_PLAYER_NAME_TEXT_ = settings_fonts.render("NAME: ", True, (255, 255, 255))
_WinS_TEXT_ = settings_fonts.render(f"WinS: {windowSize}", True, (255, 255, 255))
_FPS_SLIDER_ = menu.Slider(160, 14, windowSize - 170, 48, 48, 48, FPS, 5, 60)
_WINS_SLIDER_ = menu.Slider(220, 76, windowSize - 230, 48, 48, 48, windowSize, 750, 1500)
_BACK_BUTTON_ = menu.Button(0, windowSize - 48, 250, 95, "Back", 56, (50, 50, 50))
_PLAYER_NAME_ = menu.Text_BOX(220, 152, 100, 55, PLAYERNAME, 45)


class Fruit:
    def __init__(self):
        self.x = randint(0, windowSize // GridSize - 1)
        self.y = randint(0, windowSize // GridSize - 1)
        self.r = GridSize // 2
        self.drawenRadius = self.r

    def draw(self, SUR):
        py.draw.circle(SUR, (0, 255, 0),
                       (self.x * GridSize + GridSize // 2 + 1, self.y * GridSize + GridSize // 2 + 1),
                       self.drawenRadius)
        if self.drawenRadius == self.r and self.drawenRadius >= 1:
            self.drawenRadius -= 1
        else:
            self.drawenRadius += 1


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
        self.settings: bool = False
        self.menu: bool = True
        self.active: bool = True
        self.winS: int = windowSize
        self.win: py.Surface = py.display.set_mode((self.winS, self.winS + 50))
        self.GridSize: int = GridSize
        self.snake = Snake()
        self.fruit = Fruit()
        self.score: int = 0
        self.font = py.font.SysFont("Arial", 60)
        self.GameoverText = self.font.render("Game0ver", True, (255, 255, 255))
        self.FPS = FPS
        self.DELAY = DELAY
        self.PlAYER = PLAYERNAME
        py.display.set_caption("SNAKE GAME")


global var  # Create globals variables
var = Game()
_SCORE_TEXT_ = settings_fonts.render(f"SCORE: {var.score}", True, (255, 255, 255))


def Menu():
    var.win.fill((0, 0, 0))
    var.win.blit(_TITLE_TEXT_, _TITLE_TEXT_POS)
    _PLAY_BUTTON_.Draw(var.win)
    _SETTING_BUTTON_.Draw(var.win)
    py.display.update()
    if _PLAY_BUTTON_.OnClick():
        var.menu = False
    elif _SETTING_BUTTON_.OnClick():
        var.settings = True
        var.menu = False


def settings():
    Clock = py.time.Clock()
    global _FPS_TEXT_, _WinS_TEXT_, _BACK_BUTTON_, _SETTING_BUTTON_, _PLAY_BUTTON_, _TITLE_TEXT_POS
    global _WINS_SLIDER_, _FPS_SLIDER_
    var.win.fill((0, 0, 0))
    var.win.blit(_FPS_TEXT_, (10, 10))
    var.win.blit(_WinS_TEXT_, (10, 76))

    _FPS_SLIDER_.Move()
    _WINS_SLIDER_.Move()
    _PLAYER_NAME_.Input()
    var.win.blit(_PLAYER_NAME_TEXT_, (10, 152))
    var.FPS = round(_FPS_SLIDER_.val)
    var.winS = round(_WINS_SLIDER_.val)

    _PLAYER_NAME_.Draw(var.win)
    _BACK_BUTTON_.Draw(var.win)
    _WINS_SLIDER_.Draw(var.win)
    _FPS_SLIDER_.Draw(var.win)
    if _BACK_BUTTON_.OnClick():
        py.display.set_mode((var.winS, var.winS))
        # reload positons
        _TITLE_TEXT_POS = _TITLE_TEXT_.get_rect()
        _TITLE_TEXT_POS.center = (var.winS // 2, 85 // 2)
        _PLAY_BUTTON_ = menu.Button(var.winS // 2 - 225, 150, 450, 100, "Play", 56, (50, 50, 50))
        _SETTING_BUTTON_ = menu.Button(var.winS // 2 - 225, 300, 450, 100, "Settings", 56, (50, 50, 50))
        _BACK_BUTTON_ = menu.Button(0, var.winS - 95, 250, 95, "Back", 56, (50, 50, 50))
        _FPS_SLIDER_ = menu.Slider(160, 14, var.winS - 170, 48, 48, 48, FPS, 5, 60)
        _WINS_SLIDER_ = menu.Slider(220, 76, var.winS - 230, 48, 48, 48, var.winS, 750, 1500)
        with open("settings.txt", "w") as f:
            f.write(f"""
FPS: {var.FPS}
DELAY: {var.DELAY}
WINDOWSIZE: {var.winS}
GRIDSIZE: {var.GridSize}
PLAYERNAME: {var.PlAYER}
#DEAFULT SETTINGS ARE
#FPS: 10
#DELAY: 50
#WINDOWSIZE: 750
#GRIDSIZE: 25"""
                    )
        var.settings = False
        var.menu = True
    _FPS_TEXT_ = settings_fonts.render(f"FPS: {var.FPS}", True, (255, 255, 255))
    _WinS_TEXT_ = settings_fonts.render(f"WinS: {var.winS}", True, (255, 255, 255))
    py.display.update()
    Clock.tick(10)


def Close():
    for e in py.event.get():
        if e.type == py.QUIT:
            var.active = False


def Game0ver():
    global var
    Gameover = var.GameoverText.get_rect()
    Gameover.center = (var.winS // 2, var.winS // 2)
    var.win.blit(var.GameoverText, Gameover)
    py.display.set_caption("Game0ver")
    py.display.update()
    with open("scores.txt", "a") as f:
        f.write(
            f' Player {var.PlAYER!r} Scored {var.score} at {localtime()[3]}:{localtime()[4]} {localtime()[1]}. {localtime()[2]}. {localtime()[0]}. \n')
    py.time.wait(2000)
    var = Game()


def FruitInBody():  # check if fruit spawn in body of snake
    for i in range(0, len(var.snake.body)):
        if var.snake.body[i][0] == var.fruit.x or var.snake.body[i][1] == var.fruit.y:
            return True
        return False


def FruitEat():
    global _SCORE_TEXT_
    if var.snake.x == var.fruit.x and var.snake.y == var.fruit.y:
        var.fruit = Fruit()
        while FruitInBody():
            var.fruit = Fruit()
        var.snake.AddBlock()
        var.score += 10 * FPS
        _SCORE_TEXT_ = settings_fonts.render(f"SCORE: {var.score}", True, (255, 255, 255))


def logic():
    FruitEat()
    var.snake.Move()
    for i in range(1, len(var.snake.body)):
        if (var.snake.body[0][0] == var.snake.body[i][0] and var.snake.body[0][1] == var.snake.body[i][1]) and len(
                var.snake.body) != 2:
            Game0ver()
            break


def DrawSnake():
    for i, p in enumerate(var.snake.body):
        if i != 0:
            py.draw.rect(var.win, (255, 0, 0),
                         (p[0] * var.GridSize + 1, p[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))
        else:
            py.draw.rect(var.win, (0, 0, 255),
                         (p[0] * var.GridSize + 1, p[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))


def DrawGrid():
    for i in range(var.winS // var.GridSize + 1):
        py.draw.line(var.win, (255, 255, 255), (i * var.GridSize, 0), (i * var.GridSize, var.winS))
        py.draw.line(var.win, (255, 255, 255), (0, i * var.GridSize), (var.winS, i * var.GridSize))


def ReDrawScreen():
    var.win.fill((0, 0, 0))
    # Drawing.DrawGrid()
    var.fruit.draw(var.win)
    DrawSnake()
    py.draw.rect(var.win, (30, 30, 30), (0, var.winS, var.winS, 55))
    var.win.blit(_SCORE_TEXT_, (0, var.winS))
    py.display.update()


def Main():
    Clock = py.time.Clock()
    if windowSize < 450:
        var.active = False
    while var.active:
        if var.menu:
            Close()
            Menu()
            Clock.tick(60)
        elif var.settings:
            Close()
            settings()
        else:
            py.time.delay(var.DELAY)
            Close()
            logic()
            ReDrawScreen()
            Clock.tick(var.FPS)


if __name__ == "__main__":
    Main()
py.quit()
