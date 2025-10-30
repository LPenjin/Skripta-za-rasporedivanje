from datetime import datetime
import argparse
from BaseObjects.shift import ShiftBase
from BaseObjects.volunteer_base import VolunteerBase
from ExcelIngestion.excel_reader import ExcelReader
from logic.sorter import Sorter


#def sort_into_shifts(volunteers: list[VolunteerBase], shift: ShiftBase):

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


def main():
    parser = argparse.ArgumentParser(description='Excel ingestion')
    parser.add_argument('-s', '--sheet-name', required=True, type=str, help='Name of the sheet to be ingested')

    args = parser.parse_args()

    people_per_position = ExcelReader.get_people_per_position(args.sheet_name)

    hard_per_position = ExcelReader.get_hard_per_position(args.sheet_name)

    volunteers = ExcelReader.get_volunteers(args.sheet_name)

    shift_base = ShiftBase('stakla', 2.0, datetime.strptime('20:00', "%H:%M"))

    shifts = shift_base.create_shifts(people_per_position, hard_per_position)

    while not Sorter.all_shifts_leader(shifts) and Sorter.get_volunteer_leader_hard_shifts_num(volunteers, shifts) > 0:
        Sorter.sort(volunteers, shifts)
        volunteer_index = 0

        for volunteer in volunteers:
            shift_taken = False
            volunteer_index += 1
            available_shifts = volunteer.get_availability_leader_hard(shifts)
            place_into_shift_leader(available_shifts, shift_taken, shifts, volunteer)


    while not Sorter.all_shifts_leader(shifts) and Sorter.get_volunteer_leader_shifts_num(volunteers, shifts) > 0:
        Sorter.sort(volunteers, shifts)
        volunteer_index = 0

        for volunteer in volunteers:
            shift_taken = False
            volunteer_index += 1
            available_shifts = volunteer.get_availability_leader(shifts)
            place_into_shift_leader(available_shifts, shift_taken, shifts, volunteer)

    while not Sorter.all_shifts_hard(shifts) and Sorter.get_volunteer_hard_shifts_num(volunteers, shifts) > 0:
        Sorter.sort(volunteers, shifts)
        volunteer_index = 0

        for volunteer in volunteers:
            shift_taken = False
            volunteer_index += 1
            available_shifts = volunteer.get_availability_hard(shifts)
            place_into_shift(available_shifts, shift_taken, shifts, volunteer)

    while not Sorter.all_shifts_full(shifts) and Sorter.get_volunteer_shifts_num(volunteers, shifts) > 0:
        Sorter.sort(volunteers, shifts)
        volunteer_index = 0

        for volunteer in volunteers:
            shift_taken = False
            volunteer_index += 1
            available_shifts = volunteer.get_availability(shifts)
            place_into_shift(available_shifts, shift_taken, shifts, volunteer)

    ExcelReader.export_shifts_and_volunteers_to_excel(shifts, volunteers, args.sheet_name[:-5] + ' rasporedeno.xlsx')
    print('Gotovo')





if __name__ == '__main__':
    main()