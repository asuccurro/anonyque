# Create unique IDs for users and perform checks for unique entries

Code to be used for different scenarios.

## Setup

```bash 
virtualenv -p /usr/bin/python3 venvpy3
source venvpy3/bin/activate
pip install -r requirements.txt
```

## Usage


### Generate
	
This example uses the `input/test.csv` file (with fields "Nome", "Cognome", "email") as input to associate a unique ID to each email address. The arguments passed here below are the defaults:
	
```bash
python anonyque.py --key 'email' --delimiter ',' --infilename '../input/test.csv' --generate
```

This run generates three files:

1. `test_wIDs.csv`: csv file identical to the input csv, plus a column with the unique IDs
2. `test_uniqueIDs.json`: json file containing the list of unique IDs
3. `test_dict.json`: json file containing the dictionary with emails as keys and IDs as values


### Check

This example uses the `output/example_validIDs.json` (as example of valid IDs, generated at the "generate" step) and the file `input/filedids.csv` (as example of IDs collected through a survey / form).

```bash
python anonyque.py --check --infilename '../input/filedids.csv' --jsonfilename '../output/example_validIDs.json' --key 'UniqueID'
```

The results printed on screen are:

```bash
These IDs have multiple entries: zbm09u
These IDs are *not* valid: h48433
These IDs are valid and missing in the input: 0dqq83, txdsrf
```

Meaning that a user completed more than once the survey (zbm09u), one user used an invalid ID (h48433) and two users did not complete the survey.

## Use case: Online anonymous, unique votes

Needs two independent people, A and B

1. *A* generates from file `X.csv` the files `X_wIDs.csv` and `X_uniqueIDs.json`
2. *A* uses a mail merge program (e.g. Outlook, LibreOffice) to send to the emails in `X_wIDs.csv` their corresponding unique code
3. *A* sends to *B* the file `X_uniqueIDs.json`
4. *B* creates a form online (e.g. Google Forms) with a field to enter the unique code and the questions to be answered / votes to be casted
5. *B* collects form inputs
6. *B* gets the list of codes entered in the survey and cross-checks with the `X_uniqueIDs.json`. If duplicates or invalid entries are found, *B* removes the faulty survey entries

	
## Use case: Online unique completion of surveys

