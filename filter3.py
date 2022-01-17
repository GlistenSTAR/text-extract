from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

finialDic={}
address1 = address2 = address3 = ''

def get_bottom_object(item, items, method, size):
    result = ''
    if(size == "lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2
    elif(size == "xlg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 3.5
    elif(size == "md"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 1.97
    point = Point(x, y)
    
    for key, polygon_object in enumerate(items) :
        ploygon = []
        if(item["Page"] == polygon_object["Page"]):    # check contain point on ploygon
            for points in polygon_object["Geometry"]["Polygon"]:
                ploygon.append((points["X"], points["Y"]))
            temp = Polygon(ploygon)
            if(temp.contains(point)):
                if(method == "obj"):
                    return polygon_object, key
                else:
                    if "Text" in polygon_object:
                      result = polygon_object["Text"]
                      
    if(method == "obj"):
        return {}, ''
    else:
        return result


def filter3(all_blocks):
  for key, item in enumerate(all_blocks):
    if(all_blocks[key]["Text"] == '(zie toelichting in bijlage)'):
      finialDic["Class"] = all_blocks[key-1]["Text"]
      continue
    if(all_blocks[key]["Text"] == 'Rijwoning hoek'):
      finialDic["Rijwoning hoek"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
    if(all_blocks[key]["Text"] == 'Straat'):
      finialDic["Straat"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
    if(all_blocks[key]["Text"] == 'Gebruiksoppervlak'):
      finialDic["Gebruiksoppervlak"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
    if(all_blocks[key]["Text"] == 'Nummer/toevoeging'):
      finialDic["Nummer/toevoeging"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
    if(all_blocks[key]["Text"] == 'Opnamedatum'):
        finialDic["Opnamedatum"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
        continue
    if(all_blocks[key]["Text"] == 'Postcode'):
      finialDic["Postcode"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
    if(all_blocks[key]["Text"] == 'Woonplaats'):
      finialDic["Woonplaats"] = get_bottom_object(all_blocks[key], all_blocks, "", "md")
      continue
      
  print(finialDic)
  time.sleep(3000)