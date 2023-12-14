=============DEPLOYED-LINK - https://sarthak-filesystem-fastapi.onrender.com/docs  (make take a minute to load)==========================


===============================================================================RUN-LOCALLY===========================================================================================================================

1)Clone the Repository:

2)Create a Virtual Environment: python -m venv venv

3)Activate the Virtual Environment: venv\Scripts\activate

4)Install Dependencies: pip install -r requirements.txt

5)Run the FastAPI Application:: uvicorn main:app --host 0.0.0.0 --port 8000 --reload







============================================================================OUTPUT-SCREENSHOTS====================================================================================================================

1)MKDIR

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/97d4ecf7-f11b-4a28-8dac-5376621357f0)

2)CD

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/86cfda23-bd68-4359-9390-8a5fa80a1eeb)

3)LS

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/259f4b59-d48b-469d-b0db-fa8471424a0e)

4)TOUCH

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/e3f2d95b-b2df-413e-8198-733d948769a4)

5)ECHO

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/96cdaa08-6fed-4b91-b62c-03d97cccaf44)

6)CAT

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/219dfcd8-14f5-4694-9d2c-4feca7397d60)

7)GREP

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/2e2ed7a1-b67c-4acd-839e-910fd649add7)


8)REMOVE

![image](https://github.com/sarthak37/memory-fastapi/assets/52873771/97d26961-31e8-4804-a4ed-8515522049a3)


===================================================================================================ABOUT=============================================================================================================

This code represents a basic implementation of a FastAPI application with a simple file system, and it includes unit tests for the defined routes. Let's break down the structure and functionality:

main.py: This is the main entry point of the FastAPI application. It creates a FastAPI instance and includes the router from the routes module.

filesystem.py: This module defines a FileSystem class, similar to the previous example. It includes methods to check the validity of paths, determine if a given path is a directory or file, get the parent and name of a path, join paths, and perform operations such as creating directories, files, moving, copying, etc.

routes.py: This module defines API routes using FastAPI's APIRouter. It uses the FileSystem class from filesystem.py to handle file system operations. Each route function corresponds to a specific HTTP endpoint and performs file system operations accordingly.

test_main.py: This file contains unit tests for the FastAPI routes defined in routes.py. It uses the TestClient from FastAPI to simulate HTTP requests and checks the responses.

The setUp method initializes the TestClient before each test.

Each test method corresponds to a specific route and checks the response status code and type.

For example, test_mkdir tests the /mkdir route, and it checks if the response status code is 200 and if the JSON response matches the expected message.

The __name__ == '__main__' block runs the unit tests when the script is executed directly.





