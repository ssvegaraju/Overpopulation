# Authors: S. Vegaraju, R. Washburne, M. Gim
# Purpose: Provide a visualization for the overpopulation simulation
# Created: 2017
# Python version 3.6.1

import svgwrite
from Overpopulation import POP_COUNT, GROWTH_RATE, WEALTH, YEAR, goal_test, goal_message

DEBUG = False

W = 500
H = 400

def getGreen(green):
    if green < 0:
        return 0
    else:
        return 255

def render_state(s):
    dwg = svgwrite.Drawing(filename = "test-svgwrite.svg",
                           id = "state_svg",
                           size = (str(W) + "px", str(H) + "px"),
                           debug = True)

    green_value = round((s.pop_count / 20) * s.growth_rate)
    green_value = green_value if (green_value >= 0 and green_value <= 255) else getGreen(green_value)
    rb_values = str(round(255 - green_value if 255 - green_value >= 0 else 0))
    color = "rgb(" + rb_values + ", " + str(green_value) + ", " + rb_values + ")"

    dwg.add(dwg.rect(insert = (0,0),
                     size = (str(W) + "px", str(H) + "px"),
                     stroke_width = "1",
                     stroke = "black",
                     fill = color))

    if s.year == 1998:
        dwg.add(dwg.text("Welcome to the Overpopulation Simulator!",
                         insert = (W/2, H/2),
                         text_anchor="middle",
                         font_size="20",
                         fill="white"))
        
    elif s.year == 1999:
        dwg.add(dwg.text("The goal of this simulation is to decrease",
                         insert = (W/2, 100),
                         text_anchor="middle",
                         font_size="17",
                         fill="white"))
        dwg.add(dwg.text("the growth rate of the population to just under 1",
                         insert = (W/2, 118),
                         text_anchor="middle",
                         font_size="17",
                         fill="white"))
        dwg.add(dwg.text("before the population exceeds 10000.",
                         insert = (W/2, 136),
                         text_anchor="middle",
                         font_size="17",
                         fill="white"))
        dwg.add(dwg.text("Keep an eye on your wealth and watch the background!",
                         insert = (W/2, 154),
                         text_anchor="middle",
                         font_size="17",
                         fill="white"))
        dwg.add(dwg.text("(The more pink the background, the closer you are to success!)",
                         insert = (W/2, 172),
                         text_anchor="middle",
                         font_size="17",
                         fill="white"))
        
    else:
        if not goal_test(s):
            # Wealth bar
            dwg.add(dwg.rect(insert = (0, 10),
                             size = (str(s.wealth * 5) + "px", str(H / 10) + "px"),
                             stroke_width = "1",
                             stroke = "black",
                             fill = "rgb(50, 50, 255)"))

            dwg.add(dwg.image("https://www.iconfinder.com/data/icons/business-investing/500/Business_Investment_2-256.png",
                              insert = (1, 10 + H / 10),
                              size = (H/10, H/10)))

            dwg.add(dwg.text("Wealth = " + str(s.wealth),
                             insert = (H / 10 + 1, 10 + (H / 7.5)),
                             text_anchor = "start",
                             font_size="12",
                             fill="white"))

            # Population bar
            dwg.add(dwg.rect(insert = (0, 130),
                             size = (str(s.pop_count / 20) + "px", str(H / 10) + "px"),
                             stroke_width = "1",
                             stroke = "black",
                             fill = "rgb(50, 50, 255)"))

            dwg.add(dwg.image("https://www.iconfinder.com/data/icons/large-svg-icons-part-3/512/community_group_people_users-512.png",
                              insert = (1, 130 + H/10),
                              size = (H/10, H/10)))

            dwg.add(dwg.text("Population count = " + str(s.pop_count),
                             insert = (H / 10 + 1, 130 + (H / 7.5)),
                             text_anchor = "start",
                             font_size="12",
                             fill="white"))

            # Growth rate bar
            dwg.add(dwg.rect(insert = (0, 260),
                             size = (str(s.growth_rate * 25) + "px", str(H / 10) + "px"),
                             stroke_width = "1",
                             stroke = "black",
                             fill = "rgb(50, 50, 255)"))
            
            dwg.add(dwg.image("http://passive-components.eu/wp-content/uploads/2016/01/analytics-icon.png",
                              insert = (1, 260 + H / 10),
                              size = (H/10, H/10)))

            dwg.add(dwg.text("Growth rate = " + str(s.growth_rate),
                             insert = (H / 10 + 1, 260 + (H / 7.5)),
                             text_anchor = "start",
                             font_size="12",
                             fill="white"))

            # Year Indicator
            dwg.add(dwg.text("Year: " + str(s.year),
                             insert = (W - 2, H - 2),
                             text_anchor = "end",
                             font_size = "17",
                             fill = "white"))

        else:
            # Game over text
            dwg.add(dwg.text("Game over.",
                            insert = (W / 2, 150),
                            text_anchor = "middle",
                            font_size = "20",
                            fill="white"))

            dwg.add(dwg.text(goal_message(s),
                            insert = (W / 2, 168),
                            text_anchor = "middle",
                            font_size = "20",
                            fill="white"))

    return (dwg.tostring())

if __name__ == '__main__':
    DEBUG = True
    INITIAL_STATE = (GROWTH_RATE, POP_COUNT)
    print(INITIAL_STATE)
    render_state(INITIAL_STATE)
