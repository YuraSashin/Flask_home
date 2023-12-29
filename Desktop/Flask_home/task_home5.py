from pydantic import BaseModel
import os
import json
from pathlib import Path
import aiofiles
from pydantic import TypeAdapter
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

class Song(BaseModel):
    id: int
    name: str
    author: str
    description: str | None = None
    genre: str

BASE_DIR = Path(__file__).resolve().parent
json_file = os.path.join(BASE_DIR, 'data.json')
if not os.path.exists(json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
with open(json_file, encoding='utf-8') as f:
    json_data = json.load(f)

app = FastAPI()
templates = Jinja2Templates('templates')
type_adapter = TypeAdapter(Song)
video: list[Song] = [type_adapter.validate_python(song) for song in json_data]

async def commit_changes():
    async with aiofiles.open(json_file, 'w', encoding='utf-8') as f:
        json_video = [song.model_dump(mode='json') for song in video]
        content = json.dumps(json_video, ensure_ascii=False, indent=2)
        await f.write(content)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'video': video})

@app.post('/video/')
async def add_song(song: Song):
    video.append(song)
    await commit_changes()
    return song

@app.get('/video/{song_id}', response_class=HTMLResponse)
async def get_song(request: Request, song_id: int):
    filtered_songs = [song for song in video if song.id == song_id]
    if not filtered_songs:
        song = None
    else:
        song = filtered_songs[0]
    return templates.TemplateResponse('song.html', {'request': request, 'song': song})

@app.put('/video/{song_id}')
async def update_song(song_id: int, new_song: Song):
    filtered_songs = [song for song in video if song.id == song_id]
    if not filtered_songs:
        return {'updated': False}
    song = filtered_songs[0]
    song.name = new_song.name
    song.author = new_song.author
    song.description = new_song.description
    song.genre = new_song.genre
    await commit_changes()
    return {'updated': True, 'song': new_song}

@app.delete('/video/{song_id}')
async def delete_song(song_id: int):
    filtered_songs = [song for song in video if song.id == song_id]
    if not filtered_songs:
        return {'deleted': False}
    song = filtered_songs[0]
    video.remove(song)
    await commit_changes()
    return {'deleted': True, 'song': song}