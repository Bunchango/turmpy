from machines import *
from conditions.borders import *

MACHINE_TYPES = {"Langton's Ant": ("machine", LangtonAnt)}
BORDER_TYPES = {"Base": BaseBorder, "Periodic": PeriodicBorder,}