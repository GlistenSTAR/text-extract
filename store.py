from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

isolatie_enum = ["-", "+", "++", "+/-", "n.v.t."]
isolatie_valuse_enum = ["Noord", "Oost", "West","Zuid", "Noordoost", "Zuidwest", "Zuidoost", "Noordwest", "Vloeren"]
finialDic = isolatie = {}
all_blocks = []
key_positions = []

# Get bottom Object
def search_bottom_filter(item, items, method, size): # return ite,
    result = ''
    if(size=="lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        if(item["Text"] == "West"):
            x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        else:
            x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 5
    elif(size=="lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2
    else:
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2
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

def filter(response):
    # declear local variable
    address1 = address2 = address3 = ''
    woningtype1 = woningtype2 = ''
    isolatie = {}

    for blocks in response:
        for item in blocks['Blocks']:
            if("Text" in item and item["BlockType"] == "LINE"):
                all_blocks.append(item)
                
    for key, item in enumerate(all_blocks):
        # Get date of register
        if(item["Text"] == "Datum registratie" and ("Datum_registratie" not in finialDic)):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            finialDic["Datum_registratie"] = search_bottom_filter(item, cutted_blocks, "", "")
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
            address1 = search_bottom_filter(item, cutted_blocks, "", "")
            continue

        if(address1 != '' and address2 == '' and item["Text"] == address1):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            address2 = search_bottom_filter(item, cutted_blocks, "", "")
            continue

        if(address2 != '' and address3 == '' and item["Text"] == address2):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            address3 = search_bottom_filter(item, cutted_blocks, "", "")
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
            woningtype1 = search_bottom_filter(item, cutted_blocks, "", "")
            continue
        if(woningtype1!='' and woningtype2=='' and item["Text"] == woningtype1):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            woningtype2 = search_bottom_filter(item, cutted_blocks, "", "")
            continue

        finialDic["woningtype"] = woningtype1 + " / " + woningtype2

        # Get power energy
        if("kWh/m² per jaar" in item["Text"] and ( "energy" not in finialDic )):
            finialDic["energy"] = item["Text"]
            continue

        # Get Isolatie values position
        if(item["Text"] == "1 Gevels" and item["Page"] > 1):
            # key_positions.append({"Gevels":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "2 Gevelpanelen" and item["Page"] > 1):
            # key_positions.append({"Gevelpanelen":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "3 Daken" and item["Page"] > 1):
            # key_positions.append({"Daken":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "4 Vloeren" and item["Page"] > 1):
            # key_positions.append({"Vloeren":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "5 Ramen" and item["Page"] > 1):
            # key_positions.append({"Ramen":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "6 Buitendeuren" and item["Page"] > 1):
            # key_positions.append({"Buitendeuren":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "7 Verwarming" and item["Page"] > 1):
            # key_positions.append({"Verwarming":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "8 Warm water"  and item["Page"] > 1):
            # key_positions.append({"Warm water":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "9 Zonneboiler" and item["Page"] > 1):
            # key_positions.append({"Zonneboiler":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "10 Ventilatie" and item["Page"] > 1):
            # key_positions.append({"Ventilatie":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "11 Koeling" and item["Page"] > 1):
            # key_positions.append({"Koeling":key})
            key_positions.append(key)
            continue
        if(item["Text"] == "12 Zonnepanelen" and item["Page"] > 1):
            # key_positions.append({"Zonnepanelen":key})
            key_positions.append(key)
            break
    
    # Get Isolatie object
    isolatie["gevels"] =  {}
    # isolatie["gevelpanelen"] = {}
    
    for key, data in enumerate(key_positions):                                              # Loop the positions
        if key < len(key_positions) - 1:                                                    # until length-1
            for index_range in range(key_positions[key],  key_positions[key + 1]):          # for example 1. Gevels ~ 2.Gevelpanelen 's indexs
                if(all_blocks[index_range+1]["Text"] in isolatie_valuse_enum):
                    if(all_blocks[key_positions[key]]["Text"] == "1 Gevels"):               # 1 Gevels
                        isolatie["gevels"][all_blocks[index_range+1]["Text"]] = []   
                        first_obj, first_obj_index = search_bottom_filter(all_blocks[index_range+1], all_blocks, "obj", "lg")
                        if(first_obj):
                            opp = first_obj["Text"]
                            Rc = all_blocks[first_obj_index+1]["Text"]
                            isolatie["gevels"][all_blocks[index_range+1]["Text"]].append({"Opp" : opp, "Rc" : Rc})
                            # Continue if more values
                            while len(first_obj) > 0:
                                first_obj, first_obj_index = search_bottom_filter(first_obj, all_blocks, "obj", "sm")
                                if(first_obj):
                                    if("m²" in first_obj["Text"]):
                                        opp = first_obj["Text"]
                                        Rc = all_blocks[first_obj_index+1]["Text"]
                                        isolatie["gevels"][all_blocks[index_range+1]["Text"]].append({"Opp" : opp, "Rc" : Rc})
                                    else:
                                        break
                                else:
                                    break
                            
                            
                    # if(all_blocks[key_positions[key]]["Text"] == "2 Gevelpanelen"):         # 1 Gevelpanelen
                    #     isolatie["gevelpanelen"][all_blocks[index_range+1]["Text"]] = []   
                    #     first_obj, first_obj_index = search_bottom_filter(all_blocks[index_range+1], all_blocks, "obj", "lg")
                    #     if(first_obj):
                    #         opp = first_obj["Text"]
                    #         U = all_blocks[first_obj_index+1]["Text"]
                    #         isolatie["gevelpanelen"][all_blocks[index_range+1]["Text"]].append({"Opp" : opp, "U" : Rc})
                    #         # Continue if more values
                    #         while len(first_obj) > 0:
                    #             first_obj, first_obj_index = search_bottom_filter(first_obj, all_blocks, "obj", "sm")
                    #             if(first_obj):
                    #                 if("m²" in first_obj["Text"]):
                    #                     opp = first_obj["Text"]
                    #                     U = all_blocks[first_obj_index+1]["Text"]
                    #                     isolatie["gevelpanelen"][all_blocks[index_range+1]["Text"]].append({"Opp" : opp, "U" : Rc})
                    #                 else:
                    #                     break
                    #             else:
                    #                 break            
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "3 Daken"):                # 1 Daken
                    #     print("Daken")
                        
                    # if(all_blocks[key_positions[key]]["Text"] == "4 Vloeren"):              # 1 Vloeren
                    #     print("Vloeren")         
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "5 Ramen"):                # 1 Ramen
                    #     print("Ramen")            
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "6 Buitendeuren"):         # 1 Buitendeuren
                    #     print("Buitendeuren")         
                        
                    # if(all_blocks[key_positions[key]]["Text"] == "7 Verwarming"):           # 1 Verwarming
                    #     print("Verwarming")         
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "8 Warm water"):           # 1 Warm water
                    #     print("Warm water")            
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "9 Zonneboiler"):          # 1 Zonneboiler
                    #     print("Zonneboiler")         
                        
                    # if(all_blocks[key_positions[key]]["Text"] == "10 Ventilatie"):          # 1 Ventilatie
                    #     print("Ventilatie")         
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "11 Koeling"):             # 1 Koeling
                    #     print("Koeling")            
                    
                    # if(all_blocks[key_positions[key]]["Text"] == "12 Zonnepanelen"):        # 1 Zonnepanelen
                    #     print("Zonnepanelen")         
                        
                            
    print(isolatie)
    print(">>>>>\n")
    # print(finialDic)
                
                    

