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
USED_INDEX_GROW = [False, False, False, False, False, False, False, False, False, False, False, False]
INFLECTION_POINT = 5000
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

def can_apply(state, role_number, used, inf):
    if state.year < 2000: return False
    if (state.pop_count < INFLECTION_POINT and inf): return False
    if (state.pop_count > INFLECTION_POINT and not inf): return False
    if (used != None):
        if USED_INDEX[used] == True: return False #if the index for the operator is not null, check array to see if it has been used before
    return not goal_test(state)

def apply_op(state, growth_factor, cost, used):
    s = state.__copy__()
    s.growth_rate += growth_factor
    s.pop_count *= s.growth_rate
    s.pop_count = round(s.pop_count)
    s.wealth += cost
    s.year += 1
    if (used != None):
        USED_INDEX[used] = True     #similar check as above, just setting it to true if it hasnt been used before
    return s

def goal_test(s):
    return s.growth_rate <= 1 or s.pop_count > 10000 or s.wealth < 0

def goal_message(s):
    if s.pop_count <=10000 and s.growth_rate <= 1 and s.wealth > 0: return "Congratulations on maintaining a sustainable population!"
    return "You failed to maintain a sustainable population."

def get_name(name, growth_rate, cost):
    if str(name) != "Next->":
        gr = ("Growth rate increases by " + str(abs(growth_rate))) if growth_rate > 0 else ("Growth rate decreases by " + str(abs(growth_rate)))
        cs = ("Profit: $" + str(abs(cost))) if cost > 0 else ("Cost: $" + str(abs(cost)))
        return str(str(name) + " " + str(gr) + " " + str(cs))
    else:
        return str(name)

class Operator:
    def __init__(self, name, precond, state_transf, growth_rate, cost, used, inf):
        self.precond = precond
        self.state_transf = state_transf
        self.growth_rate = growth_rate
        self.cost = cost
        self.name = get_name(name, growth_rate, cost)
        self.used = used
        self.inf = inf

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
                      lambda s, v: can_apply(s,v,0,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.01, -5, 0, True),
             Operator("Support Planned Parenthood.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.01, -5, None, True),
             Operator("Increase investment in technology sector of domestic economy.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, -5, None, True),
             Operator("One-Child Policy.",
                      lambda s, v: can_apply(s,v,3,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.1, 0, 3, True),
             Operator("Universal access to safe contraceptives.",
                      lambda s, v: can_apply(s,v,4,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.2, -5, 4, True),
             Operator("Guarantee secondary education, especially for girls.",
                      lambda s, v: can_apply(s,v,5,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.001, -5, 5, True),
             Operator("Eradicate gender bias from law, economic opportunity, health, and culture.",
                      lambda s, v: can_apply(s,v,6,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.0025, -5, 6, True),
             Operator("End policies that offer financial incentives based on number of children.",
                      lambda s, v: can_apply(s,v,7,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.075, 5, 7, True),
             Operator("Stress education on population, environment, and development.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.075, -5, None, True),
             Operator("Put prices on environmental costs/impacts.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.005, -5, None, True),
             Operator("Promote transition from childbearing population to an aging population.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.075, -5, None, True),
             Operator("Commit to stabilizing population growth through the\
                       exercise of human rights and development.",
                      lambda s, v: can_apply(s,v,None,True), lambda s, g, c, u: apply_op(s, g, c, u), -0.01, -5, None, True),
             Operator("Do Nothing.",
                      lambda s, v: can_apply(s, v, None, True), lambda s, g, c, u: apply_op(s, g, c, u), 0, 0, None, True),
             Operator("Next->", lambda s, v: can_apply_vis(s,v,None), lambda s, g, c, u: apply_vis(s, g, c, u), 0, 0, None, True),
             Operator("Invest into machinery and manufacturing.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.15, -5, None, False),
             Operator("Invest into health sector.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.3, -5, None, False),
             Operator("Promote Family Farms.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 5, None, False),
             Operator("Support negative stance on contraceptives.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.01, 0, None, False),
             Operator("Promote policies that offer financial incentives based on number of children.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.01, -5, None, False),
             Operator("Support women not working.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.0015, 0, None, False),
             Operator("Work with religious organization to spread beliefs on family values.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0.0075, 0, None, False),
             Operator("Support universal education.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), -0.01, -5, None, False),
             Operator("Do Nothing.",
                      lambda s, v: can_apply(s, v, None, False), lambda s, g, c, u: apply_op(s, g, c, u), 0, 0, None, False)]

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
