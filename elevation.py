import os
import csv
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def extract_elevation_from_kml(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # Handle XML namespace for KML
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Find all coordinate tags
    coordinates = root.findall('.//kml:coordinates', ns)
    elevations = []

    for coord in coordinates:
        lines = coord.text.strip().split()
        for line in lines:
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    elevation = float(parts[2])
                    elevations.append(elevation)
                except ValueError:
                    continue

    return elevations

def save_to_csv(elevations, output_path):
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Elevation (m)'])  # Header
        for e in elevations:
            writer.writerow([e])

if __name__ == "__main__":
    # Ask user for the path to the KML file
    root = tk.Tk()
    root.withdraw()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    kml_path = filedialog.askopenfile(initialdir=desktop_path, title="Select a file")
    #kml_path = input("Enter the full path to your .kml file: ").strip()



    if not os.path.exists(kml_path) or not kml_path.endswith('.kml'):
        print("Invalid file path or file type.")
    else:
        elevations = extract_elevation_from_kml(kml_path)

        if not elevations:
            print("No elevation data found in the KML file.")
        else:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file = os.path.join(desktop_path, "elevations.csv")
            save_to_csv(elevations, output_file)
            print(f"Elevation data saved to: {output_file}")
