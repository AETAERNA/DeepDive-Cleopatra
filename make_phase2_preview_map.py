"""
Generate an interactive map of the Taposiris Phase II anomaly and 2025 tunnel.

This script uses the folium library to create an HTML map centered on the
Taposiris Magna temple.  It overlays the refined Phase II resistive anomaly
polygon, draws an approximate line for the 2025 tunnel connecting the temple
to the submerged port, and places a marker at the port location.  The map is
saved to the `output/` directory.
"""
import json
import os

# Attempt to import folium; if unavailable, print a message and exit gracefully.
try:
    import folium  # type: ignore
    _HAS_FOLIUM = True
except ImportError:
    _HAS_FOLIUM = False

# File paths and parameters
GEOJSON_PATH = 'data/geojson/phase2_refined_deep_zone.geojson'
MAP_CENTER = [30.96920, 29.03456]  # Latitude, longitude

def main() -> None:
    if not _HAS_FOLIUM:
        print('Error: folium is not installed. Please install folium to generate the interactive map.')
        return

    # Load anomaly polygon
    with open(GEOJSON_PATH, 'r') as f:
        geojson_data = json.load(f)

    # Create base map
    m = folium.Map(location=MAP_CENTER, zoom_start=18, tiles='OpenStreetMap')

    # Add anomaly polygon layer
    folium.GeoJson(geojson_data, name='Phase II Anomaly').add_to(m)

    # Add tunnel polyline (approximate coordinates)
    folium.PolyLine(
        [
            [30.96920, 29.03456],
            [30.96850, 29.03380]
        ],
        tooltip='2025 Tunnel'
    ).add_to(m)

    # Add port marker
    folium.Marker(
        location=[30.965, 29.030],
        popup='Submerged Port 2025'
    ).add_to(m)

    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    # Save map to HTML
    m.save('output/taposiris_2026_preview.html')
    print('Interactive map saved to output/taposiris_2026_preview.html')


if __name__ == '__main__':
    main()