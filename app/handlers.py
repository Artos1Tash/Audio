from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router, html
from aiogram.types import FSInputFile
import logging

from pytube import YouTube 
import os 

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Handler for commnad help /help")
    
@router.message()
async def get_link(message: Message):
    try:
        link = message.text
        logging.warning(link)
        yt = YouTube(str(link)) 

        video = yt.streams.filter(only_audio=True).first() 

        out_file = video.download(output_path='.') 

        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
        
        file = FSInputFile(new_file)
        
        await message.answer_audio(file)
    except:
        await message.answer("Unsuccesful")
    
    finally:
        os.remove(new_file)