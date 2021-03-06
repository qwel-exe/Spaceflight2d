import pygame
from pygame.locals import *
from math import *

from clock import ABClock
pygame.init()

WIDTH, HEIGHT = 900, 500
Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
Font = pygame.font.Font("mksanstallx.ttf", 14)
BigFont = pygame.font.Font("mksanstallx.ttf", 18)


class sli(object):
    __slots__ = ("index", "max", "min")

    def __init__(self, tup):
        self.index = tup[0]
        self.min = tup[1]
        self.max = tup[2]


class chk(object):
    __slots__ = "checked"

    def __init__(self, checked):
        self.checked = checked


def Menu(
    Items,
    Xoffset,
    Xoffset2,
    Yoffset,
    itemheight,
    totalheight = HEIGHT,
    boxwidth = WIDTH,
    FontSurface = Font,
    focus=0,
    
    
):
    Clock = ABClock()
    sliderdata = {}
    for item in Items:
        if item[2] == "slider":
            sliderdata[item[1]] = sli(item[3])
        elif item[2] == "checkbox":
            sliderdata[item[1]] = chk(item[3])
    while True:
        Clock.tick(10)
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                return "exit", sliderdata
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return "cancel", sliderdata
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if Xoffset < event.pos[
                        0
                    ] < Xoffset + boxwidth and Yoffset < event.pos[
                        1
                    ] < totalheight * len(
                        Items
                    ):
                        clicked_item = (event.pos[1] - 20) / totalheight
                        if Items[clicked_item][2] in ("button", "cancelbutton"):
                            return Items[clicked_item][1], sliderdata
                        elif Items[clicked_item][2] == "slider":
                            if Xoffset2 < event.pos[0]:
                                p = sliderdata[Items[clicked_item][1]]
                                p.index = int(
                                    round(
                                        float(event.pos[0] - Xoffset2)
                                        / (boxwidth - Xoffset2 + Xoffset)
                                        * p.max
                                        + p.min
                                    )
                                )
                        elif Items[clicked_item][2] == "checkbox":
                            if Xoffset + boxwidth - itemheight < event.pos[0]:
                                p = sliderdata[Items[clicked_item][1]]
                                p.checked = not p.checked
            elif event.type == MOUSEMOTION:
                if Xoffset < event.pos[0] < Xoffset + boxwidth and Yoffset < event.pos[
                    1
                ] < totalheight * len(Items):
                    focus = (event.pos[1] - Yoffset) / totalheight
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    focus = (focus + 1) % len(Items)
                if event.key == K_RIGHT:
                    if Items[focus][2] == "slider":
                        if (
                            sliderdata[Items[focus][1]].index
                            < sliderdata[Items[focus][1]].max
                        ):
                            sliderdata[Items[focus][1]].index += 1
                    else:
                        focus = (focus + 1) % len(Items)
                elif event.key == K_UP:
                    focus = (focus - 1) % len(Items)
                if event.key == K_LEFT:
                    if Items[focus][2] == "slider":
                        if (
                            sliderdata[Items[focus][1]].index
                            > sliderdata[Items[focus][1]].min
                        ):
                            sliderdata[Items[focus][1]].index -= 1
                    else:
                        focus = (focus - 1) % len(Items)
                elif event.key in (K_RETURN, K_SPACE):
                    if Items[focus][2] in ("button", "cancelbutton"):
                        return Items[focus][1], sliderdata
                    elif Items[focus][2] == "checkbox":
                        p = sliderdata[Items[focus][1]]
                        p.checked = not p.checked
                else:
                    pass
        Surface.fill((0, 0, 0))
        if Yoffset + focus * totalheight + itemheight > Surface.get_height():
            Ymod = (
                Yoffset + (focus + 1) * totalheight + itemheight - Surface.get_height()
            )
        else:
            Ymod = 0
        for n in range(len(Items)):
            draw_item = Items[n][0]
            draw_type = Items[n][2]
            if focus == n:
                if draw_type == "button":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                    )
                    drawcolor = (0, 0, 0)
                elif draw_type == "cancelbutton":
                    pygame.draw.rect(
                        Surface,
                        (200, 200, 200),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                    )
                    drawcolor = (0, 0, 0)
                elif draw_type == "disabled":
                    pygame.draw.rect(
                        Surface,
                        (155, 155, 155),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                    )
                    drawcolor = (0, 0, 0)
                elif draw_type == "slider":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset2,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth - Xoffset2 + Xoffset,
                            itemheight,
                        ),
                    )
                    p = sliderdata[Items[n][1]]
                    if p.index > p.min:
                        pygame.draw.rect(
                            Surface,
                            (200, 200, 200),
                            (
                                Xoffset2,
                                Yoffset + n * totalheight - Ymod,
                                float(p.index - p.min)
                                / (p.max - p.min)
                                * (boxwidth - Xoffset2 + Xoffset),
                                itemheight,
                            ),
                        )
                    drawcolor = (255, 255, 255)
                elif draw_type == "checkbox":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset + boxwidth - itemheight,
                            Yoffset + n * totalheight - Ymod,
                            itemheight,
                            itemheight,
                        ),
                    )
                    p = sliderdata[Items[n][1]]
                    if not p.checked:
                        pygame.draw.rect(
                            Surface,
                            (0, 0, 0),
                            (
                                Xoffset + boxwidth - itemheight + 8,
                                Yoffset + n * totalheight + 8 - Ymod,
                                itemheight - 16,
                                itemheight - 16,
                            ),
                        )
                    drawcolor = (255, 255, 255)
            else:
                if draw_type == "button":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                        1,
                    )
                    drawcolor = (255, 255, 255)
                elif draw_type == "cancelbutton":
                    pygame.draw.rect(
                        Surface,
                        (200, 200, 200),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                        1,
                    )
                    drawcolor = (200, 200, 200)
                elif draw_type == "disabled":
                    pygame.draw.rect(
                        Surface,
                        (155, 155, 155),
                        (
                            Xoffset,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth,
                            itemheight,
                        ),
                        1,
                    )
                    drawcolor = (155, 155, 155)
                elif draw_type == "slider":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset2,
                            Yoffset + n * totalheight - Ymod,
                            boxwidth - Xoffset2 + Xoffset,
                            itemheight,
                        ),
                        1,
                    )
                    p = sliderdata[Items[n][1]]
                    if p.index > p.min:
                        pygame.draw.rect(
                            Surface,
                            (255, 255, 255),
                            (
                                Xoffset2,
                                Yoffset + n * totalheight - Ymod,
                                float(p.index - p.min)
                                / (p.max - p.min)
                                * (boxwidth - Xoffset2 + Xoffset),
                                itemheight,
                            ),
                        )
                    drawcolor = (255, 255, 255)
                elif draw_type == "checkbox":
                    pygame.draw.rect(
                        Surface,
                        (255, 255, 255),
                        (
                            Xoffset + boxwidth - itemheight,
                            Yoffset + n * totalheight - Ymod,
                            itemheight,
                            itemheight,
                        ),
                        1,
                    )
                    p = sliderdata[Items[n][1]]
                    if p.checked:
                        pygame.draw.rect(
                            Surface,
                            (255, 255, 255),
                            (
                                Xoffset + boxwidth - itemheight + 8,
                                Yoffset + n * totalheight + 8 - Ymod,
                                itemheight - 16,
                                itemheight - 16,
                            ),
                        )
                    drawcolor = (255, 255, 255)
            Surface.blit(
                Font.render(draw_item, True, drawcolor),
                (Xoffset + 15, Yoffset + 5 + n * totalheight - Ymod),
            )
        pygame.display.flip()
