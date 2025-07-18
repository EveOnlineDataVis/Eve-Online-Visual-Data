What is this?

https://www.eveonline.com/ 

Update Log:

PvP Metrics for June, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/PvPForJune2025/PvPMetricsforJune2025 

Killmail Dashboard for July 17, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-17-25/Dashboard1

Killmail Dashboard for July 16, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-16-25/Dashboard1

Killmail Dashboard for July 15, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-15-25/Dashboard1

Killmail Dashboard for July 14, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-14-25/Dashboard1

Killmail Dashboard for July 13, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-13-25/Dashboard1

Killmail Dashboard for July 12, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-12-25/Dashboard1

Killmail Dashboard for July 11, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-11-25/Dashboard1?publish=yes

Killmail Dashboard for July 10, 2025: [https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-09-25/Dashboard1?publish=yes](https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-10-25/Dashboard1)

Killmail Dashboard for July 9, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-09-25/Dashboard1?publish=yes

Killmail Dashboard for July 8, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-08-25/Dashboard1?publish=yes

Killmail Dashboard for July 7, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-07-25/Dashboard1?publish=yes

Killmail Dashboard for July 6, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-06-25/Dashboard1?publish=yes

Killmail Dashboard for July 5, 2025: [https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-05-25/Dashboard1#1](https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-05-25/KillMailDashboard)

Killmail Dashboard for July 4, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-04-25/KillMailDashboard

System Jumps for July 5, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/SystemJumps7-5-25/SystemJumpsDashboard

------------------------------------------------------------------------------------------------------------------

# Eve Online Killmail JSON Conversion

A Python utility to convert Eve Online killmail JSON files into a single, analysis-ready CSV file. The script enriches killmail data with ship names, weapon type names, and solar system names using reference CSV files.

---

## Features

- **Batch Conversion:** Converts all killmail JSON files in a folder to a single CSV.
- **Data Enrichment:** Adds ship names/types, weapon type names, and solar system names using lookup tables.
- **Flexible Lookups:** Works with customizable CSVs for ships, weapon types, and solar systems.
- **Robust Parsing:** Handles missing or malformed data gracefully and provides detailed logs.
- **Extensible:** Easily add more enrichments or output fields as needed.

---

## Input Requirements

- **Killmail JSON files:** Each file should contain a single killmail in Eve Online’s JSON format.
- **shiplist.csv:** Maps ship type IDs to ship names and types.
- **typeid.csv:** Maps weapon type IDs to weapon names.
- **mapSolarSystems.csv:** Maps solar system IDs to solar system names.

---

## Usage

### 1. Install Dependencies

```bash
pip install python-dateutil
```
*(Standard library modules are used for everything else.)*

### 2. Prepare Your Data

- Place all killmail JSON files in a folder (e.g., `killmails/`).
- Prepare `shiplist.csv`, `typeid.csv`, and `mapSolarSystems.csv` in the same or a known directory.

### 3. Run the Script

Edit the configuration section at the bottom of the script to point to your data files:

```python
INPUT_FOLDER = r"C:\path\to\killmails"
OUTPUT_CSV = r"C:\path\to\output\killmails.csv"
SHIPLIST_CSV = r"C:\path\to\shiplist.csv"
TYPEID_CSV = r"C:\path\to\typeid.csv"
MAP_SOLAR_SYSTEMS_CSV = r"C:\path\to\mapSolarSystems.csv"
```

Then run:

```bash
python "Eve Online Killmail.py"
```

### 4. Output

- The script will generate a CSV file with one row per killmail, including enriched columns such as `attacker_weapon_type_name`, `victim_ship_name`, and `solar_system_name`.

---

## Example Output Columns

- `killmail_id`
- `killmail_time`
- `solar_system_id`
- `solar_system_name`
- `victim_ship_type_id`
- `victim_ship_name`
- `attacker_weapon_type_id`
- `attacker_weapon_type_name`
- ...and more

---

## Customization

- Add or modify enrichment logic in `flatten_killmail` to include more fields.
- Update lookup CSVs as Eve Online data changes.

------------------------------------------------------------------------------------------------------------------

# EVE Online System Jumps Converter

A Python utility to convert EVE Online system jump data from JSON format to CSV format with system name mapping.

## Description

This tool converts EVE Online system jump data that comes in JSON format into a more readable CSV format. It automatically maps system IDs to their corresponding system names using the EVE Online static data export (SDE) solar systems mapping file.

## Features

- Parses JSON arrays containing ship jump data
- Handles both complete and incomplete JSON files
- Maps system IDs to human-readable system names
- Exports clean CSV format with system names
- Provides detailed error reporting and missing system warnings
- Robust error handling for malformed JSON data

## Requirements

- Python 3.6 or higher
- pandas library

## Installation

2. Install required dependencies:
```bash
pip install pandas
```

## Usage

### Basic Usage

1. Update the file paths in the script:
   - `json_file_path`: Path to your system jumps JSON file
   - `csv_mapping_path`: Path to your `mapSolarSystems.csv` file
   - `output_csv_path`: Desired output location for the converted CSV

2. Run the script:
```bash
python json_to_csv_converter.py
```

### Input Format

The tool expects JSON input in the following format:
```json
[
  {"ship_jumps":15,"system_id":30002808},
  {"ship_jumps":9,"system_id":30002006},
  {"ship_jumps":24,"system_id":30000751}
]
```

### Output Format

The tool generates a CSV file with the following columns:
- `system_id`: The original system ID
- `system_name`: The mapped system name from the SDE data
- `ship_jumps`: Number of ship jumps recorded

Example output:
```csv
system_id,system_name,ship_jumps
30002808,Rancer,15
30002006,Rancer,9
30000751,Hek,24
```

## Required Files

### System Jumps JSON File
Your main data file containing the jump statistics. The file should contain a JSON array of objects with `ship_jumps` and `system_id` fields.

### mapSolarSystems.csv
This file should contain the EVE Online static data export for solar systems. The tool specifically uses:
- `solarSystemID`: System identifier
- `solarSystemName`: Human-readable system name

You can obtain this file from the EVE Online Static Data Export (SDE) available from CCP Games.

## Error Handling

The tool includes comprehensive error handling:
- **Incomplete JSON**: Automatically attempts to repair truncated JSON files
- **Missing Systems**: Reports any system IDs that couldn't be found in the mapping file
- **File Access**: Provides clear error messages for file reading issues
- **Data Validation**: Validates JSON structure and data types

## Configuration

You can customize the following variables in the script:
```python
json_file_path = "system-jumps-latest.json"  # Your input JSON file
csv_mapping_path = "path/to/mapSolarSystems.csv"  # Your SDE mapping file
output_csv_path = "system-jumps-converted.csv"  # Output file location
```

## Example

```bash
$ python json_to_csv_converter.py
Parsing JSON file...
Raw content preview: [{"ship_jumps":15,"system_id":30002808},{"ship_jumps":9,"system_id":30002006}...
Successfully parsed 1247 records
First record example: {'ship_jumps': 15, 'system_id': 30002808}
Loading system mapping...
Loaded 8285 system mappings
Writing to system-jumps-converted.csv...
Successfully converted 1247 records to CSV

Conversion complete!
Output file: system-jumps-converted.csv
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is not affiliated with CCP Games or EVE Online. EVE Online is a trademark of CCP Games.
