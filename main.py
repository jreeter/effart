from points import points
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#### Calculation Helpers

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


def normalize(activity):

    normalizer = lambda lat, long: [
        get_normalized_y(y_max, y_min, x_max, x_min, lat, long),
        get_normalized_x(y_max, y_min, x_max, x_min, lat, long)
    ]

    lat_long_pairs = list(map(normalizer, activity.latitude, activity.longitude))

    return map_dataframe(lat_long_pairs)


# Takes an array of arrays that contain [lat,long] points, each child of the outermost array is a separate activity
# recorded by the athlete.
def map_dataframe(points):
    data = np.array(points)
    return pd.DataFrame({
        'latitude': data[:, 0],
        'longitude': data[:, 1]
    })

#### Calculation Helpers


#### Program Work:

# Create a list of dataframes for each activity.
activities = list(map(map_dataframe, points))

# Get the min/max of long/lat across all activities.
x_max = max(list(map(lambda x: x.longitude.max(), activities)))
x_min = max(list(map(lambda x: x.longitude.min(), activities)))
y_max = max(list(map(lambda x: x.latitude.max(), activities)))
y_min = max(list(map(lambda x: x.latitude.min(), activities)))

# For each activity normalize the lat, long pairs
normalized_activities = list(map(normalize, activities))

# Plot all the activities
fig, plots = plt.subplots(1, len(normalized_activities), figsize=(10,1))
for index, plot in enumerate(plots):
    ds = normalized_activities[index]
    # plot.axis('off')
    # plot.set_xlim(0, 1)
    # plot.set_ylim(0, 1)
    plot.set_aspect(1)
    plot.plot(ds.longitude, ds.latitude)

fig.tight_layout()
# plt.subplot_tool()
plt.show()
