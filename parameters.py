from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id" : item_id}

# the order is important so we need to define the paths in order
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Usin
# g the same parameter 2 times it makes no sense if they are using the same path parameters to be called

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet": # pretty cool that enum support this :)
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

#pretty cool my first interaction with fastapi
#:)

# Now lets take a look at query parameters

fake_items_db = [{"item_name" : "Foo"}, {"item_name" : "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int =10):
    return fake_items_db[skip: skip + limit]

#now optional query parameters

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q":q}
    return {"item_id": item_id}

# so what about query parameters that are not optional just avoid to put a default value
# and for  items that are bool values a lot items are taken as bool like
# [1, True, true, on , yes]

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q":q})
        if not short:
            item.update(
                {"description": "This is an amazing item that has a long description"}
            )
        return item

# So until now we see 2 types of ways to send data
#path parameters
#and query paramethers

