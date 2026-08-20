#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# gui/intelligence/memory.py
# MEMORY VIEW - Memory Systems
# ============================================================

import customtkinter as ctk
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, MemoryStats


class Memory(IntelligencePage):
    """
    Memory systems status view.
    """
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.memory_stats_data = {}
        self.bot = None
        self._build_ui()
        self.update_data()
    
    def _build_ui(self):
        """Build the memory view UI."""
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
            text="💾 Memory Systems",
            font=("Segoe UI", 22, "bold"),
            text_color="#E8EDF2"
        ).pack(side="left")
        
        self.memory_status = StatusIndicator(header, label="Memory")
        self.memory_status.pack(side="right", padx=10)
        
        self.last_update_label = ctk.CTkLabel(
            header,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.pack(side="right", padx=10)
        
        # ====================================================
        # MEMORY CARDS
        # ====================================================
        
        self.short_term_card = MetricCard(
            self,
            title="⚡ Short-term Memory",
            value="0",
            subtitle="Items"
        )
        self.short_term_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.long_term_card = MetricCard(
            self,
            title="📚 Long-term Memory",
            value="0",
            subtitle="Items"
        )
        self.long_term_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # MEMORY STATS
        # ====================================================
        
        self.memory_stats = MemoryStats(self)
        self.memory_stats.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # ====================================================
        # DETAILS
        # ====================================================
        
        details = ctk.CTkFrame(self, fg_color="#131A22", corner_radius=10)
        details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            details,
            text="📋 Memory Details",
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
        """Update memory data."""
        if not self.is_running:
            return
        
        try:
            memory_data = self._get_memory_data()
            
            if memory_data:
                # Parse data
                total, categories = self._parse_memory_data(memory_data)
                
                # Update UI
                self._update_ui(total, categories, memory_data)
            else:
                self._show_no_data()
            
        except Exception as e:
            print(f"[Memory] Update error: {e}")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", f"Error: {e}\n\n{traceback.format_exc()}")
            self.memory_status.set_status(False)
        
        # Schedule next update
        if self.is_running:
            self.after(self.update_interval, self.update_data)
    
    def _parse_memory_data(self, memory_data: Dict) -> tuple:
        """
        Parse memory data into total and categories.
        
        Returns:
            (total, categories) tuple
        """
        total = 0
        categories = {}
        
        # Get raw categories
        raw_categories = memory_data.get('categories', {})
        
        if isinstance(raw_categories, dict):
            categories = raw_categories
            # Sum all numeric values
            for key, value in categories.items():
                if isinstance(value, (int, float)):
                    total += value
                elif isinstance(value, dict):
                    total += len(value)
                elif isinstance(value, (list, tuple)):
                    total += len(value)
                elif value is not None:
                    try:
                        total += int(value)
                    except (ValueError, TypeError):
                        pass
        elif isinstance(raw_categories, (list, tuple)):
            total = len(raw_categories)
            categories = {'items': total}
        else:
            # Try to get total from data
            total_from_data = memory_data.get('total', 0)
            if isinstance(total_from_data, (int, float)):
                total = int(total_from_data)
            categories = {'total': total}
        
        # Ensure total is int
        try:
            total = int(total)
        except (ValueError, TypeError):
            total = 0
        
        # Ensure categories is dict
        if not isinstance(categories, dict):
            categories = {'items': total}
        
        return total, categories
    
    def _update_ui(self, total: int, categories: dict, memory_data: dict):
        """Update UI with memory data."""
        # Update cards
        self.short_term_card.update_value(str(total))
        self.long_term_card.update_value(str(len(categories) if categories else 0))
        self.memory_status.set_status(total > 0)
        
        # Update memory stats widget
        if hasattr(self.memory_stats, 'update_stats'):
            self.memory_stats.update_stats(categories)
        
        # Update details
        self.details_text.delete("1.0", "end")
        self.details_text.insert(
            "1.0",
            json.dumps({
                "timestamp": datetime.now().isoformat(),
                "total": total,
                "categories": categories,
                "source": memory_data.get('source', 'unknown')
            }, indent=2, default=str)[:3000]
        )
        
        self.last_update_label.configure(
            text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
        )
    
    def _show_no_data(self):
        """Show no data message."""
        self.memory_status.set_status(False)
        self.details_text.delete("1.0", "end")
        self.details_text.insert(
            "1.0",
            "⚠️ Memory data not available.\n\n"
            "Please ensure:\n"
            "1. core.memory is properly imported\n"
            "2. Memory engine is initialized\n"
            "3. Memory data is accessible"
        )
    
    # ============================================================
    # GET MEMORY DATA
    # ============================================================
    
    def _get_memory_data(self) -> Dict[str, Any]:
        """Get memory data from various sources."""
        
        # Try sources in order
        sources = [
            self._get_from_core_memory,
            self._get_from_learning_memory,
            self._get_from_semantic_memory,
            self._get_from_bot,
            self._get_from_brain,
        ]
        
        for source_func in sources:
            try:
                result = source_func()
                if result:
                    return result
            except Exception as e:
                print(f"[Memory] Source error: {e}")
                continue
        
        return {}
    
    def _get_from_core_memory(self) -> Dict:
        """Get memory from core.memory."""
        try:
            from core.memory import memory
            if memory is not None:
                if hasattr(memory, 'stats'):
                    stats = memory.stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'core.memory')
                
                if hasattr(memory, 'get_stats'):
                    stats = memory.get_stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'core.memory')
                
                if hasattr(memory, 'status'):
                    status = memory.status()
                    if status and isinstance(status, dict):
                        mem_stats = status.get('stats', {})
                        if mem_stats:
                            return self._parse_memory_stats(mem_stats, 'core.memory(status)')
        except ImportError:
            pass
        return {}
    
    def _get_from_learning_memory(self) -> Dict:
        """Get memory from learning_memory."""
        try:
            from core.learning.learning_memory import learning_memory
            if learning_memory is not None and hasattr(learning_memory, 'stats'):
                stats = learning_memory.stats()
                if stats is not None:
                    return self._parse_memory_stats(stats, 'learning_memory')
        except ImportError:
            pass
        return {}
    
    def _get_from_semantic_memory(self) -> Dict:
        """Get memory from semantic_memory."""
        try:
            from core.learning.semantic_memory import semantic_memory
            if semantic_memory is not None:
                if hasattr(semantic_memory, 'count'):
                    count = semantic_memory.count()
                    if count is not None:
                        try:
                            count_int = int(count)
                            return {
                                'total': count_int,
                                'categories': {'semantic': count_int},
                                'source': 'semantic_memory(count)'
                            }
                        except (ValueError, TypeError):
                            pass
                
                if hasattr(semantic_memory, 'get_all'):
                    items = semantic_memory.get_all()
                    if items is not None:
                        if isinstance(items, (list, tuple)):
                            return {
                                'total': len(items),
                                'categories': {'semantic': len(items)},
                                'source': 'semantic_memory(get_all)'
                            }
                        elif isinstance(items, dict):
                            return {
                                'total': len(items),
                                'categories': {'semantic': len(items)},
                                'source': 'semantic_memory(get_all)'
                            }
        except ImportError:
            pass
        return {}
    
    def _get_from_bot(self) -> Dict:
        """Get memory from bot."""
        if self.bot is not None:
            try:
                if hasattr(self.bot, 'get_memory_stats'):
                    stats = self.bot.get_memory_stats()
                    if stats is not None:
                        return self._parse_memory_stats(stats, 'bot')
                
                if hasattr(self.bot, 'get_status'):
                    status = self.bot.get_status()
                    if status and isinstance(status, dict):
                        memory_keys = ['memory', 'mem', 'memory_stats', 'mem_stats']
                        for key in memory_keys:
                            if key in status:
                                mem_data = status[key]
                                if mem_data is not None:
                                    return self._parse_memory_stats(mem_data, 'bot(status)')
            except Exception:
                pass
        return {}
    
    def _get_from_brain(self) -> Dict:
        """Get memory from brain."""
        if self.bot is not None and hasattr(self.bot, 'brain'):
            brain = self.bot.brain
            if brain is not None:
                try:
                    if hasattr(brain, 'get_state'):
                        state = brain.get_state()
                        if state and isinstance(state, dict):
                            memory_keys = ['memory', 'short_term_memory', 'long_term_memory']
                            for key in memory_keys:
                                if key in state:
                                    mem_data = state[key]
                                    if mem_data is not None:
                                        if isinstance(mem_data, (list, tuple)):
                                            return {
                                                'total': len(mem_data),
                                                'categories': {key: len(mem_data)},
                                                'source': f'brain({key})'
                                            }
                except Exception:
                    pass
        return {}
    
    # ============================================================
    # PARSE MEMORY STATS
    # ============================================================
    
    def _parse_memory_stats(self, stats: Any, source: str) -> Dict[str, Any]:
        """Parse memory stats from various formats."""
        result = {'source': source}
        
        if stats is None:
            return {}
        
        # If stats is dict
        if isinstance(stats, dict):
            # Get total
            if 'total' in stats:
                total = stats['total']
                if isinstance(total, (int, float)):
                    result['total'] = int(total)
                else:
                    result['total'] = 0
            
            # Get categories
            categories = {}
            for key, value in stats.items():
                if key == 'total':
                    continue
                if isinstance(value, (int, float)):
                    categories[key] = int(value)
                elif isinstance(value, (list, tuple)):
                    categories[key] = len(value)
                elif isinstance(value, dict):
                    if value:
                        if all(isinstance(v, (int, float)) for v in value.values()):
                            categories[key] = int(sum(value.values()))
                        else:
                            categories[key] = len(value)
                    else:
                        categories[key] = 0
            
            # If no categories found, use all numeric values
            if not categories:
                for key, value in stats.items():
                    if isinstance(value, (int, float)):
                        categories[key] = int(value)
            
            # If still no categories, create one with total
            if not categories and 'total' in result:
                categories['items'] = result['total']
            
            result['categories'] = categories
            
            # Calculate total if not set
            if 'total' not in result:
                total = 0
                for value in categories.values():
                    if isinstance(value, (int, float)):
                        total += value
                result['total'] = total
            
            return result
        
        # If stats is list or tuple
        if isinstance(stats, (list, tuple)):
            total = len(stats)
            return {
                'total': total,
                'categories': {'items': total},
                'source': source
            }
        
        # If stats is number
        if isinstance(stats, (int, float)):
            return {
                'total': int(stats),
                'categories': {'items': int(stats)},
                'source': source
            }
        
        return {}
    
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