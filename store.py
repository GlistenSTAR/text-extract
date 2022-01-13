from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time    
import re

isolatie_enum = ["-", "+", "++", "+/-", "n.v.t."]

def search_bottom_filter(item, items):
    x = item["Polygon"][0]["X"] + 1e-2
    y = item["Polygon"][0]["Y"] + item["BoundingBox"]["Height"]*2
    point = Point(x, y)

    for polygon_object in items:
        if(polygon_object["BlockType"] == "LINE"):
            # check contain point on ploygon
            ploygon = []
            for points in polygon_object["Geometry"]["Polygon"]:
                ploygon.append((points["X"], points["Y"]))
            temp = Polygon(ploygon)
            if(temp.contains(point)):
                if "Text" in polygon_object:
                    result = polygon_object["Text"]
    return result

# get the right field on isolatie case of enum
def search_right_filter_enum(index, item, items):
    if items[0]['Blocks'][index+1]["Text"] in isolatie_enum:
        return items[0]['Blocks'][index+1]["Text"]
    else:
        return ''

def filter(response):
    # declear variable
    Datum_registratie = ClassName = Gevels = Gevelpanelen = Daken = Vloeren = Ramen = Buitendeuren = ''
    Verwarming = Warm_water = Zonneboiler = Ventilatie = Koeling = Zonnepanelen = ''
    address = address1 = address2 = address3 = ''
    Bouwjaar = Compactheid = Vloeroppervlakte = ''
    woningtype = woningtype1 = woningtype2 = ''

    # blocks = response[0]['Blocks']
    for blocks in response:
        blocks = blocks['Blocks']
        key = -1

        for item in blocks:
            key = key+1
            if("Text" in item and item["BlockType"] == "LINE"): # search for only blocktype="line"
                
                # Get date of register
                if(item["Text"] == "Datum registratie" and Datum_registratie == ''):
                    cutted_blocks = blocks[key:] # cut the array for speed
                    Datum_registratie = search_bottom_filter(item["Geometry"], cutted_blocks)
                    continue

                # Get class name
                if(item["Text"] == "heeft energielabel"):
                    ClassName = response[0]['Blocks'][key+1]["Text"]
                    continue    
                
                # Get isolatie object  
                if("Gevels" in item["Text"] and Gevels==''):
                    Gevels = search_right_filter_enum(key, item, response)
                    continue
                if("Gevelpanelen" in item["Text"] and Gevelpanelen==''):
                    Gevelpanelen = search_right_filter_enum(key, item, response)
                    continue
                if("Daken" in item["Text"] and Daken==''):
                    Daken = search_right_filter_enum(key, item, response)
                    continue
                if("Vloeren" in item["Text"] and Vloeren==''):
                    Vloeren = search_right_filter_enum(key, item, response)
                    continue
                if("Ramen" in item["Text"] and Ramen==''):
                    Ramen = search_right_filter_enum(key, item, response)
                    continue
                if("Buitendeuren" in item["Text"] and Buitendeuren==''):
                    Buitendeuren = search_right_filter_enum(key, item, response)
                    continue
                    
                

