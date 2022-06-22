from ast import Assert
import sys
import traceback
from time import sleep
from threading import Thread

import tango

class BraggBugTest(tango.LatestDeviceImpl):

    _Position = [0.0, 0.0]

    def __init__(self, cl, name):
        tango.LatestDeviceImpl.__init__(self, cl, name)

        self.debug_stream("__init__ method")
        self.runBackgroundWrite = True
        BraggBugTest.init_device(self)

    def backgroundWrite(self):
        while self.runBackgroundWrite:
            self.get_device_attr().get_attr_by_name('Position').set_write_value([1.2, 3.4])
            self.debug_stream("Set_write_value [1.2, 3.4]")
            sleep(0.001)
 

    def init_device(self):

        try:
            self.debug_stream("In init_device method")

            # Change Device State to INIT and push event:
            self.set_state(tango.DevState.INIT)
            self.push_change_event('State', tango.DevState.INIT)

            # Get device properties
            self.get_device_properties(self.get_device_class())

            self.set_state(tango.DevState.ON)
            self.push_change_event('State', tango.DevState.ON)

            self.debug_stream("Device ON")

            backgroundThread = Thread(target=self.backgroundWrite)
            backgroundThread.start()

        except Exception as e:
            self.error_stream("Problems in init_device method: {} "
                              "\n {}".format(e, traceback.format_exc())
                              )
            self.set_state(tango.DevState.FAULT)
            self.push_change_event('State', tango.DevState.FAULT)
            self.error_stream("Device from INIT to FAULT state.")

    def delete_device(self):
        self.debug_stream("delete_device method on",self.get_name())
        tango.LatestDeviceImpl.delete_device(self)

    def read_Position(self, attr):
        attr.set_value(self._Position)

    def write_Position(self, attr):
        newPos = attr.get_write_value()
        self._Position = newPos
        try:
            assert (newPos == [5.6, 7.8]).all(), "Not writting correct value"
        except AssertionError:
            self.debug_stream("newPos = {}".format(newPos))
            self.runBackgroundWrite = False
            raise

        

class BraggBugTestClass(tango.DeviceClass):

    attr_list = {
        "Position":
            [[tango.DevDouble,
              tango.SPECTRUM,
              tango.READ_WRITE,
              4096], {
                "label": 'Position Test',
              }
             ]
    }


def main():
    try:
        util = tango.Util(sys.argv)
        util.add_class(BraggBugTestClass, BraggBugTest, 'BraggBugTest')

        db = tango.Database()
        classes = db.get_device_class_list("BraggBugTest/{}".format(sys.argv[1]))[
                  1::2]
        print("Found {} classes for device server BraggBugTest".format(classes))

        ui = tango.Util.instance()
        ui.server_init()
        ui.server_run()

    except Exception as e:
        print("-------> Received an unforeseen exception occurred:")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

