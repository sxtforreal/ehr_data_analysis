"""The input data for parse_data function should be text files which entries 
are separated by tabs.
"""

from logging import raiseExceptions
import sqlite3

con = sqlite3.connect("ehr.db")
cur = con.cursor()


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
    return
    # The function has computational complexity 0(NM)


def parse_lab_data(filename: str) -> None:
    """Read the file and parse the data files into a SQLite table.
    The analysis of computational complexity is based on the assumption that
    the input data is N by M.
    """
    # Create a table for Lab
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Lab([id] TEXT, [admission] INTEGER, [name] TEXT, \
            [value] FLOAT, [units] TEXT, [time] TEXT)"
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
                ]  # O(6)
                cur.execute(
                    "INSERT or REPLACE INTO Lab VALUES (?, ?, ?, ?, ?, ?)", lst
                )  # O(1)
    return
    # The function has computational complexity 0(NM)

def num_older_than(given_age: float, cursor) -> int:
    """Returns the number of patients older than a given age."""
    cursor.execute(
        "UPDATE Patient SET age = (strftime('%Y', 'now') - strftime('%Y', dob))\
             - (strftime('%m-%d', 'now') < strftime('%m-%d', dob))"
    )
    ct = cursor.execute("SELECT COUNT(*) FROM Patient WHERE age > ?", (given_age,))
    return list(ct)[0][0]
    # The function has computational complexity 0(1)


def sick_patients(lab: str, gt_lt: str, value: float, cursor) -> list:
    """Returns a unique list of patients who have a given test with
    value above (">") or below ("<") a given value.
    """
    if gt_lt == ">":
        names = cursor.execute(
            "SELECT DISTINCT id FROM Lab WHERE name = ? AND value > ?", (lab, value)
        )
    elif gt_lt == "<":
        names = cursor.execute(
            "SELECT DISTINCT id FROM Lab WHERE name = ? AND value < ?", (lab, value)
        )
    else:
        raise ValueError("gt_lt should be either < or >")
    return list(names)
    # The function has computational complexity 0(1)


def first_admission(id: str, name: str, cursor) -> int:
    """Returns the age of the patient's (specified by id)
    first admission to the lab(specified by lab_name).
    """
    visit_age = cursor.execute(
        "SELECT MIN((strftime('%Y', time) - strftime('%Y', (SELECT dob FROM \
            Patient WHERE id = ?))) - (strftime('%m-%d', time) < \
                strftime('%m-%d', (SELECT dob FROM Patient WHERE \
                    id = ?)))) FROM Lab WHERE id = ? AND \
                        admission = 1 AND name = ?",
        (id, id, id, name),
    )
    return list(visit_age)[0][0]
    # The function has computational complexity 0(1)
