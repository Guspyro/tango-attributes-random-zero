from time import sleep

import tango

device = tango.DeviceProxy('test/braggbugtest/1')
while True:
    try:
        pos = device.read_attribute('Position')
        print("Position:",pos.value)
        print("Write value:",pos.w_value)
        device.write_attribute('Position', [5.6, 7.8])
        print('Write_attribute [5.6, 7.8]')
        sleep(0.1)
    except KeyboardInterrupt:
        print("Exit")
        quit()
    except Exception as e:
        print("Client failed to write", e)
        quit()
