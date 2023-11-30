from typing import Optional
from fastapi import APIRouter, FastAPI
import json


router_v1 = APIRouter(prefix='/api/energy/v1)

@router_v1.get("/res-forecast")
def get_res_forecast_v2():
    try:
        with open("./res-data/res_percentage.json") as file:
            data = json.load(file)
            for i in range(len(data)):
                beginningTimeStamp = data[i]["beginningTimeStamp"]
                position = int(beginningTimeStamp.split("T")[1].split(":")[0])
                data[i]["position"] = position
                data[i]["quantity"] = float(data[i]["value"].split("'")[1])

            ordered_data = []
            for i in range(len(data)):
                ordered_data.append(data[i])
            for datapoint in data:
                actual_position = datapoint["position"]
                ordered_data[actual_position] = datapoint

            return ordered_data
    except:
        pass

    return []

app = FastAPI()
app.include_router(router_v1)