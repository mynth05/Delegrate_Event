from enum_exception import DeviceStatus

from abc import ABC
from datetime import datetime
from enum_exception import DeviceStatus, AlertSeverity
from event_args import DeviceStatusChangedEventArgs, DeviceAlertEventArgs
from enum_exception import InvalidDeviceReadingException

class TeachingDevice(ABC):
    def __init__(self, device_id: str, device_name: str):
        self.id = device_id
        self.name = device_name
        self._status = DeviceStatus.Available
        
        # Danh sách các hàm đăng ký sự kiện (Delegate/Listeners simulation)
        self.status_changed_listeners = []
        self.alert_raised_listeners = []

    @property
    def status(self) -> DeviceStatus:
        return self._status

    def change_status(self, new_status: DeviceStatus):
        if self._status == new_status:
            return
        
        old_status = self._status
        self._status = new_status
        
        args = DeviceStatusChangedEventArgs(self.id, old_status, new_status, datetime.now())
        self.on_status_changed(args)

    def raise_alert(self, message: str, severity: AlertSeverity):
        args = DeviceAlertEventArgs(self.id, message, severity, datetime.now())
        self.on_alert_raised(args)

    def on_status_changed(self, e: DeviceStatusChangedEventArgs):
        for listener in self.status_changed_listeners:
            listener(self, e)

    def on_alert_raised(self, e: DeviceAlertEventArgs):
        for listener in self.alert_raised_listeners:
            listener(self, e)


class ProjectorRemote(TeachingDevice):
    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name)
        self.battery_level = 100

    def update_battery_level(self, new_level: int):
        if not (0 <= new_level <= 100):
            raise InvalidDeviceReadingException(self.id, new_level)
        
        old_level = self.battery_level
        self.battery_level = new_level

        if self.battery_level == 0:
            self.raise_alert("Pin máy chiếu đã cạn kiệt hoàn toàn!", AlertSeverity.Critical)
        elif self.battery_level < 20 and old_level >= 20:
            self.raise_alert("Mức pin máy chiếu xuống thấp dưới 20%.", AlertSeverity.Warning)


class AirConditionerRemote(TeachingDevice):
    def __init__(self, device_id: str, name: str, assigned_room: str):
        super().__init__(device_id, name)
        self.assigned_room = assigned_room
        self.is_responsive = True

    def update_response_state(self, is_responsive: bool):
        if self.is_responsive and not is_responsive:
            self.raise_alert(f"Điều hòa tại phòng {self.assigned_room} chuyển sang trạng thái không phản hồi.", AlertSeverity.Critical)
        self.is_responsive = is_responsive


class WirelessMicrophone(TeachingDevice):
    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name)
        self.battery_level = 100
        self.signal_quality = 100

    def update_battery_level(self, new_level: int):
        if not (0 <= new_level <= 100):
            raise InvalidDeviceReadingException(self.id, new_level)
        
        self.battery_level = new_level
        if self.battery_level == 0:
            self.raise_alert("Micro: Pin bằng 0!", AlertSeverity.Critical)
        elif self.battery_level < 30:
            self.raise_alert("Micro: Pin dưới 30%.", AlertSeverity.Warning)

    def update_signal_quality(self, new_quality: int):
        if not (0 <= new_quality <= 100):
            raise InvalidDeviceReadingException(self.id, new_quality)
        
        self.signal_quality = new_quality
        if self.signal_quality == 0:
            self.raise_alert("Micro: Chất lượng tín hiệu bằng 0!", AlertSeverity.Critical)
        elif self.signal_quality < 40:
            self.raise_alert("Micro: Chất lượng tín hiệu thấp dưới 40%.", AlertSeverity.Warning)