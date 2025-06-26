from datetime import  timedelta
import json
import os
import time
from telethon import TelegramClient, events, functions,types
from telethon.client.updates import asyncio




# api_id = 2040
# api_hash = 'b18441a1ff607e10a989891a5462e627'
# 139.144.4.230:13621:modeler_ogwXqv:dUdTmdfZGscG
#proxy=('http','139.144.4.230',13621,True,'modeler_ogwXqv','dUdTmdfZGscG')
#p20471120
# 7092618681
# 415372152
FORWARD_TO_1='p20471120'
FORWARD_TO_2='givenchy777'

HEAD_ID_1=7092618681
HEAD_ID_2=6473028847

# #client = TelegramClient('./sessions/919714029263/919714029263.session', api_id, api_hash,proxy=proxy)

async def main():
    # Initialize the Telegram client
    dirs = []
    tasks = []
    k=0
    i=0
    folder_path = './sessions'
    proxies=[]
    with open("proxies.json", 'r') as f:
        data = json.load(f)
    for proxy in data['proxies']:
        proxies.append((proxy['mode'],proxy['ip'],proxy['port'],True,proxy['user'],proxy['password']))
    for name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, name)
        if os.path.isdir(full_path):
            dirs.append(name)
    for dir in dirs:
        with open(f"./sessions/{dir}/{dir}.json", 'r') as f:
            json_data = json.load(f)
            task=asyncio.create_task(start_client(f"./sessions/{dir}/{dir}.session",json_data['app_id'],json_data['app_hash'],proxies[k],f"+{dir}"))
            i+=1
            if i==5:
                k+=1
                i=0
            tasks.append(task)
    await asyncio.gather(*tasks)

async def start_client(session_path:str,app_id:int,app_hash:str,proxy:tuple,phone_number:str):
    try:
        client = TelegramClient(session_path, app_id, app_hash, proxy=proxy)
    except Exception as e:
        print(f"Error initializing Telegram client: {e}")
        return
    @client.on(events.NewMessage())
    async def normal_handler(event):
        print(event.message)
        chat='Unknown'
        name='Unknown'
        filepath='deb'
        if isinstance(event.message.peer_id, types.PeerChat):
            async for dialog in client.iter_dialogs():
                if event.message.peer_id==dialog.message.peer_id:
                    name=await client.get_entity(event.message.from_id.user_id)
                    name=name.first_name
                    chat=dialog.name
            date_str = (event.message.date + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
            await client.send_message(FORWARD_TO_1, f'Сообщение от {name} в {chat} в {date_str}: {event.message.message}')
            if event.message.media!=None:
                await event.message.forward_to(FORWARD_TO_1)
            return
        if event.message.peer_id.user_id==HEAD_ID_1 or event.message.peer_id.user_id==HEAD_ID_2:
            try:
                user=0
                name=event.message.message.split(':')[0]
                message=event.message.message.split(':')[1]
                if event.message.media:
                    filepath=await event.message.download_media()
                    print(f"путь файла:{filepath}")

                    async for dialog in client.iter_dialogs():
                        if name.lower()==dialog.name.lower():
                            try:
                                user=dialog.message.peer_id.user_id
                            except:
                                user=dialog.message.peer_id.chat_id
                    m=await client.send_file(user, filepath,caption=message)
                    os.remove(filepath)
                    await client.send_read_acknowledge(name)
                    if event.message.peer_id.user_id==HEAD_ID_1:
                        await client.send_message(FORWARD_TO_1,f"Сообщение от головы {FORWARD_TO_1}")
                        await m.forward_to(FORWARD_TO_1)
                        await client.send_message(FORWARD_TO_2,f"Сообщение от головы {FORWARD_TO_1}")
                        await m.forward_to(FORWARD_TO_2)
                    elif event.message.peer_id.user_id==HEAD_ID_2:
                        await client.send_message(FORWARD_TO_1,f"Сообщение от головы {FORWARD_TO_2} отправлено с текстом: {message}")
                        await client.send_message(FORWARD_TO_2,f"Сообщение от головы {FORWARD_TO_2} отправлено с текстом: {message}")
                else:
                    async for dialog in client.iter_dialogs():
                        if name.lower()==dialog.name.lower():
                            try:
                                user=dialog.message.peer_id.user_id
                            except:
                                user=dialog.message.peer_id.chat_id
                    await client.send_message(user,message)
                    await client.send_read_acknowledge(name)
                    if event.message.peer_id.user_id==HEAD_ID_1:
                        await client.send_message(FORWARD_TO_1,f"Сообщение от головы {FORWARD_TO_1} отправлено с текстом: {message}")
                        await client.send_message(FORWARD_TO_2,f"Сообщение от головы {FORWARD_TO_1} отправлено с текстом: {message}")
                    elif event.message.peer_id.user_id==HEAD_ID_2:
                        await client.send_message(FORWARD_TO_1,f"Сообщение от головы {FORWARD_TO_2} отправлено с текстом: {message}")
                        await client.send_message(FORWARD_TO_2,f"Сообщение от головы {FORWARD_TO_2} отправлено с текстом: {message}")
            except Exception as e:
                print(e)
                if os.path.exists(filepath):
                    os.remove(filepath)
                if event.message.peer_id.user_id==HEAD_ID_1:
                    await client.send_message(FORWARD_TO_1, f"Ошибка при отправке сообщения напишите в формате имя:сообщение: {e}")
                elif event.message.peer_id.user_id==HEAD_ID_2:
                    await client.send_message(FORWARD_TO_2, f"Ошибка при отправке сообщения напишите в формате имя:сообщение: {e}")
            return

        print(event.message.to_dict()['message'])
        async for dialog in client.iter_dialogs():
            if event.message.peer_id==dialog.message.peer_id:
                chat=dialog.name
        await client.send_message(FORWARD_TO_1, f'Сообщение от {chat} в {(event.message.date+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}: {event.message.message}')
        await client.send_message(FORWARD_TO_2, f'Сообщение от {chat} в {(event.message.date+timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')}: {event.message.message}')
        if event.message.media!=None:
            await event.message.forward_to(FORWARD_TO_1)
            await event.message.forward_to(FORWARD_TO_2)

    print(f"Telegram client initialized on proxy{client._proxy}")
    await client.start(phone=phone_number)
    print("Telegram client connected")
    try:
        user:types.User=await client.get_me()
        print(user.username)
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        client.disconnect()


asyncio.run(main())
