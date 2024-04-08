from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import controller
import time

class Good(BaseModel):
    shelf_number: int
    spiral_number: int


def bytes_translator(shelf, spiral):
    number = 5
    d = b'0xnumber'
    shelf_bytes = bytes(f'{shelf:02X}', 'utf-8')
    index = d.index(b'number')
    translated_shelf = d[:index] + shelf_bytes + d[index + len(b'number'):]
    # Translate spiral to bytes
    spiral_bytes = bytes(f'{spiral:02X}', 'utf-8')
    index = d.index(b'number')
    translated_spiral = d[:index] + spiral_bytes + d[index + len(b'number'):]
    
    return translated_shelf, translated_spiral

app = FastAPI()

@app.post('/get_goods/')
def goods(data: Good):
    print('-------------------')
    for i in range(15):
        response = controller.get_good(ndeck=data.shelf_number, ndisp=data.spiral_number)
#        time.sleep(18)
        if b"\x1a" in response:
            return {'Response': response}
        else:
            raise HTTPException(status_code=400, detail="Controller error")
