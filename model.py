""" Model of the break schedule problem for call center. """
import pandas as pd
from pyomo.environ import *


""" Define an abstract model. """
m = AbstractModel()

""" Define sets. """
m.t = Set(ordered=True, doc='Time periods.')
m.w = Set(ordered=True, doc='Workers')

""" Define parameters. """
m.demand = Param(m.t, doc='Prediction of expected calls.')
m.cap = Param(m.w, doc='Number of calls a worker can handle.')
m.break_length = Param(m.w, doc='Length of the break.')
m.num_breaks = Param(m.w, doc='Number of breaks')
m.earliest_break_start = Param(m.w, doc='Earliest start of break.')
m.latest_break_end = Param(m.w, doc='Latest end of break.')
m.shift_schedule = Param(m.t, m.w, doc='Given shift schedule.')

""" Define variables. """
m.break_on = Var(m.t, m.w, within=Binary, doc='Break status.')
m.break_start = Var(m.t, m.w, within=Binary, doc='Break start.')
m.break_end = Var(m.t, m.w, within=Binary, doc='Break end.')


def obj_expression(m):
    """ Objective function """
    return (sum(sum(m.cap[w]*(m.shift_schedule[t, w]-m.break_on[t, w])
                for w in m.w)-m.demand[t] for t in m.t))
m.obj = Objective(rule=obj_expression, sense=maximize)


def break_during_worktime(m, t, w):
    """ A break is during the working time. """
    return m.break_on[t, w] <= m.shift_schedule[t, w]
m.BreakDuringWorktime = Constraint(m.t, m.w, rule=break_during_worktime)


def relation_between_binaries(m, t, w):
    """ Relations between start, end and on-time of the break. """
    if t < m.t.next(m.t.first()):
        return Constraint.Skip
    else:
        return (m.break_on[t, w] - m.break_on[t-1, w] ==
                m.break_start[t, w] - m.break_end[t, w])
m.RelationBetweenBinaries = Constraint(m.t, m.w,
                                       rule=relation_between_binaries)


def start_before_end(m, t, w):
    """ The break must start before it is ending. """
    return (sum(m.break_start[i, w] for i in range(m.t.first(), t+1)) >=
            sum(m.break_end[i, w] for i in range(m.t.first(), t+1)))
m.StartBeforeEnd = Constraint(m.t, m.w, rule=start_before_end)


def break_obligation(m, w):
    """ Compliance with the break is compulsory. """
    return sum(m.break_on[t, w] for t in m.t) == m.break_length[w]
m.BreakObligation = Constraint(m.w, rule=break_obligation)


def break_length_per_shift(m, t, w):
    """ The break lenght per shift. """
    if t < m.break_length[w]+1:
        return Constraint.Skip
    else:
        return (sum(m.break_start[i, w]
                    for i in range(t-m.break_length[w]+1, t+1)) ==
                m.break_on[t, w])
m.BreakLengthPerShift = Constraint(m.t, m.w, rule=break_length_per_shift)


def number_breaks_1(m, w):
    """ The number of breaks per shift. """
    return sum(m.break_start[t, w] for t in m.t) == m.num_breaks[w]
m.NumberBreaks1 = Constraint(m.w, rule=number_breaks_1)


def number_breaks_2(m, w):
    """ The number of breaks per shift. """
    return sum(m.break_end[t, w] for t in m.t) == m.num_breaks[w]
m.NumberBreaks2 = Constraint(m.w, rule=number_breaks_2)


def latest_break_end_per_shift(m, t, w):
    """ The latest end of the break. """
    if (m.shift_schedule[t, w] == 1 and t <= m.t.last()-m.latest_break_end[w]+1):
        if (m.shift_schedule[t, w]-m.shift_schedule[t+m.latest_break_end[w]-1, w] == 0):
            return m.break_end[t, w] <= 1
        else:
            return m.break_end[t, w] <= 0
    else:
        return m.break_end[t, w] <= 0
m.LatestBreakEndPerShift = Constraint(m.t, m.w, rule=latest_break_end_per_shift)


def earliest_break_start_per_shift(m, t, w):
    """ The earliest start of the break. """
    if(m.shift_schedule[t, w] == 1) and (t >= m.earliest_break_start[w]+1):
        if(m.shift_schedule[t, w]-m.shift_schedule[t-m.earliest_break_start[w], w] == 0):
            return m.break_start[t, w] <= 1
        else:
            return m.break_start[t, w] <= 0
    else:
        return m.break_start[t, w] <= 0
m.EarliestBreakStartPerShift = Constraint(m.t, m.w,
                                          rule=earliest_break_start_per_shift)
