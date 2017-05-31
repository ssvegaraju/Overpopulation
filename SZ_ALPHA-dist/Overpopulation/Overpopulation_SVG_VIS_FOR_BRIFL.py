# Authors: S. Vegaraju, R. Washburne, M. Gim
# Purpose: Provide a visualization for the overpopulation simulation
# Created: 2017
# Python version 3.6.1

import svgwrite
from Overpopulation import POP_COUNT, GROWTH_RATE, WEALTH, goal_test

DEBUG = False

W = 500
H = 400

def render_state(s):
    dwg = svgwrite.Drawing(filename = "test-svgwrite.svg",
                           id = "state_svg",
                           size = (str(W) + "px", str(H) + "px"),
                           debug = True)

    dwg.add(dwg.rect(insert = (0,0),
                     size = (str(W) + "px", str(H) + "px"),
                     stroke_width = "1",
                     stroke = "black",
                     fill = "rgb(100, 100, 100)")) #grey

    if not goal_test(s):
        # Wealth bar
        dwg.add(dwg.rect(insert = (0, 10),
                         size = (str(s.wealth * 5) + "px", str(H / 10) + "px"),
                         stroke_width = "1",
                         stroke = "black",
                         fill = "rgb(50, 50, 255)"))

        dwg.add(dwg.text("Wealth = " + str(s.wealth),
                         insert = (1, 10 + (H / 20)),
                         text_anchor = "start",
                         font_size="12",
                         fill="white"))

        # Population bar
        dwg.add(dwg.rect(insert = (0, 130),
                         size = (str(s.pop_count / 50) + "px", str(H / 10) + "px"),
                         stroke_width = "1",
                         stroke = "black",
                         fill = "rgb(50, 50, 255)"))

        dwg.add(dwg.text("Population count = " + str(s.pop_count),
                         insert = (1, 130 + (H / 20)),
                         text_anchor = "start",
                         font_size="12",
                         fill="white"))

        # Growth rate bar
        dwg.add(dwg.rect(insert = (0, 260),
                         size = (str(s.growth_rate * 25) + "px", str(H / 10) + "px"),
                         stroke_width = "1",
                         stroke = "black",
                         fill = "rgb(50, 50, 255)"))

        dwg.add(dwg.text("Growth rate = " + str(s.growth_rate),
                         insert = (1, 260 + (H / 20)),
                         text_anchor = "start",
                         font_size="12",
                         fill="white"))

    else:
        dwg.add(dwg.text("The Simulation has Concluded, thanks for playing!",
                insert = (W / 2, H / 2),
                text_anchor = "middle",
                font_size = "20",
                fill="white"))

    return (dwg.tostring())

if __name__ == '__main__':
    DEBUG = True
    INITIAL_STATE = (GROWTH_RATE, POP_COUNT)
    print(INITIAL_STATE)
    render_state(INITIAL_STATE)
