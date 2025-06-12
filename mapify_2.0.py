import folium
import pandas
from folium.plugins import MarkerCluster

# Read volcano data
data = pandas.read_csv("volcano_data.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# Function to determine color based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Create map object with new zoom level and map center
map = folium.Map(location=[20.0, 0.0], zoom_start=5)  # Adjusted center and zoom level

# Feature group for markers
fg = folium.FeatureGroup(name="School & Volcano Markers")

# Add school markers with tooltip and popup customization
for coordinates in [[-43.52, -79.64], [-42.31, -78.41], [-43.01, -79.12]]:
    fg.add_child(folium.Marker(location=coordinates, 
                               popup="School", 
                               icon=folium.Icon(color='red'),
                               tooltip="Click me!"))  # Tooltip added

# Feature group for volcano circles
fgv = folium.FeatureGroup(name="Volcano Circles")

# Add circle markers colored by elevation with new popup format (emoji + bold text)
for lt, ln, el in zip(lat, lon, elev):
    html = """<h4><strong>Volcano Information:</strong></h4><p>🌋 Elevation: %s m</p>"""
    iframe = folium.IFrame(html=html % str(el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=12,  # Increased radius
                                      popup=folium.Popup(iframe),
                                      fill_color=color_producer(el),
                                      color='grey', fill_opacity=0.7,
                                      tooltip="Click me!"))  # Tooltip added

# Add a specific school marker
fg.add_child(folium.Marker(location=[43.5212, -79.6473], 
                           popup="Iona CSS", 
                           icon=folium.Icon(color='cadetblue'),
                           tooltip="Click me!"))

# Add a new marker for Mount Vesuvius (famous volcano)
fg.add_child(folium.Marker(location=[40.8213, 14.4263],  # Mount Vesuvius Coordinates
                           popup="Mount Vesuvius 🌋",
                           icon=folium.Icon(color='purple'),
                           tooltip="Click me!"))

# Add a new feature group for rivers (example marker for the Nile River)
fg_rivers = folium.FeatureGroup(name="Rivers")
fg_rivers.add_child(folium.Marker(location=[30.0444, 31.2357],  # Nile River Coordinates (Cairo)
                                  popup="Nile River 🌊",
                                  icon=folium.Icon(color='blue'),
                                  tooltip="Click me!"))

# Seven Wonders of the World coordinates and names
seven_wonders = [
    {"name": "Great Wall of China", "lat": 40.4319, "lon": 116.5704},
    {"name": "Petra, Jordan", "lat": 30.3285, "lon": 35.4444},
    {"name": "Christ the Redeemer, Brazil", "lat": -22.9519, "lon": -43.2105},
    {"name": "Machu Picchu, Peru", "lat": -13.1631, "lon": -72.5450},
    {"name": "Chichen Itza, Mexico", "lat": 20.6829, "lon": -88.5678},
    {"name": "Roman Colosseum, Italy", "lat": 41.8902, "lon": 12.4922},
    {"name": "Taj Mahal, India", "lat": 27.1751, "lon": 78.0421}
]

# Add markers for the Seven Wonders of the World
for wonder in seven_wonders:
    fg.add_child(folium.Marker(location=[wonder["lat"], wonder["lon"]], 
                               popup=wonder["name"] + " 🌍",
                               icon=folium.Icon(color='purple'),
                               tooltip="Click me!"))

# MarkerCluster for volcanoes
marker_cluster = MarkerCluster().add_to(map)

# Add volcano markers to the marker cluster
for lt, ln, el in zip(lat, lon, elev):
    folium.Marker(location=[lt, ln],
                  popup=f"Elevation: {el} m",
                  icon=folium.Icon(color=color_producer(el)),
                  tooltip="Click me!").add_to(marker_cluster)

# Add feature groups to map
map.add_child(fg)
map.add_child(fgv)
map.add_child(fg_rivers)
map.add_child(folium.LayerControl())

# Save map to an HTML file
map.save("mapify_with_seven_wonders.html")