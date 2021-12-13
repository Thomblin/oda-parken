import pandas as pd
import numpy as np
from osmgeocode.osmgeocode import Geocoder
from osmgeocode.osm import OSM

#import the datasets corresponding to these years
years = ["2019", "2020"]

fines = current_fines = pd.read_csv("../data/fines_"+years[0]+".csv", sep=";", dtype={"Tattag": str, "Zeit": str, "Tatort 2": str, "Tatbestand": str, "Geldbuße": int})

for year in years[1:]:
    current_fines = pd.read_csv("../data/fines_"+year+".csv", sep=";",dtype={"Tattag": str, "Zeit": str, "Tatort 2": str, "Tatbestand": str, "Geldbuße": int})
    fines.append(current_fines)
    
fines = fines.rename(columns={"Tatort 2": "location_description"})
fines["location_description"] = fines["location_description"].astype(str)

#fines = fines.head(1000)

#initialize geocoder with aachen osm data
print("Loading OSM data...")
geocoder = Geocoder(OSM('./osmgeocode/aachen.osm'))

def parse_street_no(number):
    
    #handle street nos with letters in them by removing them (future potential for improvement!)
    separators = ["-", "/"]
    number = "".join([char for char in number if (char.isdigit() or char in separators)])
    
    if len(number) == 0:
        return None
        
    for sep in separators:
        if sep in number:
            try:
                return [int(no) for no in number.split(sep)]
            except ValueError:
                return None
    
    #is only reached when number does not contain a separator
    try:
        return [int(number)]
    except ValueError:
        return None
    
print("Parsing addresses...")
location_descriptions = list(fines["location_description"])

identified = 0
addresses = []
for description in location_descriptions:
    was_identified = False
    #bring input into a uniform format and split into components
    components = description.lower().split()
    
    major_part = []
    relation = ""
    minor_part = []

    for i in range(0, len(components)):
        component = components[i]
        if component in ["ggü.", "vor", "neben", "ecke", "gegenüber", "haltestelle", "laterne", "hinter"]:
            if component == "ggü." or component == "gegenüber":
                relation = "ggü."
            elif component == "neben" or component == "hinter":
                relation = "vor"
            else:
                relation = component
                
            minor_part = components[i+1:]
            break
        elif parse_street_no(component) != None:
            relation = "number"
            minor_part = component
            break
        else:
            major_part.append(component)
            
    street_name = ""
            
    if relation == "number":
        street_name = " ".join(major_part)
        street_no = parse_street_no(minor_part)
        addresses.append(street_name+" "+"-".join([str(s) for s in street_no]))
        was_identified = True
    
    elif relation == "vor":
        if "haus-nr." in minor_part and parse_street_no(minor_part[-1]):
            street_name = " ".join(major_part)
            street_no = parse_street_no(minor_part[-1])
            addresses.append(street_name+" "+"-".join([str(s) for s in street_no]))
            was_identified = True
            
    elif relation == "ggü.":
        if "haus-nr." in minor_part and parse_street_no(minor_part[-1]):
            street_name = " ".join(major_part)
            street_no = parse_street_no(minor_part[-1])
            addresses.append(street_name+" "+"-".join([str(s) for s in street_no]))
            was_identified = True
            
    # street crossings are disabled for now, but are an opportnunity for improvement in the future
    #elif relation == "ecke":
    #    if len(minor_part) == 1:
    #        street_name = " ".join(major_part)
    #        minor_street_name = minor_part[0]
    #        was_identified = True
    
    if was_identified == False:
        addresses.append("")

print("Geocoding locations...")

#get location information from the parsed addresses
progress = 0
location_dict = {}
unique_addresses = np.unique(addresses)
for address in unique_addresses:
    if address == "":
        continue
        
    # use the osm geocoder in order to get a lat long location for the parsed address
    geocoder_name, geocoder_way = geocoder.resolve(address)
    if geocoder_way != None:
        location_dict[address] = geocoder_way.get_projected_points()[-1]
    else:
        location_dict[address] = (0, 0)
        
    progress += 1
    if progress % 1000 == 0:
        print(str((progress / len(unique_addresses))*100)+"%")
        
#assign locations for all datapoints

locations = []
for address in addresses:
    locations.append(location_dict.get(address, (0,0)))
    
fines["address"] = addresses
fines["lat"] = [tup[0] for tup in locations]
fines["lon"] = [tup[1] for tup in locations]

#print(fines.head())
        
#performance: 0.8083
#print(len(locations))
#print(np.unique(addresses))
#print(len(np.unique(addresses)))
#print(identified / len(location_descriptions))

print("Saving results...")
fines.to_csv("../data/fines_with_locations.csv", sep=';')

print("Done!")
