import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pandas as pd
from sqlalchemy import create_engine


def load_data(database_filepath):
    """
    INPUT:
    database_filepath - path to database
    OUTPUT
    X - pandas dataframe with variables
    y - pandas dataframes with prices
    """
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql("SELECT * FROM casas", engine)
    X = df[['apartments', 'houses', 'areas_sqm', 'quartos', 'Latitude', 'Longitude', 'CodPostal', 'Cod_Condition']]
    y = df[['Price']]
    return X, y

def build_model():
    pipeline = Pipeline([
    ('clf',RandomForestRegressor())
])
    params = {
        'clf__n_estimators':[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    }
    #create grid_search
    cv = GridSearchCV(pipeline, param_grid=params, verbose=3)
    return cv

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print('Random Forest accuracy is --> ', r2_score(y_test, y_pred) * 100)
    pass


def save_model(model, model_filepath):
    """
    save model
    INPUT:
    model: the trained model
    model_filepath: path to store the model
    OUTPUT:
    none
    """
    joblib.dump(model.best_estimator_, model_filepath, compress=3)
    pass


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, y_train.values.ravel())

        print('Evaluating model...')
        evaluate_model(model, X_test, y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the casas database ' \
              'as the first argument and the filepath of the pickle file to ' \
              'save the model to as the second argument. \n\nExample: python ' \
              'train_classifier.py ../data/casas.db casas.pkl')


if __name__ == '__main__':
    main()
