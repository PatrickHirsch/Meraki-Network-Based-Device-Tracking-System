This program is a rudimentary tracking system for network-connected devices within a [Cisco Meraki](https://www.cisco.com/site/us/en/about/corporate-strategy-office/acquisitions/meraki/index.html)-managed network using Wireless Access Points.  Because Meraki is implemented in larger institutional networks and handles smooth handoffs between Wireless Access Points as a device physically travels and moves across a large physical environment the idea is that a device that travels/moves frequently such as a robot or hand held device that may be  easily lost/misplaced could run this script to report its location within the institution.

# Requirements/Assumptions
* [Cisco Meraki](https://www.cisco.com/site/us/en/about/corporate-strategy-office/acquisitions/meraki/index.html), the script relies on the [MR access point local status page](https://documentation.meraki.com/Platform_Management/Dashboard_Administration/Troubleshooting_and_Support/Troubleshooting/Using_the_Cisco_Meraki_Device_Local_Status_Page#:~:text=local%20status%20page%3A-,10.128.128.126,-Use%20the%20following) to derive the device's location from the name of the WAP it is currently connected to.
	* The assumption is made that the access points within the network are named consistently and logically in a way that describes their physical locations such as room numbers
		* Specifically, the current assumption is that they are named as "Room_Number-ArbitraryData" so a location is reported as "Room Number" ***Todo: Move this to a helper function or external module for simpler configuration/adaptation***
* [S3 compatible Bucket](https://docs.aws.amazon.com/en_en/AmazonS3/latest/userguide/Welcome.html), the script publishes the device's determined current location to an S3 bucket for easy and inexpensive storage/retrieval over the internet.

# Todo:
* Move AP Name-to-room parsing to a helper function or external module for simpler configuration/adaptation
* Convert `myS3AuthConfig.py` to `config.json` ***Do not forget to add `config.json` to `.gitignore`***
	* Move all potentially variable parts of the code to `config.json`
	* Create and appropriately comment `config.json.template`
* Add a timeout/expiration for published data so that services retrieving data from bucket can somehow determine that data is out of date when script is offline/not running.
* Comment code better
* Expand on reporting page.  
	* Make an API?
* Historical data?
* Proper logging
* How necessary is better error handling?  Fail on first error?  Consistent errors?
	* Fail on S3 authentication failures?
	* Fail on malformed JSON?