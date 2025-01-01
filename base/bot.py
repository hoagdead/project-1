import discord
import requests
import asyncio
from discord.ext import tasks, commands

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Chỉ định backend để không cần GUI
import matplotlib.pyplot as plt
from io import BytesIO

BOT_TOKEN = "MTMyMDM1ODM1MDM2OTcxODI3Mg.G1Is6I.wwGAFPtV2RyNR8s2FPFKi1nSH2FyBEFT1Sm-Qc"
API_URL = "http://127.0.0.1:8000//api/user-activity/"  # Thay bằng domain EC2
CHANNEL_ID = 1320359136214388758

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công với tên: {bot.user}")
    fetch_user_activity.start()  # Bắt đầu job lặp 24h

@tasks.loop(hours=24)
async def fetch_user_activity():
    """Mỗi 24h gọi API, vẽ biểu đồ, gửi vào kênh."""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Không tìm thấy channel. Kiểm tra CHANNEL_ID.")
        return

    try:
        # 1. Gọi API
        response = requests.get(API_URL)
        if response.status_code != 200:
            await channel.send(f"Không thể lấy dữ liệu (status != 200): {response.status_code}")
            return

        data = response.json()  # list các record UserActivity
        if not data:
            await channel.send("Không có lượt truy cập nào trong 24h qua.")
            return

        # 2. Chuyển sang DataFrame, group theo giờ
        df = pd.DataFrame(data)
        # df['timestamp'] đang là string, convert sang datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Tạo cột hour
        df['hour'] = df['timestamp'].dt.hour
        # Group by hour, đếm số lượng
        visits_by_hour = df.groupby('hour').size()

        # 3. Vẽ biểu đồ cột
        plt.figure(figsize=(8,4))
        plt.bar(visits_by_hour.index, visits_by_hour.values, color='skyblue')
        plt.xlabel("Giờ trong ngày (0-23)")
        plt.ylabel("Số lượt truy cập")
        plt.title("Thống kê lượt truy cập theo giờ (24h qua)")
        plt.xticks(range(24))  # hiển thị đủ 24 giờ

        # Lưu biểu đồ vào bộ nhớ
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()  # đóng figure

        # 4. Gửi ảnh lên Discord
        file = discord.File(buf, filename="visits_chart.png")
        await channel.send(content="**[ Thống kê 24h ]**", file=file)

        # 5. (Tuỳ chọn) - Thống kê vòng đời (lượt truy cập theo path)
        visits_by_path = df.groupby('path').size().sort_values(ascending=False)
        msg_lines = ["**[ Số lượt truy cập theo trang ]**"]
        for path, count in visits_by_path.items():
            msg_lines.append(f"- `{path}`: {count} lượt")
        final_msg = "\n".join(msg_lines)
        await channel.send(final_msg)

    except Exception as e:
        await channel.send(f"Lỗi khi gọi API hoặc vẽ biểu đồ: {e}")

bot.run(BOT_TOKEN)
