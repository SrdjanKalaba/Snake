from datetime import datetime
from random import randint
from time import perf_counter  # , time
from json import load, dump
from pygame.locals import *

import pygame as py

import menu

py.init()
scores = []
snake_body_part_colors = {
    0: (255, 0, 0),
    1: (0, 0, 255)
}


# offset = 0

def Sort_list(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j]["Score"] < arr[j + 1]["Score"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# with open("scores.txt", "w") as file:
#    dump(list1, file, sort_keys=True)

with open("scores.json", "r") as score:
    scores = load(score)

scores = Sort_list(scores)

PLACE = "Menu"


class Game:
    def __init__(self):
        self.winS = 750
        self.GridSize = 25
        self.Fps = 10
        self.Delay = 50
        self.Player_Name = "Player1"
        try:
            with open("settings.json", "r") as file:
                self.settings = load(file)

            self.winS = self.settings['Window size']
            self.GridSize = self.settings['GridSize']
            self.Fps = self.settings['Fps']
            self.Delay = self.settings['Delay']
            self.Player_Name = self.settings['Player Name']
        except FileNotFoundError or KeyError:
            print(f"   ¯\_(ツ)_/¯   ")
        finally:
            print(f"Successfully loaded settings {self.settings}.")
        self.font = py.font.SysFont("Arial", 85)
        self.settings_fonts = py.font.SysFont("Arial", 45)
        self.Game_title_text = self.font.render("SNAKE GAME", True, (255, 255, 255))
        self.Game_title_pos = ((self.winS - self.font.size("SNAKE GAME")[0]) // 2, 0)
        self.Play_Button = menu.Button(self.winS // 2 - 225, 150, 450, 100, "Play", 56, (50, 50, 50))
        self.Settings_Button = menu.Button(self.winS // 2 - 225, 300, 450, 100, "Settings", 56, (50, 50, 50))
        self.ScoreBoard_Button = menu.Button(self.winS // 2 - 225, 450, 450, 100, "Scoreboard", 56, (50, 50, 50))
        self.Fps_Text = self.settings_fonts.render(f"Fps: {self.Fps}", True, (255, 255, 255))
        self.Delay_Text = self.settings_fonts.render(f"Delay: {self.Delay}", True, (255, 255, 255))
        self.Player_Name_Text = self.settings_fonts.render("Name:", True, (255, 255, 255))
        self.WinS_TEXT = self.settings_fonts.render(f"WinS: {self.winS}", True, (255, 255, 255))
        self.Fps_slider = menu.Slider(220, 14, self.winS - 230, 48, 48, 48, self.Fps, 5, 60)
        self.WinS_Slider = menu.Slider(220, 90, self.winS - 230, 48, 48, 48, self.winS, 750, 1500)
        self.Delay_Slider = menu.Slider(220, 166, self.winS - 230, 48, 48, 48, self.Delay, 0, 100)
        self.Save_Button = menu.Button(0, self.winS - 48, 250, 95, "Ok", 56, (50, 50, 50))
        self.Cancel_Button = menu.Button(self.winS - 250, self.winS - 48, 250, 95, "Cancel", 56, (50, 50, 50))
        self.Back_Button = menu.Button(0, self.winS - 48, 250, 95, "Back", 56, (50, 50, 50))
        self.Player_Name_TextBox = menu.Text_BOX(220, 242, 100, 55, self.Player_Name, 45)
        self.Scoreboard_Font = py.font.SysFont("Arial", 20, True)
        self.Score: int = 0
        self.Score_Text = self.settings_fonts.render(f"Score: {self.Score}", True, (255, 255, 255))
        self.font = py.font.SysFont("Arial", 60)
        self.Gameover_Text = self.font.render("Game0ver", True, (255, 255, 255))
        self.active = True
        py.display.set_caption("Snake Game")


var = Game()
window: py.Surface = py.display.set_mode((var.winS, var.winS + 50))
Clock = py.time.Clock()
call = perf_counter()


class Snake_part:
    def __init__(self, x: int, y: int, color: int = 0):
        self.pos = (x, y)
        self.color = color

    def draw(self):
        py.draw.rect(window, snake_body_part_colors[self.color], (
            self.pos[0] * var.GridSize + 1, self.pos[1] * var.GridSize + 1, var.GridSize - 1, var.GridSize - 1))


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
        self.body = [Snake_part(self.x, self.y, 1)]
        self.len: int = len(self.body)

    def AddBlock(self):
        self.body.append(Snake_part(self.x + self.direct[0], self.y + self.direct[1]))
        self.len += 1

    def UpdatePos(self):
        for i in range(self.len - 1, 0, -1):
            self.body[i].pos = self.body[i - 1].pos
        self.body[0].pos = (self.x, self.y)

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
            self.x = var.winS // var.GridSize - 1
        elif self.x > var.winS // var.GridSize - 1:
            self.x = 0
        elif self.y < 0:
            self.y = var.winS // var.GridSize
        elif self.y > var.winS // var.GridSize - 1:
            self.y = 0
        if self.direct != [0, 0]:
            self.UpdatePos()


snake = Snake()
fruit = Fruit()


def GoBack():
    global var, snake, fruit, PLACE
    keys = py.key.get_pressed()
    if keys[K_ESCAPE]:
        if PLACE == ("Scoreboard" or "Game"):
            var = Game()
            snake = Snake()
            fruit = Fruit()
            var.Score_Text = var.settings_fonts.render(f"Score: {var.Score}", True, (255, 255, 255))
        PLACE = "Menu"


def Menu():
    global PLACE
    window.fill((0, 0, 0))
    window.blit(var.Game_title_text, var.Game_title_pos)
    var.Play_Button.Draw(window)
    var.Settings_Button.Draw(window)
    var.ScoreBoard_Button.Draw(window)
    py.display.update()
    if var.Play_Button.Click():
        PLACE = "Game"
    elif var.Settings_Button.Click():
        PLACE = "Settings"
    elif var.ScoreBoard_Button.Click():
        PLACE = "Scoreboard"
    Clock.tick(60)


def Scoreboard():
    global PLACE, scores  # , offset
    # Mx, My = py.mouse.get_pos()
    # click = py.mouse.get_pressed()
    window.fill((0, 0, 0))
    py.draw.rect(window, (255, 127, 80), (100, 50, var.winS - 200, 20 * 30))
    # renders background
    for i in range(15):
        py.draw.rect(window, (255, 99, 71), (100, i * 40 + var.winS - 700, var.winS - 200, 20))

    # Shows list
    for y in range(min(15, scores.__len__())):
        window.blit(var.Scoreboard_Font.render(scores[y]["Player"], True, (255, 255, 255)),
                    (120, y * 20 + 20 + var.winS - 700))

        window.blit(var.Scoreboard_Font.render(scores[y]["date"], True, (255, 255, 255)),
                    (100 + (var.winS - 180) // 2 - var.Scoreboard_Font.size(scores[y]["date"])[0] // 2,
                     y * 20 + 20 + var.winS - 700))

        window.blit(var.Scoreboard_Font.render(str(scores[y]["Score"]), True, (255, 255, 255)),
                    (var.winS - 160 - var.Scoreboard_Font.size(str(scores[y]["Score"]))[0] // 2,
                     y * 20 + 20 + var.winS - 700))

    window.blit(var.Scoreboard_Font.render("Score", True, (0, 0, 0)), (var.winS - 20 * 9, var.winS - 700))
    window.blit(var.Scoreboard_Font.render("Name", True, (0, 0, 0)), (120, var.winS - 700))
    window.blit(var.Scoreboard_Font.render("Time and Date", True, (0, 0, 0)),
                (100 + (var.winS - 20 * 9) // 2 - var.Scoreboard_Font.size("Time and Date")[0] // 2, var.winS - 700))
    var.Back_Button.Draw(window)
    if var.Back_Button.Click():
        PLACE = "Menu"
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
        var.settings["Window size"] = var.winS
        var.settings["Delay"] = var.Delay
        var.settings["Fps"] = var.Fps
        var.settings["GridSize"] = var.GridSize
        var.settings["Player Name"] = var.Player_Name
        with open("settings.json", "w") as setting:
            dump(var.settings, setting, sort_keys=True)
        var = Game()
        snake = Snake()
        fruit = Fruit()
        PLACE = "Menu"
    if var.Cancel_Button.Click():
        var.winS = 750
        var.GridSize = 25
        var.Fps = 10
        var.Delay = 50
        var.Player_Name = "ERR"
        try:
            with open("settings.json", "r") as file:
                var.settings = load(file)

            var.winS = var.settings['Window size']
            var.GridSize = var.settings['GridSize']
            var.Fps = var.settings['Fps']
            var.Delay = var.settings['Delay']
            var.Player_Name = var.settings['Player Name']
        except FileNotFoundError or KeyError:
            pass
        PLACE = "Menu"
    var.Fps_Text = var.settings_fonts.render(f"Fps: {var.Fps}", True, (255, 255, 255))
    var.WinS_TEXT = var.settings_fonts.render(f"WinS: {var.winS}", True, (255, 255, 255))
    var.Delay_Text = var.settings_fonts.render(f"Delay: {var.Delay}", True, (255, 255, 255))
    py.display.update()
    Clock.tick(30)


def Close():
    if py.event.poll().type == py.QUIT:
        var.active = False
    GoBack()


def Game0ver():
    global var, snake, fruit, scores
    Gameover = var.Gameover_Text.get_rect()
    Gameover.center = (var.winS // 2, var.winS // 2)
    window.blit(var.Gameover_Text, Gameover)
    py.display.set_caption("Game0ver")
    py.display.update()
    scores.append({"Player": var.Player_Name, "Score": var.Score, "Date": datetime.now().strftime("%H:%M %d/%m/%Y")})
    with open("scores.json", "a") as f:
        dump(scores, f)
    py.time.wait(2000)
    var = Game()
    snake = Snake()
    fruit = Fruit()
    _SCORE_TEXT_ = var.settings_fonts.render(f"Score: {var.Score}", True, (255, 255, 255))


def FruitInBody():  # Check if fruit spawn inside of snake's body
    return (fruit.x, fruit.y) in snake.body


def FruitEat():
    global fruit
    if (snake.x, snake.y) == (fruit.x, fruit.y):
        snake.AddBlock()
        fruit.New_Pos()
        while FruitInBody():
            fruit.New_Pos()
        var.Score += 10 * var.Fps
        var.Score_Text = var.settings_fonts.render(f"Score: {var.Score}", True, (255, 255, 255))


def logic():
    FruitEat()
    snake.Move()
    if (snake.x, snake.y) in snake.body[1:] and snake.len > 1:
        Game0ver()


def DrawGrid():
    for o in range(var.winS // var.GridSize + 1):
        py.draw.line(window, (255, 255, 255), (o * var.GridSize, 0), (o * var.GridSize, var.winS))
        py.draw.line(window, (255, 255, 255), (0, o * var.GridSize), (var.winS, o * var.GridSize))


def Draw():
    window.fill((0, 0, 0))
    # DrawGrid()
    fruit.Draw(window)
    for pa in snake.body:
        pa.draw()
    py.draw.rect(window, (30, 30, 30), (0, var.winS, var.winS, 55))
    window.blit(var.Score_Text, (0, var.winS))
    py.display.update()


def MainGame():
    # stime = time()
    py.time.delay(var.Delay)

    Close()
    logic()
    Draw()
    Clock.tick(var.Fps)
    # py.display.set_caption(f"{1 / (time() - stime)}")


Places = {"Menu": Menu,
          "Settings": Settings,
          "Scoreboard": Scoreboard,
          "Game": MainGame
          }


def Main():
    if var.winS < 450:
        var.winS = 450
    while var.active:
        Close()
        Places[PLACE]()
    py.quit()


if __name__ == '__main__':
    Main()
