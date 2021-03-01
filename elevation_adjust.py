#!/usr/bin/env python3

import gpxpy
import sys
import os
import copy
import datetime
import argparse
from argparse import ArgumentParser

class GPXModifier(object):
    start_timedelta = datetime.timedelta(minutes=1)

    def __init__(self, gpx_fd):
        self.gpx = gpxpy.parse(gpx_fd)
        
    def get_points(self, elevation_in_meters):
        net = 0.0
        track_idx = 0
        points = []
        if len(self.gpx.tracks) == 0:
            return None
        l_segments = len(self.gpx.tracks[-1].segments)
        if l_segments == 0:
            return None
        l_points = len(self.gpx.tracks[-1].segments[-1].points)
        if l_points == 0:
            return None
        last_point = self.gpx.tracks[-1].segments[-1].points[-1]
        # start the new points for the new segment with a time delta of 1 minute from the last point
        # the segment points are sorted by time. So it should be safe
        new_start_time = last_point.time + self.start_timedelta
        last_time = None
        last_elevation = 0
        ## keep fetching required points from existing track/segment/points
        for track in self.gpx.tracks:
            for segment in track.segments:
                for p in segment.points:
                    if net < elevation_in_meters:
                        new_p = copy.copy(p)
                        if last_time is None:
                            new_p.time = new_start_time
                        else:
                            new_p.time = last_time + (p.time - last_p.time)
                            net += p.elevation - last_p.elevation
                        last_time = new_p.time
                        last_p = p
                        points.append(new_p)
                    else:
                        return points

        return None

    def get_track_name(self):
        if len(self.gpx.tracks) == 0:
            return None
        return self.gpx.tracks[0].name

    def elevation_adjust(self, elevation_in_meters):
        track_name = self.get_track_name()
        if not track_name:
            track_name = 'New-Elevation-Adjusted Track Name'
        points = self.get_points(elevation_in_meters)
        if not points:
            return None
        # lets append a new track with a new segment and the elevation adjusted points for the segment
        track = gpxpy.gpx.GPXTrack(track_name)
        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)
        segment.points = points
        self.gpx.tracks.append(track)
        return self.gpx.to_xml()


def main(args):
    gpx_file = args.gpx
    elevation = args.elevation
    if not os.access(gpx_file, os.F_OK):
        raise Exception('gpx file {} not accessible'.format(gpx_file))
    with open(gpx_file) as f:
        gpx_mod = GPXModifier(f)
        print('Elevation adjust to %.2f meters for GPX %s' %(elevation, gpx_file))
        modified_gpx_xml = gpx_mod.elevation_adjust(elevation)
        if not modified_gpx_xml:
            raise Exception('No points found to adjust to the target elevation of {:.2f}'.format(elevation))
        parts = os.path.splitext(gpx_file)
        new_gpx_file = '_'.join(parts[:1] + ('modified',)) + parts[-1]
        with open(new_gpx_file, 'w') as wf:
            wf.write(modified_gpx_xml)
            print('Elevation modified and written to %s' %(new_gpx_file))

    return 0

if __name__ == '__main__':
    parser = ArgumentParser(description='GPX elevation adjuster',
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-gpx', '--gpx', type=str, default='sample_everesting.gpx',
                        help='Specify GPX file to adjust the elevation')
    parser.add_argument('-elevation', '--elevation', type=float, default=10.0,
                        help='Specify elevation to adjust in meters')
    args = parser.parse_args()
    sys.exit(main(args))
    
