from typing import List, Optional
from datetime import datetime, timedelta
from typing import List, Optional

from BaseObjects.volunteer_base import VolunteerBase


class ShiftBase:
    """
    Shift object that defines characteristics of shifts

    Duration - How long the shift lasts (1-2 hours)
    Positions - Number of positions for shift (Entrance 1 and 2)
    Days - Number of days the shift is repeated (3 days)
    Start - Start time (22:00)
    End - End time (04:00)
    People_per_shift - Table of amount of people required for each shift
    """


    __slots__ = ['name', 'duration', 'start', 'people_per_shift']

    name: str
    start: datetime
    duration: float

    def __init__(self, name: str, duration: float, start: datetime):
        self.name = name
        self.start = start
        self.duration = duration

    @property
    def people_number(self):
        return sum(sum(people) for people in self.people_per_shift)

    def create_shifts(self, people_per_position: List[List[int]], hard_per_position: List[List[bool]]) -> List[List[
        'IndividualShift']]:
        shifts = [[IndividualShift(num_volunteers, hard, self.start + timedelta(self.duration), self.duration) for num_volunteers, hard in zip(people_per_position[shift], hard_per_position[shift])]
                  for shift in range(len(people_per_position))]
        return shifts



class IndividualShift:

    __slots__ = ['num_volunteers', 'hard', 'start', 'duration', 'volunteers', 'leader']

    num_volunteers: int
    hard: bool
    start: datetime
    duration: float
    volunteers: List[VolunteerBase]
    leader: Optional[VolunteerBase]

    def __init__(self, num_volunteers: int, hard: bool, start: datetime, duration: float):
        self.num_volunteers = num_volunteers
        self.hard = hard
        self.start = start
        self.duration = duration
        self.volunteers = []
        self.leader = None

    def is_full(self):
        return len(self.volunteers) >= self.num_volunteers