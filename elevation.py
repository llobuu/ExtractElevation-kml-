import os
import csv
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import pandas as pd

def extract_elevation_from_kml(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Handle XML namespace for KML
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Find all coordinate tags
    coordinates = root.findall('.//kml:coordinates', ns)
    latitude = []
    longitude = []
    elevations = []

    for coord in coordinates:
        lines = coord.text.strip().split()
        for line in lines:
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    lat = float(parts[0])
                    latitude.append(lat)

                    long = float(parts[1])
                    longitude.append(long)

                    elevation = float(parts[2])
                    elevations.append(elevation)
                except ValueError:
                    continue
    return latitude, longitude, elevations

def save_to_csv(latitude, longitude, elevations, output_path):
    dataset = {'latitude':latitude,
               'longitude':longitude,
               'elevations': elevations}

    df_data = pd.DataFrame.from_dict(dataset, orient='columns')
    print(df_data)

    writer = pd.ExcelWriter(output_path, engine = 'xlsxwriter')
    df_data.to_excel(writer)
    writer.close()


if __name__ == "__main__":
    # Ask user for the path to the KML file
    root = tk.Tk()
    root.withdraw()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    file = filedialog.askopenfile(initialdir=desktop_path, title="Select a file")
    if file:
        kml_path = file.name

    folder = os.path.dirname(kml_path)
    output_file = os.path.join(folder, "kml elevations.xlsx")

    if not os.path.exists(kml_path) or not kml_path.endswith('.kml'):
        print("Invalid file path or file type.")
    else:

        latitude, longitude, elevations = extract_elevation_from_kml(kml_path)

        if not latitude:
            print("No latitude data found in the KML file.")
        if not longitude:
            print("No longitude data found in the KML file.")
        if not elevations:
            print("No elevation data found in the KML file.")
        else:
            save_to_csv(latitude, longitude, elevations, output_file)
            print(f"Elevation data saved to: {output_file}")
