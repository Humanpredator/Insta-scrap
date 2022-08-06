from bot.helper.ext_utils.bot_utils import usercheck
from bot.helper.telegram_helper.message_utils import *
import time
import pytz
import glob
from datetime import datetime
from bot import DOWNLOAD_STATUS_UPDATE_INTERVAL, LOGGER
from videoprops import get_audio_properties
from pyrogram.errors import FloodWait
from bot.helper.ext_utils.bot_utils import progress_bar, usercheck
from telegram import InputMediaPhoto, InputMediaVideo
USER = usercheck()
IST = pytz.timezone('Asia/Kolkata')
session = f"./{USER}"

# A functionUpload Content to Telegram


def tgup(chat_id, dir):
    m = bot.send_message(chat_id, f"Uploading to Telegram, Plase wait...")
    videos = glob.glob(f"{dir}/*.mp4")
    VDO = []
    GIF = []
    for video in videos:
        try:
            has_audio = get_audio_properties(video)
            VDO.append(video)
        except Exception as e:
            has_audio = None
            GIF.append(video)
            pass
    PIC = glob.glob(f"{dir}/*.jpg")
    print(f"Gif- {GIF}")
    print(f"\n\nVideo - {VDO}")
    print(f"\n\nPictures - {PIC}")

    totalpics = len(PIC)
    totalgif = len(GIF)
    totalvideo = len(VDO)
    TOTAL = totalpics+totalvideo+totalgif
    total = TOTAL

    up = 0
    rm = TOTAL
    if total == 0:
        print("No Files Found")
        return
    if totalpics > 0:
        for i in range(0, len(PIC), 10):
            chunk = PIC[i:i + 10]
            media = []
            for photo in chunk:
                media.append(InputMediaPhoto(open(photo, 'rb')))
                up += 1
                rm -= 1
            try:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_media_group(chat_id=chat_id, media=media)
            except FloodWait as e:
                time.sleep(e.x)
                bot.send_media_group(chat_id=chat_id, media=media)
            except Exception as e:
                print(f"{e}")
                pass
            msg = f'''
<b>Uploading: </b><code>{progress_bar(up,total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>Pictures</code>
'''
            editMessage(msg, m)

    if totalvideo > 0:
        for i in range(0, len(VDO), 10):
            chunk = VDO[i:i + 10]
            print(chunk)
            media = []
            for video in chunk:
                media.append(InputMediaVideo(media=open(video, 'rb')))
                up += 1
                rm -= 1
            try:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_media_group(chat_id=chat_id, media=media)
            except FloodWait as e:
                time.sleep(e.x)
                bot.send_media_group(chat_id=chat_id, media=media)
                rm -= 1
            except Exception as e:
                print(f"{e}")
                pass
            msg = f'''
<b>Uploading: </b><code>{progress_bar(up,total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>Videos</code>
'''
            editMessage(msg, m)

    if totalgif > 0:
        for gif in GIF:
            try:
                datetime_ist = datetime.now(IST)
                ISTIME = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")
                up += 1
                time.sleep(DOWNLOAD_STATUS_UPDATE_INTERVAL)
                bot.send_animation(chat_id=chat_id, animation=open(gif, 'rb'))
                rm -= 1
                msg = f'''
<b>Uploading: </b><code>{progress_bar(up,total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>GIFS</code>
'''
                editMessage(msg, m)
            except FloodWait as e:
                up += 1
                time.sleep(e.x)
                bot.send_animation(chat_id=chat_id, animation=open(gif, 'rb'))
                rm -= 1
                msg = f'''
<b>Uploading: </b><code>{progress_bar(up,total)}</code>
<b>Files uploaded: </b><code>0{up}/{total}</code>
<b>Files remaining: </b><code>0{rm}/{total}</code>
<b>Total Files : </b><code>{total}</code>
<b>Last Updated : </b><code>{ISTIME}</code>
<b>Currently Uploading: </b><code>GIFS</code>
'''
                editMessage(msg, m)
            except Exception as e:
                print(f"{e}")
                pass

    editMessage("Telegram Upload Completed", m)
    LOGGER.info(f"Telegram Upload Completed")
    return True
