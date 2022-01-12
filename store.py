from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time    
import re

isolatie_enum = ["-", "+", "++", "+/-", "n.v.t."]

def search_bottom_filter(item, items):
    # print("Bottom search function")
    x = item["Polygon"][0]["X"] + 1e-2
    y = item["Polygon"][0]["Y"] + item["BoundingBox"]["Height"]*1.5
    point = Point(x, y)
    result = []

    for polygon_object in items:
        # check contain point on ploygon
        ploygon = []
        for points in polygon_object["Geometry"]["Polygon"]:
            ploygon.append((points["X"], points["Y"]))
        temp = Polygon(ploygon)
        if(temp.contains(point)):
          if "Text" in polygon_object:
           result.append(polygon_object["Text"])
    
    return result[0]

# get the right field on isolatie case of enum
def search_right_filter_enum(index, item, items):
    if items[0]['Blocks'][index+1]["Text"] in isolatie_enum:
        return items[0]['Blocks'][index+1]["Text"]
    else:
        return ''


def filter(response):
    Gevels = Gevelpanelen = Daken = Vloeren = Ramen = Buitendeuren = ''
    blocks = response[0]['Blocks']
    key = -1

    for item in blocks:
        key = key+1
        if "Text" in item:
            if(item["Text"] == "Datum registratie"):
                # get data register
                cutted_blocks = blocks[key:] # cut the array for speed
                Datum_registratie = search_bottom_filter(item["Geometry"], cutted_blocks)
            if(item["Text"] == "heeft energielabel"):
                # get Class name
                ClassName = response[0]['Blocks'][key+1]["Text"]

            # get isolatie object  
            if(item["Text"] == "Gevels"):
                Gevels = search_right_filter_enum(key, item, response)
            if(item["Text"] == "Gevelpanelen"):
                Gevelpanelen = search_right_filter_enum(key, item, response)
            if(item["Text"] == "Daken"):
                Daken = search_right_filter_enum(key, item, response)
            if(item["Text"] == "Vloeren"):
                Vloeren = search_right_filter_enum(key, item, response)
            if(item["Text"] == "Ramen"):
                Ramen = search_right_filter_enum(key, item, response)
            if(item["Text"] == "Buitendeuren"):
                Buitendeuren = search_right_filter_enum(key, item, response)

            if(item["Text"] == "Verwarming"):
                Verwarming = response[0]['Blocks'][key+1]["Text"]
            if(item["Text"] == "Warm water"):
                Warm_water = response[0]['Blocks'][key+1]["Text"]
            if(item["Text"] == "Zonneboiler"):
                Zonneboiler = response[0]['Blocks'][key+1]["Text"]
            if(item["Text"] == "Ventilatie"):
                Ventilatie = response[0]['Blocks'][key+1]["Text"]
            if(item["Text"] == "Koeling"):
                Koeling = response[0]['Blocks'][key+1]["Text"]
            if(item["Text"] == "Zonnepanelen"):
                Zonnepanelen = response[0]['Blocks'][key+1]["Text"]
        
    # print(Verwarming, Warm_water, Zonneboiler, Ventilatie, Koeling, Zonnepanelen)
            


            
       
