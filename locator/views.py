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
        
        results = {'latitude': latitude_get, 'longitude': longitude_get, 'area': area, 'city': city, 'raw_address': address, 'ip': ipaddress}
        with open('./data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        return HttpResponse(json.dumps(results), content_type="application/json") 
    
