import sqlalchemy
import pandas as pd

def KauflandDB():
    engine = sqlalchemy.create_engine(f"mysql://root:@localhost/kaufland")
    con = engine.connect()

    return con

def Hochladen(data, con, name):
    if isinstance(data, dict):
        df = pd.DataFrame(data)
        df.to_sql(name=name, con=con, if_exists='append')