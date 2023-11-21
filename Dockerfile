FROM python:3.10

WORKDIR /app

# Добавляем зависимости для библиотеки libGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы из текущей директории в контейнер
COPY . .

# Обновляем pip
RUN pip install --upgrade pip

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Определяем команду, которая будет запускаться при старте контейнера
CMD ["python", "main.py"]
