from pandas import read_csv
from sqlalchemy import create_engine

engine =create_engine('sqlite:///api_db.sqlite3')

def excercises_to_sql(csv_file_path, engine):
    
    with open(csv_file_path, 'r') as file:
        data_df = read_csv(file,names=["name", "link", "muscle", "sub_muscle"]
                        ,index_col=False)
        data_df["muscle"] = 21
        data_df["sub_muscle"] = 23
        print(data_df)
        data_df.to_sql('exercises', con=engine, index=False, index_label='id', if_exists='append')

def get_links(csv_file_path: str) -> tuple:
     with open(csv_file_path, 'r') as file:
        data_df = read_csv(file,names=["name", "link"])
        links = tuple(data_df["link"])
        return links
        
        #data_df.to_sql('exercises', con=engine, index=False, index_label='id', if_exists='append')

if __name__ == "__main__":
    excercises_to_sql('app/api/abs/kosie.csv', engine)
    get_links('app/api/abs/kosie.csv', engine)