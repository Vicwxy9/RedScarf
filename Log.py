import datetime

def log(str:str):
    datetime_object = datetime.datetime.now()
    print(f'[{datetime_object} INFO] {str}')