#!/usr/bin/env python3
import asyncio
import time
import os
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.idle import idle

# ================= ENV =================
API_ID = int(os.environ.get("API_ID", 8898405))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
PORT = int(os.environ.get("PORT", 8080))

if not BOT_TOKEN or not API_HASH or not OWNER_ID:
    raise ValueError("❌ Missing ENV variables")

# ================= BOT =================
app = Client(
    "ZEN_BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=50,
    sleep_threshold=1
)

# ============== CUSTOM LINES ==============
CUSTOM_LINES = [
    "🔥 ZEN MODE ACTIVE 🔥",
    "⚡ SYSTEM READY ⚡",
    "💀 TARGET LOCKED 💀",
    "🌀 POWER FULL ZEN 🌀",
]

# ============== OWNER CHECK ==============
def owner_only(func):
    async def wrapper(client, message: Message):
        if not message.from_user or message.from_user.id != OWNER_ID:
            return
        return await func(client, message)
    return wrapper


# ================= ALIVE =================
@app.on_message(filters.command("alive", prefixes="."))
@owner_only
async def alive(_, message):
    await message.reply_text("✅ ZEN BOT IS ALIVE 🔥 READY FOR ACTION")


# ================= SPEED =================
@app.on_message(filters.command("speed", prefixes="."))
@owner_only
async def speed(_, message):
    await message.reply_text("⚡ SUPER FAST MODE ACTIVE ⚡")


# ================= PING =================
@app.on_message(filters.command("ping", prefixes="."))
@owner_only
async def ping(_, message):
    start = time.time()
    msg = await message.reply_text("🏓 Pinging...")
    end = time.time()

    ping = round((end - start) * 1000, 2)
    await msg.edit_text(f"⚡ PONG\n🔥 Speed: {ping} ms")


# ================= CUSTOM REPLY =================
# Safe version: no spam, only single reply
@app.on_message(filters.command("r", prefixes="."))
@owner_only
async def custom_reply(_, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Kisi message ko reply karo")

    target = message.reply_to_message.from_user
    line = random.choice(CUSTOM_LINES)

    await message.reply_text(f"{target.mention} {line}")


# ================= STOP (placeholder safety) =================
@app.on_message(filters.command("stop", prefixes="."))
@owner_only
async def stop(_, message):
    await message.reply_text("🛑 STOP RECEIVED (no active task system)")


# ================= WEB SERVER =================
from aiohttp import web

async def health(request):
    return web.Response(text="ZEN BOT RUNNING OK", status=200)

async def web_server():
    try:
        app_web = web.Application()
        app_web.router.add_get("/", health)
        app_web.router.add_get("/health", health)

        runner = web.AppRunner(app_web)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", PORT)
        await site.start()
        print(f"🌐 Web running on port {PORT}")
    except Exception as e:
        print("Web error:", e)


# ================= MAIN =================
async def main():
    print("⚡ STARTING ZEN BOT...")

    await web_server()

    await app.start()

    me = await app.get_me()
    print(f"🤖 Bot Running: @{me.username}")

    await idle()

    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
