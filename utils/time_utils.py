from datetime import datetime
from zoneinfo import ZoneInfo


def format_ist(timestamp):
    """
    Convert a UTC timestamp to India Standard Time
    and return it in the application's display format.
    """

    if not timestamp:
        return "-"

    if isinstance(timestamp, str):

        timestamp = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

    india_time = timestamp.astimezone(
        ZoneInfo("Asia/Kolkata")
    )

    return india_time.strftime(
        "%d %b %Y, %I:%M %p"
    )