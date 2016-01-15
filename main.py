import os
from pyCiscoSparkAPI import SparkClient

def main():
    token = os.environ['SPARK_ACCESS_TOKEN']

    client = SparkClient(token)
    rooms = client.rooms.getRooms()
    for room in rooms:
        print(room.title())

#    client = SparkClient(token,timeout=60)
#
#    rooms = client.rooms.getRooms(showSipAddress=False,max=1000)
#
#    for room in rooms:
#        print(room.title()) 
#        print(room.sipAddress()) 


if __name__ == "__main__":
    main()
