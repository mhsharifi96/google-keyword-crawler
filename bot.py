from telethon import TelegramClient, events
import  re
from g_search import main as g_main
import  time
import config

# Remember to use your own values from my.telegram.org!

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")


# api_id = 281931
# api_hash = '2536e06ebbf8c63edc74aa4a0f7c062e'
# bot_token = "970347099:AAG3f5Mgaa1QRbMxg-tNeKmFT1dnT3_Cm_o"

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
bot_token = config['Telegram']['bot_token']

client =  TelegramClient('bot', api_id, api_hash)
regex_lsi = r"key\s?:\s?"

@client.on(events.NewMessage)
async def main(event):
    print("event handel")
    print(event.message.message)
    print(event.message.peer_id.user_id)
    # Getting information about yourself
    client_message = event.message.message

    if(client_message == "/start")  : 
        text1 = """
  به بات a28 خوش امدید.
جهت یافتن related word بر روی /related کلیک نمایید. 
جهت یافتن lsi ها بر روی /lsi کلیک نمایید.
        کلیک کنید
        """
        text = """
  به بات a28 خوش امدید.
جهت یافتن lsi ها بر روی /lsi کلیک نمایید.
        کلیک کنید
        """
        sapmple ='This message has **bold**, `code`, __italics__ and ''a [nice website](https://example.com)!'
        message = await client.send_message(
            event.message.peer_id.user_id,
            text,
            link_preview=False
            )
    
    if(client_message == "/lsi"):
        text = """عبارت کلیدی خود را به صورت زیر تایپ کنید :
        key: دیجیتال مارکتینگ
        """
        message = await client.send_message(
            event.message.peer_id.user_id,
            text,
            link_preview=False
            )
    if(sum(1 for _ in  re.finditer(regex_lsi, client_message, re.MULTILINE))>0):
        keyword = re.sub(regex_lsi,"",client_message)
        text = """کلمه کلیدی شما : {}""".format(keyword)
        message = await client.send_message(
            event.message.peer_id.user_id,
            text,
            link_preview=False
            )
        send_me = await client.send_message(
            197418176,
            text,
            link_preview=False
            )
        message = await client.send_message(
            event.message.peer_id.user_id,
            "ممکنه چند دقیقه طول بکشه،صبور باشید!\n تموم که شد یه فایل براتون اینجا ارسال میشه .",
            link_preview=False
            )
        file_name = str(int(time.time()))+"_a28_ir.txt"
        res = g_main(search_val=keyword,rec_search_dir=file_name) 
        # print(res)
        await client.send_file(event.message.peer_id.user_id, res)
        #TODO:  remove file after send
        message = await client.send_message(
            event.message.peer_id.user_id,"ممنونم از همراهیتون :)",
            link_preview=False)
        
    print(sum(1 for _ in  re.finditer(regex_lsi, client_message, re.MULTILINE)))
    # # "me" is a user object. You can pretty-print
    # # any Telegram object with the "stringify" method:
    # print(me.stringify())

    # # When you print something, you see a representation of it.
    # # You can access all attributes of Telegram objects with
    # # the dot operator. For example, to get the username:
    # username = me.username
    # print(username)
    # print(me.phone)

    # # You can print all the dialogs/conversations that you are part of:
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    # # You can send messages to yourself...
    # await client.send_message('me', 'Hello, myself!')
    # # ...to some chat ID
    # await client.send_message(-100123456, 'Hello, group!')
    # # ...to your contacts
    # await client.send_message('+34600123123', 'Hello, friend!')
    # # ...or even to any username
    # await client.send_message('username', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    

    # Sending a message returns the sent message object, which you can use
    # print(message.raw_text)

    # You can reply to messages directly if you have a message object
    # await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    # await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # You can print the message history of any chat:
    # async for message in client.iter_messages('me'):
    #     print(message.id, message.text)

    #     # You can download media from messages, too!
    #     # The method will return the path where the file was saved.
    #     if message.photo:
    #         path = await message.download_media()
    #         print('File saved to', path)  # printed after download is done

# with client:
#     client.loop.run_until_complete(main())


client.start(bot_token=bot_token)
client.run_until_disconnected()
