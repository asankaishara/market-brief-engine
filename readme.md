## Set python in Intelij Idea
- Project Structure ->  Project Settings -> Project,
  - set, SDK: select the <path>\market-brief-engine\.venv
- Platform Settings -> SDKs, remove java 25, only keep python .venv
- Once this is done, when you open terminal in intelij idea, it will automatically activate the python environment

## Install python dependencies
- Upgrade pip -> python -m pip install --upgrade pip
- Install requirements -> pip install -r requirements.txt

## Run the FastAPI app using uvicorn
- uvicorn app.main:app --reload
- application swagger url: http://127.0.0.1:8000/docs

## Run DB server
- Make sure docker desktop is up and running
- Run ```docker compose up -d```
- Verify the container ```docker compose ps```

