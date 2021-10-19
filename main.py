import json
from fastapi import FastAPI, HTTPException, Body, Depends

from model import UserSchema, UserLoginSchema
from auth_bearer import JWTBearer
from auth_handler import signJWT

from unicodedata import name
with open("menu.json", "r") as read_file:
	data = json.load(read_file)
app = FastAPI()

@app.get('/')
def root():
	return{'Hello': 'World'}

@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			return menu_item
	raise HTTPException(
		status_code=404, detail=f'Item not found'
	)

@app.post('/menu')
async def add_menu(name: str):
	id = 1
	if (len(data['menu']) > 0):
		id = data['menu'][len(data['menu'])-1]['id']+1
	new_data = {'id': id, 'name': name}
	data['menu'].append(dict(new_data))
	
	read_file.close()
	with open("menu.json", "w") as write_file:
		json.dump(data, write_file, indent = 2)
	write_file.close()

	return(new_data)
	
	raise HTTPException(
		status_code=400, detail=f'Unsuccessful'
	)

@app.put('/menu/{item_id}')
async def update_menu(item_id: int, name: str):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			menu_item['name'] = name
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(data, write_file, indent = 2)
			write_file.close()

			return{"message": "Your update was saved"}
			
			raise  HTTPException(
				status_code=404, detail=f'Item not found'
			)

@app.delete('/menu/{item_id}')
async def delete_menu(item_id: int):
	for menu_item in data['menu']:
		if menu_item['id'] == item_id:
			data['menu'].remove(menu_item)
			read_file.close()
			with open("menu.json", "w") as write_file:
				json.dump(data, write_file, indent = 2)
			write_file.close()

			return{"message": "Your delete was saved"}
			
			raise  HTTPException(
				status_code=404, detail=f'Item not found'
			)

user = {
    "username": "asdf",
    "password": "asdf"
}

def check_user(data: UserLoginSchema):
    if user.username == data.username and user.password == data.password:
        return True

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Wrong login details!"
    }