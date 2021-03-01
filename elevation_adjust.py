#!/usr/bin/env python3

import gpxpy
import sys
import os

def get_track_name(gpx):
    if len(gpx.tracks) == 0:
        return ''
    return gpx.tracks[0].name

def get_points(gpx, elevation_in_meters):
    net = 0
    track_idx = 0
    points = []
    ## keep fetching required points from existing track/segment/points
    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                if net < elevation_in_meters:
                    net += p.elevation
                    points.append(p)
                else:
                    return points
    return []

def elevation_adjust(gpx, elevation_in_meters):
    track_name = get_track_name(gpx)
    if track_name == '':
        raise Exception('No track name that can be used to form a new track')
    points = get_points(gpx, elevation_in_meters)
    if not points:
        raise Exception('No points found from segments to adjust elevation')
    track = gpxpy.gpx.GPXTrack(track_name)
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    for p in points:
        segment.points.append(p)
    
    gpx.tracks.append(track)
    return gpx.to_xml()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s [gpx_file] [elevation_to_adjust_in_meters]' %(sys.argv[0]))
    gpx_file = sys.argv[1]
    elevation = float(sys.argv[2])
    if not os.access(gpx_file, os.F_OK):
        raise Exception('gpx file %s not accessible' %(gpx_file))
    with open(gpx_file) as f:
        gpx = gpxpy.parse(f)
        modified_gpx_xml = elevation_adjust(gpx, elevation)
        parts = os.path.splitext(gpx_file)
        new_gpx_file = '_'.join(parts[:1] + ('modified',)) + parts[-1]
        with open(new_gpx_file, 'w') as wf:
            wf.write(modified_gpx_xml)
            print('Elevation modified and written to %s' %(new_gpx_file))
    
