from telethon import TelegramClient, sync, events

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
#3mopZxEbiCsA4hq5:3mopZxEbiCsA4hq5@45.154.205.7:14189
proxy=('socks5','45.154.205.7',14189,True,'3mopZxEbiCsA4hq5','3mopZxEbiCsA4hq5')

client = TelegramClient('./sessions/919714029263/919714029263.session', api_id, api_hash,proxy=proxy)

@client.on(events.NewMessage())
async def normal_handler(event):
    print(event.message)
    user_mess=event.message.to_dict()['message']

    s_user_id=event.message.to_dict()['from_id']['user_id']
    print(s_user_id)
    user_id=int(s_user_id)

    mess_date=event.message.to_dict()['date']

    f.write(mess_date.strftime("%d-%m-%Y %H:%M")+"\n")
    f.write(str(user_id) +"\n")
    f.write(user_mess+"\n\n")

    f.flush()

client.start(phone="+919714029263")



users={}

# for partic in client.iter_participants(group):
#     lastname=""
#     if partic.last_name:
#        lastname=partic.last_name
#     users[partic.id]=partic.first_name+" "+lastname

f=open('messages_from_chat', 'a')

client.run_until_disconnected()
f.close()
