from BaseObjects.constraints import Constraint, ConstraintUnavailable, ConstraintCapable, ConstraintPause, ConstraintMaxShifts
from BaseObjects.shift import IndividualShift
from BaseObjects.volunteer_base import VolunteerBase
from typing import List


class Sorter:

    @staticmethod
    def sort(volunteer_list: List[VolunteerBase], shifts: List[List[IndividualShift]]):

        volunteer_list.sort(key=lambda volunteer:
        sum(len(available_shifts) for available_shifts in volunteer.get_availability(shifts)))

    @staticmethod
    def sort_leader(volunteer_list: List[VolunteerBase], shifts: List[List[IndividualShift]]):

        volunteer_list.sort(key=lambda volunteer:
        sum(len(available_shifts) for available_shifts in volunteer.get_availability_leader(shifts)))

    @staticmethod
    def all_shifts_full(shifts) -> bool:
        for shift_period in shifts:
            for shift in shift_period:
                if len(shift.volunteers) <= shift.num_volunteers:
                    return False
        return True

    @staticmethod
    def all_shifts_leader(shifts) -> bool:
        for shift_period in shifts:
            for shift in shift_period:
                if not shift.leader:
                    return False
        return True

    @staticmethod
    def get_volunteer_shifts_num(volunteer_list, shifts):
        return sum([sum([len(shifts_available) for shifts_available in volunteer.get_availability(shifts)])
                    for volunteer in volunteer_list])

    @staticmethod
    def get_volunteer_leader_shifts_num(volunteer_list, shifts):
        return sum([sum([len(shifts_available) for shifts_available in volunteer.get_availability_leader(shifts)])
                    for volunteer in volunteer_list])