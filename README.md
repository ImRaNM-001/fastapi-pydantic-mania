# fastapi-pydantic-rules
starting with a new project on fastapi &amp; pydantic for data validation

> ### commands used
uv --version
uv venv
source .venv/bin/activate
uv init
uv add pytest
uv add fastapi
uv add uvicorn
uv add email-validator

> ### to synchronize the project's virtual environment with the dependencies defined in the project's lock file (uv.lock) or pyproject.toml.
uv sync     

### check existing libs version
python3 -c "import fastapi; print(fastapi.__version__)"
0.116.1


### start FastAPI server
uvicorn 06-dependency_injection_fastapi.user_signup:app --reload

and hit, 
http://localhost:8000/docs



