import pygame as py
import keyboard

py.init()


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, FontSize: int, background: tuple = ()):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.background = background
        self.font = py.font.SysFont("Arial", FontSize)
        self.TEXT = self.font.render(text, True, (255, 255, 255))
        self._TEXT_POS_ = self.TEXT.get_rect()
        self._TEXT_POS_.center = (self.x + self.width // 2, self.y + self.height // 2)

    def Draw(self, Win: py.Surface):
        global Mx, My
        Mx, My = py.mouse.get_pos()
        if self.x + self.width > Mx > self.x and self.y + self.height > My > self.y:
            py.draw.rect(Win, (78, 139, 237), (self.x, self.y, self.width, self.height))
        else:
            py.draw.rect(Win, self.background, (self.x, self.y, self.width, self.height))
        py.draw.rect(Win, (255, 255, 255), (self.x, self.y, self.width, self.height), 4)
        Win.blit(self.TEXT, self._TEXT_POS_)

    def Click(self):
        return py.mouse.get_pressed()[0] and self.x + self.width > Mx > self.x and self.y + self.height > My > self.y


class Slider:
    def __init__(self, x: int, y: int, w: int, h: int, Sh: int, Sw: int, value: int, valueMin: int, valueMax: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Sh = Sh
        self.Sw = Sw
        self.val = value
        self.MaxVal = valueMax
        self.MinVal = valueMin

    def Draw(self, Win: py.Surface):
        py.draw.rect(Win, (50, 50, 50), (self.x, self.y, self.w, self.h))
        py.draw.rect(Win, (255, 255, 255), (self.x, self.y, self.val / self.MaxVal * self.w, self.h))
        py.draw.rect(Win, (50, 50, 50), (self.x, self.y, self.w, self.h), 6)

    def Move(self):
        mouse = py.mouse.get_pressed()
        Mx, My = py.mouse.get_pos()
        if mouse[0] and self.x + self.w > Mx > self.x and self.y + self.h > My > self.y:
            self.val = (Mx - self.x) / self.w * self.MaxVal
            if self.val < self.MinVal:
                self.val = self.MinVal


class Text_BOX:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, font_size: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.font = py.font.SysFont("Arial", font_size)
        self._TEXT_ = self.font.render(self.text, True, (0, 0, 0))

    def Draw(self, Sur: py.Surface):
        if self._TEXT_.get_width() > self.w:
            self.w = self._TEXT_.get_width() + 10
        py.draw.rect(Sur, (255, 255, 255), (self.x, self.y, self.w, self.h))
        py.draw.rect(Sur, (50, 50, 50), (self.x, self.y, self.w, self.h), 4)
        Sur.blit(self._TEXT_, (self.x + 5, self.y))

    def Input(self):
        Mx, My = py.mouse.get_pos()
        if self.x + self.w > Mx > self.x and self.y + self.h > My > self.y:
            for e in py.event.get():
                if e.type == py.KEYDOWN:
                    try:
                        if e.key == py.K_BACKSPACE:
                            self.text = self.text[:-1]
                        if e.key == py.KMOD_SHIFT:
                            self.text += e.unicode
                        else:
                            self.text += e.unicode
                    except:
                        pass
            self._TEXT_ = self.font.render(self.text, True, (0, 0, 0))
