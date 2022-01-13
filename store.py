from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

isolatie_enum = ["-", "+", "++", "+/-", "n.v.t."]
isolatie_valuse_enum = ["Noord", "Oost", "West","Zuid", "Noordoost", "Zuidwest", "Zuidoost", "Noordwest", "Vloeren"]
finialDic = {}
all_blocks = []

def search_bottom_filter(item, items):
    result = ''
    x = item["Polygon"][0]["X"] + 1e-2
    y = item["Polygon"][0]["Y"] + item["BoundingBox"]["Height"] * 2
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

# def search_isolatie_filter(index, blocks):
#     blocks = blocks[index:]
#     for items in blocks:
#       for sub_block in items:
    

def filter(response):
    # declear local variable
    address1 = address2 = address3 = ''
    woningtype1 = woningtype2 = ''

    for blocks in response:
        for item in blocks['Blocks']:
            if("Text" in item and item["BlockType"] == "LINE"):
                all_blocks.append(item)
                
    for key, item in enumerate(all_blocks):
        # Get date of register
        if(item["Text"] == "Datum registratie" and ("Datum_registratie" not in finialDic)):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            finialDic["Datum_registratie"] = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue

        # Get class name
        if(item["Text"] == "heeft energielabel"):
            finialDic["className"] = all_blocks[key+1]["Text"]
            continue    
        
        # Get isolatie object  
        if("Verwarming" in item["Text"] and ( "verwarming" not in finialDic )):
            finialDic["verwarming"] = all_blocks[key+1]["Text"]
            continue
        if("Warm water" in item["Text"] and ( "warm_water" not in finialDic )):
            finialDic["warm_water"] = all_blocks[key+1]["Text"]
            continue
        if("Zonneboiler" in item["Text"] and ( "zonneboiler" not in finialDic )):
            finialDic["zonneboiler"] = all_blocks[key+1]["Text"]
            continue
        if("Ventilatie" in item["Text"] and ( "ventilatie" not in finialDic )):
            finialDic["ventilatie"] = all_blocks[key+1]["Text"]
            continue
        if("Koeling" in item["Text"] and ( "koeling" not in finialDic )):
            finialDic["koeling"] = all_blocks[key+1]["Text"]
            continue
        if("Zonnepanelen" in item["Text"] and ( "zonnepanelen" not in finialDic )):
            finialDic["zonnepanelen"] = all_blocks[key+1]["Text"]
            continue

        # Get address
        if(item["Text"] == "Adres" and address1==''):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            address1 = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue

        if(address1 != '' and address2 == '' and item["Text"] == address1):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            address2 = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue

        if(address2 != '' and address3 == '' and item["Text"] == address2):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            address3 = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue
        
        finialDic["address"] = address1 + " / " + address2 + " / " + address3

        # Get Deíailaanduiding
        if("Bouwjaar" in item["Text"] and ( "bouwjaar" not in finialDic )):
            finialDic["bouwjaar"] = all_blocks[key+1]["Text"]
            continue
        if("Compactheid" in item["Text"] and ( "compactheid" not in finialDic )):
            finialDic["compactheid"] = all_blocks[key+1]["Text"]
            continue
        if("Vloeroppervlakte" in item["Text"] and ( "vloeroppervlakte" not in finialDic )):
            finialDic["vloeroppervlakte"] = item["Text"].split(' ', 1)[1]
            continue

        # Get Woningtype
        if(item["Text"] == "Woningtype" and woningtype1==''):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            woningtype1 = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue
        if(woningtype1!='' and woningtype2=='' and item["Text"] == woningtype1):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            woningtype2 = search_bottom_filter(item["Geometry"], cutted_blocks)
            continue

        finialDic["woningtype"] = woningtype1 + " / " + woningtype2

        # Get power energy
        if("kWh/m² per jaar" in item["Text"] and ( "energy" not in finialDic )):
            finialDic["energy"] = item["Text"]
            continue

        # # GEt Isolatie each values
        # if(item["Text"] == "Isolatie"):
        #     isolatie_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Gevels"):
        #     gevels_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Daken"):
        #     daken_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Vloeren"):
        #     vloeren_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Buitendeuren"):
        #     buitendeuren_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Verwarming"):
        #     verwarming_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Warm water"):
        #     warmwater_start_pos = [index, key]
        #     continue
        # if(item["Text"] == "Zonneboiler"):
        #     zonneboiler_start_pos = [index, key]
        #     continue

    print(finialDic)

