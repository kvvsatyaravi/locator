from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from geopy.geocoders import Nominatim
import json,socket

def index(request):
	Template_get="index.html"
	
	if request.method=='GET':
		return render(request,Template_get)

		
def js_passing(request):
    if request.method == 'POST':
        ipaddress = request.POST['ipaddress']
        latitude_get = request.POST['latitude']
        longitude_get = request.POST['longitude']
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(latitude_get+","+longitude_get)
        address = location.raw['address']
        area = address.get('suburb','')
        city = address.get('city', '')
        
        results = {
            'ip': ipaddress,
            'latitude': latitude_get, 
            'longitude': longitude_get, 
            'area': area, 
            'city': city, 
            'raw_address': address
            }

        with open('./data.json','r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            
            users_temp = file_data["users"]
            ip_addresses_temp = []
            for i in range(len(users_temp)):
                ip_addresses_temp.append(users_temp[i]['ip'])
            print(ip_addresses_temp)

            if(len(ip_addresses_temp) == 0):
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
    
