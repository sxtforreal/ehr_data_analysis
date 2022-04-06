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

con = sqlite3.connect("ehr400.db")
print(con)
cur = con.cursor()
print(cur)

# Put your own directory to the data here
dir_patient = "/Users/sunxiaotan/Desktop/BIO821/ehr/PatientCorePopulatedTable.txt"
dir_lab = "/Users/sunxiaotan/Desktop/BIO821/ehr/LabsCorePopulatedTable.txt"

parse_patient_data(dir_patient)
parse_lab_data(dir_lab)


def test_num_older_than():
    """Test num_older_than."""
    assert (
        num_older_than(
            50.0,
            cur,
        )
        == 79
    )
    assert (
        num_older_than(
            80.0,
            cur,
        )
        == 18
    )


def test_sick_patients():
    """Test sick_patients."""
    assert sick_patients("METABOLIC: GLUCOSE", ">", 139.0, cur,) == [
        ("0BC491C5-5A45-4067-BD11-A78BEA00D3BE",),
        ("69B5D2A0-12FD-46EF-A5FF-B29C4BAFBE49",),
        ("B3892204-880B-40EF-B3BB-B824B50E99E5",),
        ("A0A976C8-9B30-4492-B8C4-5B25095B9192",),
        ("016A590E-D093-4667-A5DA-D68EA6987D93",),
        ("C5D09468-574F-4802-B56F-DB38F4EB1687",),
        ("EA7C2F0F-DA1C-4CE8-9700-4BB1FC7AF3FB",),
        ("35FE7491-1A1D-48CB-810C-8DC2599AB3DD",),
        ("714823AF-C52C-414C-B53B-C43EACD194C3",),
        ("3231F930-2978-4F50-8234-755449851E7B",),
        ("EEAFC0B3-B835-4D99-AB33-2F9428E54E5F",),
        ("36775002-9EC3-4889-AD4F-80DC6855C8D8",),
        ("4C201C71-CCED-40D1-9642-F9C8C485B854",),
        ("80AC01B2-BD55-4BE0-A59A-4024104CF4E9",),
        ("DCE5AEB8-6DB9-4106-8AE4-02CCC5C23741",),
        ("66154E24-D3EE-4311-89DB-6195278F9B3C",),
        ("FE0B9B59-1927-45B7-8556-E079DC1DE30A",),
        ("7A7332AD-88B1-4848-9356-E5260E477C59",),
        ("8AF47463-8534-4203-B210-C2290F6CE689",),
        ("65A7FBE0-EA9F-49E9-9824-D8F3AD98DAC0",),
        ("6E70D84D-C75F-477C-BC37-9177C3698C66",),
        ("C60FE675-CA52-4C55-A233-F4B27E94987F",),
        ("B39DC5AC-E003-4E6A-91B6-FC07625A1285",),
        ("1A40AF35-C6D4-4D46-B475-A15D84E8A9D5",),
        ("C54B5AAD-98E8-472D-BAA0-638D9F3BD024",),
        ("D8B53AA2-7953-4477-9EA4-68400EBAAC5C",),
        ("25B786AF-0F99-478C-9CFA-0EA607E45834",),
        ("F00C64F8-2033-4640-80FE-F1F62CBE26A5",),
        ("F0B53A2C-98CA-415D-B928-E3FD0E52B22A",),
    ]
    assert (
        sick_patients(
            "METABOLIC: GLUCOSE",
            ">",
            140.0,
            cur,
        )
        == []
    )


def test_first_admission():
    """Test first_admission."""
    assert (
        first_admission(
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "METABOLIC: GLUCOSE",
            cur,
        )
        == 20
    )

