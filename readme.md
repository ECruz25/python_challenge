# Usage

## Parameters

|Parameter|Description|
|---------|-----------|
|-f, --file|Use this if you wish to use a file with IPs to get the geo location or make a RDAP Lookup. A local filename has to be passed. |
|-i, --ip|Use this if you wish to pass a single or a list of IP addresses. Include all IP Address as a single string but separated with commas|
|-g, --geo| Use this to enable the geo location feature. This works as a boolean|
|-r, -rdap| Use this to enable the RDAP Lookup feature. This works as a boolean|

### Example
The following example will do a geolocation and RDAP Lookup for the ip: 157.240.14.35 
`python main.py -i "157.240.14.35" -g -r`

The following example will do a geolocation for the ips: 157.240.14.35 and 142.250.64.206
`python main.py -i "157.240.14.35,142.250.64.206" --geo`

The following example will do a geolocation for the ips within the file list_of_ips.txt
`python main.py --file "list_of_ips.txt" --geo -rdap`