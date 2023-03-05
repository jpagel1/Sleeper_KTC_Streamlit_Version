from geopy.geocoders import Nominatim

def getlatlong(name):

    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    
    location = geolocator.geocode(name)
    print(location)
    if location is not None:
        print("The latitude of the location is: ", location.latitude)
        print("The longitude of the location is: ", location.longitude)
        if (location.latitude == None):
            print('yes')
            location.latitude = 0
        if (location.longitude == None):
            print('yes')
            location.longitude = 0
        return [location.latitude,location.longitude]
    else:
        return[0,0]
        
#test = getlatlong('South Dakota State')
#print(test)
    
