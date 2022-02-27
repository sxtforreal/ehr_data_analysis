### For end user:
## Setup/installation instructions:
$ git clone https://github.com/sxtforreal/ehr_analysis.git
$ cd ../path/to/the/file 

## The expected input file formats
* parse_data() takes text files with the first row as variable names as input.
* Remaining functions takes the output of parse_data as input.

## API description:
This repo contains modules working with electronic health record data.
** Defined classes:
* class:Patient has 
        6 instance attributes: ID, gender, DOB, race, marital, language, PPPBP
        1 property: Age
* class:Lab has 
        5 instance attributes: PatientID, Admission, Name, Value, Units, Time
        1 method: visit_age
** Defined functions:
* parse_data() parse the input ehr text file into a list of class:Patient or class:Lab.
* num_older_than() takes a list of class:Patient and return the number of patients older than a given age (in years).
* sick_patients() take a list of class:Lab and return a unique list of patients who have a given test with value above (">") or below ("<") a given level.
* first_admission() take a list of class:Patient, a list of class:Lab and computes the age at first admission of any given patient id and lab name.

## Examples:
* A = parse_data('/Users/sunxiaotan/Desktop/BIO821/ehr/PatientCorePopulatedTable.txt', 'patient')
* B = parse_data('/Users/sunxiaotan/Desktop/BIO821/ehr/LabsCorePopulatedTable.txt', 'lab')
* num_older_than(50, A) -> 3
* sick_patients("METABOLIC: GLUCOSE", ">", 103.0, B) -> ["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"]       
* first_admission(B, A, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "METABOLIC: GLUCOSE") -> 44


### For contributor:
## Testing instructions:
* Test: pytest test_ehr_analysis.py
* Coverage: pytest --cov=..
