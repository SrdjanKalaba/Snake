import pygame as py
import menu
from random import randint
from datetime import datetime

py.init()


class Game:
    def __init__(self):
        try:
            with open("settings.txt", "r") as file:
                settings = file.read()
                settings = settings.split("\n")

            self.winS = int(settings[2][12:])
            self.GridSize = int(settings[3][10:])
            self.FPS = int(settings[0][5:])
            self.DELAY = int(settings[1][6:])
            self.Player_Name = settings[4][12:]
        except:
            self.winS = 750
            self.GridSize = 25
            self.FPS = 10
            self.DELAY = 50
            self.Player_Name = "ERR"

        self.font = py.font.SysFont("Arial", 85)
        self.settings_fonts = py.font.SysFont("Arial", 45)
        self.TITLE_TEXT = self.font.render("SNAKE GAME", True, (255, 255, 255))
        self.TITLE_TEXT_POS = self.TITLE_TEXT.get_rect()
        self.TITLE_TEXT_POS.center = (self.winS // 2, 85 // 2)
        self.PLAY_BUTTON = menu.Button(self.winS // 2 - 225, 150, 450, 100, "Play", 56, (50, 50, 50))
        self.SETTING_BUTTON = menu.Button(self.winS // 2 - 225, 300, 450, 100, "Settings", 56, (50, 50, 50))
        self.FPS_TEXT = self.settings_fonts.render(f"Fps: {self.FPS}", True, (255, 255, 255))
        self.Delay_Text = self.settings_fonts.render(f"Delay: {self.DELAY}", True, (255, 255, 255))
        self.PLAYER_NAME_TEXT = self.settings_fonts.render("Name: ", True, (255, 255, 255))
        self.WinS_TEXT = self.settings_fonts.render(f"WinS: {self.winS}", True, (255, 255, 255))
        self.FPS_SLIDER = menu.Slider(160, 14, self.winS - 170, 48, 48, 48, self.FPS, 5, 60)
        self.WINS_SLIDER = menu.Slider(220, 76, self.winS - 230, 48, 48, 48, self.winS, 750, 1500)
        self.Delay_Slider = menu.Slider(220, 152, self.winS - 230, 48, 48, 48, self.DELAY, 0, 100)
        self.Save_BUTTON = menu.Button(0, self.winS - 48, 250, 95, "Save", 56, (50, 50, 50))
        self.Cancel_BUTTON = menu.Button(self.winS - 250, self.winS - 48, 250, 95, "Cancel", 56, (50, 50, 50))
        self.PLAYER_NAME_BOX = menu.Text_BOX(220, 228, 100, 55, self.Player_Name, 45)
        self.settings: bool = False
        self.menu: bool = True
        self.active: bool = True
        self.win: py.Surface = py.display.set_mode((self.winS, self.winS + 50))
        self.score: int = 0
        self.SCORE_TEXT = self.settings_fonts.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.font = py.font.SysFont("Arial", 60)
        self.GameoverText = self.font.render("Game0ver", True, (255, 255, 255))
        py.display.set_caption("SNAKE GAME")


var = Game()  # MAIN GAME VARIABLES


class Fruit:
    def __init__(self):
        self.x = randint(0, var.winS // var.GridSize - 1)
        self.y = randint(0, var.winS // var.GridSize - 1)
        self.r = var.GridSize // 2
        self.drawenRadius = self.r

    def draw(self, SUR):
        py.draw.circle(SUR, (0, 255, 0),
                       (self.x * var.GridSize + var.GridSize // 2 + 1, self.y * var.GridSize + var.GridSize // 2 + 1),
                       self.drawenRadius)
        if self.drawenRadius == self.r and self.drawenRadius >= 1:
            self.drawenRadius -= 1
        else:
            self.drawenRadius += 1


class Snake:
    def __init__(self):
        self.x, self.y = (10, 10)
        self.direct: list = [0, 0]                       # [x, y]
        self.body = [(self.x, self.y), (self.x, self.y + 1)]
        self.len: int = len(self.body)

    def AddBlock(self):
        self.body.append((-1, -1))
        self.len = len(self.body)

    def UpdatePos(self):
        for i in range(1, len(self.body)):
            self.body[len(self.body) - i] = self.body[len(self.body) - i - 1]
        self.body[0] = (self.x, self.y)

    def BlockCheck(self, x=0, y=1, uslov=var.winS // var.GridSize - 1, p="y"):
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
        if keys[py.K_UP] and self.direct[1] != 1:             # KEY UP
            self.direct = [0, -1]
        elif keys[py.K_DOWN] and self.direct[1] != -1:        # KEY DOWN
            self.direct = [0, 1]
        elif keys[py.K_RIGHT] and self.direct[0] != -1:       # KEY RIGHT
            self.direct = [1, 0]
        elif keys[py.K_LEFT] and self.direct[0] != 1:         # KEY LEFT
            self.direct = [-1, 0]
        self.y += self.direct[1]
        self.x += self.direct[0]
        if self.x < 0:
            self.BlockCheck()
            self.x = var.winS // var.GridSize - 1
        elif self.x > var.winS // var.GridSize - 1:
            self.BlockCheck(0, 1, 0)
            self.x = 0
        elif self.y < 0:
            self.BlockCheck(1, 0, var.winS // var.GridSize, "x")
            self.y = var.winS // var.GridSize
        elif self.y > var.winS // var.GridSize - 1:
            self.BlockCheck(1, 0, 0, "x")
            self.y = 0
        self.UpdatePos()


snake = Snake()
fruit = Fruit()


def GoBack():
    global var, snake, fruit
    keys = py.key.get_pressed()
    if keys[py.K_ESCAPE]:
        if not var.menu and not var.settings:
            var = Game()
            snake = Snake()
            fruit = Fruit()
            var.SCORE_TEXT = var.settings_fonts.render(f"SCORE: {var.score}", True, (255, 255, 255))
        var.settings = False
        var.menu = True


def Menu():
    var.win.fill((0, 0, 0))
    var.win.blit(var.TITLE_TEXT, var.TITLE_TEXT_POS)
    var.PLAY_BUTTON.Draw(var.win)
    var.SETTING_BUTTON.Draw(var.win)
    py.display.update()
    if var.PLAY_BUTTON.OnClick():
        var.menu = False
    elif var.SETTING_BUTTON.OnClick():
        var.settings = True
        var.menu = False


def settings():
    global var, snake, fruit
    Clock = py.time.Clock()
    var.win.fill((0, 0, 0))
    var.win.blit(var.FPS_TEXT, (10, 10))
    var.win.blit(var.WinS_TEXT, (10, 76))
    var.win.blit(var.Delay_Text, (10, 158))

    var.FPS_SLIDER.Move()
    var.WINS_SLIDER.Move()
    var.PLAYER_NAME_BOX.Input()
    var.Delay_Slider.Move()
    var.win.blit(var.PLAYER_NAME_TEXT, (10, 228))
    var.FPS = round(var.FPS_SLIDER.val)
    var.winS = round(var.WINS_SLIDER.val)
    var.DELAY = round(var.Delay_Slider.val)
    var.Player_Name = var.PLAYER_NAME_BOX.text

    var.PLAYER_NAME_BOX.Draw(var.win)
    var.Save_BUTTON.Draw(var.win)
    var.Cancel_BUTTON.Draw(var.win)
    var.WINS_SLIDER.Draw(var.win)
    var.FPS_SLIDER.Draw(var.win)
    var.Delay_Slider.Draw(var.win)
    if var.Save_BUTTON.OnClick():
        py.display.set_mode((var.winS, var.winS + 50))
        with open("settings.txt", "w") as f:
            f.write(f"""Fps: {var.FPS}
Delay: {var.DELAY}
WindowSize: {var.winS}
GridSize: {var.GridSize}
PlayerName: {var.Player_Name}
#DEAFULT SETTINGS ARE
#Fps: 10
#Delay: 50
#WindowSize: 750
#GridSize: 25""")
        var = Game()
        snake = Snake()
        fruit = Fruit()
    if var.Cancel_BUTTON.OnClick():
        try:
            with open("settings.txt", "r") as file:
                settings = file.read()
                settings = settings.split("\n")

            var.winS = int(settings[3][12:])
            var.GridSize = int(settings[4][10:])
            var.FPS = int(settings[1][5:])
            var.DELAY = int(settings[2][6:])
            var.Player_Name = settings[5][12:]
        except:
            var.winS = 750
            var.GridSize = 25
            var.FPS = 10
            var.DELAY = 50
            var.Player_Name = "ERR"
        var.menu = True
        var.settings = False
    var.FPS_TEXT = var.settings_fonts.render(f"FPS: {var.FPS}", True, (255, 255, 255))
    var.WinS_TEXT = var.settings_fonts.render(f"WinS: {var.winS}", True, (255, 255, 255))
    var.Delay_Text = var.settings_fonts.render(f"Delay: {var.DELAY}", True, (255, 255, 255))
    py.display.update()
    Clock.tick(10)


def Close():
    for e in py.event.get():
        if e.type == py.QUIT:
            var.active = False
    GoBack()


def Game0ver():
    global var, snake, fruit
    Gameover = var.GameoverText.get_rect()
    Gameover.center = (var.winS // 2, var.winS // 2)
    var.win.blit(var.GameoverText, Gameover)
    py.display.set_caption("Game0ver")
    py.display.update()
    with open("scores.txt", "w") as f:
        f.write(f' Player {var.Player_Name!r} Scored {var.score} at {datetime.now().strftime("%H:%M %d/%m/%Y")}. \n')
    py.time.wait(2000)
    var = Game()
    snake = Snake()
    fruit = Fruit()
    _SCORE_TEXT_ = var.settings_fonts.render(f"SCORE: {var.score}", True, (255, 255, 255))


def FruitInBody():  # check if fruit spawn in body of snake
    for part in snake.body:
        if fruit.x == part[0] and fruit.y == part[1]:
            return True
        return False


def FruitEat():
    global fruit
    if snake.x == fruit.x and snake.y == fruit.y:
        snake.AddBlock()
        while True:
            fruit = Fruit()
            if not FruitInBody():
                break
        var.score += 10 * var.FPS
        var.SCORE_TEXT = var.settings_fonts.render(f"SCORE: {var.score}", True, (255, 255, 255))


def logic():
    FruitEat()
    snake.Move()
    for i, part in enumerate(snake.body):
        if snake.x == part[0] and snake.y == part[1] and snake.len != 2 and i != 0:
            Game0ver()
            break


def DrawSnake():
    for i, p in enumerate(snake.body):
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
    # DrawGrid()
    fruit.draw(var.win)
    DrawSnake()
    py.draw.rect(var.win, (30, 30, 30), (0, var.winS, var.winS, 55))
    var.win.blit(var.SCORE_TEXT, (0, var.winS))
    py.display.update()


def Main():
    Clock = py.time.Clock()
    if var.winS < 450:
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
