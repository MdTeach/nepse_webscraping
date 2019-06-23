from flask import Flask
import json
from utils.nepse_scarping import NepseData 

app = Flask(__name__)
nepse_data = NepseData()

data = "" 

@app.route('/')
def home():
    #data = nepse_data.getAllData()
    return data

if __name__ == "__main__":
    data = json.dumps(nepse_data.getAllData())
    print(data)
    app.run()
