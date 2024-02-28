import json
import pygame
from scipy.ndimage.filters import *


class Animation:
    def __init__(self, images, idleSprite=None, airSprite=None, deltaTime=7):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.idleSprite = idleSprite
        self.airSprite = airSprite
        self.deltaTime = deltaTime

    def update(self):
        self.timer += 1
        if self.timer % self.deltaTime == 0:
            if self.index < len(self.images) - 1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.images[self.index]

    def idle(self):
        self.image = self.idleSprite

    def inAir(self):
        self.image = self.airSprite


class Sprite:
    def __init__(self, image, colliding, animation=None, redrawBackground=False):
        self.image = image
        self.colliding = colliding
        self.animation = animation
        self.redrawBackground = redrawBackground

    def drawSprite(self, x, y, screen):
        dimensions = (x * 32, y * 32)
        if self.animation is None:
            screen.blit(self.image, dimensions)
        else:
            self.animation.update()
            screen.blit(self.animation.image, dimensions)


class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./assets/settings/Player.json",
                "./assets/settings/Goomba.json",
                "./assets/settings/Koopa.json",
                "./assets/settings/Animations.json",
                "./assets/settings/BackgroundSprites.json",
                "./assets/settings/ItemAnimations.json",
                "./assets/settings/RedMushroom.json"
            ]
        )

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = Spritesheet(data["spriteSheetURL"])
                dic = {}
                if data["type"] == "background":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                            ),
                            sprite["collision"],
                            None,
                            sprite["redrawBg"],
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite["colorKey"],
                                )
                            )
                        dic[sprite["name"]] = Sprite(
                            None,
                            None,
                            animation=Animation(images, deltaTime=sprite["deltaTime"]),
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "character" or data["type"] == "item":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                                True,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                            sprite["collision"],
                        )
                    resDict.update(dic)
                    continue
        return resDict


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None, ignoreTileSize=False,
                 xTileSize=16, yTileSize=16):
        if ignoreTileSize:
            rect = pygame.Rect((x, y, xTileSize, yTileSize))
        else:
            rect = pygame.Rect((x * xTileSize, y * yTileSize, xTileSize, yTileSize))
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )


class Tile:
    def __init__(self, sprite, rect):
        self.sprite = sprite
        self.rect = rect

    def drawRect(self, screen):
        try:
            pygame.draw.rect(screen, pygame.Color(255, 0, 0), self.rect, 1)
        except Exception:
            pass

class Font(Spritesheet):
    def __init__(self, filePath, size):
        Spritesheet.__init__(self, filename=filePath)
        self.chars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        self.charSprites = self.loadFont()

    def loadFont(self):
        font = {}
        row = 0
        charAt = 0

        for char in self.chars:
            if charAt == 16:
                charAt = 0
                row += 1
            font.update(
                {
                    char: self.image_at(
                        charAt,
                        row,
                        2,
                        colorkey=pygame.color.Color(0, 0, 0),
                        xTileSize=8,
                        yTileSize=8
                    )
                }
            )
            charAt += 1
        return font


class GaussianBlur:
    def __init__(self, kernelsize=7):
        self.kernel_size = kernelsize

    def filter(self, srfc, xpos, ypos, width, height):
        nSrfc = pygame.Surface((width, height))
        pxa = pygame.surfarray.array3d(srfc)
        blurred = gaussian_filter(pxa, sigma=(self.kernel_size, self.kernel_size, 0))
        pygame.surfarray.blit_array(nSrfc, blurred)
        del pxa
        return nSrfc
