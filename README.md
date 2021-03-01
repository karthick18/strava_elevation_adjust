# strava_elevation_adjust

Tries to adjust the elevation of a gpx file taking input gpx file and target elevation in meters.

Strava does not provide elevation adjust for devices with barometric altimeter.

This tries to hack around by faking a secondary track with points (lat/long/elevation) taken
from the existing tracks to create a new modified GPX that can work with strava.

In order to use this, try to provide a higher elevation value from target (very high) as strava auto-corrects the 
timestamps and elevations during upload from the existing GPX track segment values.

Run it as:
`./elevation_adjust.py sample_everesting.gpx 3000`



