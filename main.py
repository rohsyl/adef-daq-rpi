from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                    AiInputMode, Range, AInFlag)
import requests


# dependencies :
# pip3 install requests uldaq

def main():

    daq_device = connect()

    temperatures = read(daq_device)

    temperatures = correct(temperatures)

    send(temperatures)

def connect():
    # Get a list of available DAQ devices
    devices = get_daq_device_inventory(InterfaceType.USB)
    # Create a DaqDevice Object and connect to the device
    daq_device = DaqDevice(devices[0])
    daq_device.connect()

    return daq_device

def read(daq_device):

    # Get AiDevice and AiInfo objects for the analog input subsystem
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()

    temperatures = {}

    # Read and display voltage values for all analog input channels
    for channel in range(ai_info.get_num_chans()):
        data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED,
                              Range.BIP10VOLTS, AInFlag.DEFAULT)
        print('Channel', channel, 'Data:', data)

        temperatures[channel] = data

    return temperatures


def send(data):
    body = {"data": data}
    requests.post(url="http://192.168.1.162/temp-monit/api/temp", params=body)


def correct(temperatures):

    for (channel, temperature) in temperatures:
        temperature[channel] = 1.42 * temperature - 726.24

    return temperatures


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
