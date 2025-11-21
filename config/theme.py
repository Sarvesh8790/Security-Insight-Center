"""
Visual theme configuration for Security Insights Center
CrowdStrike/SentinelOne-inspired cybersecurity theme
"""

CYBER_THEME = {
    "bg_main": "#050506",
    "bg_card": "#0E0F14",
    "border_glow": "#5E5CE6",
    "accent": "#00AEEF",
    "accent_soft": "#6A5ACD",
    "text_primary": "#E5E5F0",
    "text_muted": "#A0A0B0",
    "text_dim": "#6B7280",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
}

SEVERITY_COLORS = {
    "Critical": CYBER_THEME["danger"],
    "High": CYBER_THEME["warning"],
    "Medium": CYBER_THEME["info"],
    "Low": CYBER_THEME["success"],
}

STATUS_COLORS = {
    "Open": CYBER_THEME["danger"],
    "In Progress": CYBER_THEME["warning"],
    "Closed": CYBER_THEME["success"],
}
