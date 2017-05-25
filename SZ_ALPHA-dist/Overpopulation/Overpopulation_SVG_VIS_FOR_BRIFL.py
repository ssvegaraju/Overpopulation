# Authors: S. Vegaraju, R. Washburne, M. Gim
# Purpose: Provide a visualization for the overpopulation simulation
# Created: 2017
# Python version 3.6.1

import svgwrite
from Overpopulation import POP_COUNT, GROWTH_RATE

DEBUG = False

W = 500
H = 400

def render_state(s):
    dwg = swgwrite.Drawing(filename = "test-svgwrite.svg",
                           id = "state_svg",
                           size = (str(W) + "px", str(H) + "px"),
                           debug = True)

    dwg.add(dwg.rect(insert = (0,0),
                     size = (str(W) + "px", str(H) + "px"),
                     stroke_width = "1",
                     stroke = "black",
                     fill = "rgb(100, 255, 0)"))

    dwg.add(dwg.text("Population: " + str(s['POP_COUNT']) + ", Rate: " + str(s['GROWTH_RATE']),
                     insert = (W / 2, H / 2),
                     text_anchor = "middle",
                     font_size="25",
                     fill = "red"))

    return (dwg.tostring())

if __name__ == '__main__':
    DEBUG = True
    INITIAL_STATE = {'POP_COUNT':500, 'GROWTH_RATE':1.185}
    print(INITIAL_STATE)
    render_state(INITIAL_STATE)
