# Docker를 활용해보자!!
# Feat. GPT
# 1. Python 3.10 version
FROM python:3.10-slim

# 2. Work Folder
WORKDIR /app

# 3. Copy Project
COPY . .

# 4. Install Library
RUN pip install --upgrade pip && \
    pip install pandas requests tqdm matplotlib notebook numpy

# 5. Jupyter Notebook 실행 명령어
CMD ["jupyter","notebook","--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]