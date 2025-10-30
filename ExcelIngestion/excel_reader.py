import pandas as pd
from BaseObjects.volunteer_base import VolunteerBase
from BaseObjects.constraints import ConstraintUnavailable, ConstraintPause, ConstraintCapable, ConstraintMaxShifts, Constraint
from typing import List
from math import isnan
from datetime import datetime, timedelta
from openpyxl import Workbook


class ExcelReaderExt:
    """ Extension class for ExcelReader """

    @staticmethod
    def get_capable(row) -> ConstraintCapable:
        return ConstraintCapable(True if row[3] == 'True' else False)

    @staticmethod
    def get_pause(row) -> ConstraintPause:
        if isinstance(row[4], str) or not isnan(row[4]):
            return ConstraintPause(row[4])
        else:
            return ConstraintPause(1)

    @staticmethod
    def get_max_shifts(row) -> ConstraintMaxShifts:
        if not isnan(row[5]):
            return ConstraintMaxShifts(row[5])
        else:
            return ConstraintMaxShifts(2)

    @staticmethod
    def get_unavailable(row) -> ConstraintUnavailable:
        if isinstance(row[6], str) or not isnan(row[6]):
            times_unavailable = row[6].split(';')
            for time in range(len(times_unavailable)):
                time_unavailable = times_unavailable[time].split('-')
                time_unavailable[0] = time_unavailable[0].strip()
                time_unavailable[1] = time_unavailable[1].strip()
                times_unavailable[time] = [datetime.strptime(time_unavailable[0], "%H:%M"),
                                           datetime.strptime(time_unavailable[1], "%H:%M")]
                if times_unavailable[time][1] < times_unavailable[time][0]:
                    times_unavailable[time][1] = times_unavailable[time][1] + timedelta(days=1)
            return ConstraintUnavailable(times_unavailable)
        else:
            return ConstraintUnavailable([])

    @staticmethod
    def get_constraints(row) -> List['Constraint']:
        return [ExcelReaderExt.get_unavailable(row), ExcelReaderExt.get_max_shifts(row),
                ExcelReaderExt.get_capable(row), ExcelReaderExt.get_pause(row)]


class ExcelReader:
    """ Utility class to read Excel files """

    @staticmethod
    def read_excel_file(file_path: str, sheet_name: str) -> pd.DataFrame:
        return pd.read_excel(file_path, sheet_name=sheet_name)

    @staticmethod
    def get_volunteers(file_path: str) -> List['VolunteerBase']:
        df = ExcelReader.read_excel_file(file_path, 'Volonteri')
        df = df.dropna(how='all')

        volunteers = []

        for i, row in df.iterrows():
            if row.isnull().all():
                break
            else:
                row_cells = row.tolist()
                volunteers.append(VolunteerBase(row_cells[0], row_cells[1], row_cells[2],
                                                ExcelReaderExt.get_constraints(row_cells)))

        return volunteers

    @staticmethod
    def get_people_per_position(file_path: str) -> List[List[int]]:
        df = ExcelReader.read_excel_file(file_path, 'Ljudi po smjeni')
        df = df.dropna(how='all')

        people_per_position = []
        for i, row in df.iterrows():
            if row.isnull().all():
                break
            else:
                row_cells = row.tolist()
                people_per_position.append(row_cells)

        return people_per_position

    @staticmethod
    def get_hard_per_position(file_path: str) -> List[List[bool]]:
        df = ExcelReader.read_excel_file(file_path, 'Težina po smjeni')
        df = df.dropna(how='all')

        hard_per_position = []
        for i, row in df.iterrows():
            if row.isnull().all():
                break
            else:
                row_cells = row.tolist()
                row_cells = [True if cell == 'True' else False for cell in row_cells]
                hard_per_position.append(row_cells)

        return hard_per_position

    @staticmethod
    def export_shifts_and_volunteers_to_excel(shifts_groups, all_volunteers, filename="shifts_and_volunteers.xlsx"):
        wb = Workbook()

        # --- Sheet 1: Shifts ---
        ws1 = wb.active
        ws1.title = "Shifts"

        # Header
        ws1.append([
            "Group Index",
            "Start Time",
            "Duration (h)",
            "Hard Shift",
            "Num Volunteers",
            "Leader",
            "Volunteer"
        ])

        for group_idx, shifts in enumerate(shifts_groups, start=1):
            for shift in shifts:
                # Add shift row
                ws1.append([
                    group_idx,
                    shift.start.strftime("%Y-%m-%d %H:%M") if isinstance(shift.start, datetime) else shift.start,
                    shift.duration,
                    "Yes" if shift.hard else "No",
                    shift.num_volunteers,
                    shift.leader.name if shift.leader else "",
                    ""  # Volunteer placeholder
                ])
                # Add volunteers under shift
                for v in shift.volunteers:
                    ws1.append([
                        "", "", "", "", "", "", v.name
                    ])

        # --- Sheet 2: Volunteers sorted by number of taken shifts ---
        ws2 = wb.create_sheet("Volunteers")
        ws2.append(["Name", "Leader", "Color", "Constraints Count", "Taken Shifts"])

        # Sort volunteers descending by number of taken shifts
        sorted_volunteers = sorted(
            all_volunteers,
            key=lambda v: len(v.taken_shifts) if hasattr(v, "taken_shifts") else 0,
            reverse=True
        )

        for v in sorted_volunteers:
            ws2.append([
                v.name,
                v.leader,
                getattr(v.color, "name", str(v.color)) if v.color else "",
                len(v.constraints) if v.constraints else 0,
                len(v.taken_shifts) if hasattr(v, "taken_shifts") else 0
            ])

        wb.save(filename)
        print(f"✅ Excel file saved: {filename}")
