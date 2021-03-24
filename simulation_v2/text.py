from typing import Tuple

import pygame as pg

import ptext
from ctx import ctx

Position = Tuple[int, int]


class Text:

    @staticmethod
    def draw(*args,
             size=3,
             color="white",
             gcolor="white",
             scolor="black",
             **kwargs
             ) -> Tuple[pg.Surface, Position]:
        return ptext.draw(
            *args,
            fontname="simulation",  # TODO
            fontsize=8 * size,
            color=pg.Color(color),
            gcolor=pg.Color(gcolor),
            scolor=pg.Color(scolor),
            surf=ctx.surface,
            **kwargs
        )
