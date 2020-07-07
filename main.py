from points import points
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_miles_per_degree_longitude(lat):
    return np.cos(np.deg2rad(lat)) * 69.172


def get_x_width(x_max, x_min, lat):
    return (x_max - x_min) * get_miles_per_degree_longitude(lat)


def get_y_height(y_max, y_min):
    return (y_max - y_min) * 69.055


def get_normalized_multiplier(y_max, y_min, x_max, x_min, long):
    return 1 / get_max_axis(y_max, y_min, x_max, x_min, long)


def get_max_axis(y_max, y_min, x_max, x_min, lat):
    return max(get_y_height(y_max, y_min), get_x_width(x_max, x_min, lat))


def get_normalized_x(y_max, y_min, x_max, x_min, lat, long):
    max_axis = get_max_axis(y_max, y_min, x_max, x_min, lat)
    mpdl = get_miles_per_degree_longitude(lat)
    x_width = get_x_width(x_max, x_min, lat)
    return ((long - x_min) * mpdl + (max_axis - x_width ) / 2) * get_normalized_multiplier(y_max, y_min, x_max, x_min, lat)

def get_normalized_y(y_max, y_min, x_max, x_min, lat, long):
    max_axis = get_max_axis(y_max, y_min, x_max, x_min, long)
    y_height = get_y_height(y_max, y_min)
    return ((lat - y_min) * 69.055 + (max_axis - y_height) / 2) * get_normalized_multiplier(y_max, y_min, x_max, x_min, lat)

# Takes an array of arrays that contain [lat,long] points, each child of the outermost array is a separate activity
# recorded by the athlete.
def map_dataframe(points):
    data = np.array(points)
    return pd.DataFrame({
        'latitude': data[:, 0],
        'longitude': data[:, 1]
    })

# Create a list of dataframes for each activity.
activities = list(map(map_dataframe, points))

x_max = max(list(map(lambda x: x.longitude.max(), activities)))
x_min = max(list(map(lambda x: x.longitude.min(), activities)))
y_max = max(list(map(lambda x: x.latitude.max(), activities)))
y_min = max(list(map(lambda x: x.latitude.min(), activities)))

dataset = []

for activity in activities:

    # x_max = activity.longitude.max()
    # x_min = activity.longitude.min()
    # y_max = activity.latitude.max()
    # y_min = activity.latitude.min()


    df = pd.DataFrame({
        'longitude': [],
        'latitude': []
    })

    normalized_xs = []
    normalized_ys = []

    # Normalize long, lat pairs
    for (long, lat) in zip(activity.longitude, activity.latitude):
        normalized_xs.append(get_normalized_x(y_max, y_min, x_max, x_min, lat, long))
        normalized_ys.append(get_normalized_y(y_max, y_min, x_max, x_min, lat, long))

    df.longitude = normalized_xs
    df.latitude = normalized_ys

    print(df)
    dataset.append(df)



fig, plots = plt.subplots(1, len(dataset), figsize=(10,10))

for index, plot in enumerate(plots):
    ds = dataset[index]
    # plot.axis('off')
    # plot.set_xlim(-0.1, 1.1)
    # plot.set_ylim(0, 1)
    plot.set_aspect('equal')
    plot.plot(ds.longitude, ds.latitude)

fig.tight_layout()
# plt.subplot_tool()
plt.show()
