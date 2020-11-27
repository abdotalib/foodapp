from flask import Flask, redirect, url_for, render_template, request
import pandas as pd

countries = []
categories = []
allergens = []
countries_data = pd.read_json('https://world.openfoodfacts.org/data/taxonomies/countries.json')
categories_data = pd.read_json('https://world.openfoodfacts.org/categories.json')
allergens_data = pd.read_json('https://world.openfoodfacts.org/data/taxonomies/allergens.json')


for i in range(len(countries_data.columns)):
	d = countries_data.columns[i]
	countries.append(d[3:])

for i in range(len(categories_data)):
	d = categories_data['tags'][i]
	d = d['id']
	categories.append(d[3:])

for i in range(len(allergens_data.columns)):
	d = allergens_data.columns[i]
	allergens.append(d[3:])


app = Flask(__name__)


@app.route('/index', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        countrie = 'en:'+request.form['Countries']
        categorie = request.form['Categories']
        allergen = request.form['Allergens']
        return  redirect(url_for('test', pays = countries_data[str(countrie)]['country_code_3'], categ = str(categorie), allerg = str(allergen)))
    return render_template("index.html", Countries = countries, Countries_len = len(countries), Categories = categories, Categories_len = len(categories), Allergens = allergens, Allergens_len = len(allergens))

@app.route('/test/<pays>/<categ>/<allerg>')
def test(pays, categ, allerg):
	return pays+categ+allerg
	


if __name__ == '__main__':
   app.run(debug = True)