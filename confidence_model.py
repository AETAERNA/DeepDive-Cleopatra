"""
Certainty scoring for Taposiris Magna excavation targets.

This module defines a function that assigns a certainty score between 0 and 1
based on whether a candidate geographic coordinate and depth fall within a
refined Phase II anomaly polygon, the depth range of interest, and proximity
to the 2025 tunnel.  Scores are multiplicative adjustments to a baseline
probability informed by the coherence of the original geophysical survey.
"""
import json
from typing import List, Tuple

# Attempt to import shapely for geometry operations.  If unavailable, fall back to
# simple implementations of point-in-polygon and point-to-line distance.
try:
    from shapely.geometry import shape, Point, LineString  # type: ignore
    _USE_SHAPELY = True
except ImportError:
    _USE_SHAPELY = False

import os

# Determine the root of the repository relative to this file so that data files
# can be located reliably regardless of the current working directory.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.normpath(os.path.join(_HERE, os.pardir))

# Path to the anomaly GeoJSON
_GEOJSON_PATH = os.path.join(_ROOT, 'data', 'geojson', 'phase2_refined_deep_zone.geojson')

# Load the anomaly polygon coordinates from the GeoJSON file
with open(_GEOJSON_PATH, 'r') as f:
    phase2_data = json.load(f)

if _USE_SHAPELY:
    # Create shapely objects
    phase2_geom = shape(phase2_data['features'][0]['geometry'])
    tunnel_line = LineString([
        (29.03456, 30.96920),
        (29.03380, 30.96850)
    ])
else:
    # Extract polygon coordinates directly
    phase2_coords: List[Tuple[float, float]] = phase2_data['features'][0]['geometry']['coordinates'][0]
    # Define tunnel endpoints for fallback distance calculation
    tunnel_p1: Tuple[float, float] = (29.03456, 30.96920)
    tunnel_p2: Tuple[float, float] = (29.03380, 30.96850)


def _point_in_polygon(lon: float, lat: float, polygon: List[Tuple[float, float]]) -> bool:
    """
    Ray casting algorithm for testing if a point is inside a polygon.
    Assumes the polygon is a list of (lon, lat) tuples.
    """
    x, y = lon, lat
    inside = False
    n = len(polygon)
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]
        intersects = ((y0 > y) != (y1 > y)) and (
            x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-12) + x0
        )
        if intersects:
            inside = not inside
    return inside


def _distance_point_to_segment(p: Tuple[float, float], a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """
    Compute the distance from point p to the line segment ab (on the Earth surface
    approximated as flat coordinates in degrees).
    Returns distance in degrees.
    """
    # Vector from a to p and from a to b
    (px, py), (ax, ay), (bx, by) = p, a, b
    apx, apy = px - ax, py - ay
    abx, aby = bx - ax, by - ay
    # Projection of AP onto AB
    ab_len_sq = abx * abx + aby * aby
    if ab_len_sq == 0:
        # a and b are the same point
        return (apx * apx + apy * apy) ** 0.5
    t = (apx * abx + apy * aby) / ab_len_sq
    t_clamped = max(0.0, min(1.0, t))
    # Closest point on segment
    cx = ax + t_clamped * abx
    cy = ay + t_clamped * aby
    dx = px - cx
    dy = py - cy
    return (dx * dx + dy * dy) ** 0.5

def compute_certainty(lon: float, lat: float, depth: float) -> float:
    """
    Compute a certainty score for a given longitude, latitude, and depth.

    Parameters
    ----------
    lon : float
        Longitude in decimal degrees.
    lat : float
        Latitude in decimal degrees.
    depth : float
        Depth below ground surface (m).

    Returns
    -------
    float
        A score between 0 and 1, where higher values indicate greater
        confidence that the location and depth correspond to the target
        anomaly.
    """
    # Baseline score reflecting Phase II anomaly coherence
    base = 0.87

    # Determine whether the point lies within the anomaly polygon
    in_polygon = False
    if _USE_SHAPELY:
        in_polygon = phase2_geom.contains(Point(lon, lat))
    else:
        in_polygon = _point_in_polygon(lon, lat, phase2_coords)

    # Boost if inside the polygon and within the depth range
    if in_polygon and 25 <= depth <= 45:
        base *= 1.15

    # Penalise shallow depths
    if depth <= 30:
        base *= 0.85

    # Compute distance to the tunnel line (in metres)
    if _USE_SHAPELY:
        dist_deg = tunnel_line.distance(Point(lon, lat))
    else:
        dist_deg = _distance_point_to_segment((lon, lat), tunnel_p1, tunnel_p2)
    dist_to_tunnel = dist_deg * 111_139  # approximate conversion from degrees to metres

    # Boost if within 20 m of the tunnel
    if dist_to_tunnel < 20:
        base *= 1.20

    # Cap the score at 1.0
    return float(min(base, 1.0))


if __name__ == '__main__':
    # Example usage
    example_lon = 29.03456
    example_lat = 30.96920
    example_depth = 35
    score = compute_certainty(example_lon, example_lat, example_depth)
    print(f"Certainty score at ({example_lon}, {example_lat}, {example_depth} m): {score:.2f}")