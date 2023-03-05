# An Example of Redirecting an SSH Stream to an HTTP Stream Asynchronously

Sometimes, your servers need to speak to each other. One communicates over ssh.
One communicates over HTTP. And you want to ship a large file from one to the
other.

You could (maybe should?) first download the file to a local disk via scp
and _then_ upload it via HTTP to your target server. But that adds a lot of
time to your process.

Instead, perhaps you want to just hook up the streams, preferably asynchronously.
How do you do that? This little code snippet shows how.

## Requirements

We use poetry. If you have it installed, then run the following to install your requirments.

```bash
poetry install
```

## Running

To run, you'll need to start two different processes with the following commands:

```
poetry run server.py  # A simple HTTP server
poetry run myssh.py   # A very simple SSH server
```

Once these are running, then you can run the test script.

```
poetry run test.py
```

This script contains an assert which checks if the response is a dictionary with a single key
(`"Hi"`) and a value of 20,000 lines of `n`.

## License

MIT
