### Build image:
sudo docker build -t alert-api .

### Run image:
sudo docker run -d -p 9095:9095 -v /opt/prometheus/alerting:/opt/prometheus/alerting alert-api

### Operations with rules:
http://localhost:9095/v1/alerting/
``` json
{
    "10.10.10.1":{
        "action": "create",
        "pending_time": "100"
    },
    "10.10.10.2":{
        "action": "update",
        "pending_time": "120"
    },
    "10.10.10.3":{
        "action": "delete",
        "pending_time": "120"
    }
}
```
