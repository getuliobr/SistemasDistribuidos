MESSAGE_TYPE_REQUEST = 0x01
MESSAGE_TYPE_RESPONSE = 0x02

STATUS_SUCCESS = 0x01
STATUS_ERROR = 0x02

COMMAND_ADDFILE = 0x01
COMMAND_DELETE = 0x02
COMMAND_GETFILESLIST = 0x03
COMMAND_GETFILE = 0x04


def convertBytesNumber(number):
    if number < 1024:
        return str(number) + " B"
    elif number < 1048576:
        return format(number/1024, '.3f') + " KB"
    elif number < 1073741824:
        return format(number/1048576, '.3f') + " MB"
    else:
        return format(number/1073741824, '.3f') + " GB"