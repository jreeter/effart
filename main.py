from points import points
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calculations import get_normalized_x, get_normalized_y

# Points is an array of arrays that contains lat, lng points, each lat,long pair is an array e.g:
# [
#     [[lat0, long0], [lat1, long1] .... [latN, long N]],
#     ...,
#     ...
# ]
# This function turns each activity array into it's own dataframe with latitude and longitude columns that hold
# their respective points.
def map_dataframe(points):
    data = np.array(points)
    return pd.DataFrame({
        'latitude': data[:, 0],
        'longitude': data[:, 1]
    })


# Runs normalization on an activity converting the lat, long pair to a normalized x, y pair between 0 and 1.
def normalize(activity):

    normalizer = lambda lat, long: [
        get_normalized_y(y_max, y_min, x_max, x_min, lat, long),
        get_normalized_x(y_max, y_min, x_max, x_min, lat, long),
    ]

    lat_long_pairs = list(map(normalizer, activity.latitude, activity.longitude))

    # Map normalized values back into a dataframe.
    return map_dataframe(lat_long_pairs)


# Main Entry...

activities = list(map(map_dataframe, points))

# Get the min/max of long/lat across all activities *BEFORE NORMALIZING*.
x_max = max(list(map(lambda x: x.longitude.max(), activities)))
x_min = max(list(map(lambda x: x.longitude.min(), activities)))
y_max = max(list(map(lambda x: x.latitude.max(), activities)))
y_min = max(list(map(lambda x: x.latitude.min(), activities)))

# For each activity normalize the lat, long pairs
normalized_activities = list(map(normalize, activities))

# Plot all the activities
fig, plots = plt.subplots(1, len(normalized_activities))
for index, plot in enumerate(plots):
    ds = normalized_activities[index]
    # plot.axis('off')
    # plot.set_xlim(0, 1)
    # plot.set_ylim(0, 1)
    plot.set_aspect(1)
    plot.plot(ds.longitude, ds.latitude)

# fig.tight_layout()
# plt.subplot_tool()
plt.show()
