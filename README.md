# Getting Started with tableau-migration
This project focuses on automating conversion of Tableau to Power BI

## Prerequisite
- python3.11 (3.8 and above is fine but if compatibility issue use this version)
- Installed required libraries (instruction can be found [in](#instruction-to-run))

## Required Libraries (recommended version)
- beautifulsoup4 v4.11.2
- bidict v0.22.1
- colorama==0.4.6
- et-xmlfile v1.1.0
- numpy v1.24.2
- openpyxl v3.1.1
- pandas v1.5.3
- python-dateutil v2.8.2
- pytz v2022.7.1
- six v1.16.0
- soupsieve v2.4
- tqdm==4.65.0

## Instruction to run
In the project directory, you can run:

**`python3 -m venv venv`** to create virtual environment

**`venv\Scripts\pip.exe install -r requirements.txt`** to install required packages into virtual environment

**`venv\Scripts\python.exe parse_twb_tds_NEW_SPLIT.py`** to run script with virtual environment's python

**`python3 parse_twb_tds_NEW_SPLIT.py`** to run script

**`pip install -r requirements.txt`** to install required packages

## Configuration
Specify input and output paths in [config.py](config.py)