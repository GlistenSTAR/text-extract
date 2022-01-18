from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

finialDic={}
address1 = address2 = address3 = ''

def get_bottom_object(item, items, method, size):
    if(size == "lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2
    elif(size == "xlg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 3.5
    elif(size == "sp"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 3.3
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

def filter2(all_blocks):
    for key, item in enumerate(all_blocks):
        if(all_blocks[key]["Text"] == "Energielabel woning" and not "address" in finialDic):
            first_obj, index = get_bottom_object(all_blocks[key], all_blocks, "obj", "lg")
            if(first_obj and first_obj["Text"]):
                address1 = first_obj["Text"]
            second_obj, index = get_bottom_object(first_obj, all_blocks, "obj", "lg")
            if(second_obj and second_obj["Text"]):
                address2 = second_obj["Text"]
            third_obj, index = get_bottom_object(second_obj, all_blocks, "obj", "lg")   
            if(third_obj and third_obj["Text"]):
                finialDic["Bag_ID"] = third_obj["Text"].split(":")[-1:][0]
                
            if(address1 == ''):
                finialDic["Adres"] = ''
            if(address2 == ''):
                finialDic["Adres"] = address1
            else:
                finialDic["Adres"] = address1 + " " + address2
                
            continue
        
        # Get energy label
        finialDic["Energielabel"] = ''

        if("Registratienummer" in all_blocks[key]["Text"] and not "Registratienummer" in finialDic):
            registe_date = all_blocks[key]["Text"].split(" ")[-1:][0]
            finialDic["Registratienummer"] = registe_date
            continue
                
        if("Datum van registratie" in all_blocks[key]["Text"] and not "Datum van registratie" in finialDic):
            registe_date = all_blocks[key]["Text"].split(" ")[-1:][0]
            finialDic["Datum van registratie"] = registe_date
            continue
        # Overzicht woningkenmerken object
        if(all_blocks[key]["Text"] == "Woningtype" and not "Woningtype" in finialDic):
            finialDic["Woningtype"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Bouwperiode" and not "Bouwperiode" in finialDic):
            finialDic["Bouwperiode"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Woonoppervlakte" and not "Woonoppervlakte" in finialDic):
            finialDic["Woonoppervlakte"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Glas woonruimte(s)" and not "Glas woonruimte(s)" in finialDic):
            finialDic["Glas woonruimte"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Glas slaapruimte(s)" and not "Glas slaapruimte(s)" in finialDic):
            finialDic["Glas slaapruimte"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Gevelisolatie" and not "Gevelisolatie" in finialDic):
            finialDic["Gevelisolatie"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Dakisolatie" and not "Dakisolatie" in finialDic):
            finialDic["Dakisolatie"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Vloerisolatie" and not "Vloerisolatie" in finialDic):
            finialDic["Vloerisolatie"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Verwarming" and not "Verwarming" in finialDic):
            finialDic["Verwarming"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Aparte warmtapwatervoorziening" and not "Aparte warmtapwatervoorziening" in finialDic):
            finialDic["Aparte warmtapwatervoorziening"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Zonne-energie" and not "Zonne-energie" in finialDic):
            finialDic["Zonne-energie"] = all_blocks[key+1]["Text"]
            continue
        if(all_blocks[key]["Text"] == "Ventilatie" and not "Ventilatie" in finialDic):
            finialDic["Ventilatie"] = all_blocks[key+1]["Text"]
            continue
        
        if(all_blocks[key]["Text"] == "Wilt u besparen op uw energierekening? Overweeg dan de volgende mogelijke maatregelen:" and not "Tip" in finialDic):
            first_obj = all_blocks[key]
            temp = []
            while first_obj:
                sp_object = first_obj
                first_obj, index = get_bottom_object(first_obj, all_blocks, "obj", "xlg")
                if(first_obj):
                    temp.append(first_obj["Text"])
                else:
                    first_obj, index = get_bottom_object(sp_object, all_blocks, "obj", "sp")
                    if(first_obj):
                      temp.append(first_obj["Text"])
                    else:
                        break
            finialDic["Tip"] = temp
    print(finialDic)
    time.sleep(3000)        
    return finialDic        
    