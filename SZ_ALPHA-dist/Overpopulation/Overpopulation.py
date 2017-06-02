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
POP_COUNT = 1000     
WEALTH = 100    
YEAR = 1998    
USED = 0                                                                                            #index of operator
USED_INDEX = [False, False, False, False, False, False, False, False, False, False, False, False]   #Checks whether an operator has been used or not
#<COMMON_CODE>

class State:
    def __init__(self, growth_rate, pop_count, wealth, year, used):
        self.growth_rate = growth_rate
        self.pop_count = pop_count
        self.wealth = wealth
        self.year = year
        self.used = used

    def __copy__(self):
        news = State(None, None, None, None, None)
        news.growth_rate = self.growth_rate
        news.pop_count = self.pop_count
        news.wealth = self.wealth
        news.year = self.year
        news.used = self.used
        return news

    def __str__(self):
        return "Current Population: " + str(self.pop_count) + ", Current growth rate: " + str(self.growth_rate) + \
        ", Current wealth: " + str(self.wealth) + ", Year: " + str(self.year)

    def __eq__(self, s):
        if self.growth_rate != s.growth_rate: return False
        if self.pop_count != s.pop_count: return False
        if self.wealth != s.wealth: return False
        if self.year != s.year: return False
        if self.used != s.used: return False
        return True

    def __hash__(self):
        return (self.__str__()).__hash__()

def can_apply_vis(state, role_number, used):
    return state.year < 2000

def apply_vis(state, growth_factor, cost, used):
    s = state.__copy__()
    s.year += 1
    return s

def can_apply(state, role_number, used):
    if state.year < 2000: return False
    if (used != None):
        if USED_INDEX[used] == True: return False #if the index for the operator is not null, check array to see if it has been used before
    return not goal_test(state)

def apply_op(state, growth_factor, cost, used):
    s = state.__copy__()
    s.growth_rate -= growth_factor
    s.pop_count *= s.growth_rate
    s.pop_count = round(s.pop_count)
    s.wealth -= cost
    s.year += 1
    if (used != None):
        USED_INDEX[used] = True     #similar check as above, just setting it to true if it hasnt been used before
    return s

def goal_test(s):
    return s.growth_rate <= 1 or s.pop_count > 10000 or s.wealth < 0

def goal_message(s):
    return "The Simulation has Concluded"

class Operator:
    def __init__(self, name, precond, state_transf, growth_rate, cost, used):
        self.precond = precond
        self.state_transf = state_transf
        self.growth_rate = growth_rate
        self.cost = cost
        self.name = name + " Growth Rate: " + str(self.growth_rate) + ", Cost: $" + str(self.cost) if name!="Next->" else name
        self.used = used

    def is_applicable(self, s, role_number):
        return self.precond(s, role_number)

    def apply(self, s):
        return self.state_transf(s, self.growth_rate, self.cost, self.used)

#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_STATE = State(GROWTH_RATE, POP_COUNT, WEALTH, YEAR, USED)
print(INITIAL_STATE)
#</INITIAL_STATE>

#<ROLES>
ROLES = [{'name':'Gov. Official', 'min':1, 'max':1}]
#</ROLES>

#<OPERATORS>
OPERATORS = [Operator("Require SexEd in Schools.",
                      lambda s, v: can_apply(s,v,0), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, 0),
             Operator("Support Planned Parenthood.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None),
             Operator("Increase investment in technology sector of domestic economy.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None),
             Operator("One-Child Policy.",
                      lambda s, v: can_apply(s,v,3), lambda s, g, c, u: apply_op(s, g, c, u), 0.02, 5, 3),
             Operator("Universal access to safe contraceptives.",
                      lambda s, v: can_apply(s,v,4), lambda s, g, c, u: apply_op(s, g, c, u), 0.01, 5, 4),
             Operator("Guarantee secondary education, especially for girls.",
                      lambda s, v: can_apply(s,v,5), lambda s, g, c, u: apply_op(s, g, c, u), 0.0005, 5, 5),
             Operator("Eradicate gender bias from law, economic opportunity, health, and culture.",
                      lambda s, v: can_apply(s,v,6), lambda s, g, c, u: apply_op(s, g, c, u), 0.0025, 5, 6),
             Operator("End policies that offer financial incentives based on number of children.",
                      lambda s, v: can_apply(s,v,7), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, 7),
             Operator("Stress education on population, environment, and development.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None),
             Operator("Put prices on environmental costs/impacts.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.005, 5, None),
             Operator("Promote transition from childbearing population to an aging population.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None),
             Operator("Commit to stabilizing population growth through the\
                       exercise of human rights and development.",
                      lambda s, v: can_apply(s,v,None), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None),
             Operator("Next->", lambda s, v: can_apply_vis(s,v,None), lambda s, g, c, u: apply_vis(s, g, c, u), 0, 0, None)]

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
    global render_state
    from Overpopulation_SVG_VIS_FOR_BRIFL import render_state
#</STATE_VIS>          
