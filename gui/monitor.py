# ============================================================
# gui/intelligence/monitor.py
# MONITOR - Module Status Dashboard
# SUPER ROBUST v2.1 - WITH FALLBACKS
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Any

import customtkinter as ctk

# ============================================================
# FALLBACK IMPORTS & CONSTANTS
# ============================================================

# Try to import monitor components with fallback
try:
    from ..monitor import ModuleMonitor, ModuleStatus, ModuleType
    MONITOR_AVAILABLE = True
except ImportError:
    MONITOR_AVAILABLE = False
    # Define fallback enums
    class ModuleStatus:
        ONLINE = "online"
        OFFLINE = "offline"
        DEGRADED = "degraded"
        ERROR = "error"
        UNKNOWN = "unknown"
    
    class ModuleType:
        CORE = "core"
        LEARNING = "learning"
        MARKET = "market"
        UI = "ui"
        UTILITY = "utility"
        UNKNOWN = "unknown"
    
    class ModuleMonitor:
        def __init__(self):
            self.modules = {}
            self._callbacks = []
        
        def add_callback(self, callback):
            self._callbacks.append(callback)
        
        def refresh(self):
            pass
        
        def start_monitoring(self):
            pass
        
        def stop_monitoring(self):
            pass
        
        def get_module_health(self):
            return {"total": 0, "online": 0, "degraded": 0, "error": 0, "offline": 0}
        
        def get_module_metrics(self, name):
            return {}
        
        def run_diagnostics(self):
            return {"status": "unavailable", "message": "Monitor module not available"}
        
        def export_diagnostics(self, filepath):
            with open(filepath, 'w') as f:
                json.dump({"status": "unavailable"}, f)

try:
    from ..monitor.widgets import StatusIndicator, ProgressCard, MetricBox, LogViewer
    WIDGETS_AVAILABLE = True
except ImportError:
    WIDGETS_AVAILABLE = False
    # Define fallback widgets if needed
    class StatusIndicator(ctk.CTkFrame):
        def __init__(self, parent, label="Status", **kwargs):
            super().__init__(parent, fg_color="transparent", **kwargs)
            self.label = ctk.CTkLabel(self, text=label, font=("Segoe UI", 10))
            self.label.pack(side="left")
            self.indicator = ctk.CTkLabel(self, text="●", font=("Segoe UI", 12), text_color="#6B7280")
            self.indicator.pack(side="left", padx=5)
        def set_status(self, online):
            self.indicator.configure(text_color="#22C55E" if online else "#EF4444")
    
    class ProgressCard:
        pass
    
    class MetricBox:
        pass
    
    class LogViewer(ctk.CTkTextbox):
        def __init__(self, parent, bg="#0B0F14", **kwargs):
            super().__init__(parent, fg_color=bg, text_color="#E8EDF2", font=("Consolas", 10), **kwargs)
            self.configure(state="disabled")
        
        def add_log(self, message, level="INFO"):
            self.configure(state="normal")
            self.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
            self.see("end")
            self.configure(state="disabled")
        
        def clear(self):
            self.configure(state="normal")
            self.delete("1.0", "end")
            self.configure(state="disabled")

# Try to import styles with fallback
try:
    from ..styles import COLORS, FONTS
except ImportError:
    # Define fallback colors and fonts
    COLORS = {
        'panel': '#1A2530',
        'background': '#0B0F14',
        'text': '#E8EDF2',
        'text_secondary': '#8D9AAA',
        'success': '#22C55E',
        'warning': '#F59E0B',
        'error': '#EF4444',
        'offline': '#6B7280',
        'accent': '#3B82F6',
        'accent_hover': '#2563EB',
        'bg_dark': '#131A22',
        'border': '#2D3748',
        'panel_light': '#2A3A4A',
        'info': '#3B82F6',
    }
    FONTS = ("Segoe UI", 10)
    FONT_BUTTON = ("Segoe UI", 11, "bold")

# Prediction availability flag
try:
    from core.learning.prediction import prediction, self_test
    PREDICTION_AVAILABLE = True
except ImportError:
    PREDICTION_AVAILABLE = False


