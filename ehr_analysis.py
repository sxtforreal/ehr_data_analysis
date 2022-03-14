"""The input data for parse_data function should be text files which entries 
are separated by tabs. The input data for num_older_than and sick_patients
should be the parsed data structures, which are list of class:Patient or
class:Lab.
"""
from datetime import date, datetime


class Patient:
    def __init__(
        self,
        ID: str,
        gender: str,
        DOB: str,
        race: str,
        marital: str,
        language: str,
        PPPBP: str,
    ):
        self.ID = ID
        self.gender = gender
        self.DOB = DOB
        self.race = race
        self.marital = marital
        self.language = language
        self.PPPBP = PPPBP

    @property
    def age(self):
        """Get the current age of the patient."""
        today = date.today()  # O(1)
        dob = self.DOB.split()  # O(1)
        dob = datetime.strptime(dob[0], "%Y-%m-%d")  # O(1)
        if today.month > dob.month:  # O(1)
            return today.year - dob.year  # O(1)
        elif today.month == dob.month and today.day >= dob.day:  # O(1)
            return today.year - dob.year  # O(1)
        elif today.month == dob.month and today.day < dob.day:  # O(1)
            return today.year - dob.year - 1  # O(1)
        elif today.month < dob.month:  # O(1)
            return today.year - dob.year - 1  # O(1)

    # The function has computational complexity 0(1)


class Lab:
    def __init__(
        self,
        PatientID: str,
        Admission: str,
        Name: str,
        Value: str,
        Units: str,
        Time: str,
    ):
        self.PatientID = PatientID
        self.Admission = Admission
        self.Name = Name
        self.Value = Value
        self.Units = Units
        self.Time = Time

    def visit_age(self, patient_info: list[Patient]):
        for patient in patient_info:  # O(N)
            if patient.ID == self.PatientID:  # O(1)
                dob = patient.DOB.split()  # O(1)
                dob = datetime.strptime(dob[0], "%Y-%m-%d")  # O(1)
                visit_date = self.Time.split()  # O(1)
                visit_date = datetime.strptime(visit_date[0], "%Y-%m-%d")  # O(1)
                if visit_date.month > dob.month:  # O(1)
                    return visit_date.year - dob.year  # O(1)
                elif (
                    visit_date.month == dob.month and visit_date.day >= dob.day
                ):  # O(2)
                    return visit_date.year - visit_date.year  # O(1)
                elif visit_date.month == dob.month and visit_date.day < dob.day:  # O(2)
                    return visit_date.year - dob.year - 1  # O(1)
                elif visit_date.month < dob.month:  # O(1)
                    return visit_date.year - dob.year - 1  # O(1)

    # The function has computational complexity 0(N)


def parse_patient_data(filename: str) -> list[Patient]:
    """Read the file and parse the data files into lists of class:Patient.
    The analysis of computational complexity is based on the assumption that
    the input data is N by M.
    """
    output_list = []  # O(1)
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
                output_list.append(
                    Patient(
                        dic["PatientID"],
                        dic["PatientGender"],
                        dic["PatientDateOfBirth"],
                        dic["PatientRace"],
                        dic["PatientMaritalStatus"],
                        dic["PatientLanguage"],
                        dic["PatientPopulationPercentageBelowPoverty"],
                    )  # O(7)
                )
    return output_list  # O(1)


def parse_lab_data(filename: str) -> list[Lab]:
    """Read the file and parse the data files into lists of class:Lab.
    The analysis of computational complexity is based on the assumption that
    the input data is N by M.
    """
    output_list = []  # O(1)
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
                output_list.append(
                    Lab(
                        dic["PatientID"],
                        dic["AdmissionID"],
                        dic["LabName"],
                        dic["LabValue"],
                        dic["LabUnits"],
                        dic["LabDateTime"],
                    )  # O(6)
                )
    return output_list  # O(1)
    # The function has computational complexity 0(NM)


def num_older_than(age: float, patient_info: list[Patient]) -> int:
    """Take the data and return the number of patients
    older than a given age (in years).
    """
    count = 0  # O(1)
    for people in patient_info:  # O(N)
        if people.age > age:  # O(1)
            count += 1  # O(1)
    return count  # O(1)
    # The function has computational complexity 0(N)


def sick_patients(lab: str, gt_lt: str, value: float, lab_info: list[Lab]) -> list[str]:
    """Take the data and return a unique list of
    patients who have a given test with value above
    (">") or below ("<") a given level.
    """
    lst = []  # O(1)
    for record in lab_info:  # O(N)
        if gt_lt == "<":  # O(1)
            if (
                (record.Name == lab)
                and (float(record.Value) < value)
                and (record.PatientID not in lst)
            ):  # O(2)
                lst.append(record.PatientID)  # O(1)
        elif gt_lt == ">":  # O(1)
            if (
                (record.Name == lab)
                and (float(record.Value) > value)
                and (record.PatientID not in lst)
            ):  # O(2)
                lst.append(record.PatientID)  # O(1)
        else:  # O(1)
            raise ValueError("gt_lt should be either < or >")  # O(1)
    return lst  # O(1)
    # The function has computational complexity 0(N)


def first_admission(
    lab_info: list[Lab],
    patient_info: list[Patient],
    id: str,
    lab_name: str,
) -> int:
    """Take the patient data, lab data, and return the age of the patient's
    (specified by id) first admission to the lab(specified by lab_name).
    Because the data contains multiple records for an individual (same
    addmission id and lab name), the decision is to take the minimum of them
    as the first date of admission.
    """
    visits = set()  # O(1)
    for record in lab_info:  # O(N)
        if (
            record.PatientID == id
            and record.Admission == "1"
            and record.Name == lab_name
        ):  # O(3)
            visits.add(record.visit_age(patient_info))  # O(1)
    first = min(visits)  # O(N)
    return first  # O(1)
    # The function has computational complexity 0(N)
