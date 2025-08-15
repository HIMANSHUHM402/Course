import random
import time
import math
import os
from vars import CREDIT
from pyrogram.errors import FloodWait
from datetime import timedelta


# ==== Timer Class ====
class Timer:
    def __init__(self, time_between=1):  # 1 second update interval
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        """Check if enough time has passed since last update."""
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


# ==== Helper Functions ====
def hrb(value, digits=2, delim="", postfix=""):
    """Convert bytes to human-readable format."""
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


def hrt(seconds, precision=0):
    """Convert seconds to human-readable time format."""
    pieces = []
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}day")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}hr")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}min")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}sec")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


# ==== Progress Bar ====
timer = Timer(time_between=1)  # Update every 1 second


async def progress_bar(current, total, reply, start):
    """Show progress bar for upload/download."""
    if timer.can_send():  # Control update frequency
        now = time.time()
        diff = now - start
        if diff < 0.5:
            return

        # Calculate progress
        perc = f"{current * 100 / total:.1f}%"
        elapsed_time = round(diff)
        speed = current / elapsed_time if elapsed_time > 0 else 0
        remaining_bytes = total - current
        eta = hrt(remaining_bytes / speed, precision=1) if speed > 0 else "-"

        sp = str(hrb(speed)) + "/s"
        tot = hrb(total)
        cur = hrb(current)

        # Bar design
        bar_length = 10
        completed_length = int(current * bar_length / total)
        remaining_length = bar_length - completed_length
        completed_symbol, remaining_symbol = "🟩", "⬜"
        progress_display = completed_symbol * completed_length + remaining_symbol * remaining_length

        # Send update
        try:
            await reply.edit(
                f"<blockquote>`╭──⌯═════𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐢𝐜𝐬══════⌯──╮\n"
                f"├⚡ {progress_display}\n"
                f"├⚙️ Progress ➤ | {perc} |\n"
                f"├🚀 Speed ➤ | {sp} |\n"
                f"├📟 Processed ➤ | {cur} |\n"
                f"├🧲 Size ➤ | {tot} |\n"
                f"├🕑 ETA ➤ | {eta} |\n"
                f"╰─═══✨🦋{CREDIT}🦋✨═══─╯`</blockquote>"
            )
        except FloodWait as e:
            time.sleep(e.x)  # Wait if Telegram limits updates
