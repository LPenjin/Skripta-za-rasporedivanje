from typing import List
from datetime import timedelta

class Constraint:


    def get_available_shifts(self, shifts, taken_shifts):
        pass


class ConstraintPause(Constraint):

    __slots__ = ['num_shifts']

    num_shifts: int

    def __init__(self, num_shifts: int = 1) -> None:
        self.num_shifts = num_shifts

    def get_available_shifts(self, shifts, taken_shifts):

        available_shifts = []
        for period_of_shifts in shifts:
            available = True
            for taken_shift in taken_shifts:
                if (taken_shift.start - timedelta(hours=taken_shift.duration) * self.num_shifts <= period_of_shifts[0].start \
                    <= taken_shift.start + timedelta(hours=taken_shift.duration) * self.num_shifts):
                    available = False
            if available:
                available_shifts.append(period_of_shifts)
            else:
                available_shifts.append([])

        return available_shifts

class ConstraintUnavailable(Constraint):

    __slots__ = ['times_unavailable']

    times_unavailable: list[tuple[str, str]]

    def __init__(self, times_unavailable: list[tuple[str, str]]) -> None:
        self.times_unavailable = times_unavailable

    def get_available_shifts(self, shifts, taken_shifts):
        available_shifts = []

        for period_of_shifts in shifts:
            available_shifts_period = []
            for shift in period_of_shifts:
                shift_available = True
                if not shift.is_full():
                    if self.times_unavailable:
                        for time_unavailable in self.times_unavailable:
                            if (shift.start <= time_unavailable[0] < shift.start + timedelta(hours=shift.duration)\
                                    or shift.start <= time_unavailable[1] < shift.start + timedelta(hours=shift.duration)):
                                shift_available = False
                                break
                        if shift_available:
                            available_shifts_period.append(shift)
                    else:
                        available_shifts_period.append(shift)

            available_shifts.append(available_shifts_period)

        return available_shifts

class ConstraintCapable(Constraint):

    __slots__ = ['capable']

    capable: bool

    def __init__(self, capable: bool) -> None:
        self.capable = capable

    def get_available_shifts(self, shifts, taken_shifts):
        available_shifts = []

        for period_of_shifts in shifts:
            available_shifts_period = []
            for shift in period_of_shifts:
                if not shift.is_full() and self.capable == shift.hard:
                    available_shifts_period.append(shift)
            available_shifts.append(available_shifts_period)

        return available_shifts

class ConstraintMaxShifts(Constraint):

    __slots__ = ['max_shifts']

    max_shifts: int

    def __init__(self, max_shifts: int) -> None:
        self.max_shifts = max_shifts

    def get_available_shifts(self, shifts, taken_shifts):
        if len(taken_shifts) >= self.max_shifts:
            return [[] for _ in shifts]
        else:
            return shifts
