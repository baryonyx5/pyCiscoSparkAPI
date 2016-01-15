pyspark
================
A simple Python SDK interface for the Spark for Developers APIs.

Overview
---------
This SDK exposes the Spark for Developers APIs in simple Python class wrappers.

For more information on Sprark for Developers see http://developer.ciscospark.com

Installation
---------

#### Manual

```
git clone https://github.com/shenning00/pyCiscoSparkAPI.git
cd pyCiscoSparkAPI
python ./setup.py build
python ./setup.py install
```


Usage
----
Here are a few simple examples.

__Note__: This SDK uses the simple Personal Access Token. See here ((see https://developer.ciscospark.com/getting-started.html)) for more info on how to get the token.

###Getting Started####
```python
from pyCiscoSparkClient import SparkClient

token="abcdef....456790"
client = SparkClient(token)
rooms = client.rooms.getRooms()
for room in rooms:
    print(room.title())
```

