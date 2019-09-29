""" intsance of the break schedule problem """

from model import *
from pyomo.opt import SolverFactory
from pyomo.environ import DataPortal
import numpy as np
import pandas as pd


path_in = 'input/'
path_out = 'output/'

""" Select a solver: cbc or glpk. """
opt = SolverFactory('cbc')

""" Load the input data. """
data = DataPortal()
data.load(filename=path_in+'demand.csv', index='t', param='demand')
data.load(filename=path_in+'workers.csv', set=m.w)
data.load(filename=path_in+'capacities.csv', index=m.w, param='cap')
data.load(filename=path_in+'break_settings.csv', index=m.w,
          param=['break_length', 'num_breaks',
                 'earliest_break_start', 'latest_break_end'])
data.load(filename=path_in+'shift_schedule.csv', param=m.shift_schedule,
          format='array')

""" Create the instanz. """
instance = m.create_instance(data)

""" Solve the optimization problem """
results = opt.solve(instance, symbolic_solver_labels=True, tee=True,
                    load_solutions=True)

""" Write the output """
output = pd.DataFrame()
for w in instance.w.value:
    for t in instance.t.value:
        output.loc[t, w+'_shift'] = instance.shift_schedule[t, w]
        output.loc[t, w+'_break_on'] = instance.break_on[t, w].value
        output.loc[t, w+'_break_start'] = instance.break_start[t, w].value
        output.loc[t, w+'_break_end'] = instance.break_end[t, w].value
output = output.fillna(0)

""" Export the shift schedule and statistic in one file """
export = pd.ExcelWriter(path_out+'break_schedule.xlsx', engine='xlsxwriter')
output.to_excel(export, 'break_schedule', startrow=0, startcol=0)
export.save()
