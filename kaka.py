import asyncio
import requests
import time
from telethon import TelegramClient

# === ТВОИ НОВЫЕ КЛЮЧИ ===
API_ID = 32126294
API_HASH = "4530b707405d10e8a442712a91cc67eb"

BOT_USERNAME = "AirAuthBot"
BET_AMOUNT = 50000
TARGET_MULTIPLIER = 1.1

BASE_URL = "https://core.fragment.press/api/crash"
BET_URL = f"{BASE_URL}/bet"
CASHOUT_URL = f"{BASE_URL}/cashout"
STATE_URL = f"{BASE_URL}/state"

# === ТОКЕН И INIT_DATA ДЛЯ ПЕРВОГО АККАУНТА ===
TOKEN = "Bearer de42a62e232d153bba2bedd864ec64af2627ff0a53348fa008328fc96520f6c9"

INIT_DATA = "query_id=AAHF0HwEBAAAAMXQfATxIFL9&user=%7B%22id%22%3A8665223365%2C%22first_name%22%3A%22psyhco%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22nightgo0d%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FgS6GgFbtm5vLnl4JtnUccU_BJp-z1gDcanknJqtQ4lWETzjbYoXxnZ4FXgUmMSEa.svg%22%7D&auth_date=1787567367&signature=3YZuhQ_GO7FF06HrCdMXzBWXBv2ZJ7nwrQr9LrTUdnxWxb6xeOGFDrYcWnX5XXsgJejDuyjNTeqgVi0dZ2b4Cg&hash=9653a655bad3368824ba222ac77d24f30dda112327dc613f1214683f6058e7cd"

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "x-telegram-init-data": INIT_DATA,
    "Origin": "https://core.fragment.press",
    "Referer": "https://core.fragment.press/"
}

client = TelegramClient("session_1", API_ID, API_HASH)

def get_state():
    try:
        r = requests.get(STATE_URL, headers=HEADERS, timeout=3)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def place_bet():
    try:
        r = requests.post(BET_URL, json={"amount": BET_AMOUNT, "initData": INIT_DATA}, headers=HEADERS, timeout=3)
        return r.status_code == 200
    except:
        return False

def force_cashout():
    try:
        r = requests.post(CASHOUT_URL, json={"initData": INIT_DATA}, headers=HEADERS, timeout=3)
        return r.status_code == 200
    except:
        return False

async def main():
    await client.start()
    print(f"🚀 АККАУНТ 1 ЗАПУЩЕН! ЦЕЛЬ: {TARGET_MULTIPLIER}x")
    print("-" * 50)

    while True:
        try:
            state = get_state()
            if not state:
                await asyncio.sleep(0.2)
                continue

            status = state.get("round", {}).get("status")
            mult = state.get("round", {}).get("currentMultiplier", 1.0)
            can_bet = state.get("canBet", False)
            wait_time = state.get("round", {}).get("waitingSecondsLeft", 0)
            my_bet = state.get("myBet")
            my_bet_exists = my_bet is not None and my_bet.get("status") == "active"

            print(f"[АКК1] [{status}] Множ: {mult:.2f}x | Моя ставка: {my_bet_exists}")

            if status == "crashed" and my_bet_exists:
                print("💥 Проигрыш")
                await asyncio.sleep(0.3)
                continue

            if can_bet and not my_bet_exists and status == "waiting":
                print("🎯 Ставлю...")
                if place_bet():
                    print("✅ Ставка принята")
                await asyncio.sleep(0.2)
                continue

            if status == "flying" and my_bet_exists and mult >= TARGET_MULTIPLIER:
                print(f"🎯 {mult:.2f}x! Забираю!")
                force_cashout()
                await asyncio.sleep(0.3)
                continue

            await asyncio.sleep(0.05)

        except KeyboardInterrupt:
            print("\n🛑 Стоп")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())