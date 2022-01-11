from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import time    

def search_bottom_filter(item, items):
    print("Bottom search function")
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

def search_right_filter(item, items):
    print("left search function")
    # x = item["Polygon"][0]["X"] + item["BoundingBox"]["Height"]*1.5
    # y = item["Polygon"][0]["Y"] + 1e-2
    # point = Point(x, y)
    # result = []

def filter(response):
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
            ClassName = response[0]['Blocks'][key+1]["Text"]


            
       
