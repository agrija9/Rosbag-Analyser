from flask import Flask, render_template
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def firstPage():
    return render_template('index.html')

@app.route('/charts')
def create_chart():
    df = pd.read_csv(
        '/home/ragith/Documents/Study Material/SDP/Webpage-code/data.csv').drop('Open', axis=1)
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("charts.html", data=data)


@app.route('/test')
def testPage():
    return render_template("test.html")

@app.route('/contributors')
def contriPage():
    return render_template('contributors.html')

if __name__ == '__main__':
    app.run()
    
