# Last edited P3, 23/11/2020.

# Libraries
import pygame as pg
from os import getcwd as getCWD
from os.path import join as joinPath
from random import randint


# Global Functions
def center(dimension):
    values = {
        "x": windowSize[0] // 2,
        "y": windowSize[1] // 2
    }
    return values[dimension]


def randomStarColour() -> tuple:
    var = randint(0, 50)
    if var in range(0, 49):
        return colours["white"]
    else:
        return colours["blue"]


# Global Variables
pg.init()
clock = pg.time.Clock()
windowSize = (1280, 720)
buttonSize = (400, 140)
charSize = (110, 110)
screen = pg.display.set_mode(windowSize)
pg.display.set_caption("Space Attack")

stages = {
    "menu": True,
    "levelOne": False
}

colours = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "marker": (1, 2, 3),
    "amethyst": (155, 89, 182),
}

starList = []

# External Files (e.g. images, sounds)
shipCrusader = pg.image.load(joinPath(getCWD(), "images", "ship_crusader.png")).convert()
shipCrusader.set_colorkey(colours["marker"])
shipCrusader = pg.transform.scale(shipCrusader, charSize)

fontConsolasTitle = pg.font.SysFont("Consolas", 75)
fontConsolasBody = pg.font.SysFont("Consolas", 55)


# Entity Classes
class Star:
    def __init__(self, entX, entY):
        self.thickness = randint(5, 8)
        self.colour = randomStarColour()
        self.rect = pg.Rect(entX, entY, self.thickness, self.thickness)

    def move(self):
        self.rect.y += 1
        if self.rect.y >= windowSize[1] + self.thickness:
            self.rect.y = self.thickness * -1


class Player:
    def __init__(self, entX, entY):
        self.rect = pg.Rect(entX, entY, charSize[0], charSize[1])


class Enemy:
    pass


# TODO Add basic enemy AI and types.

# Pre-game Set-up
xConcentration = 6  # This determines the star concentration across the screen.
yConcentration = 50  # This determines the star concentration from the top to the bottom of the screen.
for x in range(xConcentration):
    for y in range(yConcentration):
        starList.append(Star(randint(0, windowSize[0]), y * (windowSize[1] / yConcentration)))

# Menu buttons
menuButtonList = (
     {"rect": pg.Rect(center("x") - (10 + buttonSize[0]), center("y"), buttonSize[0], buttonSize[1]),
      "text": "start"},
     {"rect": pg.Rect(center("x") - (10 + buttonSize[0]), center("y") + buttonSize[1] + 20, buttonSize[0], buttonSize[1]),
      "text": "customisation"},
     {"rect": pg.Rect(center("x") + 10, center("y"), buttonSize[0], buttonSize[1]),
      "text": "achievements"},
     {"rect": pg.Rect(center("x") + 10, center("y") + buttonSize[1] + 20, buttonSize[0], buttonSize[1]),
      "text": "quit"}
)

for buttonIndex in range(len(menuButtonList)):
    menuButtonList[buttonIndex]["textSurf"] = fontConsolasBody.render(str.title(menuButtonList[buttonIndex]["text"]), True, (0, 0, 0))

titleSurf = fontConsolasTitle.render("Space Attack", True, (0, 0, 0))

# Stage loops
def menuLoop(var):
    while var:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                var = False
            if event.type == pg.KEYDOWN:  # If the player pressed a key down...
                if event.key == pg.K_ESCAPE:  # If a player presses Esc, quit.
                    var = False  # Do this by: Breaking the loop.
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed(num_buttons=3)[0]:
                    for button in menuButtonList:
                        if button["rect"].collidepoint(mouse[0], mouse[1]):
                            if button["text"] == "start":
                                levelOneLoop(True)
                            elif button["text"] == "achievements":
                                achievementsLoop(True)
                            elif button["text"] == "customisation":
                                customisationLoop(True)
                            elif button["text"] == "quit":
                                var = False

        screen.fill(colours["black"])  # Fill the screen with solid black.
        for star in starList:
            pg.draw.rect(screen, star.colour, star.rect)
            star.move()
        for button in menuButtonList:
            pg.draw.rect(screen, colours["amethyst"], button["rect"])
            screen.blit(button["textSurf"],
                        (button["rect"].centerx - button["textSurf"].get_width() / 2, button["rect"].centery - button["textSurf"].get_height() / 2))
        pg.draw.rect(screen, colours["white"], pg.Rect(center("x") - titleSurf.get_width() * 0.6, center("y") - titleSurf.get_height() * 0.6 - 100, titleSurf.get_width() * 1.2, titleSurf.get_height() * 1.2))
        screen.blit(titleSurf, (center("x") - titleSurf.get_width() / 2, center("y") - titleSurf.get_height() / 2 - 100))
        # TODO Add menu title, buttons.

        pg.display.flip()
        clock.tick(60)


def levelOneLoop(var):  # Whilst the player is playing on level one...
    while var:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                var = False
            if event.type == pg.KEYDOWN:  # If the player pressed a key down...
                if event.key == pg.K_ESCAPE:  # If a player presses Esc, quit.
                    var = False  # Do this by: Breaking the loop.
        screen.fill(colours["white"])
        screen.blit(shipCrusader, (center("x"), center("y")))
        pg.display.flip()
        clock.tick(60)
    # TODO Add basic elements of level 1.


def customisationLoop(var):
    return var


def achievementsLoop(var):
    return var


# Bootstrap
menuLoop(True)
pg.quit()  # If no game loop is occurring, quit the game.
