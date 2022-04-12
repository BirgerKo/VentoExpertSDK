from enum import Enum

class Func(Enum):
    READ = 1        # parameter read
    WRITE = 2       # parameter write. The controller does not send any response regarding the status of the given parameters
    WRITEREAD = 3   # parameter write with subsequent controller response regarding the status of the given parameters
    INCREAD = 4     # parameter increment with subsequent controller response regarding the status of the given parameters
    DECREAD = 5     # parameter decrement with subsequent controller response regarding the status of the given parameters
    RESPONSE = 6    # controller response to the request (FUNC = 0x01(READ), 0x03(WRITEREAD), 0x04(INCREAD), 0x05(DECREAD))