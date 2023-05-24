# Connecting to a M5 over CLI (via MQTT)

This example file connects to your machine over MQTT to view basic data.

1. Navigate to wherever you cloned this repository to. Open the "examples" folder and open a terminal window there, just like in the previous section.

2. In order to achieve a successful connection via `mqtt-connect.py`, it's important to understand each argument that is required to be input. Here's a valid command to run this script if your AnkerMake account was registered in the USA:

   ```bash
   python3 mqtt-connect.py -r us -A "YOUR_AUTH_TOKEN_HERE"
   ```

   The first required argument is `-r`  (or `--region`) for the region your AnkerMake account was registered in. Use either `eu`  or `us`.

   The second required argument is `-A`  (or `--auth`) and you should paste in your Authentication Token here. You can extract that from your `login.json` file by following [this guide](/documentation/example-file-usage/extract-auth-token-example-file-usage.md).

3. **[Optional Step]** If desired, you can save the contents of the output to a log file by adding `> output.log` to the end of the command in the previous step:

   ```bash
   python3 mqtt-connect.py -r us -A "YOUR_AUTH_TOKEN_HERE" > output.log
   ```

Now you should see a bunch of data updating in your terminal and this will update anytime a data point changes values. It should look something like this and will be quite a bit more colorful:

```
TOPIC [/phone/maker/YOUR_SERIAL_NUMBER_HERE/notice]
4d41c1000501020546c00100045b126436353163383633612d366266652d313033622d396234372d35623534393334336637356100000000000000000000000080d48d67e412394ccc2ef9d76b966687e047c862d36ca291d70a7c732aec8f28e7a315dc1dab0fc51eed678bee3959ae14af8ef3670553412e13cc90a0a6d2c4c0a949f072a716ef9153eed115eb7a7decf9c88bcb07922bae5cc925a96e954b1f70dfb55b079b696178f2c918c0af5c9e5861ae7809b97b80614cec6e948f86cc
MqttMsg(
    size=193,
    m3=5,
    m4=1,
    m5=2,
    m6=5,
    m7=70,
    packet_type=<MqttPktType.Single: 192>,
    packet_num=1,
    time=1678924548,
    device_guid='SOME_DATA_HERE',
    data=b'[{"commandType":1003,"currentTemp":5263,"targetTemp":18000},{"commandType":1004,"currentTemp":3990,"targetTemp":6000}]'
)
```

Refer to the [MQTT documentation](https://github.com/Ankermgmt/ankermake-m5-research/tree/master/mqtt) for information on what values you're seeing in this output. For the general structure and abstract explanation of the AnkerMake MQTT communications, reference the documentation in this repository starting with the [MQTT Overview](../mqtt-overview.md).

