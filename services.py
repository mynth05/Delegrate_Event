from enum_exception import AlertSeverity
from event_args import DeviceAlertEventArgs, DeviceStatusChangedEventArgs

class ConsoleNotificationService:
    def handle_alert(self, sender, e: DeviceAlertEventArgs):
        print(f"[{e.severity.name}] Thiết bị {e.device_id}: {e.message} (Lúc: {e.occurred_at})")


class DeviceAuditLogger:
    def __init__(self):
        self._entries = []

    @property
    def entries(self):
        return self._entries

    def handle_status_changed(self, sender, e: DeviceStatusChangedEventArgs):
        log_msg = f"{e.changed_at}: {e.device_id}, {e.old_status.name} -> {e.new_status.name}"
        self._entries.append(log_msg)
        print(f"[AUDIT LOG]: {log_msg}")


class MaintenanceService:
    def __init__(self):
        self._requests = []

    @property
    def requests(self):
        return self._requests

    def handle_critical_alert(self, sender, e: DeviceAlertEventArgs):
        if e.severity != AlertSeverity.Critical:
            return
        req = f"Yêu cầu bảo trì cho thiết bị {e.device_id}: {e.message}"
        self._requests.append(req)
        print(f"[MAINTENANCE TICKET CREATED]: {req}")


class FilteredAlertSubscriber:
    def __init__(self, filter_func, action_func):
        self.filter_func = filter_func
        self.action_func = action_func

    def handle_alert(self, sender, e: DeviceAlertEventArgs):
        if self.filter_func(e):
            self.action_func(e)