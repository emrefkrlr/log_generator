import os
import random
import gzip
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Konfigürasyon
ANOMALY_IPS = ["192.168.100.100", "10.0.0.99"]
ANOMALY_TRAFFIC_COUNT = 1000
NORMAL_TRAFFIC_COUNT = 2000
LOG_SIZE_LIMIT = 200 * 1024  
DAYS = 5

methods = ["GET", "POST", "PUT", "DELETE"]
urls = [
    "/downloads/product_1", "/downloads/product_2", "/login", "/home", "/api/device/status",
    "/api/user/profile", "/static/image.jpg", "/static/script.js"
]
status_codes = [200, 200, 200, 301, 404, 500]

user_agents = {
    "web": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)"
    ],
    "mobile": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F)"
    ],
    "iot": [
        "Debian APT-HTTP/1.3 (1.0.1ubuntu2)",
        "Wget/1.20.3 (linux-gnu)",
        "curl/7.68.0"
    ]
}

error_messages = [
    "client denied by server configuration: /restricted",
    "script not found or unable to stat: /cgi-bin/test.cgi",
    "File does not exist: /var/www/favicon.ico",
    "upstream timed out (110: Connection timed out) while reading response header"
]

# Yardımcı fonksiyonlar
def get_random_log_datetime(day_offset):
    date = datetime.now() - timedelta(days=day_offset)
    time = datetime.min.time()
    random_time = datetime.combine(date, time) + timedelta(seconds=random.randint(0, 86399))
    return random_time.strftime("%d/%b/%Y:%H:%M:%S +0000")

def generate_access_log(ip, user_agent, timestamp):
    method = random.choice(methods)
    url = random.choice(urls)
    status = random.choice(status_codes)
    size = random.randint(200, 4000)
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "-" "{user_agent}"'

def generate_error_log(ip, timestamp):
    msg = random.choice(error_messages)
    return f'[{timestamp}] [error] [client {ip}] {msg}'

def write_rotated_logs(filename, entries):
    index = 0
    count = 1
    while index < len(entries):
        part = []
        size = 0
        while index < len(entries):
            line = entries[index] + "\n"
            if size + len(line.encode("utf-8")) > LOG_SIZE_LIMIT:
                break
            part.append(line)
            size += len(line.encode("utf-8"))
            index += 1
        fname = f"{filename}.{count}" if count > 1 else filename
        with open(fname, "w") as f:
            f.writelines(part)
        count += 1

# Ana üretim fonksiyonu
def generate_logs():
    all_access_logs = []
    all_error_logs = []

    for day in range(DAYS):
        for _ in range(NORMAL_TRAFFIC_COUNT):
            ip = fake.ipv4()
            device = random.choice(list(user_agents.keys()))
            ua = random.choice(user_agents[device])
            ts = get_random_log_datetime(day)
            all_access_logs.append(generate_access_log(ip, ua, ts))

            if random.random() < 0.1:
                all_error_logs.append(generate_error_log(ip, ts))

        # Anomali IP'leri
        for ip in ANOMALY_IPS:
            for _ in range(ANOMALY_TRAFFIC_COUNT // DAYS):
                device = random.choice(list(user_agents.keys()))
                ua = random.choice(user_agents[device])
                ts = get_random_log_datetime(day)
                all_access_logs.append(generate_access_log(ip, ua, ts))

                if random.random() < 0.3:
                    all_error_logs.append(generate_error_log(ip, ts))

    os.makedirs("logs", exist_ok=True)
    write_rotated_logs("logs/access.log", all_access_logs)
    write_rotated_logs("logs/error.log", all_error_logs)
    print("Log dosyaları 'logs/' klasörüne yazıldı.")

if __name__ == "__main__":
    generate_logs()
