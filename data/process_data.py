import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(apart_filepath, houses_filepath):
    df_apart = pd.read_csv(apart_filepath, encoding = "utf-8", sep=';', header=0)
    df_houses = pd.read_csv(houses_filepath, encoding = "utf-8", sep=';', header=0)

    df_apart.rename({'#quartos': 'quartos'}, axis=1, inplace=True)
    df_houses.rename({'#quartos': 'quartos'}, axis=1, inplace = True)

    frames = [df_apart, df_houses]

    #unir dataframes
    df = pd.concat(frames)
    return df

def clean_data(df):
    var1 = pd.get_dummies(df['property_type'], prefix=['Apartments', 'Houses'])
    var1.rename(columns= {"['Apartments', 'Houses']_Apartments": 'apartments', "['Apartments', 'Houses']_Houses": 'houses'}, inplace = True)

    df = df.drop(['property_type', 'Tipology', 'Condition', 'Location2'],axis=1)
    return df

def save_data(df, database_filename):
    engine = create_engine('sqlite:///casas.db')
    df.to_sql('casas', engine, index=False)
    pass

def main():
    if len(sys.argv) == 4:

        apart_filepath, houses_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(apart_filepath, houses_filepath))
        df = load_data(apart_filepath, houses_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories ' \
              'datasets as the first and second argument respectively, as ' \
              'well as the filepath of the database to save the cleaned data ' \
              'to as the third argument. \n\nExample: python process_data.py ' \
              'dados_apartamentos.csv houses_dados.csv ' \
              'casas.db')


if __name__ == '__main__':
    main()
