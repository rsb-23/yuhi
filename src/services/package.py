import asyncio

import httpx


class HttpService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get(self, url: str):
        return await self.client.get(url)


class PackageService:
    def __init__(self, http: HttpService, url_pattern: str):
        self.http = http
        self.url = url_pattern

    async def fetch(self, package):
        return package, await self.http.get(self.url.format(package=package))

    async def fetch_all(self, packages):
        tasks = [asyncio.create_task(self.fetch(p)) for p in packages]
        return await asyncio.gather(*tasks)
