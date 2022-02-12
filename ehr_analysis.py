"""The rationale for parsing the data file into lists of dictionaries is that
dictionaries use hash tables and they are efficient to compute with.
The input data for parse_data function should be text files which entries 
are separated by tabs. The input data for num_older_than and sick_patients
should be the parsed data structures, which are list of dictionaries.
"""
from datetime import date, datetime


def parse_data(
    filename: str,
) -> list[dict[str, str]]:
    """Read the file and parse the data files into lists of dictionaries.
    The analysis of computational complexity is based on the assumption
    that the input data is N by M.
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
                output_list.append(dic)  # O(1)
        return output_list  # O(1)
        # The function has computational complexity 0(NM)


def num_older_than(age: float, patient_info: list[dict[str, str]]) -> int:
    """Take the data and return the number of patients
    older than a given age (in years).
    """

    today = date.today()  # O(1)
    age_list = []  # O(1)
    for patient in patient_info:  # O(N)
        dob = patient.get("PatientDateOfBirth")  # O(1)
        if not isinstance(dob, str):  # O(1)
            raise ValueError("Date of Birth should be of type str.")
        else:
            dob = dob.split()  # O(1)
            dob = datetime.strptime(dob[0], "%Y-%m-%d")  # O(1)
            if today.month > dob.month:  # O(1)
                patient_age = today.year - dob.year  # O(1)
            elif today.month == dob.month and today.day >= dob.day:  # O(1)
                patient_age = today.year - dob.year  # O(1)
            elif today.month == dob.month and today.day < dob.day:  # O(1)
                patient_age = today.year - dob.year - 1  # O(1)
            elif today.month < dob.month:  # O(1)
                patient_age = today.year - dob.year - 1  # O(1)
            age_list.append(patient_age)  # O(1)
    count = len([i for i in age_list if i > age])  # O(1)
    return count  # O(1)
    # The function has computational complexity 0(N)


def sick_patients(
    lab: str, gt_lt: str, value: float, lab_info: list[dict[str, str]]
) -> set[str]:
    """Take the data and return a unique list of
    patients who have a given test with value above
    (">") or below ("<") a given level.
    """
    lst = set()  # O(1)
    for patient in lab_info:  # O(N)
        if gt_lt == "<":  # O(1)
            if (patient["LabName"] == lab) and (
                float(patient["LabValue"]) < value
            ):  # O(2)
                lst.add(patient["PatientID"])  # O(1)
        elif gt_lt == ">":  # O(1)
            if (patient["LabName"] == lab) and (
                float(patient["LabValue"]) > value
            ):  # O(2)
                lst.add(patient["PatientID"])  # O(1)
        else:
            raise ValueError("gt_lt should be either < or >")
    return lst  # O(1)
    # The function has computational complexity 0(N)


def first_admission(
    lab_info: list[dict[str, str]],
    patient_info: list[dict[str, str]],
    id: str,
    lab_name: str,
) -> int:
    """Take the patient data, lab data, and return the age of the patient's
    (specified by id) first admission to the lab(specified by lab_name).
    Because the data contains multiple records for an individual (same
    addmission id and lab name), the decision is to take the minimum of them
    as the first date of admission.
    """
    for patient in patient_info:  # O(N)
        if patient["PatientID"] == id:  # O(1)
            dob = patient.get("PatientDateOfBirth")  # O(1)
            if not isinstance(dob, str):  # O(1)
                raise ValueError("Date of Birth should be of type str.")  # O(1)
            else:  # O(1)
                dob = dob.split()  # O(1)
                dob = datetime.strptime(dob[0], "%Y-%m-%d")  # O(1)
    visits = set()  # O(1)
    for patient_visit in lab_info:  # O(N)
        if (
            patient_visit["PatientID"] == id
            and patient_visit["AdmissionID"] == "1"
            and patient_visit["LabName"] == lab_name
        ):  # O(3)
            visit_date = patient_visit.get("LabDateTime")  # O(1)
            if not isinstance(visit_date, str):  # O(1)
                raise ValueError("Date of visit should be of type str.")  # O(1)
            else:  # O(1)
                visit_date = visit_date.split()  # O(1)
                visit_date = datetime.strptime(visit_date[0], "%Y-%m-%d")  # O(1)
                visits.add(visit_date)  # O(1)
    first = min(visits)  # O(N)
    if first.month > dob.month:  # O(1)
        first_adm = first.year - dob.year  # O(1)
    elif first.month == dob.month and first.day >= dob.day:  # O(1)
        first_adm = first.year - dob.year  # O(1)
    elif first.month == dob.month and first.day < dob.day:  # O(1)
        first_adm = first.year - dob.year - 1  # O(1)
    elif first.month < dob.month:  # O(1)
        first_adm = first.year - dob.year - 1  # O(1)
    return first_adm  # O(1)
    # The function has computational complexity 0(N)
