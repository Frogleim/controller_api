from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import controller
import time


class Good(BaseModel):
    shelf_number: int
    spiral_number: int


app = FastAPI()


@app.middleware("http")
async def whitelist_ips(request: Request, call_next):
    client_host = request.client.host
    # Only allow 0.0.0.0 to access this API
    if client_host != "0.0.0.0":
        return JSONResponse(status_code=403, content={"message": "Access forbidden"})
    response = await call_next(request)
    return response


@app.post('/get_goods/')
def goods(data: Good):
    print('-------------------')
    for i in range(8):
        response = controller.get_good(ndeck=data.shelf_number, ndisp=data.spiral_number)
        #        time.sleep(18)
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
