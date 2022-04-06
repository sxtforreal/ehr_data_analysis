"""The input data for parse_data function should be text files which entries 
are separated by tabs.
"""

from logging import raiseExceptions
import sqlite3

con = sqlite3.connect("ehr.db")
print(con)
cur = con.cursor()
print(cur)


def parse_patient_data(filename: str) -> None:
    """Read the file and parse the data files into a SQLite table.
    The analysis of computational complexity is based on the assumption that
    the input data is N by M.
    """
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Patient([id] TEXT PRIMARY KEY , [gender] TEXT, [dob] TEXT, [age] FLOAT)"
    )  # O(1)
    with open(filename, encoding="utf-8-sig") as p:  # O(1)
        lines = p.readlines()  # O(1)
        col_name = []  # O(1)
        first_row = True  # O(1)
        for line in lines:  # O(N)
            line = line.strip()  # O(1)
            if first_row:  # O(1)
                col_name = line.split()  # O(1)
                first_row = False  # O(1)
            elif not first_row:  # O(1)
                dic = {}  # O(1)
                dat = line.split("\t")  # O(1)
                for count, ele in enumerate(dat, 0):  # O(M)
                    dic[col_name[count]] = dat[count]  # O(1)
                lst = [
                    dic["PatientID"],
                    dic["PatientGender"],
                    dic["PatientDateOfBirth"],
                    0.0,
                ]  # O(4)
                cur.execute(
                    "INSERT or REPLACE INTO Patient VALUES (?, ?, ?, ?)", lst
                )  # O(1)
    return None
    # The function has computational complexity 0(NM)


def parse_lab_data(filename: str) -> None:
    """Read the file and parse the data files into a SQLite table.
    The analysis of computational complexity is based on the assumption that
    the input data is N by M.
    """
    # Create a table for Lab
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Lab([id] TEXT, [admission] INTEGER, [name] TEXT, \
            [value] FLOAT, [units] TEXT, [time] TEXT, [visit_age] FLOAT)"
    )  # O(1)
    with open(filename, encoding="utf-8-sig") as p:  # O(1)
        lines = p.readlines()  # O(1)
        col_name = []  # O(1)
        first_row = True  # O(1)
        for line in lines:  # O(N)
            line = line.strip()  # O(1)
            if first_row:  # O(1)
                col_name = line.split()  # O(1)
                first_row = False  # O(1)
            elif not first_row:  # O(1)
                dic = {}  # O(1)
                dat = line.split("\t")  # O(1)
                for count, ele in enumerate(dat, 0):  # O(M)
                    dic[col_name[count]] = dat[count]  # O(1)
                lst = [
                    dic["PatientID"],
                    dic["AdmissionID"],
                    dic["LabName"],
                    dic["LabValue"],
                    dic["LabUnits"],
                    dic["LabDateTime"],
                    0.0,
                ]  # O(7)
                cur.execute(
                    "INSERT or REPLACE INTO Lab VALUES (?, ?, ?, ?, ?, ?, ?)", lst
                )  # O(1)
    return None
    # The function has computational complexity 0(NM)


class Patient:
    def __init__(self, cur, id: str):
        self.cursor = cur
        self.id = id

    @property
    def gender(self):
        gender = self.cursor.execute(
            f"SELECT gender FROM Patient WHERE id = '{self.id}'"
        )
        return list(gender)[0][0]

    @property
    def dob(self):
        dob = self.cursor.execute(f"SELECT dob FROM Patient WHERE id = '{self.id}'")
        return list(dob)[0][0]

    @property
    def age(self):
        """Get the current age of the patient."""
        age = self.cursor.execute(
            f"SELECT (strftime('%Y', 'now') - strftime('%Y', dob)) - (strftime('%m-%d', 'now')\
                 < strftime('%m-%d', dob)) FROM Patient WHERE id = '{self.id}'"
        )
        return list(age)[0][0]


class Lab:
    def __init__(self, cursor, id: str, admission: int, name: str):
        self.cursor = cursor
        self.id = id
        self.admission = admission
        self.name = name

    @property
    def value(self):
        value = self.cursor.execute(
            f"SELECT value FROM Lab WHERE id = '{self.id}' AND admission = '{self.admission}' AND name = '{self.name}'"
        )
        return list(value)

    @property
    def units(self):
        units = self.cursor.execute(
            f"SELECT units FROM Lab WHERE id = '{self.id}' AND admission = '{self.admission}' AND name = '{self.name}'"
        )
        return list(units)

    @property
    def time(self):
        time = self.cursor.execute(
            f"SELECT time FROM Lab WHERE id = '{self.id}' AND admission = '{self.admission}' AND name = '{self.name}'"
        )
        return list(time)


def num_older_than(given_age: float, cursor) -> int:
    """Returns the number of patients older than a given age."""
    cur = cursor
    cur.execute(
        "UPDATE Patient SET age = (strftime('%Y', 'now') - strftime('%Y', dob))\
             - (strftime('%m-%d', 'now') < strftime('%m-%d', dob))"
    )
    ct = cur.execute(f"SELECT COUNT(*) FROM Patient WHERE age > '{given_age}'")
    return list(ct)[0][0]
    # The function has computational complexity 0(1)


def sick_patients(lab: str, gt_lt: str, value: float, cursor) -> list:
    """Returns a unique list of patients who have a given test with
    value above (">") or below ("<") a given value.
    """
    cur = cursor
    if gt_lt == ">":
        names = cur.execute(
            f"SELECT DISTINCT id FROM Lab WHERE name = '{lab}' AND value > '{value}'"
        )
    elif gt_lt == "<":
        names = cur.execute(
            f"SELECT DISTINCT id FROM Lab WHERE name = '{lab}' AND value < '{value}'"
        )
    else:
        raise ValueError("gt_lt should be either < or >")
    return list(names)
    # The function has computational complexity 0(1)


def first_admission(id: str, name: str, cursor) -> int:
    cur = cursor
    """Returns the age of the patient's (specified by id) 
    first admission to the lab(specified by lab_name).
    """
    visit_age = cur.execute(
        f"SELECT MIN((strftime('%Y', time) - strftime('%Y', (SELECT dob FROM \
            Patient WHERE id = '{id}'))) - (strftime('%m-%d', time) < \
                strftime('%m-%d', (SELECT dob FROM Patient WHERE \
                    id = '{id}')))) FROM Lab WHERE id = '{id}' AND \
                        admission = 1 AND name = '{name}'"
    )
    return list(visit_age)[0][0]
    # The function has computational complexity 0(1)
