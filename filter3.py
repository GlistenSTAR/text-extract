from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

finialDic={}
address1 = address2 = address3 = ''
advice_for_home = []

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
  start_pos = end_pos = 0
  for key, item in enumerate(all_blocks):
    if(all_blocks[key]["Text"] == '(zie toelichting in bijlage)'):
      finialDic["Class"] = all_blocks[key-1]["Text"]
      continue
    if(all_blocks[key]["Text"] == 'Labelklasse maakt vergelijking met woning(en) van het volgende type mogelijk.'):
      finialDic["Label Class"] = all_blocks[key+1]["Text"]
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
    
    if("(elektriciteit)" in all_blocks[key]["Text"] and not "Elektriciteit" in finialDic):
      finialDic["Elektriciteit"] = all_blocks[key]["Text"].split("(")[0]
    if("(gas)" in all_blocks[key]["Text"] and not "Gas" in finialDic):
      finialDic["Gas"] = all_blocks[key]["Text"].split("(")[0]
    if("(warmte)" in all_blocks[key]["Text"] and not "Warmte" in finialDic):
      finialDic["Warmte"] = all_blocks[key]["Text"].split("(")[0]
      
    if(all_blocks[key]["Text"] == "Advies voor uw woning" and start_pos == 0):
        start_pos = key
    if(all_blocks[key]["Text"] == "BIJLAGE" and end_pos == 0):
        end_pos = key
      
    if(all_blocks[key]["Text"] == "(energie-index)" and not "Energie Index" in finialDic):
      finialDic["Energie Index"] = all_blocks[key-1]["Text"].split(" ")[-1:][0]
      
  for index in range(start_pos, end_pos):
    if(float(all_blocks[index]["Geometry"]["Polygon"][0]["X"]) > 0.74):
      advice_for_home.append(all_blocks[index]["Text"])
  finialDic["Advice"] = advice_for_home
  
  # print(finialDic)
  # time.sleep(3000)
  return finialDic