class MonitorPage(ctk.CTkFrame):
    """
    Super Robust Module Monitor Page.
    
    Features:
    - Displays module status with fallback when monitor not available
    - Graceful degradation when dependencies missing
    - Auto-refresh with configurable interval
    - Manual refresh and export
    - Log viewer
    - Detailed module information
    """
    
    def __init__(self, parent, bot=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.bot = bot
        self.is_monitoring = False
        self.update_interval = 3000  # 3 seconds
        self._after_id = None
        
        # Initialize monitor if available
        if MONITOR_AVAILABLE:
            self.monitor = ModuleMonitor()
            self.monitor.add_callback(self._on_update)
        else:
            self.monitor = ModuleMonitor()  # fallback dummy
            self._create_dummy_modules()
        
        self.selected_module = None
        
        self._setup_ui()
        self._start_monitoring()
        self._refresh()
    
    # ============================================================
    # DUMMY DATA FOR FALLBACK
    # ============================================================
    
    def _create_dummy_modules(self):
        """Create dummy modules when real monitor not available."""
        class DummyModule:
            def __init__(self, name, type_str, version="1.0", status=ModuleStatus.UNKNOWN):
                self.name = name
                self.type = ModuleType(type_str) if hasattr(ModuleType, type_str) else ModuleType.UNKNOWN
                self.version = version
                self.status = status
                self.description = f"Dummy module for {name}"
                self.last_check = datetime.now().strftime("%H:%M:%S")
                self.dependencies = []
        
        dummy_modules = [
            ("Brain", "core", "4.2.3", ModuleStatus.ONLINE),
            ("Learning Engine", "learning", "2.0", ModuleStatus.ONLINE),
            ("Memory", "core", "1.5", ModuleStatus.ONLINE),
            ("Consciousness", "core", "2.1", ModuleStatus.DEGRADED),
            ("Scanner", "market", "1.0", ModuleStatus.OFFLINE),
        ]
        self.monitor.modules = {}
        for name, type_str, ver, status in dummy_modules:
            self.monitor.modules[name] = DummyModule(name, type_str, ver, status)
    
    # ============================================================
    # UI SETUP
    # ============================================================
    
    def _setup_ui(self):
        """Setup the UI with fallback for missing widgets."""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Stats bar at top
        self._setup_stats_bar(main_container)
        
        # Main content split
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left: Module list
        left_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['panel'],
                                 corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self._setup_module_list(left_frame)
        
        # Right: Details
        right_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['panel'],
                                  corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        self._setup_details_panel(right_frame)
        
        # Bottom: Log
        log_frame = ctk.CTkFrame(main_container, fg_color=COLORS['panel'],
                                corner_radius=10, height=120)
        log_frame.pack(fill="x", pady=(10, 0))
        self._setup_log_panel(log_frame)
    
    def _setup_stats_bar(self, parent):
        """Setup stats bar."""
        stats_frame = ctk.CTkFrame(parent, fg_color=COLORS['panel'],
                                  corner_radius=10, height=80)
        stats_frame.pack(fill="x", pady=(0, 5))
        stats_frame.pack_propagate(False)
        
        self.stats_labels = {}
        stats = [
            ('total', 'Total', '0', COLORS['info']),
            ('online', 'Online', '0', COLORS['success']),
            ('degraded', 'Degraded', '0', COLORS['warning']),
            ('error', 'Error', '0', COLORS['error']),
            ('offline', 'Offline', '0', COLORS['offline'])
        ]
        
        for key, label, value, color in stats:
            frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            frame.pack(side="left", padx=20, pady=10)
            
            ctk.CTkLabel(frame, text=label, font=("Segoe UI", 10),
                        text_color=COLORS['text_secondary']).pack()
            
            label_obj = ctk.CTkLabel(frame, text=value, font=("Segoe UI", 18, "bold"),
                                    text_color=color)
            label_obj.pack()
            self.stats_labels[key] = label_obj
        
        # Refresh button
        refresh_btn = ctk.CTkButton(stats_frame, text="🔄 Refresh",
                                   font=FONT_BUTTON,
                                   fg_color=COLORS['accent'],
                                   hover_color=COLORS['accent_hover'],
                                   width=120, height=35,
                                   command=self._refresh)
        refresh_btn.pack(side="right", padx=15, pady=10)
        
        # Export button
        export_btn = ctk.CTkButton(stats_frame, text="📤 Export",
                                  font=FONT_BUTTON,
                                  fg_color=COLORS['accent'],
                                  hover_color=COLORS['accent_hover'],
                                  width=100, height=35,
                                  command=self._export_report)
        export_btn.pack(side="right", padx=5, pady=10)
    
    def _setup_module_list(self, parent):
        """Setup module list using treeview."""
        # Header
        header = ctk.CTkLabel(parent, text="📋 Modules",
                             font=("Segoe UI", 14, "bold"),
                             text_color=COLORS['text'])
        header.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Treeview frame
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        columns = ('status', 'version', 'type')
        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                show='tree headings', height=12)
        
        self.tree.heading('#0', text='Module')
        self.tree.heading('status', text='Status')
        self.tree.heading('version', text='Version')
        self.tree.heading('type', text='Type')
        
        self.tree.column('#0', width=200)
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('version', width=100, anchor='center')
        self.tree.column('type', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical',
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
    
    def _setup_details_panel(self, parent):
        """Setup details panel with tabs."""
        # Header
        header = ctk.CTkLabel(parent, text="📊 Module Details",
                             font=("Segoe UI", 14, "bold"),
                             text_color=COLORS['text'])
        header.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Notebook
        self.notebook = ctk.CTkTabview(parent, fg_color=COLORS['background'])
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Tabs
        self.notebook.add("General")
        self.notebook.add("Metrics")
        self.notebook.add("Dependencies")
        self.notebook.add("Status")
        
        self._setup_general_tab()
        self._setup_metrics_tab()
        self._setup_deps_tab()
        self._setup_status_tab()
    
    def _setup_general_tab(self):
        """Setup general info tab."""
        tab = self.notebook.tab("General")
        self.detail_labels = {}
        fields = [
            ('Name', 'name'),
            ('Type', 'type'),
            ('Status', 'status'),
            ('Version', 'version'),
            ('Description', 'description'),
            ('Last Check', 'last_check'),
        ]
        
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            
            frame = ctk.CTkFrame(tab, fg_color="transparent")
            frame.grid(row=row, column=col, sticky="w", padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=f"{label}:",
                        font=("Segoe UI", 10),
                        text_color=COLORS['text_secondary']).pack(side="left")
            
            label_obj = ctk.CTkLabel(frame, text="-",
                                    font=("Segoe UI", 10, "bold"),
                                    text_color=COLORS['text'])
            label_obj.pack(side="left", padx=(5, 0))
            self.detail_labels[key] = label_obj
        
        tab.grid_rowconfigure(3, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_columnconfigure(3, weight=1)
    
    def _setup_metrics_tab(self):
        """Setup metrics tab."""
        tab = self.notebook.tab("Metrics")
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ('metric', 'value')
        self.metrics_tree = ttk.Treeview(tree_frame, columns=columns,
                                        show='headings', height=10)
        self.metrics_tree.heading('metric', text='Metric')
        self.metrics_tree.heading('value', text='Value')
        self.metrics_tree.column('metric', width=200)
        self.metrics_tree.column('value', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical',
                                 command=self.metrics_tree.yview)
        self.metrics_tree.configure(yscrollcommand=scrollbar.set)
        self.metrics_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def _setup_deps_tab(self):
        """Setup dependencies tab."""
        tab = self.notebook.tab("Dependencies")
        self.deps_text = ctk.CTkTextbox(tab, fg_color=COLORS['background'],
                                       text_color=COLORS['text'],
                                       font=("Consolas", 10))
        self.deps_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.deps_text.configure(state="disabled")
    
    def _setup_status_tab(self):
        """Setup status tab."""
        tab = self.notebook.tab("Status")
        status_frame = ctk.CTkFrame(tab, fg_color="transparent")
        status_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        health_frame = ctk.CTkFrame(status_frame, fg_color=COLORS['bg_dark'],
                                   corner_radius=8)
        health_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(health_frame, text="🟢 Health Status",
                    font=("Segoe UI", 12, "bold"),
                    text_color=COLORS['success']).pack(anchor="w", padx=15, pady=10)
        
        self.status_text = ctk.CTkTextbox(health_frame, height=80,
                                         fg_color="transparent",
                                         text_color=COLORS['text'],
                                         font=("Consolas", 10))
        self.status_text.pack(fill="x", padx=15, pady=(0, 10))
        self.status_text.configure(state="disabled")
    
    def _setup_log_panel(self, parent):
        """Setup log panel."""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(header_frame, text="📝 Activity Log",
                    font=("Segoe UI", 11, "bold"),
                    text_color=COLORS['text']).pack(side="left")
        
        clear_btn = ctk.CTkButton(header_frame, text="Clear",
                                 font=("Segoe UI", 9),
                                 fg_color=COLORS['border'],
                                 hover_color=COLORS['panel_light'],
                                 width=60, height=25,
                                 command=self._clear_log)
        clear_btn.pack(side="right")
        
        # Use fallback LogViewer if not available
        if WIDGETS_AVAILABLE:
            self.log_viewer = LogViewer(parent, bg=COLORS['bg_dark'])
        else:
            self.log_viewer = LogViewer(parent, bg=COLORS['bg_dark'])
        self.log_viewer.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    # ============================================================
    # REFRESH & UPDATE METHODS
    # ============================================================
    
    def _refresh(self):
        """Refresh all data."""
        try:
            self.monitor.refresh()
            self._update_tree()
            self._update_stats()
            self._update_selected()
            self._update_status_text()
            self.log_viewer.add_log("🔄 Refresh completed", "INFO")
        except Exception as e:
            self.log_viewer.add_log(f"❌ Refresh error: {e}", "ERROR")
    
    def _update_tree(self):
        """Update module tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        modules = getattr(self.monitor, 'modules', {})
        for name, module in modules.items():
            icon = self._get_status_icon(module.status)
            values = (module.status.value, module.version, module.type.value)
            item = self.tree.insert('', 'end', text=f"{icon} {name}", values=values)
            
            tag = module.status.value.lower()
            self.tree.tag_configure(tag, foreground=self._get_status_color(module.status))
            self.tree.item(item, tags=(tag,))
        
        if self.tree.get_children():
            self.tree.selection_set(self.tree.get_children()[0])
    
    def _update_stats(self):
        """Update stats labels."""
        try:
            health = self.monitor.get_module_health()
        except Exception:
            health = {"total": 0, "online": 0, "degraded": 0, "error": 0, "offline": 0}
        self.stats_labels['total'].configure(text=str(health.get('total', 0)))
        self.stats_labels['online'].configure(text=str(health.get('online', 0)))
        self.stats_labels['degraded'].configure(text=str(health.get('degraded', 0)))
        self.stats_labels['error'].configure(text=str(health.get('error', 0)))
        self.stats_labels['offline'].configure(text=str(health.get('offline', 0)))
    
    def _update_selected(self):
        """Update selected module details."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        name = self.tree.item(item, 'text')
        for icon in ['✅', '⚠️', '❌', '⛔', '❓']:
            if name.startswith(icon):
                name = name[2:].strip()
                break
        
        modules = getattr(self.monitor, 'modules', {})
        if name in modules:
            module = modules[name]
            self._update_details(module)
            self._update_metrics(module)
            self._update_dependencies(module)
    
    def _update_details(self, module):
        """Update details panel."""
        self.detail_labels['name'].configure(text=getattr(module, 'name', '-'))
        self.detail_labels['type'].configure(text=getattr(module, 'type', ModuleType.UNKNOWN).value)
        status = getattr(module, 'status', ModuleStatus.UNKNOWN)
        self.detail_labels['status'].configure(
            text=status.value,
            text_color=self._get_status_color(status)
        )
        self.detail_labels['version'].configure(text=getattr(module, 'version', '-'))
        self.detail_labels['description'].configure(text=getattr(module, 'description', '-'))
        self.detail_labels['last_check'].configure(
            text=getattr(module, 'last_check', 'Never')
        )
    
    def _update_metrics(self, module):
        """Update metrics tab."""
        for item in self.metrics_tree.get_children():
            self.metrics_tree.delete(item)
        
        try:
            metrics = self.monitor.get_module_metrics(module.name)
        except Exception:
            metrics = {}
        for key, value in metrics.items():
            self.metrics_tree.insert('', 'end', values=(key, str(value)))
    
    def _update_dependencies(self, module):
        """Update dependencies tab."""
        self.deps_text.configure(state="normal")
        self.deps_text.delete('1.0', 'end')
        
        text = f"Module: {getattr(module, 'name', 'Unknown')}\n"
        text += f"Type: {getattr(module, 'type', ModuleType.UNKNOWN).value}\n"
        text += f"Version: {getattr(module, 'version', '-')}\n\n"
        text += "Dependencies:\n"
        text += "-" * 40 + "\n"
        
        deps = getattr(module, 'dependencies', [])
        if deps:
            modules = getattr(self.monitor, 'modules', {})
            for dep in deps:
                dep_module = modules.get(dep)
                if dep_module:
                    icon = self._get_status_icon(dep_module.status)
                    text += f"{icon} {dep}\n"
                else:
                    text += f"❓ {dep} (Unknown)\n"
        else:
            text += "No dependencies\n"
        
        self.deps_text.insert('1.0', text)
        self.deps_text.configure(state="disabled")
    
    def _update_status_text(self):
        """Update status tab."""
        self.status_text.configure(state="normal")
        self.status_text.delete('1.0', 'end')
        try:
            diagnostics = self.monitor.run_diagnostics()
            text = json.dumps(diagnostics, indent=2, default=str)
        except Exception as e:
            text = f"Error running diagnostics: {e}"
        self.status_text.insert('1.0', text)
        self.status_text.configure(state="disabled")
    
    def _on_select(self, event):
        """Handle selection."""
        self._update_selected()
    
    def _on_update(self):
        """Callback from monitor."""
        self.after(0, self._refresh)
    
    # ============================================================
    # MONITORING CONTROL
    # ============================================================
    
    def _start_monitoring(self):
        """Start monitoring."""
        if not self.is_monitoring:
            self.is_monitoring = True
            try:
                self.monitor.start_monitoring()
            except Exception:
                pass
            self.log_viewer.add_log("🔄 Monitoring started", "SUCCESS")
            self._schedule_auto_refresh()
    
    def _schedule_auto_refresh(self):
        """Schedule auto refresh."""
        if self.is_monitoring:
            self._after_id = self.after(self.update_interval, self._auto_refresh)
    
    def _auto_refresh(self):
        """Auto refresh callback."""
        if self.is_monitoring:
            self._refresh()
            self._schedule_auto_refresh()
    
    def _stop_monitoring(self):
        """Stop monitoring."""
        if self.is_monitoring:
            self.is_monitoring = False
            if self._after_id:
                try:
                    self.after_cancel(self._after_id)
                except Exception:
                    pass
                self._after_id = None
            try:
                self.monitor.stop_monitoring()
            except Exception:
                pass
            self.log_viewer.add_log("⏹️ Monitoring stopped", "INFO")
    
    # ============================================================
    # EXPORT & LOG
    # ============================================================
    
    def _export_report(self):
        """Export report."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            try:
                self.monitor.export_diagnostics(filepath)
                self.log_viewer.add_log(f"📤 Report exported to {filepath}", "SUCCESS")
                messagebox.showinfo("Success", f"Report exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
                self.log_viewer.add_log(f"❌ Export failed: {e}", "ERROR")
    
    def _clear_log(self):
        """Clear log."""
        self.log_viewer.clear()
        self.log_viewer.add_log("🗑️ Log cleared", "INFO")
    
    # ============================================================
    # STATUS HELPERS
    # ============================================================
    
    def _get_status_icon(self, status) -> str:
        """Get status icon."""
        if hasattr(status, 'value'):
            status = status.value
        icons = {
            'online': "✅",
            'offline': "⛔",
            'degraded': "⚠️",
            'error': "❌",
            'unknown': "❓"
        }
        return icons.get(str(status).lower(), "❓")
    
    def _get_status_color(self, status) -> str:
        """Get status color."""
        if hasattr(status, 'value'):
            status = status.value
        colors = {
            'online': COLORS['success'],
            'offline': COLORS['offline'],
            'degraded': COLORS['warning'],
            'error': COLORS['error'],
            'unknown': COLORS['offline']
        }
        return colors.get(str(status).lower(), COLORS['text'])
    
    # ============================================================
    # LIFECYCLE
    # ============================================================
    
    def on_show(self):
        """Called when page is shown."""
        self._refresh()
        self._start_monitoring()
    
    def on_hide(self):
        """Called when page is hidden."""
        self._stop_monitoring()
    
    def destroy(self):
        """Clean up."""
        self._stop_monitoring()
        super().destroy()