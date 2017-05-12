''' Overpopulation.py

A SOLUZION problem formulation of the wicked problem
"Overpopulation"

The main point of this formulation is to propose a
formulation and state-space for the current problem
of Human Overpopulation.

This formulation uses references from research obtained
from multiple sources, including a video, WorldBank
statistics, and a series of articles on the subject.

'''

#<METADATA>
SOLUZION_VERSION = "SZ001.0"
PROBLEM_NAME = "Overpopulation"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Vegaraju', 'R. Washburne', 'M. Gim']
PROBLEM_CREATION_DATE = "10-MAY-2017"
PROBLEM_DESC =\
'''
Overpopulation is the wicked problem that describes
the unsustainable growth of human populations across
Earth. This game aims to present a set of operators
that can be applied to help solve the problem of
Overpopulation.

'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>
GROWTH_RATE = 1.185
POP_COUNT = 500
#<COMMON_CODE>
class State:
    def __init__(self, growth_rate, pop_count):
        self.growth_rate = growth_rate
        self.pop_count = pop_count

    def __copy__(self):
        news = State(None, None)
        news.growth_rate = self.growth_rate
        news.pop_count = self.pop_count
        return news

    def __str__(self):
        return "Current Population: " + str(self.pop_count) + ", Current growth rate: " + str(self.growth_rate)

    def __eq__(self, s):
        if self.growth_rate != s.growth_rate: return False
        if self.pop_count != s.pop_count: return False
        return True

    def __hash__(self):
        return (self.__str__()).__hash__()

def can_apply(state):
    return goal_test(state)

def apply_op(state, growth_factor):
    s = state.__copy__()
    s.growth_rate -= growth_factor
    s.pop_count *= s.growth_rate
    return s

def goal_test(s):
    return s.growth_rate == 1 and s.pop_count > 10000

def goal_message(s):
    return "The Simulation has Concluded"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s, growth_factor):
        return self.state_transf(s, growth_factor)

#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_STATE = State(GROWTH_RATE, POP_COUNT)
print(INITIAL_STATE)
#</INITIAL_STATE>

#<ROLES>
ROLES = [{'name':'Player', 'min':1, 'max':1}]
#</ROLES>

#<OPERATORS>
OPERATORS = [Operator("Require SexEd in Schools. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Support Planned Parenthood. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Increase investment in technology sector of domestic\
                      economy. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("One-Child Policy. Growth Rate - 0.02.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Universal access to safe contraceptives. Growth Rate - 0.01.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Guarantee secondary education, especially for girls\
                       . Growth Rate - 0.0005.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Eradicate gender bias from law, economic\
                       opportunity, health, and culture. Growth Rate - 0.0025.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("End policies that offer financial incentives\
                       based on number of children. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Stress education on population, environment, \
                       and development. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Put prices on environmental costs/impacts. Growth Rate - 0.005.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Promote transition from childbearing population\
                       to an aging population. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),
             Operator("Commit to stabilizing population growth through the\
                       exercise of human rights and development. Growth Rate - 0.0015.",
                      lambda s: can_apply(s), lambda s: apply_op(s, 0.0015)),]

#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
BRIFL_SVG = True
render_state = None
def use_BRIFL_SVG():
    global render_State
    from Overpopulation_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>          
