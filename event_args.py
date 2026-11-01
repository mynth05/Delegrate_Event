from datetime import datetime
from enum_exception import DeviceStatus, AlertSeverity

class DeviceStatusChangedEventArgs:
    def __init__(self, device_id: str, old_status: DeviceStatus, new_status: DeviceStatus, changed_at: datetime):
        self.device_id = device_id
        self.old_status = old_status
        self.new_status = new_status
        self.changed_at = changed_at

class DeviceAlertEventArgs:
    def __init__(self, device_id: str, message: str, severity: AlertSeverity, occurred_at: datetime):
        self.device_id = device_id
        self.message = message
        self.severity = severity
        self.occurred_at = occurred_at