# Python Flask RESTful tutorial

Following along with the courses at [Percipio: Track 4: Building Restful Web Services with Python](https://leidos.percipio.com/track/9ca289af-b509-4ba0-af0e-74468f3254ef)

This git repo picks up at [Flask-RESTful: Integrating the API Server with a MySQL Database](https://leidos.percipio.com/courses/ff307df7-22fc-4ef5-9d4b-f0349e09bff3)

### Initial setup:

#### Install virtual environment
```sh
export VENV_TARGET=".venv"
python -m venv ${VENV_TARGET}
source ${VENV_TARGET}/bin/activate
```
#### Set Python Interpreter in VS Code
- Help > Show All Commands
- Python: Select Interpreter
- choose the one inside your .venv/ directory
- this will help with linting and such
#### Install dependencies
```sh
pip install flask-restful
```
#### Verify dependencies
At the bash command prompt, type `python` to enter into the interpreter. Then:
```python
import flask
import flask_restful
import importlib
importlib.metadata.version("flask")
# you should see '3.0.0'
importlib.metadata.version("flask-restful")
# you should see '0.3.10'
exit()
```
#### Ensure `curl`
Make sure you have `curl` installed: `curl -h`

At this point, you should be ready to pick up with the tutorial wherever you left off.

#### MySQL
If the tutorial requires a local MySQL server to already be present, first, follow the instructions at [this video](https://leidos.percipio.com/courses/ff307df7-22fc-4ef5-9d4b-f0349e09bff3/videos/0123a499-e9a4-4b33-984b-beba59d5f96c) which walks through the MySQL installation process for MacOS.

In short:
- download and install MySQL Server
- download and install MySQL Workbench
- make sure the workbench version and the server version are compatible
- open up your workbench and establish the following using a simple script:
  ```sql
  create database bookshop;
  use bookshop;
  show tables;
  ```
- there will be no tables to see, at present, as these are created programmatically via SQLAlchemy and Flask
- see [CreatingTables](./CreatingTables/creating_tables.py) for more detail, and be sure that you have installed the necessary packages, too:
  ```sh
  pip install mysql-connector-python
  pip install Flask-SQLAlchemy
  ```
