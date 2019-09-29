# Break Schedule
We consider a typical working day of a call center. Usually the optimal shift schedule based on a prediction of the expected calls is created weeks before. With respect to the day ahead prediction the shift schedule could not be optimal. In most cases it is not possible to adjust the shift schedule. But there are flexibilities because of planing the breaks optimal. 

## The model
The aim is to maximize the number of the received calls subject to the constraints:
* The break ist during the shift.
* Compliance with the break is compulsory.
* The shift can not start/end with a break.

The objective funtion and the constraints are formulatet in the model.py. The instance.py reads the input data, starts the optimization and write the output data. 

## Minimal example
For the test example we consider a shift schedule for one day (96 quarter hours) for 11 workers. Compare the graphic named shift_schedule_without_breaks.png. In total there are 841 expected calls. Without breaks there are 15 loss calls. 

 The input folder consists of:
* break_settings.csv: with the number of breaks (0 or 1), the break lenght, the earliest start of break and the latest end of break.
* capacities.csv: with the number of calls a worker can handle in a time step.
* demand.csv: with the day ahead prediction of the expected calls.
* shift_schedule.csv: with the shfit schedule.
* workers.csv: with a list of the workers.

The shift schedule including the breaks are visualized in the graphic named shift_schedule_with_breaks.png. With breaks there are 40 loss calls. 

## Extensions
In this version is allowed only one or no break per shift. The next step could include a second break for the workers.    