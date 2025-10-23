from datetime import datetime

from BaseObjects.shift import ShiftBase


#def sort_into_shifts(volunteers: list[VolunteerBase], shift: ShiftBase):


def main():
    people_per_position = [[2, 2, 2, 2],
                           [2, 2, 2, 2],
                           [2, 2, 2, 2],
                           [2, 3, 3, 2]]

    hard_per_position = [[False, False, False, False],
                         [False, False, False, False],
                         [False, False, False, False],
                         [False, True, True, False]]

    stakla = ShiftBase('stakla', 2.0, datetime.strptime('22:00', "%H:%M"))

    stakla_smjene = stakla.create_shifts(people_per_position, hard_per_position)

    print('Gotovo')


if __name__ == '__main__':
    main()