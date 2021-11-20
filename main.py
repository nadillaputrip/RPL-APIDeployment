import json
from fastapi import FastAPI, HTTPException, Body, Depends

from model import UserLoginSchema
from auth_bearer import JWTBearer
from auth_handler import signJWT

from unicodedata import name
with open("admin.json", "r") as read_file:
	data_admin = json.load(read_file)
with open("konten.json", "r") as read_file:
	data = json.load(read_file)
app = FastAPI()

@app.get('/', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
def root():
	return{'Dashboard Admin Look at Me': 'Konten'}

@app.get('/konten', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
async def get_all_konten():
	return data
	raise HTTPException(
		status_code=404, detail=f'Item not found'
	)

@app.get('/konten/{idkonten}', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
async def read_konten(idkonten: int):
	for konten_item in data['konten']:
		if konten_item['idKonten'] == idkonten:
			return konten_item
	raise HTTPException(
		status_code=404, detail=f'Konten tidak ditemukan'
	)

@app.post('/konten', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
async def add_konten(judul: str, deskripsi: str):
	id = 1
	if (len(data['konten']) > 0):
		id = data['konten'][len(data['konten'])-1]['idKonten']+1
	new_data = {'idKonten': id, 'judulKonten': judul, 'deskripsi': deskripsi}
	data['konten'].append(dict(new_data))
	
	read_file.close()
	with open("konten.json", "w") as write_file:
		json.dump(data, write_file, indent = 2)
	write_file.close()

	return(new_data)
	
	raise HTTPException(
		status_code=400, detail=f'Konten tidak dapat ditambahkan'
	)

@app.patch('/konten/{idkonten}', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
async def update_konten(idkonten: int, deskripsi: str):
	for konten_item in data['konten']:
		if konten_item['idKonten'] == idkonten:
			konten_item['deskripsi'] = deskripsi
			read_file.close()
			with open("konten.json", "w") as write_file:
				json.dump(data, write_file, indent = 2)
			write_file.close()

			return{"Konten berhasil diupdate"}
			
			raise  HTTPException(
				status_code=404, detail=f'Konten tidak ditemukan'
			)

@app.delete('/konten/{idkonten}', dependencies=[Depends(JWTBearer())], tags=['CRUD Konten'])
async def delete_konten(idkonten: int):
	for konten_item in data['konten']:
		if konten_item['idKonten'] == idkonten:
			data['konten'].remove(konten_item)
			read_file.close()
			with open("konten.json", "w") as write_file:
				json.dump(data, write_file, indent = 2)
			write_file.close()

			return{"Konten berhasil dihapus"}
			
			raise  HTTPException(
				status_code=404, detail=f'Konten tidak ditemukan'
			)

def check_user(data: UserLoginSchema):
    for user in data_admin['admin']:
        if user["username"] == data.username and user["password"] == data.password:
            return True
    return False

@app.post("/user/login", tags=["User"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Username atau password salah!"
    }