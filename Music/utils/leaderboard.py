import asyncio
import datetime
import os
import time
import traceback

import aiofiles
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup

from config import Config
from Music.core.database import db


class Leaderboard:
    def __init__(self) -> None:
        # file used to log failed chats during broadcast
        self.file_name = "leaderboard.txt"

    def get_hrs(self) -> int:
        try:
            hrs = int(Config.LEADERBOARD_TIME.split(":")[0])
        except Exception:
            hrs = 3
        return hrs

    def get_min(self) -> int:
        try:
            mins = int(Config.LEADERBOARD_TIME.split(":")[1])
        except Exception:
            mins = 0
        return mins

    async def get_top_10(self) -> list:
        """Return a list of at most 10 users sorted by songs_played desc.

        Each item is a dict: {"id": int, "songs": int, "user": str}
        This function is tolerant to older user docs that may be missing
        songs_played or user_name.
        """
        users_cursor = await db.get_all_users()
        all_guys = []

        async for user in users_cursor:
            # user_id
            try:
                uid = int(user.get("user_id"))
            except (TypeError, ValueError):
                # skip malformed records
                continue

            # songs_played may be missing -> default 0
            songs = int(user.get("songs_played", 0) or 0)

            # username / display name fallback chain
            user_name = (
                user.get("user_name")
                or user.get("first_name")
                or user.get("name")
                or "Unknown User"
            )

            all_guys.append({"id": uid, "songs": songs, "user": user_name})

        if not all_guys:
            return []

        all_guys = sorted(all_guys, key=lambda x: x["songs"], reverse=True)
        return all_guys[:10]

    async def generate(self, bot_details: dict) -> str:
        """Generate the leaderboard text for /topusers or similar commands.

        bot_details must contain:
          - mention: bot mention string
          - client: bot client (not used here but kept for compatibility)
          - username: bot username (for deep-links)
        """
        index = 0
        top_10 = await self.get_top_10()
        text = f"**🧡 Top 10 Users of {bot_details['mention']}**\n\n"

        # If there is no data yet, show a friendly message
        if not top_10:
            text += "_No data yet — start playing songs to enter the leaderboard!_\n"
            text += "\n**🧡 Enjoy Streaming! Have Fun!**"
            return text

        for top in top_10:
            index += 1
            link = f"https://t.me/{bot_details['username']}?start=user_{top['id']}"
            # index is <= 10 anyway but keep padding like original
            text += (
                f"**⤷ {'0' if index <= 9 else ''}{index}:** "
                f"[{top['user']}]({link}) — `{top['songs']}` songs\n"
            )

        text += "\n**🧡 Enjoy Streaming! Have Fun!**"
        return text

    async def broadcast(self, hellbot, text, buttons):
        """Broadcast leaderboard text to all chats.

        hellbot is expected to be the main bot wrapper that has:
          - app: pyrogram Client
          - logit(tag, text, file_name=None)
        """
        start = time.time()
        success = failed = count = 0
        chats = await db.get_all_chats()

        async with aiofiles.open(self.file_name, mode="w") as leaderboard_log_file:
            async for chat in chats:
                try:
                    sts, msg = await self.send_message(
                        hellbot.app,
                        buttons,
                        int(chat["chat_id"]),
                        text,
                    )
                except Exception:
                    # Don't break the whole broadcast loop for one bad chat
                    continue

                if msg is not None:
                    await leaderboard_log_file.write(msg)

                if sts == 1:
                    success += 1
                elif sts == 2:
                    failed += 1

                count += 1
                await asyncio.sleep(0.3)

        time_taken = datetime.timedelta(seconds=int(time.time() - start))
        await asyncio.sleep(3)

        to_log = (
            "**Leaderboard Auto Broadcast Completed in "
            f"{time_taken}**\n\n"
            f"**Total Chats:** `{count}`\n"
            f"**Successful:** `{success}`\n"
            f"**Failed:** `{failed}`\n\n"
            "**🧡 Enjoy Streaming! Have Fun!**"
        )

        if failed == 0:
            await hellbot.logit("leaderboard", to_log)
        else:
            await hellbot.logit("leaderboard", to_log, self.file_name)

        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    async def send_message(self, hellbot, buttons, chat: int, text: str):
        try:
            await hellbot.send_message(
                chat,
                text,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True,
            )
            return 1, None
        except FloodWait as e:
            await asyncio.sleep(e.x)
            return await self.send_message(hellbot, buttons, chat, text)
        except PeerIdInvalid:
            return 2, f"{chat} -:- chat id invalid\n"
        except Exception:
            return 3, f"{chat} -:- {traceback.format_exc()}\n"


leaders = Leaderboard()
