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

Next, you'll need to create a `.env` file with the contents that are listed in `.env.sample`.
We used a small AWS instance for our testing (hence the `AWS_` prefixes). But this works
with any ssh server that does public key auth. Just provide your host (`AWS_IP`), username
(`AWS_USER`), and the path to your private key (`AWS_KEY`).

## Running

To run, open a terminal and start the little FastAPI server that we'll be catting to:

```
poetry run server.py
```

Then in a new terminal, run the test script:

```
poetry run test.py
```

You should get a json dictionary with a single key (`"Hi"`) and a value of 20,000 lines of `n`.

## TODO

Really, we should probably start a small SSHServer locally for this test, a la [this mock](https://gist.github.com/vxgmichel/d0b7e4cc3caab32601051ee262ee7b31).
But that's outside of scope for the moment. :-)

## License

MIT
