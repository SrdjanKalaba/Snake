import pygame as py

py.init()


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, FontSize: int, backcolor: tuple = ()):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.backcolor = backcolor
        self.font = py.font.SysFont("Arial", FontSize)
        self.TEXT = self.font.render(text, True, (255, 255, 255))
        self._TEXT_POS_ = self.TEXT.get_rect()
        self._TEXT_POS_.center = (self.x + self.width // 2, self.y + self.height // 2)

    def Draw(self, Window: py.Surface):
        Mx, My = py.mouse.get_pos()
        if self.x + self.width > Mx > self.x and self.y + self.height > My > self.y:
            py.draw.rect(Window, (78, 139, 237), (self.x, self.y, self.width, self.height))
        else:
            py.draw.rect(Window, self.backcolor, (self.x, self.y, self.width, self.height))
        py.draw.rect(Window, (255, 255, 255), (self.x, self.y, self.width, self.height), 8)
        Window.blit(self.TEXT, self._TEXT_POS_)

    def OnClick(self):
        for e in py.event.get():
            if e.type == py.MOUSEBUTTONDOWN:
                if e.button == 1:
                    return True
                else:
                    return False
            else:
                return False
