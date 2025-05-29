from geopy.distance import geodesic
from shapely.geometry import LineString
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os


def extract_elevation_from_txt(txt_path):
    # Load the tab-delimited file
    #output_path = txt_path.replace('.txt', '.csv')
    dist_list = [0]

    # Read using tab separator
    df = pd.read_csv(txt_path, sep='\t')
    coords=[]
    lat_list = df['latitude']
    long_list = df['longitude']
    elevation_list = df['altitude (m)']
    for i in range(len(df['latitude'])):
        coords.append((df['latitude'][i].item(),df['longitude'][i].item()))
   
    # Reverse to (lat, lon)
    latlon_coords = [(lat, lon) for lat, lon in coords]
    # Calculate distance in meters
    total_distance_m = 0.0
    for i in range(1, len(latlon_coords)):
        segment_distance = geodesic(latlon_coords[i - 1], latlon_coords[i]).meters
        total_distance_m += segment_distance
        dist_list.append(total_distance_m)

    return lat_list, long_list, elevation_list, dist_list


def save_to_csv(latitude, longitude, elevations, distance, output_path):
    dataset = {"latitude": latitude, "longitude": longitude, "distance": distance,"elevations": elevations}

    df_data = pd.DataFrame.from_dict(dataset, orient="columns")
    print(df_data)

    writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
    df_data.to_excel(writer)
    writer.close()


if __name__ == "__main__":
    # Ask user for the path to the KML file
    root = tk.Tk()
    root.withdraw()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    file = filedialog.askopenfile(initialdir=desktop_path, title="Select a file")
    if file:
        txt_path = file.name
   
    folder = os.path.dirname(txt_path)
    latitude, longitude, elevations, distance = extract_elevation_from_txt(txt_path)


    output_file = os.path.join(folder, "elevations.xlsx")


    save_to_csv(latitude, longitude, elevations, distance, output_file)
    #print(f"Elevation data saved to: {output_file}")
