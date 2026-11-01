from typing import Iterable
from teaching_device import TeachingDevice
from services import ConsoleNotificationService, DeviceAuditLogger, MaintenanceService

class DeviceMonitoringCoordinator:
    def __init__(
        self,
        devices: Iterable[TeachingDevice],
        notification_service: ConsoleNotificationService,
        audit_logger: DeviceAuditLogger,
        maintenance_service: MaintenanceService
    ):
        self.devices = list(devices)
        self.notification_service = notification_service
        self.audit_logger = audit_logger
        self.maintenance_service = maintenance_service
        self._is_subscribed = False

    def subscribe(self):
        if self._is_subscribed:
            return

        for device in self.devices:
            # Tránh đăng ký trùng lặp
            if self.notification_service.handle_alert not in device.alert_raised_listeners:
                device.alert_raised_listeners.append(self.notification_service.handle_alert)
            
            if self.maintenance_service.handle_critical_alert not in device.alert_raised_listeners:
                device.alert_raised_listeners.append(self.maintenance_service.handle_critical_alert)

            if self.audit_logger.handle_status_changed not in device.status_changed_listeners:
                device.status_changed_listeners.append(self.audit_logger.handle_status_changed)

        self._is_subscribed = True

    def unsubscribe(self):
        if not self._is_subscribed:
            return

        for device in self.devices:
            if self.notification_service.handle_alert in device.alert_raised_listeners:
                device.alert_raised_listeners.remove(self.notification_service.handle_alert)
            
            if self.maintenance_service.handle_critical_alert in device.alert_raised_listeners:
                device.alert_raised_listeners.remove(self.maintenance_service.handle_critical_alert)

            if self.audit_logger.handle_status_changed in device.status_changed_listeners:
                device.status_changed_listeners.remove(self.audit_logger.handle_status_changed)

        self._is_subscribed = False

    def dispose(self):
        self.unsubscribe()

    def __enter__(self):
        self.subscribe()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()