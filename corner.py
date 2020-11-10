import enum


class Corner(enum.Enum):
    LEFT = (-1, 0)
    TOPLEFT = (-1, -1)
    TOP = (0, -1)
    TOPRIGHT = (1, -1)
    RIGHT = (1, 0)
    BOTTOMRIGHT = (1, 1)
    BOTTOM = (0, 1)
    BOTTOMLEFT = (-1, 1)


CORNERS = (
    Corner.TOPLEFT,
    Corner.TOPRIGHT,
    Corner.BOTTOMLEFT,
    Corner.BOTTOMRIGHT,
)

SIDES = (
    Corner.LEFT,
    Corner.RIGHT,
    Corner.TOP,
    Corner.BOTTOM,
)

corner_iters = {
    #Corner.LEFT: ((-1, 1), (-1, 0), (-1, -1)),
    Corner.LEFT: ((-1, 0),),
    Corner.TOPLEFT: ((-1, 0), (-1, -1), (0, -1)),
    #Corner.TOP: ((-1, -1), (0, -1), (1, -1)),
    Corner.TOP: ((0, -1),),
    Corner.TOPRIGHT: ((0, -1), (1, -1), (1, 0)),
    #Corner.RIGHT: ((1, -1), (1, 0), (1, 1)),
    Corner.RIGHT: ((1, 0),),
    Corner.BOTTOMRIGHT: ((1, 0), (1, 1), (0, 1)),
    #Corner.BOTTOM: ((1, 1), (0, 1), (-1, 1)),
    Corner.BOTTOM: ((0, 1),),
    Corner.BOTTOMLEFT: ((0, 1), (-1, 1), (-1, 0)),
}
