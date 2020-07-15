import numpy as np


# COS(RADIANS(Latitude)) * 69.172
def get_miles_per_degree_longitude(lat):
    return np.cos(np.deg2rad(lat)) * 69.172


# (X (Max) - X (Min)) * X (miles per longitude)
def get_x_width(x_max, x_min, lat):
    return (x_max - x_min) * get_miles_per_degree_longitude(lat)


# (Y (Max) - Y (min)) * Y (miles per latitude)
def get_y_height(y_max, y_min):
    return (y_max - y_min) * 69.055


# IF [(Supporting Calc) Y (Height)]>[(Supporting Calc) X (Width)] THEN
#     // Use height
#     1/[(Supporting Calc) Y (Height)]
# ELSE
#     1/[(Supporting Calc) X (Width)]
# END
def get_normalized_multiplier(y_max, y_min, x_max, x_min, lat):

    y_height = get_y_height(y_max, y_min)

    x_width = get_x_width(x_max, x_min, lat)

    if y_height > x_width:
        return 1 / y_height
    else:
        return 1 / x_width


# MAX(Y (Height), X (Width))
def get_max_axis(y_max, y_min, x_max, x_min, lat):
    return max(get_y_height(y_max, y_min), get_x_width(x_max, x_min, lat))


# (( X (Longitude - X MIN ) * X (miles per longitude) + (Max Axis - X (Width)) /2 ) * Normalize Multiplier
def get_normalized_x(y_max, y_min, x_max, x_min, lat, long):

    max_axis = get_max_axis(y_max, y_min, x_max, x_min, lat)

    mpdl = get_miles_per_degree_longitude(lat)

    x_width = get_x_width(x_max, x_min, lat)

    return ((long - x_min) * mpdl + (max_axis - x_width) / 2) * get_normalized_multiplier(y_max, y_min, x_max, x_min, lat)


# ((Y (Latitude) - Y (min)) * Y (miles per latitude) + (Max Axis - Y (Height))/2) * Normalize Multiplier
def get_normalized_y(y_max, y_min, x_max, x_min, lat, long):

    max_axis = get_max_axis(y_max, y_min, x_max, x_min, lat)

    y_height = get_y_height(y_max, y_min)

    return ((lat - y_min) * 69.055 + (max_axis - y_height) / 2) * get_normalized_multiplier(y_max, y_min, x_max, x_min, lat)
