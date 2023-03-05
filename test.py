import asyncio
import json
from asyncio import Queue

import asyncssh
import httpx
from dotenv import load_dotenv

load_dotenv()


async def simple_main():
    """
    A very simple bit of code essentially forwarding the output of
    the SSH server to the HTTP server
    """
    # key = asyncssh.read_private_key(key_filename)  # How to read a private key
    async with httpx.AsyncClient() as client:
        async with asyncssh.connect(
            "localhost",  # Host
            12361,  # port
            username="none",
            # client_keys=[key],  # If you have public key auth
            known_hosts=None,  # TODO: Should probably specify the known_hosts
            encoding=None,  # Returns raw bytes on stdout
        ) as conn:
            async with conn.create_process(r"yes n | head -n 20000") as proc:

                async def reader():
                    while chunk := await proc.stdout.read(8192):
                        yield chunk

                response = await client.post("http://localhost:8000", content=reader())
                print(response.content)


async def queued_main():
    """
    In this example, we use an asyncio Queue to buffer the data coming
    from the SSH server in case the HTTP server is slow

    Note that this is potentially quite a slow buffer as we're going
    through Python's async/await semantics, but it's a lot easier to
    write than Cython :-)
    """
    async with httpx.AsyncClient() as client:
        async with asyncssh.connect(
            "localhost", 12361, known_hosts=None, encoding=None
        ) as conn:
            async with conn.create_process(r"yes n | head -n 20000") as proc:
                # The maxsize here and chunksize below probably should be tuned
                queue = Queue(maxsize=128_000)

                async def queuer():
                    while chunk := await proc.stdout.read(8192):
                        await queue.put(chunk)

                    # The empty bytes signals the end of the file
                    await queue.put(b"")

                async def reader():
                    while chunk := await queue.get():
                        yield chunk
                        queue.task_done()

                    # Don't forget the final empty chunk
                    queue.task_done()

                # TODO: In 3.11, can do this with a task group
                queue_task = asyncio.create_task(queuer())
                response_task = asyncio.create_task(
                    client.post("http://localhost:8000", content=reader())
                )

                await asyncio.gather(queue_task, response_task)
                await queue.join()  # This shouldn't be necessary

                response = response_task.result()

                j = json.loads(response.content.decode("utf8"))
                assert list(j) == ["Hi"]
                assert j["Hi"] == "n\n" * 20000


if __name__ == "__main__":
    asyncio.run(queued_main())
