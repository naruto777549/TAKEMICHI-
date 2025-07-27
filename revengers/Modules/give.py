from pyrogram import filters
from pyrogram.types import Message
from revengers.db import add_balance, reduce_balance, get_balance
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from revengers import bot