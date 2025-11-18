from datetime import datetime

from BaseObjects.shift import ShiftBase
from ExcelIngestion.excel_reader import ExcelReader
from logic.sorter import Sorter


class ShiftAssigner:

    @staticmethod
    def place_into_shift(available_shifts: list, shift_taken: bool, shifts,
                         volunteer):
        for i, shift_period in enumerate(available_shifts):
            for shift in shift_period:
                if shift and len(shifts[i][shift.position].volunteers) < shifts[i][shift.position].num_volunteers:
                    volunteer.taken_shifts.append(shift)
                    shifts[i][shift.position].volunteers.append(volunteer)
                    shift_taken = True
                    break
            if shift_taken:
                break

    @staticmethod
    def place_into_shift_leader(available_shifts: list, shift_taken: bool, shifts,
                                volunteer):
        for i, shift_period in enumerate(available_shifts):
            for shift in shift_period:
                if shift and not shifts[i][shift.position].leader:
                    volunteer.taken_shifts.append(shift)
                    shifts[i][shift.position].leader = volunteer
                    shift_taken = True
                    break
            if shift_taken:
                break

    @staticmethod
    def assign_shifts(shifts, volunteers):
        while not Sorter.all_shifts_leader(shifts) and Sorter.get_volunteer_leader_difficult_shifts_num(volunteers, shifts) > 0:
            Sorter.sort(volunteers, shifts)
            volunteer_index = 0

            for volunteer in volunteers:
                shift_taken = False
                volunteer_index += 1
                available_shifts = volunteer.get_availability_leader_difficult(shifts)
                ShiftAssigner.place_into_shift_leader(available_shifts, shift_taken, shifts, volunteer)

        while not Sorter.all_shifts_leader(shifts) and Sorter.get_volunteer_leader_shifts_num(volunteers, shifts) > 0:
            Sorter.sort(volunteers, shifts)
            volunteer_index = 0

            for volunteer in volunteers:
                shift_taken = False
                volunteer_index += 1
                available_shifts = volunteer.get_availability_leader(shifts)
                ShiftAssigner.place_into_shift_leader(available_shifts, shift_taken, shifts, volunteer)

        while not Sorter.all_shifts_difficult(shifts) and Sorter.get_volunteer_difficult_shifts_num(volunteers, shifts) > 0:
            Sorter.sort(volunteers, shifts)
            volunteer_index = 0

            for volunteer in volunteers:
                shift_taken = False
                volunteer_index += 1
                available_shifts = volunteer.get_availability_difficult(shifts)
                ShiftAssigner.place_into_shift(available_shifts, shift_taken, shifts, volunteer)

        while not Sorter.all_shifts_full(shifts) and Sorter.get_volunteer_shifts_num(volunteers, shifts) > 0:
            Sorter.sort(volunteers, shifts)
            volunteer_index = 0

            for volunteer in volunteers:
                shift_taken = False
                volunteer_index += 1
                available_shifts = volunteer.get_availability(shifts)
                ShiftAssigner.place_into_shift(available_shifts, shift_taken, shifts, volunteer)

    @staticmethod
    def read_excel_and_assign_shifts(args):
        people_per_position = ExcelReader.get_people_per_position(args.sheet_name)

        difficult_per_position = ExcelReader.get_difficult_per_position(args.sheet_name)

        volunteers = ExcelReader.get_volunteers(args.sheet_name)

        shift_base = ShiftBase(args.sheet_name[:-5], args.duration, datetime.strptime(args.start_time, "%H:%M"))

        shifts = shift_base.create_shifts(people_per_position, difficult_per_position)

        ShiftAssigner.assign_shifts(shifts, volunteers)

        ExcelReader.export_shifts_and_volunteers_to_excel(shifts, volunteers,
                                                          args.sheet_name[:-5] + ' rasporedeno.xlsx')
        print('Gotovo')