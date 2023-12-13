import unittest
from fastapi.testclient import TestClient
from main import app

class TestFileSystemRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_mkdir(self):
        response = self.client.post("/mkdir", data={"path": "/test_directory"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Directory created successfully"})

    def test_cd(self):
        response = self.client.post("/cd", data={"path": "/test_directory"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Current directory changed successfully"})

    def test_ls(self):
        response = self.client.get("/ls")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_grep(self):
        response = self.client.get("/grep", params={"path": "/test_file", "pattern": "example"})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_cat(self):
        response = self.client.get("/cat", params={"path": "/test_file"})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_touch(self):
        response = self.client.post("/touch", data={"path": "/test_file"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "File created successfully"})

    def test_echo(self):
        response = self.client.post("/echo", data={"path": "/test_file", "data": "Hello, World!"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Data written to file successfully"})

    def test_mv(self):
        response = self.client.post("/mv", data={"source": "/test_file", "destination": "/new_path"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Path moved successfully"})

    def test_cp(self):
        response = self.client.post("/cp", data={"source": "/test_file", "destination": "/copy_file"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Path copied successfully"})

if __name__ == '__main__':
    unittest.main()
