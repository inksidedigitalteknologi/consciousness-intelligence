#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# gui/intelligence/pattern.py
# PATTERN VIEW - Pattern Recognition
# ============================================================

import customtkinter as ctk
import json
from datetime import datetime

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, PatternList


class Pattern(IntelligencePage):
    """
    Pattern recognition status view.
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pattern_data = {}
        self._build_ui()
        self.update_data()
    
    def _build_ui(self):
        """Build the pattern view UI."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # ====================================================
        # HEADER
        # ====================================================
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=20, pady=15, sticky="ew")
        
        ctk.CTkLabel(
            header,
            text="🔍 Pattern Recognition",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).pack(side="left")
        
        self.pattern_status = StatusIndicator(header, label="Pattern")
        self.pattern_status.pack(side="right", padx=10)
        
        self.last_update_label = ctk.CTkLabel(
            header,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.pack(side="right", padx=10)
        
        # ====================================================
        # PATTERN CARDS
        # ====================================================
        
        self.total_patterns = MetricCard(
            self,
            title="📊 Total Patterns",
            value="0",
            subtitle="Detected patterns"
        )
        self.total_patterns.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.unique_patterns = MetricCard(
            self,
            title="🔐 Unique Patterns",
            value="0",
            subtitle="Unique fingerprints"
        )
        self.unique_patterns.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # PATTERN LIST
        # ====================================================
        
        self.pattern_list = PatternList(self)
        self.pattern_list.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # DETAILS
        # ====================================================
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            details,
            text="📋 Pattern Details",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        self.details_text = ctk.CTkTextbox(
            details,
            font=("Consolas", 10),
            fg_color="#0B0F14",
            text_color="#8D9AAA",
            height=120
        )
        self.details_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    # ============================================================
    # UPDATE DATA
    # ============================================================
    
    def update_data(self):
        """Update pattern data."""
        if not self.is_running:
            return
        
        try:
            pattern_data = self._get_pattern_data()
            
            if pattern_data:
                # Update cards
                total = pattern_data.get('patterns', 0)
                unique = pattern_data.get('unique_fingerprints', 0)
                
                self.total_patterns.update_value(str(total))
                self.unique_patterns.update_value(str(unique))
                self.pattern_status.set_status(True)
                
                # Update pattern list
                top_patterns = pattern_data.get('top_tokens', {})
                if top_patterns:
                    # Sort by value (frequency) and get top 10
                    sorted_patterns = sorted(
                        top_patterns.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    pattern_names = [p[0] for p in sorted_patterns[:10]]
                    self.pattern_list.update_patterns(pattern_names)
                else:
                    self.pattern_list.update_patterns([])
                
                # Update details
                self.details_text.delete("1.0", "end")
                self.details_text.insert(
                    "1.0",
                    json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "total_patterns": total,
                        "unique_patterns": unique,
                        "top_patterns": top_patterns,
                        "raw_data": pattern_data
                    }, indent=2, default=str)[:3000]
                )
                
                self.last_update_label.configure(
                    text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
                )
                
            else:
                # No pattern data
                self.pattern_status.set_status(False)
                self.details_text.delete("1.0", "end")
                self.details_text.insert(
                    "1.0",
                    "⚠️ Pattern data not available.\n\n"
                    "Please ensure:\n"
                    "1. core.learning.pattern is properly imported\n"
                    "2. Pattern Engine is initialized"
                )
                self.pattern_list.update_patterns([])
            
        except Exception as e:
            print(f"[PatternView] Update error: {e}")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", f"Error: {e}")
            self.pattern_status.set_status(False)
        
        # Schedule next update
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _get_pattern_data(self) -> dict:
        """Get pattern data from various sources."""
        result = {}
        
        # Try core.learning.pattern
        try:
            from core.learning.pattern import pattern
            if pattern and hasattr(pattern, 'get_state'):
                state = pattern.get_state()
                if state:
                    result = state
                    result['source'] = 'core.learning.pattern'
                    return result
        except ImportError:
            pass
        
        # Try from bot
        if self.bot:
            try:
                if hasattr(self.bot, 'get_patterns'):
                    patterns = self.bot.get_patterns()
                    if patterns:
                        if isinstance(patterns, dict):
                            result = patterns
                        else:
                            result = {'patterns': len(patterns), 'data': patterns}
                        result['source'] = 'bot'
                        return result
            except Exception:
                pass
        
        # Try from scanner
        if self.bot and hasattr(self.bot, 'scanner'):
            try:
                scanner = self.bot.scanner
                if scanner and hasattr(scanner, 'get_summary'):
                    summary = scanner.get_summary()
                    if summary:
                        result = {
                            'patterns': summary.get('total', 0),
                            'top_tokens': {},
                            'source': 'scanner'
                        }
                        return result
            except Exception:
                pass
        
        return result
    
    # ============================================================
    # CONTROL METHODS
    # ============================================================
    
    def set_bot(self, bot):
        """Set bot reference."""
        self.bot = bot
    
    def refresh(self):
        """Force refresh."""
        self.update_data()
    
    def stop(self):
        """Stop updates."""
        self.is_running = False
    
    def destroy(self):
        """Clean up."""
        self.stop()
        super().destroy()