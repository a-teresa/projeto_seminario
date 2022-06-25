import json
import plotly
import pandas as pd
import re
from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
import joblib
import numpy as np # library to handle data in a vectorized manner
import plotly.graph_objects as go
import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

import folium # map rendering library
import math

app = Flask(__name__)

# load data
engine = create_engine('sqlite:///../data/casas.db')
df = pd.read_sql("SELECT * FROM casas", engine)

# load model
model = joblib.load("../models/casas.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    global df
    df_apart = df[df['apartments'] == 1]
    df_houses = df[df['apartments'] == 0]
    price_by_room_houses = df_houses.groupby(['quartos']).mean()['Price'].sort_values()
    price_by_room_apartments = df_apart.groupby(['quartos']).mean()['Price'].sort_values()


    # create visuals
    # TODO: Below is an example - modify to create your own visuals

    graphs = [
        {
            'data': [
                Bar(
                    x=price_by_room_houses,

                )
            ],

            'layout': {
                'title': 'Prices by typology (houses)',
                'yaxis': {
                    'title': "Prices"
                },
                'xaxis': {
                    'title': "typology"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=price_by_room_apartments,
                )
            ],

            'layout': {
                'title': 'Prices by typology (Apartments)',
                'yaxis': {
                    'title': "prices"
                },
                'xaxis': {
                    'title': "typology"
                }
            }
        }
    ]



    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '')

    # use model to predict classification for query
    casas_labels = model.predict([query])[0]
    casas_results = dict(zip(df.columns[5:], casas_labels))

    # This will render the go.html Please see that file.
    return render_template(
        'go.html',
        query=query,
        casas_result=casas_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
