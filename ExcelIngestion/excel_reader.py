import pandas as pd
from BaseObjects.volunteer_base import VolunteerBase
from BaseObjects.constraints import ConstraintUnavailable, ConstraintPause, ConstraintCapable, ConstraintMaxShifts, Constraint
from typing import List
from math import isnan


class ExcelReaderExt:
    """ Extension class for ExcelReader """

    @staticmethod
    def get_capable(row) -> ConstraintCapable:
        return ConstraintCapable(True if row[3] == 'True' else False)

    @staticmethod
    def get_pause(row) -> ConstraintPause:
        return ConstraintPause(row[4])

    @staticmethod
    def get_max_shifts(row) -> ConstraintMaxShifts:
        return ConstraintMaxShifts(row[5])

    @staticmethod
    def get_unavailable(row) -> ConstraintUnavailable:
        if not isnan(row[6]):
            times_unavailable = row[6].split(';')
            for time in range(len(times_unavailable)):
                time_unavailable = times_unavailable[time].split('-')
                time_unavailable[0] = time_unavailable[time][0].strip()
                time_unavailable[1] = time_unavailable[time][1].strip()
                times_unavailable[time] = (time_unavailable[0], time_unavailable[1])
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
            if i == 0:
                continue
            if row.isnull().all():
                break
            else:
                row_cells = row.tolist()
                volunteers.append(VolunteerBase(row_cells[0], row_cells[1], True if row_cells[2] == 'True' else False,
                                                ExcelReaderExt.get_constraints(row_cells)))

        return volunteers

    @staticmethod
    def get_people_per_position(file_path: str) -> List[List[int]]:
        df = ExcelReader.read_excel_file(file_path, 'Ljudi po smjeni')
        df = df.dropna(how='all')

        people_per_position = []
        for i, row in df.iterrows():
            if i == 0:
                continue
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
            if i == 0:
                continue
            if row.isnull().all():
                break
            else:
                row_cells = row.tolist()
                row_cells = [True if cell == 'True' else False for cell in row_cells]
                hard_per_position.append(row_cells)

        return hard_per_position