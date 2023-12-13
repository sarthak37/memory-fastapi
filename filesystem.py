from io import BytesIO
import os
import re



class FileSystem:
    def __init__(self):
        self.fs = {"/": set()}
        self.current_dir = "/"

    def is_valid_path(self, path):
        return path.startswith("/") and not re.search(r"[^\w/.-]", path)

    def is_directory(self, path):
        return path in self.fs and isinstance(self.fs[path], set)

    def is_file(self, path):
        return path in self.fs and isinstance(self.fs[path], BytesIO)

    def get_parent(self, path):
        if path == "/":
            return None
        else:
            return os.path.dirname(path)

    def get_name(self, path):
        if path == "/":
            return "/"
        else:
            return os.path.basename(path)

    def join_paths(self, path1, path2):
        if path2.startswith("/"):
            return path2
        else:
            return os.path.join(path1, path2)

    def remove_path(self, path):
        if path == "/":
            raise HTTPException(status_code=400, detail="Cannot remove root directory")
        if path not in self.fs:
            raise HTTPException(status_code=400, detail="Path does not exist")

        parent = self.get_parent(path)
        name = self.get_name(path)

        if self.is_file(path):
            del self.fs[path]
            self.fs[parent].remove(name)
        elif self.is_directory(path):
            for subpath in list(self.fs[path]):
                subpath_full = self.join_paths(path, subpath)
                self.remove_path(subpath_full)
            del self.fs[path]
            self.fs[parent].remove(name)        
