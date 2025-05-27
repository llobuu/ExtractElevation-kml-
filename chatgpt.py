import os
import csv
import xml.etree.ElementTree as ET

def extract_elevation_from_kml(kml_path):
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # KML uses namespaces
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Find all <coordinates> tags
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
    kml_path = input("Enter the full path to your .kml file: ").strip()

    if not os.path.exists(kml_path) or not kml_path.endswith('.kml'):
        print("Invalid file path or file type.")
    else:
        elevations = extract_elevation_from_kml(kml_path)

        if not elevations:
            print("No elevation data found in the KML file.")
        else:
            folder = os.path.dirname(kml_path)
            output_file = os.path.join(folder, "elevations.csv")
            save_to_csv(elevations, output_file)
            print(f"Elevation data saved to: {output_file}")