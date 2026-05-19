#!/usr/bin/env python
"""
Convert LS4 field grid CSV to ZTF_Fields.txt format
"""
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# Read LS4 field grid
ls4_csv = pd.read_csv('data/LS4_field_grid.csv')

# Create field_id: using sequential numbering starting from 1
# You could also use the Field Name if it has numeric format
ls4_csv['field_id'] = range(1, len(ls4_csv) + 1)

# Rename columns to match ZTF format
ls4_csv = ls4_csv.rename(columns={'ra_deg': 'ra', 'dec_deg': 'dec'})

# Calculate galactic coordinates (l, b) and ecliptic coordinates
coords = SkyCoord(ra=ls4_csv['ra'].values*u.deg, 
                  dec=ls4_csv['dec'].values*u.deg, 
                  frame='fk5')

# Galactic coordinates
ls4_csv['l'] = coords.galactic.l.deg
ls4_csv['b'] = coords.galactic.b.deg

# Ecliptic coordinates (BarycentricMeanEcliptic)
ecliptic_coords = coords.barycentricmeanecliptic
ls4_csv['ecliptic_lon'] = ecliptic_coords.lon.deg
ls4_csv['ecliptic_lat'] = ecliptic_coords.lat.deg

# Set extinction values (can be improved with actual maps)
# Using 0.0 as placeholder - can be replaced with SFD98 dust map values
ls4_csv['ebv'] = 0.0

# Create entry number
ls4_csv['number'] = range(len(ls4_csv))

# Filter to keep only fields with even_even dither pattern
# Parse field name as "X_Y" and check if both X and Y are even
def is_even_even(field_name):
    try:
        parts = field_name.split('_')
        if len(parts) == 2:
            x, y = int(parts[0]), int(parts[1])
            return x % 2 == 0 and y % 2 == 0
    except (ValueError, IndexError):
        pass
    return False

ls4_csv = ls4_csv[ls4_csv['Field Name'].apply(is_even_even)]
print(f"Filtered to {len(ls4_csv)} fields with even_even dither pattern")

# Reorder columns to match ZTF format
output_df = ls4_csv[['field_id', 'ra', 'dec', 'ebv', 'l', 'b', 
                     'ecliptic_lon', 'ecliptic_lat', 'number']]

# Write to file in ZTF format (space-separated, with header comment)
with open('data/LS4_Fields.txt', 'w') as f:
    f.write('% ID         RA         Dec       Ebv      Gal Long  Gal Lat    Ecl Long  Ecl Lat   Entry\n')
    # Format each line to match ZTF format
    for idx, row in output_df.iterrows():
        f.write(f'{int(row["field_id"]):06d} {row["ra"]:10.5f} {row["dec"]:10.5f} {row["ebv"]:6.2f} '
                f'{row["l"]:10.4f} {row["b"]:9.4f} {row["ecliptic_lon"]:10.4f} {row["ecliptic_lat"]:8.4f} {int(row["number"]):6d}\n')

print(f"Converted {len(output_df)} LS4 fields to ZTF_Fields.txt format")
print(f"Output written to: data/LS4_Fields.txt")
