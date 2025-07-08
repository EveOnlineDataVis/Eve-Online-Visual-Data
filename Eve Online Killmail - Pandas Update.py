import pandas as pd
import json
import os
from pathlib import Path
from typing import Dict, Optional, List

def load_ship_data(shiplist_csv_path: str) -> Dict[int, Dict[str, str]]:
    """
    Load ship data from CSV using pandas for better performance.
    Returns a dictionary with ship_type_id as key and ship info as value.
    """
    try:
        # Read CSV and handle potential encoding issues
        df = pd.read_csv(shiplist_csv_path, encoding='utf-8')
        
        # Print columns for debugging
        print(f"Ship CSV columns: {df.columns.tolist()}")
        
        # Handle different possible column structures
        if len(df.columns) >= 3:
            # Assume first 3 columns are ID, name, type
            df.columns = ['ship_id', 'ship_name', 'ship_type'] + list(df.columns[3:])
        else:
            print(f"Warning: Expected at least 3 columns in ship CSV, got {len(df.columns)}")
            return {}
        
        # Convert to dictionary for fast lookups
        ship_data = {}
        for _, row in df.iterrows():
            try:
                ship_id = int(row['ship_id'])
                ship_data[ship_id] = {
                    'name': str(row['ship_name']),
                    'type': str(row['ship_type'])
                }
            except (ValueError, TypeError):
                continue
        
        print(f"Successfully loaded {len(ship_data)} ships")
        return ship_data
        
    except Exception as e:
        print(f"Warning: Could not load ship data from {shiplist_csv_path}: {e}")
        return {}

def load_type_data(typeid_csv_path: str) -> Dict[int, str]:
    """
    Load type data from CSV using pandas.
    Returns a dictionary with type_id as key and type_name as value.
    """
    try:
        # Read CSV with flexible column detection
        df = pd.read_csv(typeid_csv_path, encoding='utf-8')
        
        print(f"Type CSV columns: {df.columns.tolist()}")
        print(f"Type CSV shape: {df.shape}")
        
        # Find the correct columns
        type_id_col = None
        type_name_col = None
        
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['typeid', 'type_id', 'id']:
                type_id_col = col
            elif col_lower in ['typename', 'type_name', 'name']:
                type_name_col = col
        
        # If not found, use first two columns
        if type_id_col is None or type_name_col is None:
            print("Using first two columns as ID and name")
            type_id_col = df.columns[0]
            type_name_col = df.columns[1]
        
        print(f"Using '{type_id_col}' for type ID and '{type_name_col}' for type name")
        
        # Clean and convert data
        df_clean = df[[type_id_col, type_name_col]].dropna()
        df_clean[type_id_col] = pd.to_numeric(df_clean[type_id_col], errors='coerce')
        df_clean = df_clean.dropna()
        
        # Convert to dictionary
        type_data = dict(zip(df_clean[type_id_col].astype(int), df_clean[type_name_col].astype(str)))
        
        print(f"Successfully loaded {len(type_data)} type mappings")
        
        # Show sample
        if type_data:
            print("Sample type mappings:")
            for i, (type_id, type_name) in enumerate(list(type_data.items())[:5]):
                print(f"  {type_id}: {type_name}")
        
        return type_data
        
    except Exception as e:
        print(f"Warning: Could not load type data from {typeid_csv_path}: {e}")
        return {}

def load_solar_system_data(map_solar_systems_csv_path: str) -> Dict[int, str]:
    """
    Load solar system data from CSV using pandas.
    Returns a dictionary with solarSystemID as key and solarSystemName as value.
    """
    try:
        # Read CSV with flexible column detection
        df = pd.read_csv(map_solar_systems_csv_path, encoding='utf-8')
        
        print(f"Solar system CSV columns: {df.columns.tolist()}")
        print(f"Solar system CSV shape: {df.shape}")
        
        # Find the correct columns
        system_id_col = None
        system_name_col = None
        
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['solarsystemid', 'solar_system_id', 'systemid', 'system_id']:
                system_id_col = col
            elif col_lower in ['solarsystemname', 'solar_system_name', 'systemname', 'system_name']:
                system_name_col = col
        
        # If not found, try positional (based on your original code)
        if system_id_col is None or system_name_col is None:
            print("Using positional columns (index 2 and 3)")
            if len(df.columns) > 3:
                system_id_col = df.columns[2]
                system_name_col = df.columns[3]
            else:
                print("Warning: Not enough columns for positional lookup")
                return {}
        
        print(f"Using '{system_id_col}' for system ID and '{system_name_col}' for system name")
        
        # Clean and convert data
        df_clean = df[[system_id_col, system_name_col]].dropna()
        df_clean[system_id_col] = pd.to_numeric(df_clean[system_id_col], errors='coerce')
        df_clean = df_clean.dropna()
        
        # Convert to dictionary
        solar_system_data = dict(zip(df_clean[system_id_col].astype(int), df_clean[system_name_col].astype(str)))
        
        print(f"Successfully loaded {len(solar_system_data)} solar system mappings")
        
        # Show sample
        if solar_system_data:
            print("Sample solar system mappings:")
            for i, (system_id, system_name) in enumerate(list(solar_system_data.items())[:5]):
                print(f"  {system_id}: {system_name}")
        
        return solar_system_data
        
    except Exception as e:
        print(f"Warning: Could not load solar system data from {map_solar_systems_csv_path}: {e}")
        return {}

