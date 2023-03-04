import asyncio
import os

import asyncssh
import httpx
from dotenv import load_dotenv

load_dotenv()


async def main():
    key = asyncssh.read_private_key(os.environ["AWS_KEY"])
    async with httpx.AsyncClient() as client:
        async with asyncssh.connect(
            os.environ["AWS_IP"],
            username=os.environ["AWS_USER"],
            client_keys=[key],
            known_hosts=None,  # TODO: Should probably specify the known_hosts
            encoding=None,  # Returns raw bytes on stdout
        ) as conn:
            async with conn.create_process(r"yes n | head -n 20000") as proc:

                async def reader():
                    while chunk := await proc.stdout.read(8192):
                        yield chunk

                response = await client.post("http://localhost:8000", content=reader())
                print(response.content)


if __name__ == "__main__":
    asyncio.run(main())
