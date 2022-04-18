import pytest
import sqlite3
from ehr_2 import (
    parse_patient_data,
    parse_lab_data,
    num_older_than,
    sick_patients,
    first_admission,
)
from logging import raiseExceptions

con = sqlite3.connect("ehr700.db")
print(con)
cur = con.cursor()
print(cur)

# Test data available from repo
parse_patient_data("PatientCorePopulatedTable.txt")
parse_lab_data("LabsCorePopulatedTable.txt")


def test_num_older_than():
    """Test num_older_than."""
    assert (
        num_older_than(
            50.0,
            cur,
        )
        == 6
    )
    assert (
        num_older_than(
            80.0,
            cur,
        )
        == 2
    )


def test_sick_patients():
    """Test sick_patients."""
    assert sick_patients("METABOLIC: GLUCOSE", ">", 100.0, cur) == [
        ("1A8791E3-A61C-455A-8DEE-763EB90C9B2C",)
    ]
    assert sick_patients("METABOLIC: ALK PHOS", ">", 60.0, cur) == [
        ("81C5B13B-F6B2-4E57-9593-6E7E4C13B2CE",)
    ]


def test_first_admission():
    """Test first_admission."""
    assert (
        first_admission(
            "81C5B13B-F6B2-4E57-9593-6E7E4C13B2CE",
            "METABOLIC: ALK PHOS",
            cur,
        )
        == 23
    )
