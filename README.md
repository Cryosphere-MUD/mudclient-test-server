This is a simple but comprehensive test server for mud clients to test protocol support and rendering.

To run, it needs python and zstandard, for example:

`python -m venv venv
source venv/bin/activate
pip install zstandard
python ./mudclient-test-server.py`

It serves on port 5050 by default. This could be altered by editing it in `./mudclient-test-server.py`
