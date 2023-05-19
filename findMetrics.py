import speedtest
import subprocess
import re
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(user='root', password='test1234', host='10.244.0.7', database='logs')

def measure_network():
    st = speedtest.Speedtest()
    download_speed = st.download()
    upload_speed = st.upload()
    ping_output = subprocess.Popen(["ping", "c", "10", "127.0.0.1"],stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    ping_times = re.findall(r"time=(+.  ̇?*. )", ping_output)
    latency_ms = sum(float(time) for time in ping_times) / len(ping_times)
    jitter_ms = sum(abs(float(time) - latency_ms) for time in ping_times) / len(ping_times)
    download_speed_mbps = download_speed / 1000000
    upload_speed_mbps = upload_speed / 1000000
    created_time = datetime.now()
    cursor = conn.cursor()
    insert_stmt = ("INSERT INTO logs(created_at, upload_speed, download_speed, latency,jitter)")
    data = (created_time, ":.2f".format(upload_speed_mbps), ":.2f".format(download_speed_mbps),":.2f".format(latency_ms), ":.2f".format(jitter_ms))
    
    try:
        cursor.execute(insert_stmt, data)
        conn.commit()
    except:
        conn.rollback()
        print("Can not connect!!!")
    
    f = open("/logs/logs.log", "w")
    f.write(f'Download speed: download_speed_mbps:.2f Mbps'
    f'Upload speed: upload_speed_mbps:.2f Mbps'
    f'Latency: latency_ms:.2f ms'
    f'Jitter: jitter_ms:.2f ms')
    f.close()
    print(f'Download speed: download_speed_mbps:.2f Mbps' f'Upload speed: upload_speed_mbps:.2f Mbps'
    f'Latency: latency_ms:.2f ms'
    f'Jitter: jitter_ms:.2f ms')

while True:
    measure_network()