def flatten_killmail(data: dict, ship_data: Optional[Dict] = None, 
                    type_data: Optional[Dict] = None, 
                    solar_system_data: Optional[Dict] = None) -> dict:
    """
    Flatten the nested killmail JSON structure into a single row dictionary.
    Optimized version with better null handling.
    """
    # Initialize with all possible fields to ensure consistent DataFrame structure
    flattened = {
        # Basic killmail info
        'killmail_id': data.get('killmail_id'),
        'killmail_time': data.get('killmail_time'),
        'solar_system_id': data.get('solar_system_id'),
        'killmail_hash': data.get('killmail_hash'),
        'http_last_modified': data.get('http_last_modified'),
        'solar_system_name': None,
        
        # Victim information
        'victim_alliance_id': None,
        'victim_character_id': None,
        'victim_corporation_id': None,
        'victim_damage_taken': None,
        'victim_ship_type_id': None,
        'victim_ship_name': None,
        'victim_ship_type': None,
        'victim_position_x': None,
        'victim_position_y': None,
        'victim_position_z': None,
        
        # Attacker information
        'attacker_alliance_id': None,
        'attacker_character_id': None,
        'attacker_corporation_id': None,
        'attacker_damage_done': None,
        'attacker_final_blow': None,
        'attacker_security_status': None,
        'attacker_ship_type_id': None,
        'attacker_ship_name': None,
        'attacker_ship_type': None,
        'attacker_weapon_type_id': None,
        'attacker_weapon_type_name': None,
        
        # Counts
        'total_attackers': 0,
        'total_items': 0,
        'items_destroyed': 0,
        'items_dropped': 0,
    }
    
    # Add solar system name
    if solar_system_data and flattened['solar_system_id']:
        flattened['solar_system_name'] = solar_system_data.get(flattened['solar_system_id'])
    
    # Victim information
    victim = data.get('victim', {})
    flattened.update({
        'victim_alliance_id': victim.get('alliance_id'),
        'victim_character_id': victim.get('character_id'),
        'victim_corporation_id': victim.get('corporation_id'),
        'victim_damage_taken': victim.get('damage_taken'),
        'victim_ship_type_id': victim.get('ship_type_id'),
    })
    
    # Victim ship info
    if ship_data and flattened['victim_ship_type_id']:
        ship_info = ship_data.get(flattened['victim_ship_type_id'])
        if ship_info:
            flattened['victim_ship_name'] = ship_info['name']
            flattened['victim_ship_type'] = ship_info['type']
    
    # Victim position
    position = victim.get('position', {})
    flattened.update({
        'victim_position_x': position.get('x'),
        'victim_position_y': position.get('y'),
        'victim_position_z': position.get('z'),
    })
    
    # Attacker information
    attackers = data.get('attackers', [])
    flattened['total_attackers'] = len(attackers)
    
    if attackers:
        # Find final blow attacker or use first one
        final_blow_attacker = next((att for att in attackers if att.get('final_blow')), attackers[0])
        
        flattened.update({
            'attacker_alliance_id': final_blow_attacker.get('alliance_id'),
            'attacker_character_id': final_blow_attacker.get('character_id'),
            'attacker_corporation_id': final_blow_attacker.get('corporation_id'),
            'attacker_damage_done': final_blow_attacker.get('damage_done'),
            'attacker_final_blow': final_blow_attacker.get('final_blow'),
            'attacker_security_status': final_blow_attacker.get('security_status'),
            'attacker_ship_type_id': final_blow_attacker.get('ship_type_id'),
            'attacker_weapon_type_id': final_blow_attacker.get('weapon_type_id'),
        })
        
        # Attacker ship info
        if ship_data and flattened['attacker_ship_type_id']:
            ship_info = ship_data.get(flattened['attacker_ship_type_id'])
            if ship_info:
                flattened['attacker_ship_name'] = ship_info['name']
                flattened['attacker_ship_type'] = ship_info['type']
        
        # Attacker weapon info
        if type_data and flattened['attacker_weapon_type_id']:
            flattened['attacker_weapon_type_name'] = type_data.get(flattened['attacker_weapon_type_id'])
    
    # Items information
    items = victim.get('items', [])
    flattened.update({
        'total_items': len(items),
        'items_destroyed': sum(1 for item in items if 'quantity_destroyed' in item),
        'items_dropped': sum(1 for item in items if 'quantity_dropped' in item),
    })
    
    return flattened

