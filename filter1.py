from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import simplejson
import time    
import re

isolatie_enum = ["-", "+", "++", "+/-", "n.v.t."]
isolatie_valuse_enum = ["Noord", "Oost", "West","Zuid", "Noordoost", "Zuidwest", "Zuidoost", "Noordwest", "Vloeren", "Horizontaal"]
finialDic  = {}
finialDic["Datum registratie"] = ''
all_blocks = []
key_positions = []
isolatie = {}
isolatie["Gevels"] =  {}
isolatie["Gevelpanelen"] = {}
isolatie["Daken"] = {}
isolatie["Vloeren"] = {}
isolatie["Ramen"] = {}
isolatie["Buitendeuren"] = {}
isolatie["Verwarming"] = {}
isolatie["Warm water"] = {}
isolatie["Ventilatie"] = {}
isolatie["Koeling"] = {}
isolatie["Zonnepanelen"] = {}

# Get bottom Object
def search_bottom_filter(item, items, method, size): # return item,
    result = ''
    if(size=="lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        if(item["Text"] == "West"):
            x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 5
    elif(size=="lg"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-3
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2
    elif(size=="md"):
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 3.15
    else:
        x = item['Geometry']["Polygon"][0]["X"] + 1e-2
        y = item['Geometry']["Polygon"][0]["Y"] + item['Geometry']["BoundingBox"]["Height"] * 2.1
        
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

def get_each_object(key, all_blocks, index_range, first_param, second_param):
    isolatie[key][all_blocks[index_range+1]["Text"]] = []   
    first_obj, first_obj_index = search_bottom_filter(all_blocks[index_range+1], all_blocks, "obj", "lg")
    if(first_obj):
        first = first_obj["Text"]
        second = all_blocks[first_obj_index+1]["Text"]
        isolatie[key][all_blocks[index_range+1]["Text"]].append({first_param : first, second_param : second})
        # Continue if more values
        while len(first_obj) > 0:
            first_obj, first_obj_index = search_bottom_filter(first_obj, all_blocks, "obj", "sm")
            if(first_obj):
                if("m²" in first_obj["Text"]):
                    first = first_obj["Text"]
                    second = all_blocks[first_obj_index+1]["Text"]
                    isolatie[key][all_blocks[index_range+1]["Text"]].append({first_param : first, second_param : second})
                else:
                    break
            else:
                break   

def get_each_object_letter(key1, key2, all_blocks, index_range):
    if(all_blocks[index_range]["Text"] == key2):
        isolatie[key1][key2] = search_bottom_filter(all_blocks[index_range], all_blocks, "", "md")
        isolatie[key1][all_blocks[index_range+1]["Text"]] = search_bottom_filter(all_blocks[index_range+1], all_blocks, "", "md")

def filter1(all_blocks):
    # declear local variable
    address1 = address2 = address3 = ''
    woningtype1 = woningtype2 = ''
                    
    for key, item in enumerate(all_blocks):
        # Get date of register
        if(item["Text"] == "Datum registratie" and ("Datum_registratie" not in finialDic)):
            cutted_blocks = all_blocks[key:] # cut the array for speed
            finialDic["Datum registratie"] = search_bottom_filter(item, cutted_blocks, "", "")
            continue

        # Get class name
        if(item["Text"] == "heeft energielabel"):
            finialDic["Class"] = all_blocks[key+1]["Text"]
            continue    
        
        # Get isolatie object  
        # if(item["Text"] == "Gevels"):
        #     Gevels = search_right_filter_enum(key, item, response)
        # if(item["Text"] == "Gevelpanelen"):
        #     Gevelpanelen = search_right_filter_enum(key, item, response)
        # if(item["Text"] == "Daken"):
        #     Daken = search_right_filter_enum(key, item, response)
        # if(item["Text"] == "Vloeren"):
        #     Vloeren = search_right_filter_enum(key, item, response)
        # if(item["Text"] == "Ramen"):
        #     Ramen = search_right_filter_enum(key, item, response)
        # if(item["Text"] == "Buitendeuren"):
        #     Buitendeuren = search_right_filter_enum(key, item, response)
            
        if("Verwarming" in item["Text"] and ( "Verwarming" not in finialDic )):
            finialDic["Verwarming"] = all_blocks[key+1]["Text"]
            continue
        if("Warm water" in item["Text"] and ( "Warm water" not in finialDic )):
            finialDic["Warm water"] = all_blocks[key+1]["Text"]
            continue
        if("Zonneboiler" in item["Text"] and ( "Zonneboiler" not in finialDic )):
            finialDic["Zonneboiler"] = all_blocks[key+1]["Text"]
            continue
        if("Ventilatie" in item["Text"] and ( "Ventilatie" not in finialDic )):
            finialDic["Ventilatie"] = all_blocks[key+1]["Text"]
            continue
        if("Koeling" in item["Text"] and ( "Koeling" not in finialDic )):
            finialDic["Koeling"] = all_blocks[key+1]["Text"]
            continue
        if("Zonnepanelen" in item["Text"] and ( "Zonnepanelen" not in finialDic )):
            finialDic["Zonnepanelen"] = all_blocks[key+1]["Text"]
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
        
        if(not address1):
            finialDic["Adres"]=''
        if(not address2):    
            finialDic["Adres"] = address1
        if(not address3):    
            finialDic["Adres"] = address1 + " " + address2
        else:
            finialDic["Adres"] = address1 + " " + address2 + " " + address3

        # Get Deíailaanduiding
        if("Bouwjaar" in item["Text"] and ( "bouwjaar" not in finialDic )):
            finialDic["Bouwjaar"] = all_blocks[key+1]["Text"]
            continue
        if("Compactheid" in item["Text"] and ( "compactheid" not in finialDic )):
            finialDic["Compactheid"] = all_blocks[key+1]["Text"]
            continue
        if("Vloeroppervlakte" in item["Text"] and ( "vloeroppervlakte" not in finialDic )):
            finialDic["Vloeroppervlakte"] = item["Text"].split(' ', 1)[1]
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

        if(not woningtype1):
            finialDic["Woningtype"] = ''
        if(not woningtype2):
            finialDic["Woningtype"] = woningtype1
        if(woningtype1 and woningtype2):
            finialDic["Woningtype"] = woningtype1 + " " + woningtype2

        # Get power energy
        if("kWh/m² per jaar" in item["Text"] or "kWh/m\u00b2 per jaar" in item["Text"] and ( "Energy" not in finialDic )):
            if(item["Text"] == "kWh/m\u00b2 per jaar"):
                finialDic["Energy"] = all_blocks[key-1]["Text"] +" " + item["Text"]
            else:    
                finialDic["Energy"] = item["Text"]
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
            key_positions.append(len(all_blocks) - 1)
            continue
        
    # Get Isolatie object with Dic
    for key, data in enumerate(key_positions):                                              # Loop the positions
        if key < len(key_positions) - 1:                                                    # until length-1
            for index_range in range(key_positions[key],  key_positions[key + 1]):          # for example 1. Gevels ~ 2.Gevelpanelen 's indexs
                if(all_blocks[index_range+1]["Text"] in isolatie_valuse_enum):
                    if(all_blocks[key_positions[key]]["Text"] == "1 Gevels"):               # 1 Gevels
                        get_each_object("Gevels", all_blocks, index_range, "Opp", "Rc") 
                        continue           
                                                        
                    if(all_blocks[key_positions[key]]["Text"] == "2 Gevelpanelen"):         #  Gevelpanelen
                        get_each_object("Gevelpanelen", all_blocks, index_range, "Opp", "U")  
                        continue          
                    
                    if(all_blocks[key_positions[key]]["Text"] == "3 Daken"):                #  Daken
                        get_each_object("Daken", all_blocks, index_range, "Opp", "Rc")     
                        continue       
                        
                    if(all_blocks[key_positions[key]]["Text"] == "4 Vloeren"):              #  Vloeren
                        get_each_object("Vloeren", all_blocks, index_range, "Opp", "Rc")    
                        continue        
                    
                    if(all_blocks[key_positions[key]]["Text"] == "5 Ramen"):                # Ramen
                        get_each_object("Ramen", all_blocks, index_range, "Opp", "Uw")      
                        continue      
                    
                    if(all_blocks[key_positions[key]]["Text"] == "6 Buitendeuren"):         #  Buitendeuren
                        get_each_object("Buitendeuren", all_blocks, index_range, "Opp", "Ud")   
                        continue         
                        
                if(all_blocks[key_positions[key]]["Text"] == "7 Verwarming"):           # Verwarming
                    get_each_object_letter("Verwarming", "Verwarmingstoestellen", all_blocks, index_range)
                    continue
                    
                if(all_blocks[key_positions[key]]["Text"] == "8 Warm water"):           # Warm water
                    get_each_object_letter("Warm water", "Warmwatertoestellen", all_blocks, index_range)
                    continue
           
                # if(all_blocks[key_positions[key]]["Text"] == "9 Zonneboiler"):          # Zonneboiler
                #     get_each_object_letter("zonneboiler", "Warmwatertoestellen", all_blocks, index_range)
                    
                if(all_blocks[key_positions[key]]["Text"] == "10 Ventilatie"):          #  Ventilatie
                    if(all_blocks[index_range]["Text"] == "Type ventilatiesysteem"):
                        isolatie["Ventilatie"]["Type ventilatiesysteem"] = "Natuurlijke ventilatie met raampjes en roosters"
                        isolatie["Ventilatie"]["Warmteterugwinning"] = search_bottom_filter(all_blocks[index_range+1], all_blocks, "", "md")      
                        isolatie["Ventilatie"]["Wisselstroomventilator"] = search_bottom_filter(all_blocks[index_range+2], all_blocks, "", "md")      
                        isolatie["Ventilatie"]["Aangesloten Oppervlakte"] = search_bottom_filter(all_blocks[index_range+3], all_blocks, "", "md")      
                
                if(all_blocks[key_positions[key]]["Text"] == "11 Koeling"):             #  Koeling
                    get_each_object_letter("Koeling", "Koeltoestellen", all_blocks, index_range)
                   
                    if(all_blocks[index_range]["Text"] == "Wattpiekvermogen"):          # Zonnepanelen
                        isolatie["Zonnepanelen"]["Wattpiekvermogen"] = search_bottom_filter(all_blocks[index_range], all_blocks, "", "md")
                        isolatie["Zonnepanelen"][all_blocks[index_range+1]["Text"]] = search_bottom_filter(all_blocks[index_range+1], all_blocks, "", "md")      
                        isolatie["Zonnepanelen"][all_blocks[index_range+2]["Text"]] = search_bottom_filter(all_blocks[index_range+2], all_blocks, "", "md")  
                        
        finialDic["Isolatie"] = isolatie           
        
    return finialDic        
