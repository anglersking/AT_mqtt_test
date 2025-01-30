import serial
import time

def send_at_command(ser, command, wait=2):
    ser.write((command + "\r\n").encode())
    time.sleep(wait)
    response = ser.read_all().decode(errors='ignore')
    print(f"Sent: {command}\nReceived: {response}")
    return response

def main():
    # 串口配置
    ser = serial.Serial('/dev/tty.usbserial-1110', 9600, timeout=5)  # 请根据实际情况修改端口
    time.sleep(2)  # 等待串口稳定
    
    try:
        # 配置 MQTT
        mqtt_cfg = 'AT+MQTTCFG="iot-06z00fomtxkz3i1.mqtt.iothub.aliyuncs.com",1883,"k29gmhpqPR2.test1|securemode=2,signmethod=hmacsha256,timestamp=1738216832605|",60,"test1&k29gmhpqPR2","115765c9143734d508626ec3d83ed91df2fb5b4d6e21ae2a3fb5bef6143a360f",1,0'
        send_at_command(ser, mqtt_cfg)
        
        # 打开 MQTT 连接
        mqtt_open = 'AT+MQTTOPEN=1,1,0,0,0'
        send_at_command(ser, mqtt_open)
        
        # 发布 MQTT 消息
        mqtt_pub = ('AT+MQTTPUB="/sys/k29gmhpqPR2/test1/thing/event/property/post",0,0,0,0,'
                    '"{params:{sws:{sw1:1,sw2:1},SoilTemperature:51.8,SoilMoisture:37,WaterOutletSwitch:1}}"')
        send_at_command(ser, mqtt_pub)
    
    finally:
        ser.close()

if __name__ == "__main__":
    main()
