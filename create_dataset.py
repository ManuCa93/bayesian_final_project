# 1. Standard library imports
import glob
import os

# 2. Third-party imports
import pandas as pd

# Load stations data (with longi, lat and alti)
stations = pd.read_csv('ticino_stations.csv')

# Directory with temperature data
temperature_dir = './temperature_bayesian'

# Get all CSV files
csv_files = sorted(glob.glob(os.path.join(temperature_dir, '*.csv')))

all_data = []

# Process each temperature CSV file
for csv_file in csv_files:
    # Extract station name from filename
    filename = os.path.basename(csv_file)
    station_name = filename.replace('.csv', '')
    
    # Handle underscore naming conventions
    if '_' in station_name:
        station_name = station_name.replace('_', ' ').title()
    else:
        station_name = station_name.capitalize()
    
    # Fix special cases to match ticino_stations.csv
    station_mapping = {
        'S Bernardino': 'San_Bernardino',
        'S Vittore': 'Sant_Vittore',
        'Delpe Aple': 'Delpe_Aple',
        'Valle Maggia': 'Valle_Maggia',
        'Piotta': 'Piota',
        'Moleno': 'Moleno',
        'Chironico': 'Chirnico'
    }
    
    for key, value in station_mapping.items():
        if key in station_name or station_name.lower() == key.lower().replace(' ', ''):
            station_name = value
            break
    
    try:
        # Read CSV, skipping comment lines (all lines starting with #)
        temp_data = pd.read_csv(
            csv_file, 
            sep=';', 
            comment='#',
            encoding='latin-1',
            dtype={'T': float}
        )
        
        # Remove the trailing semicolon empty column if it exists
        temp_data = temp_data.iloc[:, :3]
        
        # Rename columns
        temp_data.columns = ['date', 'temperature', 'provisional_flag']
        
        # Parse date
        temp_data['date'] = pd.to_datetime(temp_data['date'], format='%d.%m.%Y %H:%M:%S')
        
        # Extract year and month
        temp_data['year'] = temp_data['date'].dt.year
        temp_data['month'] = temp_data['date'].dt.month
        
        # Filter 2025 data only
        temp_data_2025 = temp_data[temp_data['year'] == 2025].copy()
        
        # Keep only relevant columns
        temp_data_2025 = temp_data_2025[['year', 'month', 'temperature']].reset_index(drop=True)
        
        # Add station name
        temp_data_2025.insert(0, 'station', station_name)
        
        all_data.append(temp_data_2025)
        
        print(f"DONE Processed {station_name} ({len(temp_data_2025)} records)")
        
    except Exception as e:
        print(f"!NOT DONE Error processing {filename}: {e}")
        import traceback
        traceback.print_exc()


if all_data:
    # Combine all data
    df_merged = pd.concat(all_data, ignore_index=True)

    # Merge with stations data
    df_final = df_merged.merge(
        stations,
        left_on='station',
        right_on='STAZIONE',
        how='left'
    )

    # Select and organize columns
    df_final = df_final[['station', 'year', 'month', 'temperature', 'LATITUDINE', 'LONGITUDINE', 'ALTITUDINE']]

    # Rename for clarity
    df_final.columns = ['station', 'year', 'month', 'temperature', 'latitude', 'longitude', 'altitude']

    # Add season flag (0=Winter, 1=Spring, 2=Summer, 3=Autumn)
    def get_season(month):
        if month in [12, 1, 2]:
            return 0  # Winter
        elif month in [3, 4, 5]:
            return 1  # Spring
        elif month in [6, 7, 8]:
            return 2  # Summer
        else:  # 9, 10, 11
            return 3  # Autumn
    
    df_final['season'] = df_final['month'].apply(get_season)

    # Drop rows with missing values
    df_final = df_final.dropna()

    # Sort by station and month
    df_final = df_final.sort_values(['station', 'month']).reset_index(drop=True)

    # Save the final dataset
    df_final.to_csv('ticino_temperature_2025.csv', index=False)

    # Print summary
    print("\n" + "="*70)
    print("DATASET CREATED SUCCESSFULLY!")
    print("="*70)
    print(f"Shape: {df_final.shape}")
    print(f"Stations: {df_final['station'].nunique()}")
    print(f"Total records: {len(df_final)}")
    print(f"Temperature range: {df_final['temperature'].min():.1f}°C to {df_final['temperature'].max():.1f}°C")
    print(f"Altitude range: {df_final['altitude'].min():.0f}m to {df_final['altitude'].max():.0f}m")
    print(f"\nSeason mapping: 0=Winter, 1=Spring, 2=Summer, 3=Autumn")
    print(f"\nFirst 5 rows:\n{df_final.head(5).to_string()}")
    print(f"\nLast 5 rows:\n{df_final.tail().to_string()}")
    print(f"\nSaved to: ticino_temperature_2025.csv")
else:
    print("!PROBLEMS PROBLEMS! No data processed!")