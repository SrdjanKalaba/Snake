from datetime import datetime
from random import randint
from time import perf_counter
from pygame.locals import *

import pygame as py

import menu

py.init()
scores = []
with open("scores.txt", "r") as file:
    scoressp = []
    for i, p in enumerate(file.read().split("\n")):
        scoressp.append(p.split(" "))
    try:
        for i, p in enumerate(scoressp):
            scores.append((p[2], p[4], p[6] + " " + p[7]))
    except:
        pass
    finally:
        print(f"Scores successfully loaded {scores}.")
PLACE = 0


class Game:
    def __init__(self):
        self.winS = 750
        self.GridSize = 25
        self.Fps = 10
        self.Delay = 50
        self.Player_Name = "Player2"
        try:
            with open("settings.txt", "r") as file:
                settings = file.read()
                settings = settings.split("\n")

            self.winS = int(settings[2][12:])
            self.GridSize = int(settings[3][10:])
            self.Fps = int(settings[0][5:])
            self.Delay = int(settings[1][6:])
            self.Player_Name = settings[4][12:]
        except:
            print(f"Settings successfully loaded {settings[:4]}.")
        finally:
            print(f"Settings successfully loaded {settings[:4]}.")
        self.font = py.font.SysFont("Arial", 85)
        self.settings_fonts = py.font.SysFont("Arial", 45)
        self.Game_title_text = self.font.render("SNAKE GAME", True, (255, 255, 255))
        self.Game_title_pos = ((self.winS - self.font.size("SNAKE GAME")[0]) // 2, 0)
        self.Play_Button = menu.Button(self.winS // 2 - 225, 150, 450, 100, "Play", 56, (50, 50, 50))
        self.Settings_Button = menu.Button(self.winS // 2 - 225, 300, 450, 100, "Settings", 56, (50, 50, 50))
        self.ScoreBorad_Button = menu.Button(self.winS // 2 - 225, 450, 450, 100, "Scoreboard", 56, (50, 50, 50))
        self.Fps_Text = self.settings_fonts.render(f"Fps: {self.Fps}", True, (255, 255, 255))
        self.Delay_Text = self.settings_fonts.render(f"Delay: {self.Delay}", True, (255, 255, 255))
        self.Player_Name_Text = self.settings_fonts.render("Name:", True, (255, 255, 255))
        self.WinS_TEXT = self.settings_fonts.render(f"WinS: {self.winS}", True, (255, 255, 255))
        self.Fps_slider = menu.Slider(160, 14, self.winS - 170, 48, 48, 48, self.Fps, 5, 60)
        self.WinS_Slider = menu.Slider(220, 90, self.winS - 230, 48, 48, 48, self.winS, 750, 1500)
        self.Delay_Slider = menu.Slider(220, 166, self.winS - 230, 48, 48, 48, self.Delay, 0, 100)
        self.Save_Button = menu.Button(0, self.winS - 48, 250, 95, "Save", 56, (50, 50, 50))
        self.Cancel_Button = menu.Button(self.winS - 250, self.winS - 48, 250, 95, "Cancel", 56, (50, 50, 50))
        self.Back_Button = menu.Button(0, self.winS - 48, 250, 95, "Back", 56, (50, 50, 50))
        self.Player_Name_TextBox = menu.Text_BOX(220, 242, 100, 55, self.Player_Name, 45)
        self.Font_Scoreboard = py.font.SysFont("Arial", 20, True)
        self.score: int = 0
        self.Score_Text = self.settings_fonts.render(f"Score: {self.score}", True, (255, 255, 255))
        self.font = py.font.SysFont("Arial", 60)
        self.Gameover_Text = self.font.render("Game0ver", True, (255, 255, 255))
        self.active = True
        py.display.set_caption("Snake Game")


var = Game()
window: py.Surface = py.display.set_mode((var.winS, var.winS + 50))
Clock = py.time.Clock()
call = perf_counter()


class Fruit:
    def __init__(self):
        self.x = randint(0, var.winS // var.GridSize - 1)
        self.y = randint(0, var.winS // var.GridSize - 1)
        self.r = var.GridSize // 2
        self.Radius = self.r
        self.isBig = True

    def Draw(self, SUR):
        global call
        py.draw.circle(SUR, (0, 255, 0),
                       (self.x * var.GridSize + var.GridSize // 2 + 1, self.y * var.GridSize + var.GridSize // 2 + 1),
                       self.Radius - (1 * 0 if self.isBig else 1))
        # Check time since last call
        if perf_counter() - call >= 0.125:
            self.isBig = not self.isBig
            call = perf_counter()

    def New_Pos(self):
        self.x, self.y = (randint(0, var.winS // var.GridSize - 1), randint(0, var.winS // var.GridSize - 1))


class Snake:
    def __init__(self):
        self.x, self.y = (10, 10)
        self.direct: list = [0, 0]  # [x, y]
        self.body = [(self.x, self.y)]
        self.len: int = len(self.body)

    def AddBlock(self):
        self.body.append((self.body[self.len - 1][0] + self.direct[0], self.body[self.len - 1][1] + self.direct[1]))
        self.len = len(self.body)

    def UpdatePos(self):
        for i in range(1, self.len):
            self.body[self.len - i] = self.body[self.len - i - 1]
        self.body[0] = (self.x, self.y)

    def BlockCheck(self, x=0, y=1, arr=var.winS // var.GridSize - 1, p="y"):
        if p == "y":
            for i, block in enumerate(self.body):
                if block[x] == arr and block[y] == self.y:
                    Game0ver()
        else:
            for i, block in enumerate(self.body):
                if block[x] == arr and block[y] == self.x:
                    Game0ver()

    def Move(self):
        keys = py.key.get_pressed()
        if keys[K_UP] and self.direct[1] != 1:  # KEY UP
            self.direct = [0, -1]
        elif keys[K_DOWN] and self.direct[1] != -1:  # KEY DOWN
            self.direct = [0, 1]
        elif keys[K_RIGHT] and self.direct[0] != -1:  # KEY RIGHT
            self.direct = [1, 0]
        elif keys[K_LEFT] and self.direct[0] != 1:  # KEY LEFT
            self.direct = [-1, 0]
        self.x += self.direct[0]
        self.y += self.direct[1]
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
        if self.direct != [0, 0]:
            self.UpdatePos()


snake = Snake()
fruit = Fruit()


def GoBack():
    global var, snake, fruit, PLACE
    keys = py.key.get_pressed()
    if keys[K_ESCAPE]:
        if PLACE != 0 and PLACE != 1:
            var = Game()
            snake = Snake()
            fruit = Fruit()
            var.Score_Text = var.settings_fonts.render(f"Score: {var.score}", True, (255, 255, 255))
        PLACE = 0


def Menu():
    global PLACE
    window.fill((0, 0, 0))
    window.blit(var.Game_title_text, var.Game_title_pos)
    var.Play_Button.Draw(window)
    var.Settings_Button.Draw(window)
    var.ScoreBorad_Button.Draw(window)
    py.display.update()
    if var.Play_Button.Click():
        PLACE = 3
    elif var.Settings_Button.Click():
        PLACE = 1
    elif var.ScoreBorad_Button.Click():
        PLACE = 2
    Clock.tick(60)


def Scoreboard():
    global PLACE
    window.fill((0, 0, 0))
    py.draw.rect(window, (255, 127, 80), (100, var.winS - 700, var.winS - 200, 20 * 30))
    for y in range(15):
        py.draw.rect(window, (255, 99, 71), (100, y * 40 + var.winS - 700, var.winS - 200, 20))
        try:
            window.blit(var.Font_Scoreboard.render(scores[y][1], True, (255, 255, 255)),
                        (var.winS - 20 * 8 - var.Font_Scoreboard.size(scores[y][1])[0] // 2,
                         y * 20 + 20 + var.winS - 700))
            window.blit(var.Font_Scoreboard.render(scores[y][0], True, (255, 255, 255)),
                        (120, y * 20 + 20 + var.winS - 700))
            window.blit(var.Font_Scoreboard.render(scores[y][2][:-1], True, (255, 255, 255)),
                        (100 + (var.winS - 20 * 9) // 2 - var.Font_Scoreboard.size(scores[y][2][:-1])[0] // 2,
                         y * 20 + 20 + var.winS - 700))
        except:
            pass
    window.blit(var.Font_Scoreboard.render("Score", True, (0, 0, 0)), (var.winS - 20 * 9, var.winS - 700))
    window.blit(var.Font_Scoreboard.render("Name", True, (0, 0, 0)), (120, var.winS - 700))
    window.blit(var.Font_Scoreboard.render("Date", True, (0, 0, 0)),
                (100 + (var.winS - 20 * 9) // 2 - var.Font_Scoreboard.size("Date")[0] // 2, var.winS - 700))
    var.Back_Button.Draw(window)
    if var.Back_Button.Click():
        PLACE = 0
    py.display.update()
    Clock.tick(30)


def Settings():
    global var, snake, fruit, PLACE
    py.time.delay(var.Delay)
    Clock = py.time.Clock()
    window.fill((0, 0, 0))
    window.blit(var.Fps_Text, (10, 14))
    window.blit(var.WinS_TEXT, (10, 90))
    window.blit(var.Delay_Text, (10, 166))

    var.Fps_slider.Move()
    var.WinS_Slider.Move()
    var.Player_Name_TextBox.Input()
    var.Delay_Slider.Move()
    window.blit(var.Player_Name_Text, (10, 242))
    var.Fps = round(var.Fps_slider.val)
    var.winS = round(var.WinS_Slider.val)
    var.Delay = round(var.Delay_Slider.val)
    var.Player_Name = var.Player_Name_TextBox.text

    var.Player_Name_TextBox.Draw(window)
    var.Save_Button.Draw(window)
    var.Cancel_Button.Draw(window)
    var.WinS_Slider.Draw(window)
    var.Fps_slider.Draw(window)
    var.Delay_Slider.Draw(window)
    if var.Save_Button.Click():
        py.display.set_mode((var.winS, var.winS + 50))
        with open("settings.txt", "w") as file:
            file.write(f"""Fps: {var.Fps}
Delay: {var.Delay}
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
    if var.Cancel_Button.Click():
        var.winS = 750
        var.GridSize = 25
        var.Fps = 10
        var.Delay = 50
        var.Player_Name = "ERR"
        try:
            with open("settings.txt", "r") as file:
                settings = file.read()
                settings = settings.split("\n")

            var.winS = int(settings[3][12:])
            var.GridSize = int(settings[4][10:])
            var.Fps = int(settings[1][5:])
            var.Delay = int(settings[2][6:])
            var.Player_Name = settings[5][12:]
        except:
            pass
        PLACE = 0
    var.Fps_Text = var.settings_fonts.render(f"Fps: {var.Fps}", True, (255, 255, 255))
    var.WinS_TEXT = var.settings_fonts.render(f"WinS: {var.winS}", True, (255, 255, 255))
    var.Delay_Text = var.settings_fonts.render(f"Delay: {var.Delay}", True, (255, 255, 255))
    py.display.update()
    Clock.tick(10)


def Close():
    for e in py.event.get():
        if e.type == py.QUIT:
            var.active = False
    GoBack()


def Game0ver():
    global var, snake, fruit, scores
    Gameover = var.Gameover_Text.get_rect()
    Gameover.center = (var.winS // 2, var.winS // 2)
    window.blit(var.Gameover_Text, Gameover)
    py.display.set_caption("Game0ver")
    py.display.update()
    scores.append((f"{var.Player_Name!r}", var.score, datetime.now().strftime("%H:%M %d/%m/%Y")))
    with open("scores.txt", "a") as f:
        f.write(f' Player {var.Player_Name!r} Scored {var.score} at {datetime.now().strftime("%H:%M %d/%m/%Y")}. \n')
    py.time.wait(2000)
    var = Game()
    snake = Snake()
    fruit = Fruit()
    _SCORE_TEXT_ = var.settings_fonts.render(f"Score: {var.score}", True, (255, 255, 255))


def FruitInBody():  # Check if fruit spawn in snake body
    for part in snake.body:
        if fruit.x == part[0] and fruit.y == part[1]:
            return True
    return False


def FruitEat():
    global fruit
    if snake.x == fruit.x and snake.y == fruit.y:
        snake.AddBlock()
        while FruitInBody():
            fruit.New_Pos()
        var.score += 10 * var.Fps
        var.Score_Text = var.settings_fonts.render(f"Score: {var.score}", True, (255, 255, 255))


def logic():
    FruitEat()
    snake.Move()
    for k, part in enumerate(snake.body):
        if snake.x == part[0] and snake.y == part[1] and snake.len != 2 and k != 0:
            Game0ver()
            break


def DrawSnake():
    for j, pa in enumerate(snake.body):
        if j != 0:
            py.draw.rect(window, (255, 0, 0),
                         (pa[0] * var.GridSize + 1, pa[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))
        else:
            py.draw.rect(window, (0, 0, 255),
                         (pa[0] * var.GridSize + 1, pa[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))


def DrawGrid():
    for o in range(var.winS // var.GridSize + 1):
        py.draw.line(window, (255, 255, 255), (o * var.GridSize, 0), (o * var.GridSize, var.winS))
        py.draw.line(window, (255, 255, 255), (0, o * var.GridSize), (var.winS, o * var.GridSize))


def Draw():
    window.fill((0, 0, 0))
    # DrawGrid()
    fruit.Draw(window)
    DrawSnake()
    py.draw.rect(window, (30, 30, 30), (0, var.winS, var.winS, 55))
    window.blit(var.Score_Text, (0, var.winS))
    py.display.update()


def MainGame():
    py.time.delay(var.Delay)
    Close()
    logic()
    Draw()
    Clock.tick(var.Fps)


Places = [Menu,
          Settings,
          Scoreboard,
          MainGame
          ]


def Main():
    if var.winS < 450:
        var.active = False
    while var.active:
        Close()
        Places[PLACE]()


if __name__ == "__main__":
    Main()
py.quit()
