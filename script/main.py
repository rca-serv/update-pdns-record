import yaml
import requests
import ipget


def entry():
    main()


def main():
    print('Hello, world!')
    config = get_config()
    address = ipget.ipget().ipaddr(config['interface'])

    update_dns(address, config)


def update_dns(address, config):
    # make request
    params = {
        "rrsets": [
            {
                "name": config['hostname'],
                "type": config['record_type'],
                "ttl": config['ttl'],
                "changetype": "REPLACE",
                "records": [
                    {
                        "content": address,
                        "disabled": False
                    }
                ]
            }
        ]
    }

    endpoint = "http://"+config['api_host']+"/api/v1/servers/"+config['server_id']+"/zones/"+config['zone_id']

    headers = {
            "X-API-Key": config['api_key'],
            "Content-Type": "application/json"
    }

    # send
    return requests.patch(endpoint, headers=headers, json=params)


def get_config():
    with open('config.yml') as f:
        return yaml.safe_load(f)
