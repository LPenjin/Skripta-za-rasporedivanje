from datetime import datetime
import argparse
from BaseObjects.shift import ShiftBase
from ExcelIngestion.excel_reader import ExcelReader


#def sort_into_shifts(volunteers: list[VolunteerBase], shift: ShiftBase):


def main():
    parser = argparse.ArgumentParser(description='Excel ingestion')
    parser.add_argument('-s', '--sheet-name', required=True, type=str, help='Name of the sheet to be ingested')

    args = parser.parse_args()

    people_per_position = ExcelReader.get_people_per_position(args.sheet_name)

    hard_per_position = ExcelReader.get_hard_per_position(args.sheet_name)

    volunteers = ExcelReader.get_volunteers(args.sheet_name)

    stakla = ShiftBase('stakla', 2.0, datetime.strptime('22:00', "%H:%M"))

    stakla_smjene = stakla.create_shifts(people_per_position, hard_per_position)

    print('Gotovo')


if __name__ == '__main__':
    main()