# strava_elevation_adjust

Tries to adjust the elevation of a gpx file taking input gpx file and target elevation in meters.

Strava does not provide elevation adjust for devices with barometric altimeter.

This tries to hack around by faking a secondary track with points (lat/long/elevation) taken
from the existing tracks since the start of the activity to create a new modified GPX that can work with strava.

The time for the segment points duplicated are taken from the last finished segment time with a delta of 1 minute.
This will make the activity appear continuous relative to the start points.

## Using the tool

First install pre-requisites with:
```
pip3 install -r requirements.txt
```

Then run it as:

```./elevation_adjust.py -gpx sample_everesting.gpx -elevation 150```

If you want to avoid strava duplicate entry error to just check uploads against your existing activity,
then use option -fake-time to fake the timestamps for the activity to avoid duplicate activity error from strava.

```./elevation_adjust.py -gpx sample_everesting.gpx -elevation 150 -fake-time```

The above takes a gpx file as input and elevation in meters and creates a new gpx file
with a new segment and points with elevation adjusted.

Needless to say that the elevation can only be adjusted if there are existing points that can
add up to the required/net elevation again.

Happy Hacking,

--Karthick
