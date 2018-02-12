import folium
import parser
from geopy import ArcGIS


def user_input():
    """
    (none) -> (int, int, int)
    This function provides user interaction

    returns: year to show films, amount of films and amount of locations
    """

    try:
        year = int(input("Enter a year to show films on the map: "))
        assert year in range(1874, 2025), "Enter correct year"
        film_amount = int(input("Enter a maximum amount of films "
                                "to show on the map: "))
        assert film_amount > 0, "Enter a positive integer"
        loc_amount = int(input("Enter a maximum amount of locations "
                               "to show: "))
        assert loc_amount > 0, "Enter a positive integer"

    except (ValueError, AssertionError) as err:
        print(err)
        exit()

    return year, film_amount, loc_amount


def get_coordinates(location):
    """
    (str) -> (float, float)
    Function finds coordinates of the specific location

    location: name of location to get
    map coordinates
    returns: tuple of latitude and longitude
    """

    geolocator = ArcGIS(timeout=10)
    locat = geolocator.geocode(location)
    return locat.latitude, locat.longitude


def map_design(diction, f_amount, l_amount):
    """
    (dict) -> (None)
    This function builds the entire map and layers

    param diction: dictionary with provided data of imbd films
    returns: nothing
    """

    world_map = folium.Map()
    marks_fg = folium.FeatureGroup(name="Markers")
    popul_fg = folium.FeatureGroup(name="Population")
    ukraine_fg = folium.FeatureGroup(name="Ukraine")
    africa_fg = folium.FeatureGroup(name="Africa")
    north_am_fg = folium.FeatureGroup(name="North America")
    south_am_fg = folium.FeatureGroup(name="South America")
    europe_fg = folium.FeatureGroup(name="Europe")
    asia_fg = folium.FeatureGroup(name="Asia")
    austr_fg = folium.FeatureGroup(name="Australia and Oceania")

    loc_count = 0
    for key, value in diction.items():
        lat, lon = get_coordinates(key)
        brief_info = ""
        film_count = 0
        for el in value:
            if film_count == f_amount:
                break
            el = el.replace("'", "").replace('"', "")
            film_count += 1
            brief_info += "{}. {}<br>".format(film_count, el)
        loc_count += 1
        print(str(loc_count) + " of " + str(l_amount) + " locations added")
        if loc_count == l_amount:
            break
        marks_fg.add_child(folium.Marker(location=[lat, lon], popup=brief_info,
                                         icon=folium.Icon(color="red",
                                                          icon_color="blue")))

    if loc_count < l_amount:
        print("That year were released only " + str(loc_count) + " films.")

    popul_fg.add_child(folium.GeoJson(open('json_files/world.json', 'r',
                                           encoding='utf-8-sig').read(),
                                      lambda x: {'fillColor': 'green'
                                      if x['properties']['POP2005'] < 10000000
                                      else 'yellow' if 10000000 <=
                                                        x['properties']
                                                        ['POP2005'] < 50000000
                                      else 'red' if 50000000 <=
                                                        x['properties']
                                                        ['POP2005'] < 100000000
                                      else 'black'}))

    ukraine_fg.add_child(folium.GeoJson(open('json_files/ukraine.json', 'r',
                                             encoding='utf-8-sig').read(),
                                        lambda x: {'fillColor': 'red'}))

    asia_fg.add_child(folium.GeoJson(open('json_files/asia.json', 'r',
                                          encoding='utf-8-sig').read(),
                                     lambda x: {'fillColor': 'yellow'}))

    africa_fg.add_child(folium.GeoJson(open('json_files/africa.json', 'r',
                                            encoding='utf-8-sig').read(),
                                       lambda x: {'fillColor': 'green'}))

    europe_fg.add_child(folium.GeoJson(open('json_files/europe.json', 'r',
                                            encoding='utf-8-sig').read(),
                                       lambda x: {'fillColor': 'purple'}))

    north_am_fg.add_child(folium.GeoJson(open('json_files/north_america.json',
                                              'r',
                                              encoding='utf-8-sig').read(),
                                         lambda x: {'fillColor': 'maroon'}))

    south_am_fg.add_child(folium.GeoJson(open('json_files/south_america.json',
                                              'r',
                                              encoding='utf-8-sig').read(),
                                         lambda x: {'fillColor': 'orange'}))

    austr_fg.add_child(folium.GeoJson(open('json_files/australia.json', 'r',
                                           encoding='utf-8-sig').read(),
                                      lambda x: {'fillColor': 'orange'}))

    world_map.add_child(marks_fg)
    world_map.add_child(popul_fg)
    world_map.add_child(ukraine_fg)
    world_map.add_child(asia_fg)
    world_map.add_child(africa_fg)
    world_map.add_child(north_am_fg)
    world_map.add_child(south_am_fg)
    world_map.add_child(austr_fg)
    world_map.add_child(europe_fg)
    world_map.add_child(folium.LayerControl())
    world_map.save("Map.html")


def main():
    """
    (none) -> (none)
    Main function to build map

    returns: nothing
    """

    year, film_amount, loc_amount = user_input()
    print("Reading the file...")
    dictionary = parser.main(year, "locations.list")
    print("Reading finished.")
    print("Building map, creating markers and additional layers")
    map_design(dictionary, film_amount, loc_amount)
    print("Creating map finished successfully.")
    print("Open Map.html to see result!")


main()