def convert_json_folder_to_csv_pandas(input_folder: str, output_csv: str = 'killmails.csv', 
                                    shiplist_csv: Optional[str] = None, 
                                    typeid_csv: Optional[str] = None, 
                                    map_solar_systems_csv: Optional[str] = None) -> None:
    """
    Convert all JSON files in a folder to a single CSV file using pandas for optimization.
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return
    
    print("Loading lookup data...")
    
    # Load lookup data
    ship_data = load_ship_data(shiplist_csv) if shiplist_csv else {}
    type_data = load_type_data(typeid_csv) if typeid_csv else {}
    solar_system_data = load_solar_system_data(map_solar_systems_csv) if map_solar_systems_csv else {}
    
    # Find all JSON files
    json_files = list(input_path.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in '{input_folder}'.")
        return
    
    print(f"Found {len(json_files)} JSON files to process...")
    
    # Process files in batches for better memory management
    batch_size = 1000
    all_data = []
    errors = []
    
    for i in range(0, len(json_files), batch_size):
        batch_files = json_files[i:i+batch_size]
        batch_data = []
        
        print(f"Processing batch {i//batch_size + 1}/{(len(json_files)-1)//batch_size + 1} ({len(batch_files)} files)...")
        
        for json_file in batch_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    flattened = flatten_killmail(data, ship_data, type_data, solar_system_data)
                    flattened['source_file'] = json_file.name
                    batch_data.append(flattened)
                    
            except json.JSONDecodeError as e:
                errors.append(f"JSON decode error in {json_file.name}: {e}")
            except Exception as e:
                errors.append(f"Error processing {json_file.name}: {e}")
        
        all_data.extend(batch_data)
    
    if not all_data:
        print("No valid data found to convert.")
        return
    
    # Convert to DataFrame for efficient processing
    print("Converting to DataFrame...")
    df = pd.DataFrame(all_data)
    
    # Optimize data types for better performance and smaller file size
    print("Optimizing data types...")
    
    # Convert integer columns
    int_columns = ['killmail_id', 'solar_system_id', 'victim_alliance_id', 'victim_character_id', 
                  'victim_corporation_id', 'victim_damage_taken', 'victim_ship_type_id',
                  'attacker_alliance_id', 'attacker_character_id', 'attacker_corporation_id',
                  'attacker_damage_done', 'attacker_ship_type_id', 'attacker_weapon_type_id',
                  'total_attackers', 'total_items', 'items_destroyed', 'items_dropped']
    
    for col in int_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
    
    # Convert float columns
    float_columns = ['victim_position_x', 'victim_position_y', 'victim_position_z', 'attacker_security_status']
    for col in float_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce', downcast='float')
    
    # Convert boolean columns
    bool_columns = ['attacker_final_blow']
    for col in bool_columns:
        if col in df.columns:
            df[col] = df[col].astype('boolean')
    
    # Write to CSV
    print(f"Writing {len(df)} records to CSV...")
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    print(f"Successfully converted {len(df)} records to '{output_csv}'")
    
    # Statistics
    print("\n=== STATISTICS ===")
    print(f"Total records: {len(df)}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Lookup statistics
    if ship_data:
        victim_ships_matched = df['victim_ship_name'].notna().sum()
        attacker_ships_matched = df['attacker_ship_name'].notna().sum()
        print(f"Ship name matches: {victim_ships_matched} victims, {attacker_ships_matched} attackers")
    
    if type_data:
        weapons_matched = df['attacker_weapon_type_name'].notna().sum()
        total_weapons = df['attacker_weapon_type_id'].notna().sum()
        print(f"Weapon type matches: {weapons_matched}/{total_weapons}")
    
    if solar_system_data:
        systems_matched = df['solar_system_name'].notna().sum()
        total_systems = df['solar_system_id'].notna().sum()
        print(f"Solar system matches: {systems_matched}/{total_systems}")
    
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")

# Example usage
if __name__ == "__main__":
    # Configuration
    INPUT_FOLDER = r"C:\Users\kyleh\Downloads\killmails-2025-07-06\killmails"
    OUTPUT_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\killmails-07-06-25-PANDAS.csv"
    SHIPLIST_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\shiplist.csv"
    TYPEID_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\typeid.csv"
    MAP_SOLAR_SYSTEMS_CSV = r"C:\Users\kyleh\OneDrive\Desktop\Professional Projects\Dashboards\Datasets\Eve-Online Killmails\mapSolarSystems.csv"
    
    # Convert files
    convert_json_folder_to_csv_pandas(
        input_folder=INPUT_FOLDER,
        output_csv=OUTPUT_CSV,
        shiplist_csv=SHIPLIST_CSV,
        typeid_csv=TYPEID_CSV,
        map_solar_systems_csv=MAP_SOLAR_SYSTEMS_CSV
    )