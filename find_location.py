"""
Trouve un emplacement sur Nominatim à partir d'une saisie de l'utilisateur. 
"""

from geopy import Nominatim

def find_location(query):
    """
    Renvoie une liste de tuples contenant le nom, les coordonnées et le type de chaque lieu correspondant à la requête donnée.
    """

    geolocator = Nominatim(user_agent="my-app")
    location_list = []
    # locations = geolocator.geocode(query, exactly_one=False, country_codes=["EN"])
    locations = geolocator.geocode(query, exactly_one=False)

    if locations:
        if isinstance(locations, list):
            for loc in locations:
                location_name = loc.raw['display_name']
                location_type = loc.raw['type']
                location_lat = loc.raw['lat']
                location_lon = loc.raw['lon']
                location_list.append((location_name, location_lat, location_lon, location_type))
            return location_list
        if isinstance((locations, str)):
            return locations
    else:
        return None


if __name__ == '__main__':
    loop = True
    while loop:
        query = input("Ville : ")
        if query == "STOP":
            loop = False
        else:
            locations = find_location(query)
            if locations:
                print(f"Voici les lieux trouvés pour la requête '{query}':")
                for loc in locations:
                    print(f"Nom: {loc[0]}, Coordonnées: {loc[1]}, {loc[2]}, Type: {loc[3]}")
            else:
                print(f"Aucun lieu trouvé pour la requête '{query}'.")
