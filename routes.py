from fastapi import APIRouter, HTTPException, Query
from filesystem import FileSystem
from io import BytesIO
import re



router = APIRouter()
fs = FileSystem()

@router.post("/mkdir")
def mkdir(path: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    if path in fs.fs:  # Access the fs attribute of the FileSystem object
        raise HTTPException(status_code=400, detail="Path already exists")
    parent = fs.get_parent(path)
    name = fs.get_name(path)
    if not fs.is_directory(parent):
        raise HTTPException(status_code=400, detail="Parent directory does not exist or is not a directory")
    fs.fs[path] = set()
    fs.fs[parent].add(name)
    return {"message": "Directory created successfully"}

@router.post("/cd")
def cd(path: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    if not fs.is_directory(path):
        raise HTTPException(status_code=400, detail="Path does not exist or is not a directory")
    fs.current_dir = path
    return {"message": "Current directory changed successfully"}
    
@router.get("/ls")
def ls(path: str = Query(None, regex="/[\\w/.-]*")):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    if not fs.is_directory(path):
        raise HTTPException(status_code=400, detail="Path does not exist or is not a directory")
    subpaths = list(fs.fs[path])  # Access the fs attribute of the FileSystem object
    subpaths.sort()
    return subpaths

@router.get("/grep")
def grep(path: str, pattern: str):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    if not fs.is_file(path):
        raise HTTPException(status_code=400, detail="Path does not exist or is not a file")
    file = fs.fs[path]
    file.seek(0)
    matches = [line.decode() for line in file if re.search(pattern, line.decode())]
    return matches

@router.get("/cat")
def cat(path: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    if not fs.is_file(path):
        raise HTTPException(status_code=400, detail="Path does not exist or is not a file")
    contents = fs.fs[path].getvalue().decode("utf-8")
    return {"contents": contents}

@router.post("/touch")
def touch(path: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    if path in fs.fs:  # Access the fs attribute of the FileSystem object
        raise HTTPException(status_code=400, detail="Path already exists")
    parent = fs.get_parent(path)
    name = fs.get_name(path)
    if not fs.is_directory(parent):
        raise HTTPException(status_code=400, detail="Parent directory does not exist or is not a directory")
    fs.fs[path] = BytesIO()
    fs.fs[parent].add(name)
    return {"message": "File created successfully"}

@router.post("/echo")
def echo(path: str = Query(..., regex="/[\\w/.-]+"), data: str = Query(...)):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    if not fs.is_file(path):
        raise HTTPException(status_code=400, detail="Path does not exist or is not a file")
    fs.fs[path].seek(0)
    fs.fs[path].truncate()
    fs.fs[path].write(data.encode("utf-8"))
    return {"message": "Data written to file successfully"}

@router.post("/mv")
def mv(source: str = Query(..., regex="/[\\w/.-]+"), destination: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    source = fs.join_paths(fs.current_dir, source)  # Use the join_paths method
    destination = fs.join_paths(fs.current_dir, destination)  # Use the join_paths method
    if source not in fs.fs:
        raise HTTPException(status_code=400, detail="Source path does not exist")
    if destination in fs.fs:
        raise HTTPException(status_code=400, detail="Destination path already exists")
    source_parent = fs.get_parent(source)
    source_name = fs.get_name(source)
    destination_parent = fs.get_parent(destination)
    destination_name = fs.get_name(destination)
    if not fs.is_directory(source_parent):
        raise HTTPException(status_code=400, detail="Source parent directory does not exist or is not a directory")
    if not fs.is_directory(destination_parent):
        raise HTTPException(status_code=400, detail="Destination parent directory does not exist or is not a directory")
    fs.fs[destination] = fs.fs.pop(source)
    fs.fs[source_parent].remove(source_name)
    fs.fs[destination_parent].add(destination_name)
    return {"message": "Path moved successfully"}

@router.post("/cp")
def cp(source: str = Query(..., regex="/[\\w/.-]+"), destination: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    source = fs.join_paths(fs.current_dir, source)  # Use the join_paths method
    destination = fs.join_paths(fs.current_dir, destination)  # Use the join_paths method

    if not fs.is_file(source):
        raise HTTPException(status_code=400, detail="Source path does not exist or is not a file")
    if destination in fs.fs:
        raise HTTPException(status_code=400, detail="Destination path already exists")

    source_parent = fs.get_parent(source)
    source_name = fs.get_name(source)
    destination_parent = fs.get_parent(destination)
    destination_name = fs.get_name(destination)

    if not fs.is_directory(source_parent):
        raise HTTPException(status_code=400, detail="Source parent directory does not exist or is not a directory")
    if not fs.is_directory(destination_parent):
        raise HTTPException(status_code=400, detail="Destination parent directory does not exist or is not a directory")

    fs.fs[destination] = BytesIO(fs.fs[source].getvalue())
    fs.fs[destination_parent].add(destination_name)

    return {"message": "Path copied successfully"}
    
@router.delete("/remove")
def remove(path: str = Query(..., regex="/[\\w/.-]+")):
    global fs  # Use the global fs object
    path = fs.join_paths(fs.current_dir, path)  # Use the join_paths method
    try:
        fs.remove_path(path)
        return {"message": "Path removed successfully"}
    except HTTPException as e:
        return {"error": str(e)}    
