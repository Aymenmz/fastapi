FROM python:3.12

WORKDIR /usr/src/app

# 👇 Install netcat explicitly (no more virtual package error)
RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
