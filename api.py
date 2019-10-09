from flask import Flask, render_template
from flask import request, jsonify
import json
import sqlite3
import pandas as pd
app = Flask(__name__)
app.config["DEBUG"] = True

with open('foods.json','r',encoding="utf-8") as json_file:
	foods = json.load(json_file)

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

@app.route('/', methods=['GET'])
def main():
	return render_template('index.html')

@app.route('/api/v1/resources/foods/all', methods=['GET'])
def api_all():
	conn = sqlite3.connect('foods.db')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	all_foods = cur.execute('SELECT * FROM foods;').fetchall()
	return jsonify(all_foods)

@app.route('/api/v1/resources/foods', methods=['GET'])
def api_filter():
	query_parameters = request.args

	name = query_parameters.get('name')
	fat = query_parameters.get('fat')
	calories = query_parameters.get('calories')
	proteins = query_parameters.get('proteins')
	carbohydrates = query_parameters.get('carbohydrates')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/tools/calories-burned',methods=['POST','GET'])
def process():
	# Calculate BMI
	weight_in_kg = float(request.form['Weight'])
	height_in_centimeters = float(request.form['height'])
	height_in_meters = height_in_centimeters / 100
	BMI = str(weight_in_kg / (height_in_meters * height_in_meters))
	bmi = float(BMI)
	if bmi <= 18.5:
		how_to_say_bmi =  {'output':'You are Under weight as your bmi is: ' + BMI}
	elif (bmi >=18.5) and (bmi <=24.9):
		how_to_say_bmi =  {'output':'Perfect!You have normal weight and your bmi is : '+ BMI}
	elif bmi >=25 and bmi <=29.9:
		how_to_say_bmi =  {'output':'You are Overweight as your bmi is: ' + BMI}
	elif bmi>=30:
		how_to_say_bmi =  {'output':'You are highly obese as your bmi is: ' + BMI}
	else :
		how_to_say_bmi =  {'output':'and your bmi is : '+ BMI}

	# Calculate Calories Burned
	sex = request.form['sex']
	age = float(request.form['age'])
	lifestyle = request.form['lifestyle']
	if sex=='F':
		rmr = 655 + 9.6 * weight_in_kg + 1.8 * height_in_centimeters - 4.7 * age
		if lifestyle == '0':
			rmr = 1.2 * rmr
		elif lifestyle == '1':
			rmr = 1.3 * rmr
		elif lifestyle == '2':
			rmr = 1.4 * rmr
		elif lifestyle == '3':
			rmr = 1.5 * rmr
		elif lifestyle == '4':
			rmr = 1.6 * rmr
		elif lifestyle == '5':
			rmr = 1.7 * rmr
		elif lifestyle == '6':
			rmr = 1.8 * rmr
		else:
			rmr = 2.0 * rmr
	elif sex =='M':
		rmr = 66 + 13.7 * weight_in_kg + 5 * height_in_centimeters - 6.8 * age
		if lifestyle == '0':
			rmr = 1.2 * rmr
		elif lifestyle == '1':
			rmr = 1.3 * rmr
		elif lifestyle == '2':
			rmr = 1.4 * rmr
		elif lifestyle == '3':
			rmr = 1.5 * rmr
		elif lifestyle == '4':
			rmr = 1.7 * rmr
		elif lifestyle == '5':
			rmr = 1.8 * rmr
		elif lifestyle == '6':
			rmr = 2.1 * rmr
		else:
			rmr = 2.3 * rmr
	RMR = str(rmr)
	how_to_say_rmr = {'Your Calories Burned': RMR}

	# Get the nutrients needed
	nutrient_data = pd.read_csv('Recommended_nutrients.csv', dtype=str)
	if age <= 8:
		if age < 1:
			# INFANT
			row_begin = 0 
			if age < 0.5:
				nutr = nutrient_data.iloc[row_begin][2:]
			else:
				nutr = nutrient_data.iloc[row_begin+1][2:]
		else:
			# CHILD
			row_begin = 2
			if age <= 3:
				nutr = nutrient_data.iloc[row_begin][2:]
			else:
				nutr = nutrient_data.iloc[row_begin+1][2:]
	else:
		if sex == 'M':
			# MALE
			row_begin = 4
			if age <= 13:
				nutr = nutrient_data.iloc[row_begin][2:]
			elif age <= 18:
				nutr = nutrient_data.iloc[row_begin+1][2:]
			elif age <= 30:
				nutr = nutrient_data.iloc[row_begin+2][2:]
			elif age <= 50:
				nutr = nutrient_data.iloc[row_begin+3][2:]
			elif age <= 70:
				nutr = nutrient_data.iloc[row_begin+4][2:]
			else:
				nutr = nutrient_data.iloc[row_begin+5][2:]
		else:
			# FEMALE
			row_begin = 10
			if age <= 13:
				nutr = nutrient_data.iloc[row_begin][2:]
			elif age <= 18:
				nutr = nutrient_data.iloc[row_begin+1][2:]
			elif age <= 30:
				nutr = nutrient_data.iloc[row_begin+2][2:]
			elif age <= 50:
				nutr = nutrient_data.iloc[row_begin+3][2:]
			elif age <= 70:
				nutr = nutrient_data.iloc[row_begin+4][2:]
			else:
				nutr = nutrient_data.iloc[row_begin+5][2:]
	nutrie_dict = {'data': [nutr.to_dict()]}

	return  jsonify(how_to_say_bmi, how_to_say_rmr, nutrie_dict)

@app.route('/showSignUp', methods=['POST','GET'])
def foodCalculator():
	food = request.form['']

app.run();
