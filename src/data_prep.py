import gpxpy
import pandas as pd

def gpx_reader(flight_name:str):

    gpx_file_dir = 'geo_log/'+flight_name+'.gpx'
    gpx_file = open(gpx_file_dir, 'r')   # open the file in read mode
    gpx_data = gpxpy.parse(gpx_file)

    gpx_points = gpx_data.tracks[0].segments[0].points

    data = [
        {
            'lon': point.longitude,
            'lat': point.latitude,
            'elev': point.elevation,
            'time': point.time
        }
        for point in gpx_points
    ]

    # Create the DataFrame from the list
    df = pd.DataFrame(data, columns=['lon', 'lat', 'elev', 'time'])

    df_clean = df.dropna()

    print(f'{len(df)-len(df_clean)} NaN entries removed')

    return df_clean

def interpolate_points(df, resolution=10):
    """
    Densify the GPS track by interpolating between points.
    """
    interpolated = {
        'lat': [],
        'lon': [],
        'elev': []
    }

    for i in range(len(df) - 1):
        lat_start, lat_end = df.loc[i, 'lat'], df.loc[i+1, 'lat']
        lon_start, lon_end = df.loc[i, 'lon'], df.loc[i+1, 'lon']
        elev_start, elev_end = df.loc[i, 'elev'], df.loc[i+1, 'elev']

        # Interpolate values between current point and the next
        for j in range(resolution):
            t = j / resolution
            interpolated['lat'].append((1 - t) * lat_start + t * lat_end)
            interpolated['lon'].append((1 - t) * lon_start + t * lon_end)
            interpolated['elev'].append((1 - t) * elev_start + t * elev_end)

    return pd.DataFrame(interpolated)