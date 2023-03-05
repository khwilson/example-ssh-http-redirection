import asyncio
import subprocess
from typing import Generator

import asyncssh


class NoAuthSSHServer(asyncssh.SSHServer):
    """No auth ssh server for local testing"""

    def begin_auth(self, username: str) -> asyncssh.misc.MaybeAwait[bool]:
        return False


async def simple_server(handler, port: int = 12361) -> Generator[int, None, None]:
    """Start a server and yield its port"""

    private_key = asyncssh.generate_private_key("ssh-rsa")
    async with asyncssh.create_server(
        NoAuthSSHServer,
        "localhost",
        port,
        server_host_keys=[private_key],
        process_factory=handler,
        encoding=None,
    ) as server:
        # Await forever
        await asyncio.Future()


if __name__ == "__main__":

    def handler(process):
        p = subprocess.run(["/bin/bash", "-c", process.command], capture_output=True)
        process.stdout.write(p.stdout)
        process.exit(0)

    asyncio.run(simple_server(handler))
