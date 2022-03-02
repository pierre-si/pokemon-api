import requests

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/pokemon/{pokemon_name}")
async def root(pokemon_name):
    species = requests.get("https://pokeapi.co/api/v2/pokemon-species/{}/".format(pokemon_name))
    if species.status_code != 200:
        raise HTTPException(status_code=species.status_code, detail=species.text)
    
    species = species.json()
    for name in species["names"]:
        if name["language"]["name"] == "en":
            break
    for description in species["flavor_text_entries"]:
        if description["language"]["name"] == "en":
            break
    return {
        "name": name["name"],
        "description": description["flavor_text"],
        "habitat": species["habitat"]["name"],
        "is_legendary": species["is_legendary"],
    }

@app.get("/pokemon/translated/{pokemon_name}")
async def translated(pokemon_name):
    result = await root(pokemon_name)

    if result["habitat"] == 'cave' or result["is_legendary"]:
        translate = translate_yoda
    else:
        translate = translate_shakespeare

    return {key: translate(value) for key, value in result.items()}

def translate_yoda(text):
    res = requests.post("https://api.funtranslations.com/translate/yoda.json", data={"text": text})
    if res.status_code != 200:
        return text
    else:
        return res.json()["contents"]["translated"]

def translate_shakespeare(text):
    res = requests.post("https://api.funtranslations.com/translate/shakespeare.json", data={"text": text})
    if res.status_code != 200:
        return text
    else:
        return res.json()["contents"]["translated"]
