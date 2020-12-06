from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import requests

def list_data(per1, per2):
	temp = []
	data = pd.read_json('https://{}.openfoodfacts.org/{}.json'.format(per1, per2))
	for i in range(len(data)):
		d = data['tags'][i]
		d = d['id']
		temp.append(d[3:])
	return temp
	 
countries = []



countries_data = pd.read_json('https://world.openfoodfacts.org/data/taxonomies/countries.json')



for i in range(len(countries_data.columns)):
	d = countries_data.columns[i]
	countries.append(d[3:])

app = Flask(__name__)
@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        countrie = 'en:'+request.form['Countries']
        pay = countries_data[str(countrie)]['country_code_3']
        return redirect(url_for('search', pays = pay['en']))
    return render_template("index.html", Countries = countries, Countries_len = len(countries))

#, Categories = categories, Categories_len = len(categories), Allergens = allergens, Allergens_len = len(allergens)
@app.route('/search/<pays>', methods = ['POST', 'GET'])
def search(pays):
	if request.method == 'POST':
		key_world = request.form['search']
		url = "https://"+str(pays)+".openfoodfacts.org/cgi/search.pl?search_terms="+str(key_world)+"&search_simple=1&action=process&json=1"
		payload = {}
		headers= {}
		response = requests.request("GET", url, headers=headers, data = payload)
		data =  response.text.encode('utf8')#pd.read_json()
		return redirect(url_for('data_aff', data = data))	
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

