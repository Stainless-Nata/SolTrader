from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import asyncio, time, os, re

load_dotenv()

# Replace these with your own values
CHANNEL_READ = os.getenv('CHANNEL_READ')
CHANNEL_WRITE = os.getenv('CHANNEL_WRITE')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BUY_SECTION = os.getenv('BUY_SECTION').split(" ")
BUY_AMOUNT = os.getenv('BUY_AMOUNT').split(" ")
prevmsg = "initial message"

# Create a new TelegramClient instance
client = TelegramClient('session_name', API_ID, API_HASH)

async def run_banana(token, amount):
    # run /start command
    await client.send_message(CHANNEL_WRITE, '/start')

    time.sleep(1)
    # enter token address
    await client.send_message(CHANNEL_WRITE, token)

    time.sleep(1)
    # click buy x amount
    message = await client.get_messages(CHANNEL_WRITE, limit=1)
    print(type(message[0].reply_markup))

    time.sleep(1)
    if(str(message).find("Switch To Buy") != -1):
        cnt = str(message[0].reply_markup).count("KeyboardButtonRow")
        print(cnt)
        if(cnt == 8):
            await message[0].click(6,0)
        else:
            await message[0].click(9,0)
        time.sleep(1)
        message = await client.get_messages(CHANNEL_WRITE, limit=1)

    time.sleep(1)
    await message[0].click(6, 1)

    # input amount as reply_to
    message = (await client.iter_messages(CHANNEL_WRITE, limit=1).__anext__())
    await client.send_message(CHANNEL_WRITE, amount, reply_to=message.id)
    print("Success")

def split_message(string):
    label = re.search(r'#(\w+)', string).group(1)
    amount1 = re.search(r'\*\*(.*?)\*\*', string.split(label)[1]).group(1)
    currency1 = re.search(r'#(\w+)', string.split(label)[1]).group(1)
    amount2 = re.search(r'\*\*(.*?)\*\*', string.split(currency1)[1]).group(1)
    currency2 = re.search(r'#(\w+)', string.split(currency1)[1]).group(1)
    token = re.search(r'/tokens/(\w+)', string).group(1)

    return {
        "label": label,
        "amount1": amount1,
        "currency1": currency1,
        "amount2": amount2,
        "currency2": currency2,
        "token": token,
        "type": "Buy" if currency1 == "SOL" else "Sell",
    }

async def get_channel_messages():
    async for message in client.iter_messages(CHANNEL_READ, limit=1):
        global prevmsg
        if(prevmsg == "initial message"):
            prevmsg = message.text
            # print(message.text)
        elif(prevmsg != message.text):
            prevmsg = message.text

            param = split_message(message.text)
            print(param)
            if(param["type"] == "Buy"):
                print("Buy Action:")
                index = -1
                for x in BUY_SECTION:
                    if(float(x) > float(param["amount1"])):
                        break
                    index = index + 1
                print(index, BUY_AMOUNT[index])
                if(index != -1):
                    await run_banana(param["token"], BUY_AMOUNT[index])
            else:
                print("Sell Action: Skip")
        else:
            print("No new messages")

async def check_every_seconds():
    while True:
        try:
            async with client:
                await get_channel_messages()
                # await run_banana("F3nefJBcejYbtdREjui1T9DPh5dBgpkKq7u2GAAMXs5B", "0.001")
        except Exception as e:
            print(str(e))
        await asyncio.sleep(5)

asyncio.run(check_every_seconds())

