import os
import requests
from io import BytesIO
from PIL import Image
from youtubesearchpython import VideosSearch


def _extract_video_id(link: str) -> str:
    """Extract YouTube video ID safely from any link or raw ID."""
    link = link.strip()

    if "v=" in link:
        return link.split("v=")[-1].split("&")[0]
    if "youtu.be/" in link:
        return link.split("youtu.be/")[-1].split("?")[0]

    return link  # fallback raw ID


def _download_thumbnail(video: str) -> str:
    """Internal helper: download raw YouTube thumbnail only."""

    # If text query → search YouTube
    if "youtu" not in video:
        data = VideosSearch(video, limit=1).result().get("result", [])
        if not data:
            raise Exception("No search results found.")
        video_id = data[0]["id"]
    else:
        video_id = _extract_video_id(video)

    # Try max resolution
    url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    r = requests.get(url, stream=True)

    # If unavailable, fallback to HQ
    if r.status_code != 200:
        url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        r = requests.get(url, stream=True)

    img = Image.open(BytesIO(r.content)).convert("RGB")

    # Save output
    os.makedirs("cache", exist_ok=True)
    path = f"cache/thumb-{video_id}.jpg"
    img.save(path, "JPEG")

    return path


# -----------------------------
# CLASS EXPECTED BY YOUR BOT
# -----------------------------
class thumb:
    @staticmethod
    def generate(video: str, *args, **kwargs) -> str:
        """
        Wrapper for compatibility with:
        from Music.utils.thumbnail import thumb
        thumb.generate(...)
        """
        try:
            return _download_thumbnail(video)
        except Exception as e:
            print("Thumbnail Error:", e)
            return None
