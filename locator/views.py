from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from geopy.geocoders import Nominatim
import json

ipaddress = ''
visitors_ipdata = []

def index(request):
    Template_get="index.html"
    if request.method=='GET':
        return render(request,Template_get)
    
    if request.method == 'POST':
        global ipaddress
        ipaddress = request.POST['user_ip']
        users_data = {"visitorip": ipaddress ,"visited": 0}
        with open('./data.json','r+') as file:
            # First we load existing data into a dict.

            load_data = json.load(file)
            visitors_ipdata = load_data["ipaddresses"]
            users_data["no_visitors"] = len(visitors_ipdata)
            
            if ipaddress in visitors_ipdata:
                print("you already visited these website")
                users_data["visited"] = 1 
            else:
                load_data["ipaddresses"].append(ipaddress)
                file.seek(0)
                json.dump(load_data, file, indent=4)

        return HttpResponse(json.dumps(users_data), content_type="application/json") 

		
def js_passing(request):
    ip_addresses_temp = []
    if request.method == 'POST':
        latitude_get = request.POST['latitude']
        longitude_get = request.POST['longitude']
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse(latitude_get+","+longitude_get)
        address = location.raw['address']
        area = address.get('suburb','')
        city = address.get('city', '')
        
        results = {
            'ipaddress': ipaddress,
            'latitude': latitude_get, 
            'longitude': longitude_get, 
            'area': area, 
            'city': city, 
            'raw_address': address
            }

        with open('./data.json','r+') as file:
            # First we load existing data into a dict.
            ip_addresses_temp = []
            file_data = json.load(file)
            users_temp = file_data["users"]
            for i in range(len(users_temp)):
                ip_addresses_temp.append(users_temp[i]['ipaddress'])
            
            if(len(users_temp) == 0):
                file_data["users"].append(results)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent = 4)
            else:
                if ipaddress in ip_addresses_temp:
                    print("you have already visited these site")
                else:
                    file_data["users"].append(results)
                    # Sets file's current position at offset.
                    file.seek(0)
                    # convert back to json.
                    json.dump(file_data, file, indent = 4)

                
        return HttpResponse(json.dumps(results), content_type="application/json") 
    
