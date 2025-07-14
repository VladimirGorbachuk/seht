# project theme
miniproject for warehouse control (microservice sample)


# to start work locally
python -m venv venv
venv\Scripts\activate.bat
source venv/bin/activate
pip install uv
uv pip install -e ./src/wh_control
uv pip install -e ./src/wh_control[tests]
uv pip install -e ./src/wh_control[lint]


# with docker
docker-compose up --build