from enum import Enum

class DeviceStatus(Enum):
    Available = 1
    Borrowed = 2
    UnderMaintenance = 3

class AlertSeverity(Enum):
    Information = 1
    Warning = 2
    Critical = 3

class InvalidDeviceReadingException(Exception):
    def __init__(self, device_id: str, invalid_value: int, message: str = None):
        self.device_id = device_id
        self.invalid_value = invalid_value
        super().__init__(message or f"Giá trị không hợp lệ [{invalid_value}] cho thiết bị {device_id}")