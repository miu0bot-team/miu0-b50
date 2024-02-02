import aiohttp
import os

from typing import Dict, Tuple, Optional, List

plugin_dir:str = os.path.dirname(__file__)

async def _get_b50_json(payload: Dict) -> Tuple[Optional[Dict], int]:
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            return None, 400
        if resp.status == 403:
            return None, 403
        
        obj = await resp.json()
        return obj, 200

async def _get_musicdata() -> Tuple[Optional[List[Dict]], int]:
    async with aiohttp.request("GET", "https://www.diving-fish.com/api/maimaidxprober/music_data") as resp:
        if resp.status == 400:
            return None, 400
        if resp.status == 403:
            return None, 403

        obj = await resp.json()
        return obj, 200

def get_cover(id:str) -> bytes:
    cover_path = plugin_dir+'/static/mai/cover/%05d.png' % int(id)
    if not os.path.exists(cover_path):
        cover_path = plugin_dir+'/static/mai/cover/00000.png'
    cover = open(cover_path,'rb').read()
    return cover


def exist_cover(id:str) -> bool:
    cover_path = plugin_dir+'/static/mai/cover/%05d.png' % int(id)
    return os.path.exists(cover_path)
    
