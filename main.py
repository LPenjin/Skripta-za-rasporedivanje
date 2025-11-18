import argparse

from logic.ShiftAssigner import ShiftAssigner


def main():
    parser = argparse.ArgumentParser(description='Excel ingestion')
    parser.add_argument('-s', '--sheet-name', required=True, type=str, help='Name of the sheet to be ingested')
    parser.add_argument('-d', '--duration', type=float, default=2.0, help='Duration of each shift')
    parser.add_argument('-p', '--start-time', type=str, default='20:00', help='Start of event')

    args = parser.parse_args()

    ShiftAssigner.read_excel_and_assign_shifts(args)


if __name__ == '__main__':
    main()