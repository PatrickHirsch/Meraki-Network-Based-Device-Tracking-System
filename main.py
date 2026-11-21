import requests
import json
import boto3
import time

# Used to suppress Insecure Request Warnings in program output.
# The Meraki page can only be accessed through an insecure connection,
#   this risk is known and accepted as necessary.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 
import myS3AuthConfig
s3 = boto3.client(
    "s3",
    endpoint_url=myS3AuthConfig.endpoint_url,
    aws_access_key_id=myS3AuthConfig.aws_access_key_id,
    aws_secret_access_key=myS3AuthConfig.aws_secret_access_key,
    region_name=myS3AuthConfig.region_name,
    config=boto3.session.Config(
        signature_version="s3v4"
    )
)




def locateRoom():
    try:
        print("Attempting to JSON data from Cisco Meraki.")
        response=requests.get('http://10.128.128.126/index.json',verify=False,allow_redirects=True)
    except:
        print("ERROR: Unable to access Cisco Meraki.")
        accessPoint="Offline/Off Campus"
    else:
        print("Cisco Meraki data retrieved.")
        try:
            data=json.loads(response.text)
            accessPoint=data["config"]["node_name"]
            print("Access Point identified as '"+accessPoint+"'")
        except:
            print("Cisco Meraki data malformed?  Unable to parse JSON.")
            accessPoint="ERROR"
    
    currentRoom=accessPoint.split("-")[0].replace("_"," ")
    print("Room identified as '"+currentRoom+"'")
    return currentRoom

def bucketPUT(room):
    print("PUT REQUEST: Attempting to put "+room+" in the bucket.")
    try:
        response=s3.put_object(
            Bucket=myS3AuthConfig.bucketName,
            Key=myS3AuthConfig.bucketObjectKey,
            Body=room,
            ContentType="text/plain"
        )
    except:
        print("PUT REQUEST ERROR: Put request unsuccessful.")
        room="Unknown"
    else:
        print("PUT REQUEST: Successfully put "+room+" in the bucket.")


def main():
    print("Starting tracker...")
    cachedRoom="Unknown"
    while True:
        currentRoom=locateRoom()
        
        if cachedRoom!=currentRoom:
            print("Room change detected ("+cachedRoom+"!="+currentRoom+")")
            cachedRoom=currentRoom
            bucketPUT(cachedRoom)
        else:
            print("No room change detected ("+cachedRoom+"=="+currentRoom+")")
    
        time.sleep(20)
    
    
main()