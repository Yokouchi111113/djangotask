FROM python:3.12-slim

WORKDIR /app

# Node.jsとPlaywrightに必要なライブラリをインストール
RUN apt-get update && apt-get install -y \
    curl \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nodeライブラリ
COPY config/package*.json ./
RUN npm install

# アプリをコピー
COPY . .

# Playwrightブラウザをインストール
RUN npx playwright install --with-deps 

WORKDIR /app/config

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]