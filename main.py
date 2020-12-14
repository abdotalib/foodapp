from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import requests
import http.client
import mimetypes
import json 
import urllib.request

def list_data(per1, per2):
	temp = []
	data = pd.read_json('https://{}.openfoodfacts.org/{}.json'.format(per1, per2))
	for i in range(len(data)):
		d = data['tags'][i]
		d = d['id']
		temp.append(d[3:])
	return temp

def fetch_data(data):
	l=[]
	for i in range(len(data)):
		d = data['products'][i]
		l.append(['image_front_small_url'])
	return l


countries = []

#(nutrient_levels)(ingredients_text_with_allergens)(ingredients_text)(image_front_small_url)

countries_data = pd.read_json('https://world.openfoodfacts.org/data/taxonomies/countries.json')



for i in range(len(countries_data.columns)):
	d = countries_data.columns[i]
	countries.append(d[3:])

app = Flask(__name__)
@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
    	countrie = 'en:'+request.form['Countries']
    	key_world = request.form['search']
    	pay = countries_data[str(countrie)]['country_code_3']
    	url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process&json=1".format(key_world)#str(pay['en']),

    	#url = "https://{}.openfoodfacts.org/cgi/search.pl?search_terms={}&user_id=abdotalib&password=abd123do&search_simple=1&jqm=1"
    	payload = {}
    	headers= {}
    	response = requests.request("GET", url, headers=headers, data = payload, verify=False)
    	data = json.loads(response.text) #text.encode('utf8')#pd.read_json()
    	#data = json.load(urllib.request.urlopen(url))

    	'''
    	conn = http.client.HTTPSConnection("{}.openfoodfacts.org".format(pays))
    	payload = ''
    	headers = {}
    	conn.request("GET", "/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=breakfast_cereals&tagtype_1=nutrition_grades&tag_contains_1=contains&tag_1=A&additives=without&ingredients_from_palm_oil=without&json=true", payload, headers)
    	res = conn.getresponse()
    	data = res.read()
    	#print(data.decode("utf-8"))
    	jsonfiles = json.loads(data.to_json(orient='records'))
    	'''
    	#d = fetch_data(data)
    	return  render_template("all_info.html", data = data)
    return render_template("index.html", Countries = countries, Countries_len = len(countries))

#, Categories = categories, Categories_len = len(categories), Allergens = allergens, Allergens_len = len(allergens)
@app.route('/search/<pays>', methods = ['POST', 'GET'])
def search(pays):
	if request.method == 'POST':
		key_world = request.form['search']
		url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms="+key_world+"&search_simple=1&action=process&json=1"
		#url = "https://{}.openfoodfacts.org/cgi/search.pl?search_terms={}&user_id=abdotalib&password=abd123do&search_simple=1&jqm=1".format(pays, key_world)

		payload = {}
		headers= {}
		response = requests.request("GET", url, headers=headers, data = payload, verify=False)
		data =  response.text.encode('utf8')#pd.read_json()
		'''
		conn = http.client.HTTPSConnection("{}.openfoodfacts.org".format(pays))
		payload = ''
		headers = {}
		conn.request("GET", "/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=breakfast_cereals&tagtype_1=nutrition_grades&tag_contains_1=contains&tag_1=A&additives=without&ingredients_from_palm_oil=without&json=true", payload, headers)
		res = conn.getresponse()
		data = res.read()
		#print(data.decode("utf-8"))'''
		return  render_template("all_info.html", d = data)	
	return render_template("search.html")
	'''brands = list_data(pays, "brands")
	categories = list_data(pays, "categories")
	additives = list_data(pays, "additives")
	allergens = list_data(pays, "allergens")
	traces = list_data(pays, "traces")
	labels = list_data(pays, "labels")
	return render_template("all_info.html",
							Brands = brands,
							Categories = categories, 
							Additives = additives, 
							Allergens = allergens,
							Traces = traces,
							Labels = labels)
	'''
@app.route('/data_aff/<data>')
def data_aff(data):
	return data


if __name__ == '__main__':
   app.run(debug = True)


