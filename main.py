from teaching_device import ProjectorRemote, AirConditionerRemote, WirelessMicrophone
from enum_exception import DeviceStatus, AlertSeverity
from services import (
    ConsoleNotificationService, 
    DeviceAuditLogger, 
    MaintenanceService, 
    FilteredAlertSubscriber
)
from coordinator import DeviceMonitoringCoordinator
from enum_exception import InvalidDeviceReadingException

if __name__ == "__main__":
    print("--- KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ THIẾT BỊ ---")
    
    # 1. Khởi tạo thiết bị
    projector = ProjectorRemote("PROJ-01", "Máy chiếu Hội trường A")
    ac = AirConditionerRemote("AC-01", "Điều hòa phòng 302", "Phòng 302")
    mic = WirelessMicrophone("MIC-01", "Micro không dây giảng đường")

    devices = [projector, ac, mic]

    # 2. Khởi tạo các Service (Subscriber)
    notification_svc = ConsoleNotificationService()
    audit_logger = DeviceAuditLogger()
    maintenance_svc = MaintenanceService()

    # 3. Sử dụng Coordinator để quản lý đăng ký
    with DeviceMonitoringCoordinator(devices, notification_svc, audit_logger, maintenance_svc):
        
        print("\n--- TEST 1: Thay đổi trạng thái thiết bị ---")
        projector.change_status(DeviceStatus.Borrowed)
        projector.change_status(DeviceStatus.UnderMaintenance)

        print("\n--- TEST 2: Cảnh báo pin máy chiếu (Warning & Critical) ---")
        projector.update_battery_level(15)  # Gây cảnh báo Warning
        projector.update_battery_level(0)   # Gây cảnh báo Critical -> Kích hoạt Maintenance Service

        print("\n--- TEST 3: Điều hòa mất phản hồi ---")
        ac.update_response_state(False)     # Gây cảnh báo Critical

        print("\n--- TEST 4: Sử dụng Delegate lọc cảnh báo tùy chỉnh ---")
        critical_filter_sub = FilteredAlertSubscriber(
            filter_func=lambda alert: alert.severity == AlertSeverity.Critical,
            action_func=lambda alert: print(f"==> [LỌC RIÊNG] Phát hiện lỗi NẶNG trên {alert.device_id}: {alert.message}")
        )
        # Đăng ký thủ công bộ lọc riêng vào micro
        mic.alert_raised_listeners.append(critical_filter_sub.handle_alert)

        mic.update_signal_quality(0)        # Gây cảnh báo Critical ở micro

        print("\n--- TEST 5: Ngoại lệ dữ liệu không hợp lệ ---")
        try:
            mic.update_battery_level(150)
        except InvalidDeviceReadingException as ex:
            print(f"[BẮT NGOẠI LỆ]: {ex}")

    print("\n--- HỆ THỐNG ĐÃ KẾT THÚC ---")