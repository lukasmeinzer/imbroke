import sqlalchemy
import pandas as pd

def KauflandDB():
    engine = sqlalchemy.create_engine(f"mysql://root:@localhost/kaufland")
    con = engine.connect()

    return con


def EdekaDB():
    engine = sqlalchemy.create_engine(f"mysql://root:@localhost/kaufland")
    con = engine.connect()

    return con


def AldiSuedDB():
    engine = sqlalchemy.create_engine(f"mysql://root:@localhost/aldi_sued")
    con = engine.connect()

    return con


def Hochladen(data, con, name: str):
    if isinstance(data, dict):
        df = pd.DataFrame(data)
        df.to_sql(name=name, con=con, if_exists='append')
    if isinstance(data, pd.DataFrame):
        data.to_sql(name=name, con=con, if_exists='append')