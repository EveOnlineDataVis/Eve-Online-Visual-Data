Update Log:

Killmail Dashboard for July 5, 2025: https://public.tableau.com/app/profile/eve.online.daily.data/viz/Killmails07-05-25/Dashboard1#1 

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

---
