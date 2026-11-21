from fastapi import Form, Response, UploadFile
from app import app
from datetime import datetime
from pathlib import Path
from typing import Annotated
from utils import consts
from utils.pipe import pipe, pipe_async
from utils.res_bodies import err, log_err, not_found
from utils.validators import safe_path

# GET

def _list_files(dir: Path):
    return True, {
        'data': [{ 'name': p.name, 'isDir': p.is_dir() } for p in dir.iterdir()]
    }

def _valid_get(res: Response, path: str):
    validat = safe_path(path)

    if validat[0] == False:
        res.status_code = 400
        return False, err(validat[1])
    if not validat[1].exists():
        res.status_code = 404
        return False, not_found()
    if not validat[1].is_dir():
        res.status_code = 400
        return False, err('Not a directory')

    return True, (validat[1],)

@app.get('/api/files')
def read_filtered(res: Response, path: str = ''):
    return pipe(
        [_valid_get],
        _list_files,
        res, path
    )


# POST

async def _valid_post(
    res: Response,
    file: UploadFile,
    path: str
):
    validat = safe_path(path)

    if validat[0] == False:
        res.status_code = 400
        return False, err(validat[1])
    if not validat[1].exists():
        res.status_code = 404
        return False, err('Directory not found')
    
    return True, (res, file, validat[1])

async def _write_file(
    res: Response,
    file: UploadFile,
    where: Path
):
    now = datetime.now()
    filename = (
        file.filename or
        f'{ now.year }{ now.month }{ now.day }{ now.hour }{ now.minute }{ now.second }{ now.microsecond }'
    )
    path_w_name = where / Path(filename).name
    total_bytes = 0

    try:
        with path_w_name.open('wb') as buffer:
            while chunk := await file.read(consts.MB):
                total_bytes += len(chunk)
                if total_bytes > consts.MAX_FILE_SIZE:
                    path_w_name.unlink(missing_ok=True)

                    res.status_code = 413
                    return (
                        False,
                        err(f'File cannot exceed the { consts.MAX_FILE_SIZE / consts.MB } MB')
                    )
                buffer.write(chunk)
            return True, None
    except Exception as e:
        res.status_code = 500
        return False, log_err(e)
    finally:
        await file.close()

@app.post('/api/files')
async def create(
    res: Response,
    file: UploadFile,
    path: Annotated[str, Form()] = ''
):
    return await pipe_async(
        [_valid_post],
        _write_file,
        res, file, path
    )
