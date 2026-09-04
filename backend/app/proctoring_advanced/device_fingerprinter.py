"""
ExamHub - Browser & Hardware Environment Fingerprinting
Detects multi-monitor setups, virtual machine indicators, and hardware environment spoofing.
"""

from typing import Dict, Any, List, Optional

class DeviceEnvironmentAuditor:
    """Audits client environment telemetry for anti-cheating enforcement."""

    @staticmethod
    def audit_client_fingerprint(client_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        client_info contains:
        {
          'screen_width': 1920, 'screen_height': 1080,
          'available_width': 1920, 'available_height': 1040,
          'device_pixel_ratio': 1.0,
          'hardware_concurrency': 8,
          'color_depth': 24,
          'user_agent': '...',
          'is_virtual_machine': False,
          'connected_screen_count': 1
        }
        """
        violations = []

        # 1. Multi-monitor detection
        screen_count = int(client_info.get("connected_screen_count", 1))
        if screen_count > 1:
            violations.append(f"Multiple display monitors detected ({screen_count} active screens). Extended desktop forbidden.")

        # 2. Virtual Machine / Remote Desktop Heuristics
        ua = client_info.get("user_agent", "").lower()
        if any(vm in ua for vm in ["vmware", "virtualbox", "qemu", "hyper-v"]):
            violations.append("Virtual Machine execution environment detected.")

        # 3. Suspicious screen dimensions (e.g. tiny resolution)
        width = int(client_info.get("screen_width", 1024))
        height = int(client_info.get("screen_height", 768))
        if width < 800 or height < 600:
            violations.append(f"Invalid screen geometry: {width}x{height} below minimum required display resolution.")

        # 4. Hardware concurrency check
        concurrency = int(client_info.get("hardware_concurrency", 4))
        if concurrency < 1:
            violations.append("Anomalous CPU core allocation (0 logical cores reported).")

        is_clean = (len(violations) == 0)

        return {
            "is_environment_secure": is_clean,
            "connected_screen_count": screen_count,
            "resolution": f"{width}x{height}",
            "hardware_concurrency": concurrency,
            "violations_detected": violations,
            "compliance_status": "Compliant" if is_clean else "Environment Breach Flagged"
        }
