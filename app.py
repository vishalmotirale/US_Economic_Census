from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

API_KEY = os.environ.get("CENSUS_API_KEY")

@app.route('/censusapp', methods=['POST'])
def get_censusdata():
    year = request.form.get('year')
    url = f'https://api.census.gov/data/{year}/ecnbasic'
    naics_var = f"NAICS{year}"

    param = {
        'get': f'{naics_var},{naics_var}_LABEL,EMP,ESTAB,NAME',
        naics_var: request.form.get('naics'),
        'for': request.form.get('geo'),
        'key': API_KEY
    }

    response = requests.get(url, params=param)
    data = response.json()

    headers = data[0]
    values = data[1:]

    return render_template("result.html", header=headers, values=values, year=year)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
