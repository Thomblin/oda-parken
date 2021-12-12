from osm import OSM
from osmgeocode import Geocoder

coder = Geocoder(OSM('aachen.osm'))

placename, way = coder.resolve('wqjjkdn')
print(placename)
print(way.nds)
print(way.tags)
print(way.get_projected_points()[-1])
