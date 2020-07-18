#Effart

An attempt to port https://www.tableau.com/about/blog/2019/3/how-make-art-out-your-strava-activity-data-tableau-104639 
to a python implementation.

Data is currently loaded from points.py that holds activities as arrays.
There are activity0.csv, activity1.csv, and activity2.csv, the number in
the filename corresponds to their positions in the points.py array.

To install and run:

1. pip install -r requirements.txt
2. python main.py