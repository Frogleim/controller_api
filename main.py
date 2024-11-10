from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import controller
import time


class Good(BaseModel):
    shelf_number: int
    spiral_number: int


app = FastAPI()




@app.post('/get_goods/')
def goods(data: Good):
    print('-------------------')
    for i in range(8):
        response = controller.get_good(ndeck=data.shelf_number, ndisp=data.spiral_number)
        #        time.sleep(18)
        print(data.shelf_number, data.spiral_number)
        if b"\x1a" in response:
            return {'Response': response}
        else:
            raise HTTPException(status_code=400, detail="Controller error")


@app.post('/turn_up/')
def turn_up(data: Good):
    print('-------------------')
    for i in range(15):
        response = controller.get_good(ndeck=data.shelf_number, ndisp=data.spiral_number)
        #        time.sleep(18)
        if b"\x1a" in response:
            return {'Response': response}
        else:
            raise HTTPException(status_code=400, detail="Controller error")
