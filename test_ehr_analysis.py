import pytest
from ehr_analysis import (
    Patient,
    Lab,
    num_older_than,
    sick_patients,
    first_admission,
)

patient_dic = [
    {
        "PatientID": "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "PatientGender": "Male",
        "PatientDateOfBirth": "1947-12-28 02:45:40.547",
        "PatientRace": "Unknown",
        "PatientMaritalStatus": "Married",
        "PatientLanguage": "Icelandic",
    },
    {
        "PatientID": "64182B95-EB72-4E2B-BE77-8050B71498CE",
        "PatientGender": "Male",
        "PatientDateOfBirth": "1952-01-18 19:51:12.917",
        "PatientRace": "African American",
        "PatientMaritalStatus": "Separated",
        "PatientLanguage": "English",
    },
    {
        "PatientID": "DB22A4D9-7E4D-485C-916A-9CD1386507FB",
        "PatientGender": "Female",
        "PatientDateOfBirth": "1970-07-25 13:04:20.717",
        "PatientRace": "Asian",
        "PatientMaritalStatus": "Married",
        "PatientLanguage": "English",
    },
    {
        "PatientID": "6E70D84D-C75F-477C-BC37-9177C3698C66",
        "PatientGender": "Male",
        "PatientDateOfBirth": "1979-01-04 05:45:29.580",
        "PatientRace": "White",
        "PatientMaritalStatus": "Married",
        "PatientLanguage": "English",
    },
]
fake_patient_data = []
for i in patient_dic:
    fake_patient_data.append(
        Patient(
            i["PatientID"],
            i["PatientGender"],
            i["PatientDateOfBirth"],
            i["PatientRace"],
            i["PatientMaritalStatus"],
            i["PatientLanguage"],
        )
    )


lab_dic = [
    {
        "PatientID": "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "AdmissionID": "1",
        "LabName": "METABOLIC: GLUCOSE",
        "LabValue": "103.3",
        "LabUnits": "mg/dL",
        "LabDateTime": "1992-06-30 09:35:52.383",
    },
    {
        "PatientID": "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "AdmissionID": "1",
        "LabName": "METABOLIC: GLUCOSE",
        "LabValue": "101.5",
        "LabUnits": "mg/dL",
        "LabDateTime": "1994-06-30 09:35:52.383",
    },
    {
        "PatientID": "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "AdmissionID": "1",
        "LabName": "METABOLIC: CHLORIDE",
        "LabValue": "105.5",
        "LabUnits": "mg/dL",
        "LabDateTime": "1992-07-30 09:35:52.383",
    },
    {
        "PatientID": "DB22A4D9-7E4D-485C-916A-9CD1386507FB",
        "AdmissionID": "1",
        "LabName": "CBC: RED BLOOD CELL COUNT",
        "LabValue": "4.8",
        "LabUnits": "m/cumm",
        "LabDateTime": "1992-07-01 01:31:08.677",
    },
]
fake_lab_data = []
for j in lab_dic:
    fake_lab_data.append(
        Lab(
            j["PatientID"],
            j["AdmissionID"],
            j["LabName"],
            j["LabValue"],
            j["LabUnits"],
            j["LabDateTime"],
        )
    )


def test_num_older_than():
    """Test num_older_than."""
    assert (
        num_older_than(
            50,
            fake_patient_data,
        )
        == 3
    )
    assert (
        num_older_than(
            80,
            fake_patient_data,
        )
        == 0
    )


def test_sick_patients():
    """Test sick_patients."""
    assert (
        sick_patients(
            "METABOLIC: GLUCOSE",
            ">",
            103.0,
            fake_lab_data,
        )
        == ["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"]
    )
    assert (
        sick_patients(
            "CBC: RED BLOOD CELL COUNT",
            ">",
            5,
            fake_lab_data,
        )
        == []
    )


def test_first_admission():
    """Test first_admission."""
    assert (
        first_admission(
            fake_lab_data,
            fake_patient_data,
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "METABOLIC: GLUCOSE",
        )
        == 44
    )
