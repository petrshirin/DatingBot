import asyncpg
import os
from envparse import env
from asyncpg.connection import Connection
from datetime import datetime


class ChatToken:

    token = None
    user = None

    all_tokens = []

    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_all(self):
        rows = await self.conn.fetch('SELECT * FROM authtoken_token')
        objects = []
        for row in rows:
            new_token = ChatToken(self.conn)
            new_token.token = row['key']
            new_token.user = row['user_id']
            objects.append(new_token)
        self.all_tokens = objects


class ChatMessage:

    sender = None
    recipient = None
    text = None
    time = None

    def __init__(self, conn: Connection, sender: int, recipient: int, text: str, time: datetime):
        self.conn = conn
        self.sender = sender
        self.recipient = recipient
        self.text = text
        self.time = time

    async def save(self):
        await self.conn.execute(f"INSERT INTO userprofile_message (sender_id, recipient_id, text, time) VALUES ($1, $2, $3, $4)", self.sender, self.recipient, self.text, self.time)






