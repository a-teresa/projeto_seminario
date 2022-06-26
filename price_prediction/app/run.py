import plotly
import numpy as np
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
import joblib
import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import json # library to handle JSON files
from flask import Flask, render_template,request


app = Flask(__name__)

# load data
engine = create_engine('sqlite:///../data/casas.db')
df = pd.read_sql("SELECT * FROM casas", engine)

# load model
model = joblib.load("../models/casas.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
def home():
    return render_template('master.html')
# web page that handles user query and displays model results
@app.route('/predict', methods=['POST'])
def predict():
    # save user input in query
    int_features = [float(x) for x in request.form.values()]
    final = [np.array(int_features)]

    # use model to predict for query
    prediction = model.predict(final)
    output = round(prediction[0], 2)
    # This will render the go.html Please see that file.
    return render_template(
        'master.html',
        query=final,
        prediction_text='The price prediction is: {}€'.format(output)
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()