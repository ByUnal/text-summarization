FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

#It creates a working directory(app) for the Docker image and container
WORKDIR /app

# It will copy the remaining files and the source code
# from the host `fast-api` folder to the `app` container working directory
COPY . /app
COPY requirements.txt ./app

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# with CPU
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install requirements
RUN pip install -r requirements.txt

# CUDA 11.7
# RUN pip torch torchvision torchaudio

#It will expose the FastAPI application on port `8000` inside the container
EXPOSE 9073

CMD ["uvicorn", "main:app"]
