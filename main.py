import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from pyshorteners import Shortener
import re

BASE_URL = "https://avtodnr.ru/?page="

HEADERS = {"User-Agent": UserAgent().random}

words = ["jetta", "джетт", "tiguan", "тигуан", "passat", "пассат", "mazda 6", "Торез", "Шахтерск", "Снежное"]


async def main():
    for i in range(20):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + str(i), headers=HEADERS) as response:
                r = await aiohttp.StreamReader.read(response.content)
                soup = BS(r, "html.parser")
                items = soup.find_all("div", {"class": "col-12 col-md-6 singleBlockCol"})
                for item in items:
                    title = item.find("a", {"class": "post-content"})
                    link = title.get("href")
                    data = item.find("div", {"class": "col-6 text-right"}).text.strip()
                    for s in words:
                        if str(title).lower().find(s.lower()) != -1:
                            print(f"{title.text.strip()[:30]} | {data} | {link}", "\n")




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
