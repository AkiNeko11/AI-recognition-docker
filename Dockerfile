FROM python:3.12.4-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
        libgomp1 \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


# 安装你实际需要的依赖
RUN pip install --no-cache-dir \
    numpy \
    pillow \
    pyyaml \
    requests \
    tqdm \
    flask \
    flask-cors

# 安装headless版本的OpenCV
RUN pip install --no-cache-dir opencv-python-headless

# 安装CPU版本的PyTorch
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# 安装ultralytics（不安装依赖）
RUN pip install --no-cache-dir ultralytics --no-deps

# 复制应用代码
COPY . .
RUN mkdir -p uploads

EXPOSE 5000
CMD ["python", "app.py"]