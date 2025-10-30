from enum import Enum
from typing import List, Optional
from BaseObjects.constraints import Constraint, ConstraintCapable
from functools import reduce


class VolunteerBase:

    __slots__ = ['name', 'color', 'leader', 'constraints', 'section', 'taken_shifts']

    name: str
    color: Optional['AssociationColor']
    leader: str
    constraints: Optional[List[Constraint]]
    section: str

    def __init__(self, name, color, leader, constraints, section):
        self.name = name
        self.color = color
        self.leader = leader
        self.constraints = constraints
        self.section = section
        self.taken_shifts = []

    def __eq__(self, other):
        if not isinstance(other, VolunteerBase):
            return NotImplemented
        return (
            self.name == other.name and
            self.color == other.color and
            self.leader == other.leader and
            self.constraints == other.constraints
        )
        
    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def get_availability(self, shifts):
        availability_list = []
        for constraint in self.constraints:
            if not isinstance(constraint, ConstraintCapable):
                availability_list.append(constraint.get_available_shifts(shifts, self.taken_shifts))

        availability_intersection = []
        for shift_period in range(len(availability_list[0])):
            intersection = [set.intersection(*(set(available_shifts[shift_period]) for available_shifts in availability_list))]
            availability_intersection.append(list(intersection[0]))

        return availability_intersection

    def get_availability_leader(self, shifts):
        if self.leader:
            availability_list = []
            for constraint in self.constraints:
                    availability_list.append(constraint.get_available_shifts(shifts, self.taken_shifts))

            availability_intersection = []
            for shift_period in range(len(availability_list[0])):
                intersection = [
                    set.intersection(*(set(available_shifts[shift_period]) for available_shifts in availability_list))]
                availability_intersection.append(list(intersection[0]))

            return availability_intersection
        else:
            return [[] for _ in range(len(shifts))]

    def get_availability_hard(self, shifts):
            availability_list = []
            for constraint in self.constraints:
                availability_list.append(constraint.get_available_shifts(shifts, self.taken_shifts))

            availability_intersection = []
            for shift_period in range(len(availability_list[0])):
                intersection = [
                    set.intersection(*(set(available_shifts[shift_period]) for available_shifts in availability_list))]
                availability_intersection.append(list(intersection[0]))

            return availability_intersection

class AssociationColor(Enum):
    BLUE = 0
    ORANGE = 1