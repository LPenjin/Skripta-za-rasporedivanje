from enum import Enum
from typing import List, Optional
from BaseObjects.constraints import Constraint


class VolunteerBase:

    __slots__ = ['name', 'color', 'leader', 'constraints']

    name: str
    color: Optional['AssociationColor']
    leader: str
    constraints: Optional[List[Constraint]]

    def __init__(self, name, color, leader, constraints):
        self.name = name
        self.color = color
        self.leader = leader
        self.constraints = constraints
        
    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)


class AssociationColor(Enum):
    BLUE = 0
    ORANGE = 1