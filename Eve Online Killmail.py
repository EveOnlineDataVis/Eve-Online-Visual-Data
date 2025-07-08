import json
import csv
import os
from pathlib import Path

def load_ship_data(shiplist_csv_path):
    """
    Load ship data from the CSV file into a dictionary for quick lookups.
    Returns a dictionary with ship_type_id as key and ship info as value.
    """
    ship_data = {}
    
    try:
        with open(shiplist_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    ship_id = int(row[0])
                    ship_name = row[1]
                    ship_type = row[2]
                    ship_data[ship_id] = {
                        'name': ship_name,
                        'type': ship_type
                    }
    except Exception as e:
        print(f"Warning: Could not load ship data from {shiplist_csv_path}: {e}")
        print("Ship names and types will not be included in the output.")
    
    return ship_data

def load_solar_system_data(map_solar_systems_csv_path):
    """
    Load solar system data from the mapSolarSystems.csv file into a dictionary for quick lookups.
    Returns a dictionary with solarSystemID as key and solarSystemName as value.
    """
    solar_system_data = {}
    
    try:
        with open(map_solar_systems_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Read the header row
            
            if header:
                print(f"Solar Systems CSV header: {header}")
                # Try to find the correct column indices
                system_id_col = None
                system_name_col = None
                
                for i, col in enumerate(header):
                    col_lower = col.lower().strip()
                    if col_lower in ['solarsystemid', 'solar_system_id', 'systemid', 'system_id']:
                        system_id_col = i
                    elif col_lower in ['solarsystemname', 'solar_system_name', 'systemname', 'system_name']:
                        system_name_col = i
                
                if system_id_col is None or system_name_col is None:
                    print(f"Warning: Could not find required columns. Trying default positions...")
                    # Based on your sample, solarSystemID is column 2, solarSystemName is column 3
                    system_id_col = 2
                    system_name_col = 3
                
                print(f"Using column {system_id_col} for solar system ID and column {system_name_col} for solar system name")
            else:
                # No header, assume positions based on your sample
                system_id_col = 2
                system_name_col = 3
                print("No header found, using positions 2 and 3 for ID and name")
            
            for row_num, row in enumerate(reader, 2):  # Start at 2 since we already read header
                if len(row) > max(system_id_col, system_name_col):
                    try:
                        system_id = int(row[system_id_col])
                        system_name = row[system_name_col].strip()  # Remove any extra whitespace
                        solar_system_data[system_id] = system_name
                    except (ValueError, IndexError):
                        # Skip rows that don't have valid integer ID or missing name
                        continue
                elif len(row) > 0:  # Skip empty rows but warn about insufficient columns
                    print(f"Warning: Row {row_num} has insufficient columns: {row}")
        
        print(f"Successfully loaded {len(solar_system_data)} solar system mappings")
        
        # Show a few examples of what was loaded
        if solar_system_data:
            print("Sample solar system mappings:")
            for i, (system_id, system_name) in enumerate(list(solar_system_data.items())[:5]):
                print(f"  {system_id}: {system_name}")
                
    except Exception as e:
        print(f"Warning: Could not load solar system data from {map_solar_systems_csv_path}: {e}")
        print("Solar system names will not be included in the output.")
    
    return solar_system_data

def load_type_data(typeid_csv_path):
    """
    Load type data from the typeid.csv file into a dictionary for quick lookups.
    Returns a dictionary with type_id as key and type_name as value.
    Assumes CSV format with type_id,type_name columns.
    """
    type_data = {}
    
    try:
        with open(typeid_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Read the header row
            
            if header:
                print(f"CSV header: {header}")
                # Try to find the correct column indices
                type_id_col = None
                type_name_col = None
                
                for i, col in enumerate(header):
                    col_lower = col.lower().strip()
                    if col_lower in ['typeid', 'type_id', 'id']:
                        type_id_col = i
                    elif col_lower in ['typename', 'type_name', 'name']:
                        type_name_col = i
                
                if type_id_col is None or type_name_col is None:
                    print(f"Warning: Could not find required columns. Using first two columns as default.")
                    type_id_col = 0
                    type_name_col = 1
                
                print(f"Using column {type_id_col} for type ID and column {type_name_col} for type name")
            else:
                # No header, assume first two columns
                type_id_col = 0
                type_name_col = 1
                print("No header found, using first two columns")
            
            for row_num, row in enumerate(reader, 2):  # Start at 2 since we already read header
                if len(row) > max(type_id_col, type_name_col):
                    try:
                        type_id = int(row[type_id_col])
                        type_name = row[type_name_col].strip()  # Remove any extra whitespace
                        type_data[type_id] = type_name
                    except (ValueError, IndexError):
                        # Skip rows that don't have valid integer ID or missing name
                        continue
                elif len(row) > 0:  # Skip empty rows but warn about insufficient columns
                    print(f"Warning: Row {row_num} has insufficient columns: {row}")
        
        print(f"Successfully loaded {len(type_data)} type mappings")
        
        # Show a few examples of what was loaded
        if type_data:
            print("Sample type mappings:")
            for i, (type_id, type_name) in enumerate(list(type_data.items())[:5]):
                print(f"  {type_id}: {type_name}")
                
    except Exception as e:
        print(f"Warning: Could not load type data from {typeid_csv_path}: {e}")
        print("Weapon type names will not be included in the output.")
    
    return type_data

def flatten_killmail(data, ship_data=None, type_data=None, solar_system_data=None):
    """
    Flatten the nested killmail JSON structure into a single row dictionary.
    """
    flattened = {}
    
    # Basic killmail info
    flattened['killmail_id'] = data.get('killmail_id')
    flattened['killmail_time'] = data.get('killmail_time')
    flattened['solar_system_id'] = data.get('solar_system_id')
    flattened['killmail_hash'] = data.get('killmail_hash')
    flattened['http_last_modified'] = data.get('http_last_modified')
    
    # Add solar system name from solar_system_data
    if solar_system_data and flattened['solar_system_id']:
        system_name = solar_system_data.get(flattened['solar_system_id'])
        flattened['solar_system_name'] = system_name
    else:
        flattened['solar_system_name'] = None
    
    # Victim information
    victim = data.get('victim', {})
    flattened['victim_alliance_id'] = victim.get('alliance_id')
    flattened['victim_character_id'] = victim.get('character_id')
    flattened['victim_corporation_id'] = victim.get('corporation_id')
    flattened['victim_damage_taken'] = victim.get('damage_taken')
    flattened['victim_ship_type_id'] = victim.get('ship_type_id')
    
    # Add victim ship name and type from ship_data
    if ship_data and flattened['victim_ship_type_id']:
        ship_info = ship_data.get(flattened['victim_ship_type_id'])
        if ship_info:
            flattened['victim_ship_name'] = ship_info['name']
            flattened['victim_ship_type'] = ship_info['type']
        else:
            flattened['victim_ship_name'] = None
            flattened['victim_ship_type'] = None
    else:
        flattened['victim_ship_name'] = None
        flattened['victim_ship_type'] = None
    
    # Victim position
    position = victim.get('position', {})
    flattened['victim_position_x'] = position.get('x')
    flattened['victim_position_y'] = position.get('y')
    flattened['victim_position_z'] = position.get('z')
    
    # Attacker information (taking the first/final blow attacker)
    attackers = data.get('attackers', [])
    if attackers:
        # Find the final blow attacker or use the first one
        final_blow_attacker = next((att for att in attackers if att.get('final_blow')), attackers[0])
        
        flattened['attacker_alliance_id'] = final_blow_attacker.get('alliance_id')
        flattened['attacker_character_id'] = final_blow_attacker.get('character_id')
        flattened['attacker_corporation_id'] = final_blow_attacker.get('corporation_id')
        flattened['attacker_damage_done'] = final_blow_attacker.get('damage_done')
        flattened['attacker_final_blow'] = final_blow_attacker.get('final_blow')
        flattened['attacker_security_status'] = final_blow_attacker.get('security_status')
        flattened['attacker_ship_type_id'] = final_blow_attacker.get('ship_type_id')
        flattened['attacker_weapon_type_id'] = final_blow_attacker.get('weapon_type_id')
        
        # Add attacker ship name and type from ship_data
        if ship_data and flattened['attacker_ship_type_id']:
            ship_info = ship_data.get(flattened['attacker_ship_type_id'])
            if ship_info:
                flattened['attacker_ship_name'] = ship_info['name']
                flattened['attacker_ship_type'] = ship_info['type']
            else:
                flattened['attacker_ship_name'] = None
                flattened['attacker_ship_type'] = None
        else:
            flattened['attacker_ship_name'] = None
            flattened['attacker_ship_type'] = None
        
        # Add attacker weapon type name from type_data
        if type_data and flattened['attacker_weapon_type_id']:
            weapon_name = type_data.get(flattened['attacker_weapon_type_id'])
            flattened['attacker_weapon_type_name'] = weapon_name
        else:
            flattened['attacker_weapon_type_name'] = None
    
    # Count of total attackers
    flattened['total_attackers'] = len(attackers)
    
    # Items information (summary)
    items = victim.get('items', [])
    flattened['total_items'] = len(items)
    flattened['items_destroyed'] = sum(1 for item in items if 'quantity_destroyed' in item)
    flattened['items_dropped'] = sum(1 for item in items if 'quantity_dropped' in item)
    
    return flattened

def convert_json_folder_to_csv(input_folder, output_csv='killmails.csv', shiplist_csv=None, typeid_csv=None, map_solar_systems_csv=None):
    """
    Convert all JSON files in a folder to a single CSV file.
    
    Args:
        input_folder (str): Path to folder containing JSON files
        output_csv (str): Output CSV filename
        shiplist_csv (str): Path to shiplist.csv file for ship name lookups
        typeid_csv (str): Path to typeid.csv file for type name lookups
        map_solar_systems_csv (str): Path to mapSolarSystems.csv file for solar system name lookups
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return
    
    # Load ship data if provided
    ship_data = None
    if shiplist_csv:
        ship_data = load_ship_data(shiplist_csv)
        if ship_data:
            print(f"Loaded {len(ship_data)} ships from {shiplist_csv}")
    
    # Load type data if provided
    type_data = None
    if typeid_csv:
        type_data = load_type_data(typeid_csv)
        if type_data:
            print(f"Loaded {len(type_data)} types from {typeid_csv}")
        else:
            print("No type data loaded - weapon type names will be empty")
    
    # Load solar system data if provided
    solar_system_data = None
    if map_solar_systems_csv:
        solar_system_data = load_solar_system_data(map_solar_systems_csv)
        if solar_system_data:
            print(f"Loaded {len(solar_system_data)} solar systems from {map_solar_systems_csv}")
        else:
            print("No solar system data loaded - solar system names will be empty")
    
    # Find all JSON files
    json_files = list(input_path.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in '{input_folder}'.")
        return
    
    print(f"Found {len(json_files)} JSON files to process...")
    
    all_data = []
    errors = []
    
    # Process each JSON file
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                flattened = flatten_killmail(data, ship_data, type_data, solar_system_data)
                flattened['source_file'] = json_file.name  # Add source filename
                all_data.append(flattened)
                
        except json.JSONDecodeError as e:
            errors.append(f"JSON decode error in {json_file.name}: {e}")
        except Exception as e:
            errors.append(f"Error processing {json_file.name}: {e}")
    
    if not all_data:
        print("No valid data found to convert.")
        return
    
    # Get all unique column names
    all_columns = set()
    for row in all_data:
        all_columns.update(row.keys())
    
    # Sort columns for consistent output
    columns = sorted(all_columns)
    
    # Write to CSV
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"Successfully converted {len(all_data)} records to '{output_csv}'")
        
        # Show some statistics about weapon type matching
        if type_data:
            weapon_ids_found = sum(1 for row in all_data if row.get('attacker_weapon_type_id') is not None)
            weapon_names_found = sum(1 for row in all_data if row.get('attacker_weapon_type_name') is not None)
            print(f"Weapon type matching: {weapon_names_found} out of {weapon_ids_found} weapon IDs matched to names")
            
            # Show some examples
            sample_matches = [(row.get('attacker_weapon_type_id'), row.get('attacker_weapon_type_name')) 
                             for row in all_data if row.get('attacker_weapon_type_name') is not None][:5]
            if sample_matches:
                print("Sample weapon matches:")
                for weapon_id, weapon_name in sample_matches:
                    print(f"  ID {weapon_id}: {weapon_name}")
        
        # Show some statistics about solar system matching
        if solar_system_data:
            system_ids_found = sum(1 for row in all_data if row.get('solar_system_id') is not None)
            system_names_found = sum(1 for row in all_data if row.get('solar_system_name') is not None)
            print(f"Solar system matching: {system_names_found} out of {system_ids_found} solar system IDs matched to names")
            
            # Show some examples
            sample_matches = [(row.get('solar_system_id'), row.get('solar_system_name')) 
                             for row in all_data if row.get('solar_system_name') is not None][:5]
            if sample_matches:
                print("Sample solar system matches:")
                for system_id, system_name in sample_matches:
                    print(f"  ID {system_id}: {system_name}")
        
        if errors:
            print(f"\nErrors encountered:")
            for error in errors:
                print(f"  - {error}")
                
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# Example usage
if __name__ == "__main__":
    # Configuration - Fixed Windows paths
    INPUT_FOLDER = r"C:\Users\kyleh\Downloads\killmails-2025-07-07\killmails"
    OUTPUT_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\killmails-07-07-25.csv"
    SHIPLIST_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\shiplist.csv"
    TYPEID_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\typeid.csv"
    MAP_SOLAR_SYSTEMS_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\mapSolarSystems.csv"
    
    # Convert files with ship name lookups, weapon type lookups, and solar system lookups
    convert_json_folder_to_csv(INPUT_FOLDER, OUTPUT_CSV, SHIPLIST_CSV, TYPEID_CSV, MAP_SOLAR_SYSTEMS_CSV)