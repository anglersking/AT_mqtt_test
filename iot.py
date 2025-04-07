import time
import paho.mqtt.client as mqtt

# 阿里云 MQTT 服务器
HOST = "iot-06z00fomtxkz3i1.mqtt.iothub.aliyuncs.com"
PORT = 1883  # 使用 TCP 连接，不使用 TLS

# ✅ **手动填充 AT 指令中的 clientId、username、password**
CLIENT_ID = "k29gmhpqPR2.test1|securemode=2,signmethod=hmacsha256,timestamp=1738216832605|"
USERNAME = "test1&k29gmhpqPR2"
PASSWORD = "115765c9143734d508626ec3d83ed91df2fb5b4d6e21ae2a3fb5bef6143a360f"

# 订阅 & 发布的 MQTT 主题
TOPIC_PUB = "/sys/k29gmhpqPR2/test1/thing/event/property/post"
TOPIC_SUB = "/sys/k29gmhpqPR2/test1/thing/service/property/set"

# ✅ **回调函数 - 连接成功**
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT 连接成功")
        client.subscribe(TOPIC_SUB)  # 订阅下行主题
    else:
        print(f"❌ 连接失败，错误码: {rc}")

# ✅ **回调函数 - 收到消息**
def on_message(client, userdata, msg):
    print(f"📩 收到消息 | 主题: {msg.topic} | 内容: {msg.payload.decode()}")

# ✅ **回调函数 - 断开连接**
def on_disconnect(client, userdata, rc):
    print(f"🔌 断开连接，错误码: {rc}")

# ✅ **创建 MQTT 客户端**
client = mqtt.Client(CLIENT_ID, transport="tcp")  # 仅使用 TCP，不使用 TLS
client.username_pw_set(username=USERNAME, password=PASSWORD)

# 绑定回调函数
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# 连接 MQTT 服务器
try:
    print("🚀 连接 MQTT 服务器...")
    client.connect(HOST, PORT, keepalive=60)
    time.sleep(10)
    client.loop_start()  # 启动 MQTT 监听

    # 发送 MQTT 消息
    payload = {
        "params": {
            "sws": {"sw1": 1, "sw2": 0},
            "SoilTemperature": 51.8,
            "SoilMoisture": 37,
            "WaterOutletSwitch": 1
        }
    }
    import json
    message = json.dumps(payload)
    print(f"🚀 发送消息 | 主题: {TOPIC_PUB} | 内容: {message}")
    client.publish(TOPIC_PUB, message, qos=0)

    # 运行一段时间后自动退出
    time.sleep(10)

except Exception as e:
    print(f"❌ 发生错误: {e}")

finally:
    client.loop_stop()
    client.disconnect()
