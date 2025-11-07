import gpxpy
import pandas as pd

from src.data_prep import gpx_reader, interpolate_points
from src.map_gen import Flight_Path_Map

flight_name = 'EGTK-LFAT-EGTR'

df = gpx_reader(flight_name)

# Step 1: Densify track
# df = interpolate_points(df, resolution=1)  # Increase resolution for smoother gradients

flight_map = Flight_Path_Map(df)

flight_map.create_figure()
flight_map.add_title(flight_name)
flight_map.save_figure(flight_name+'.png')
