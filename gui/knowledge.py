#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================================
# gui/knowledge.py
# KNOWLEDGE BASE - COGNITIVE MEMORY & LEARNING DASHBOARD
# VERSION: 9.0 - TRENDING TOPICS + SMART SUGGESTIONS
# ============================================================

import customtkinter as ctk
import json
import logging
import threading
import re
import csv
import io
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from urllib import request, error
from html.parser import HTMLParser
from collections import Counter

from .page import IntelligencePage
from .widgets import StatusIndicator, MetricCard, InsightCard

# ============================================================
# IMPORT CONFIG DARI config.py
# ============================================================

from config import (
    KNOWLEDGE_ITEMS_PER_PAGE,
    KNOWLEDGE_MAX_ITEMS_DISPLAY,
    KNOWLEDGE_DETAILS_MAX_LENGTH,
    KNOWLEDGE_INSIGHTS_MAX_DISPLAY,
    KNOWLEDGE_UPDATE_INTERVAL,
    KNOWLEDGE_CATEGORIES,
    KNOWLEDGE_DEFAULT_CATEGORY,
    KNOWLEDGE_CATEGORY_ICONS,
    KNOWLEDGE_QA_PLACEHOLDER,
    KNOWLEDGE_TEXT_PLACEHOLDER,
    KNOWLEDGE_URL_PLACEHOLDER,
    KNOWLEDGE_RAW_PLACEHOLDER,
    KNOWLEDGE_URL_STATUS_DEFAULT,
    KNOWLEDGE_RAW_STATUS_DEFAULT,
    KNOWLEDGE_EMPTY_TEXT,
    KNOWLEDGE_NO_RESULTS_TEXT,
    KNOWLEDGE_FETCH_TIMEOUT,
    KNOWLEDGE_MIN_CONTENT_LENGTH,
    KNOWLEDGE_MAX_CONTENT_LENGTH,
    KNOWLEDGE_MAX_SENTENCES,
    KNOWLEDGE_MIN_SENTENCE_LENGTH,
    KNOWLEDGE_SKIP_PATTERNS,
)

logger = logging.getLogger(__name__)

# ============================================================
# SKIP PATTERNS - BOILERPLATE
# ============================================================

SKIP_PATTERNS_COMPILED = [re.compile(p, re.I) for p in KNOWLEDGE_SKIP_PATTERNS]

# ============================================================
# HTML TEXT EXTRACTOR
# ============================================================

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    
    def handle_data(self, d):
        self.text.append(d)
    
    def get_data(self):
        return ' '.join(self.text)


def strip_html(html: str) -> str:
    s = MLStripper()
    try:
        s.feed(html)
        text = s.get_data()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception:
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return text


def fetch_url_content(url: str, timeout: int = KNOWLEDGE_FETCH_TIMEOUT) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            charset = 'utf-8'
            ct = resp.headers.get('Content-Type', '')
            if 'charset=' in ct:
                charset = ct.split('charset=')[-1].split(';')[0].strip()
            html = resp.read().decode(charset, errors='ignore')
            text = strip_html(html)
            if len(text) < KNOWLEDGE_MIN_CONTENT_LENGTH:
                title = re.search(r'<title>(.*?)</title>', html, re.I)
                title = title.group(1) if title else "No title"
                text = f"{title}\n\n{text}"
            return text
    except error.URLError as e:
        raise Exception(f"Network error: {e.reason}")
    except error.HTTPError as e:
        raise Exception(f"HTTP {e.code}: {e.reason}")
    except Exception as e:
        raise Exception(f"Failed to fetch: {str(e)}")


def parse_raw_data(raw_text: str) -> str:
    raw_text = raw_text.strip()
    if not raw_text:
        return ""
    try:
        data = json.loads(raw_text)
        if isinstance(data, dict):
            lines = []
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    lines.append(f"{k}: {json.dumps(v, indent=2, ensure_ascii=False)}")
                else:
                    lines.append(f"{k}: {v}")
            return "\n".join(lines)
        elif isinstance(data, list):
            return "\n".join(json.dumps(item, indent=2, ensure_ascii=False) for item in data[:10])
        else:
            return str(data)
    except json.JSONDecodeError:
        pass
    try:
        for delim in [',', ';', '\t', '|']:
            try:
                csv_file = io.StringIO(raw_text)
                reader = csv.reader(csv_file, delimiter=delim)
                rows = list(reader)
                if rows and len(rows) > 1:
                    lines = []
                    headers = rows[0]
                    lines.append(f"Columns: {', '.join(headers)}")
                    for i, row in enumerate(rows[1:11], 1):
                        if len(row) == len(headers):
                            pairs = [f"{h}: {v}" for h, v in zip(headers, row)]
                            lines.append(f"Row {i}: {' | '.join(pairs)}")
                    if len(rows) > 11:
                        lines.append(f"... and {len(rows)-11} more rows")
                    return "\n".join(lines)
            except Exception:
                continue
    except Exception:
        pass
    return raw_text


# ============================================================
# CLASS KNOWLEDGE
# ============================================================

class Knowledge(IntelligencePage):
    """Knowledge Base v9.0 — Trending Topics + Smart Suggestions."""

    ITEMS_PER_PAGE = KNOWLEDGE_ITEMS_PER_PAGE

    def __init__(self, parent, *args, **kwargs):
        # Data Storage
        self.knowledge_items: List[Dict] = []
        self.knowledge_stats: Dict = {}
        self.trending_topics: List[Dict] = []
        self.smart_suggestions: List[str] = []
        self.filtered_items: List[Dict] = []

        # Categories
        self.categories = KNOWLEDGE_CATEGORIES

        # Status
        self.is_connected = False
        self.last_error: Optional[str] = None
        self.update_count = 0
        self.success_count = 0
        self.error_count = 0
        self.is_running = True
        self.update_interval = KNOWLEDGE_UPDATE_INTERVAL
        self.bot = None
        self._is_destroyed = False
        self.current_page = 0
        self.total_pages = 0

        self._qa_response = None
        self._qa_entry = None
        self._qa_button = None
        self._add_status_label = None
        self._url_status_label = None
        self._raw_status_label = None
        self.main_container = None
        self.knowledge_status = None
        self.last_update_label = None
        self.refresh_btn = None
        self.total_items_card = None
        self.pattern_count_card = None
        self.insight_count_card = None
        self.confidence_avg_card = None
        self.add_tabview = None
        self.add_textbox = None
        self.url_entry = None
        self.url_fetch_button = None
        self.raw_textbox = None
        self.raw_process_button = None
        self.add_category_menu = None
        self.add_button = None
        self.topic_buttons: List[ctk.CTkButton] = []
        self.suggestion_buttons: List[ctk.CTkButton] = []
        self.category_filter_menu = None
        self.search_entry = None
        self.count_label = None
        self.list_container = None
        self.prev_btn = None
        self.next_btn = None
        self.page_label = None
        self.topics_frame = None
        self.suggestions_frame = None

        super().__init__(parent, *args, **kwargs)
        self.after(500, self.update_data)

    # ============================================================
    # SAFETY HELPERS
    # ============================================================
    
    def _safe_widget_exists(self, widget) -> bool:
        try:
            if widget and not self._is_destroyed:
                return widget.winfo_exists()
        except Exception:
            pass
        return False

    def _safe_configure(self, widget, **kwargs) -> bool:
        try:
            if self._safe_widget_exists(widget):
                widget.configure(**kwargs)
                return True
        except Exception as e:
            logger.debug(f"Widget configure error: {e}")
        return False

    def _normalize_item(self, item) -> Dict:
        if item is None:
            return {}
        if isinstance(item, dict):
            return item
        try:
            return {
                "content": getattr(item, 'content', ''),
                "category": getattr(item, 'category', 'general'),
                "confidence": getattr(item, 'confidence', 0),
                "type": getattr(item, 'type', 'fact'),
                "status": getattr(item, 'status', 'active'),
                "timestamp": getattr(item, 'created_at', ''),
                "id": getattr(item, 'id', ''),
                "tags": getattr(item, 'tags', []),
            }
        except Exception:
            return {"content": str(item), "category": "general", "confidence": 0}

    # ============================================================
    # CLEAN CONTENT
    # ============================================================
    
    def _clean_content(self, raw_text: str) -> str:
        if not raw_text:
            return ""
        lines = raw_text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            if len(line) < 40:
                continue
            skip = False
            for pattern in SKIP_PATTERNS_COMPILED:
                if pattern.search(line):
                    skip = True
                    break
            if skip:
                continue
            clean_lines.append(line)
        text = ' '.join(clean_lines)
        sentences = re.split(r'[.!?]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > KNOWLEDGE_MIN_SENTENCE_LENGTH]
        informative = []
        for sent in sentences:
            skip = False
            for pattern in SKIP_PATTERNS_COMPILED:
                if pattern.search(sent):
                    skip = True
                    break
            if skip:
                continue
            if len(sent) > KNOWLEDGE_MIN_SENTENCE_LENGTH and re.search(r'[a-zA-Z]{4,}', sent):
                informative.append(sent)
                if len(informative) >= KNOWLEDGE_MAX_SENTENCES:
                    break
        if not informative:
            informative = sorted(sentences, key=len, reverse=True)[:3]
        content = '. '.join(informative)
        if len(content) > KNOWLEDGE_MAX_CONTENT_LENGTH:
            content = content[:KNOWLEDGE_MAX_CONTENT_LENGTH] + "..."
        return content

    # ============================================================
    # BUILD UI — KONSEP BARU
    # ============================================================
    
    def _build_ui(self):
        self.main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        row = 0

        # ------------------------------------------------------------
        # HEADER
        # ------------------------------------------------------------
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="📚 Knowledge Base",
            font=("Segoe UI", 24, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")

        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.grid(row=0, column=1, sticky="e")

        self.knowledge_status = StatusIndicator(status_frame, label="KB")
        self.knowledge_status.pack(side="left", padx=5)

        self.last_update_label = ctk.CTkLabel(
            status_frame,
            text="Last update: --",
            font=("Segoe UI", 10),
            text_color="#5F6B78"
        )
        self.last_update_label.pack(side="left", padx=10)

        self.refresh_btn = ctk.CTkButton(
            status_frame,
            text="🔄 Refresh",
            width=80,
            height=28,
            font=("Segoe UI", 11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.refresh
        )
        self.refresh_btn.pack(side="left", padx=5)

        row += 1

        # ------------------------------------------------------------
        # STATISTICS
        # ------------------------------------------------------------
        stats_frame = ctk.CTkFrame(self.main_container, fg_color="#131A22", corner_radius=10)
        stats_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            stats_frame,
            text="📊 Statistics",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=4, padx=15, pady=10, sticky="w")

        self.total_items_card = MetricCard(stats_frame, title="📄 Total Items", value="0")
        self.total_items_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

        self.pattern_count_card = MetricCard(stats_frame, title="🔍 Topics", value="0")
        self.pattern_count_card.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")

        self.insight_count_card = MetricCard(stats_frame, title="💡 Categories", value="0")
        self.insight_count_card.grid(row=1, column=2, padx=8, pady=8, sticky="nsew")

        self.confidence_avg_card = MetricCard(stats_frame, title="🎯 Avg Confidence", value="0%")
        self.confidence_avg_card.grid(row=1, column=3, padx=8, pady=8, sticky="nsew")

        row += 1

        # ------------------------------------------------------------
        # Q&A SECTION
        # ------------------------------------------------------------
        qa_frame = ctk.CTkFrame(self.main_container, fg_color="#1A2530", corner_radius=10)
        qa_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        qa_frame.grid_columnconfigure(0, weight=4)
        qa_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            qa_frame,
            text="💬 Ask Knowledge Base",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="w")

        self._qa_entry = ctk.CTkEntry(
            qa_frame,
            placeholder_text=KNOWLEDGE_QA_PLACEHOLDER,
            height=36,
            font=("Segoe UI", 12)
        )
        self._qa_entry.grid(row=1, column=0, padx=(15, 5), pady=5, sticky="ew")
        self._qa_entry.bind("<Return>", lambda e: self._ask_knowledge())

        self._qa_button = ctk.CTkButton(
            qa_frame,
            text="🔍 Ask",
            height=36,
            width=80,
            fg_color="#3B82F6",
            hover_color="#2563EB",
            font=("Segoe UI", 12, "bold"),
            command=self._ask_knowledge
        )
        self._qa_button.grid(row=1, column=1, padx=(5, 15), pady=5)

        self._qa_response = ctk.CTkTextbox(
            qa_frame,
            height=80,
            font=("Segoe UI", 11),
            fg_color="#0B0F14",
            border_width=1,
            border_color="#2D3748",
            wrap="word"
        )
        self._qa_response.grid(row=2, column=0, columnspan=2, padx=15, pady=(5, 10), sticky="ew")
        self._qa_response.insert("1.0", "💡 Ask anything about stored knowledge...")
        self._qa_response.configure(state="disabled")

        row += 1

        # ------------------------------------------------------------
        # ADD KNOWLEDGE
        # ------------------------------------------------------------
        add_main_frame = ctk.CTkFrame(self.main_container, fg_color="#1A2530", corner_radius=10)
        add_main_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        add_main_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            add_main_frame,
            text="✏️ Add Knowledge",
            font=("Segoe UI", 13, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self.add_tabview = ctk.CTkTabview(
            add_main_frame,
            fg_color="#0B0F14",
            segmented_button_fg_color="#1A2530",
            segmented_button_selected_color="#3B82F6",
            text_color="#E8EDF2"
        )
        self.add_tabview.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        # Tab 1: Text
        self.add_tabview.add("📝 Text")
        text_tab = self.add_tabview.tab("📝 Text")
        text_tab.grid_columnconfigure(0, weight=1)
        self.add_textbox = ctk.CTkTextbox(text_tab, height=50, font=("Segoe UI", 12), fg_color="#0B0F14", border_width=1, border_color="#2D3748")
        self.add_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.add_textbox.insert("1.0", KNOWLEDGE_TEXT_PLACEHOLDER)
        self.add_textbox.bind("<FocusIn>", self._on_textbox_focus)

        # Tab 2: URL
        self.add_tabview.add("🌐 URL")
        url_tab = self.add_tabview.tab("🌐 URL")
        url_tab.grid_columnconfigure(0, weight=3)
        url_tab.grid_columnconfigure(1, weight=1)
        self.url_entry = ctk.CTkEntry(url_tab, placeholder_text=KNOWLEDGE_URL_PLACEHOLDER, height=36, font=("Segoe UI", 12))
        self.url_entry.grid(row=0, column=0, padx=(5, 5), pady=5, sticky="ew")
        self.url_entry.bind("<Return>", lambda e: self._fetch_and_extract_from_url())
        self.url_fetch_button = ctk.CTkButton(url_tab, text="🚀 Fetch", height=36, width=100, fg_color="#8B5CF6", hover_color="#7C3AED", font=("Segoe UI", 12, "bold"), command=self._fetch_and_extract_from_url)
        self.url_fetch_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self._url_status_label = ctk.CTkLabel(url_tab, text=KNOWLEDGE_URL_STATUS_DEFAULT, font=("Segoe UI", 10), text_color="#8D9AAA")
        self._url_status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        # Tab 3: Raw
        self.add_tabview.add("📊 Raw")
        raw_tab = self.add_tabview.tab("📊 Raw")
        raw_tab.grid_columnconfigure(0, weight=3)
        raw_tab.grid_columnconfigure(1, weight=1)
        self.raw_textbox = ctk.CTkTextbox(raw_tab, height=50, font=("Segoe UI", 11), fg_color="#0B0F14", border_width=1, border_color="#2D3748")
        self.raw_textbox.grid(row=0, column=0, padx=(5, 5), pady=5, sticky="ew")
        self.raw_textbox.insert("1.0", KNOWLEDGE_RAW_PLACEHOLDER)
        self.raw_process_button = ctk.CTkButton(raw_tab, text="⚙️ Parse", height=36, width=100, fg_color="#F59E0B", hover_color="#D97706", font=("Segoe UI", 12, "bold"), command=self._process_raw_data)
        self.raw_process_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self._raw_status_label = ctk.CTkLabel(raw_tab, text=KNOWLEDGE_RAW_STATUS_DEFAULT, font=("Segoe UI", 10), text_color="#8D9AAA")
        self._raw_status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        # Category & Save
        add_bottom_frame = ctk.CTkFrame(add_main_frame, fg_color="transparent")
        add_bottom_frame.grid(row=2, column=0, padx=15, pady=(5, 10), sticky="ew")
        add_bottom_frame.grid_columnconfigure(0, weight=1)
        add_bottom_frame.grid_columnconfigure(1, weight=0)
        add_bottom_frame.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(add_bottom_frame, text="Category:", font=("Segoe UI", 12), text_color="#8D9AAA").grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.add_category_menu = ctk.CTkOptionMenu(add_bottom_frame, values=self.categories[1:], height=32, width=140, fg_color="#1A2530", button_color="#2A3A4A", button_hover_color="#3B4A5A")
        self.add_category_menu.grid(row=0, column=1, padx=5, sticky="e")
        self.add_category_menu.set(KNOWLEDGE_DEFAULT_CATEGORY)
        self.add_button = ctk.CTkButton(add_bottom_frame, text="➕ Save", height=32, width=100, fg_color="#22C55E", hover_color="#16A34A", font=("Segoe UI", 12, "bold"), command=self._add_knowledge_from_active_tab)
        self.add_button.grid(row=0, column=2, padx=(10, 0), sticky="e")
        self._add_status_label = ctk.CTkLabel(add_main_frame, text="", font=("Segoe UI", 10), text_color="#8D9AAA")
        self._add_status_label.grid(row=3, column=0, padx=15, pady=(0, 10), sticky="w")

        row += 1

        # ============================================================
        # 🔥 TRENDING TOPICS — KONSEP BARU
        # ============================================================
        topics_frame = ctk.CTkFrame(self.main_container, fg_color="#131A22", corner_radius=10)
        topics_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        topics_frame.grid_columnconfigure(0, weight=1)

        topics_header = ctk.CTkFrame(topics_frame, fg_color="transparent")
        topics_header.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        topics_header.grid_columnconfigure(0, weight=1)
        topics_header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(
            topics_header,
            text="🔥 Trending Topics",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, sticky="w")

        self.topic_count_label = ctk.CTkLabel(
            topics_header,
            text="",
            font=("Segoe UI", 11),
            text_color="#8D9AAA"
        )
        self.topic_count_label.grid(row=0, column=1, sticky="e", padx=10)

        # Topic buttons container
        self.topics_container = ctk.CTkFrame(topics_frame, fg_color="transparent")
        self.topics_container.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.topics_container.grid_columnconfigure(0, weight=1)
        self.topics_container.grid_columnconfigure(1, weight=1)

        self.topic_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.topics_container,
                text="Loading...",
                height=30,
                corner_radius=6,
                fg_color="#1A2530",
                hover_color="#2A3A4A",
                font=("Segoe UI", 11),
                anchor="w",
                command=lambda idx=i: self._on_topic_click(idx)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            self.topic_buttons.append(btn)

        # Placeholder jika tidak ada topik
        self.topics_empty_label = ctk.CTkLabel(
            self.topics_container,
            text="📭 No topics yet. Add knowledge to generate trending topics.",
            font=("Segoe UI", 12),
            text_color="#5F6B78"
        )
        # Tidak ditampilkan dulu

        row += 2

        # ============================================================
        # 💡 SMART SUGGESTIONS — KONSEP BARU
        # ============================================================
        suggestions_frame = ctk.CTkFrame(self.main_container, fg_color="#131A22", corner_radius=10)
        suggestions_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        suggestions_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            suggestions_frame,
            text="💡 Smart Suggestions",
            font=("Segoe UI", 14, "bold"),
            text_color="#E8EDF2"
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.suggestions_container = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
        self.suggestions_container.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.suggestions_container.grid_columnconfigure(0, weight=1)
        self.suggestions_container.grid_columnconfigure(1, weight=1)

        self.suggestion_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.suggestions_container,
                text="Loading...",
                height=28,
                corner_radius=6,
                fg_color="#1A2530",
                hover_color="#2A3A4A",
                font=("Segoe UI", 10),
                anchor="w",
                command=lambda idx=i: self._on_suggestion_click(idx)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            self.suggestion_buttons.append(btn)

        row += 2

        # ------------------------------------------------------------
        # FILTER, SEARCH & LIST
        # ------------------------------------------------------------
        filter_frame = ctk.CTkFrame(self.main_container, fg_color="#131A22", corner_radius=10)
        filter_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        filter_frame.grid_columnconfigure(0, weight=0)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(2, weight=0)
        filter_frame.grid_columnconfigure(3, weight=0)

        ctk.CTkLabel(filter_frame, text="🔍 Filter:", font=("Segoe UI", 12), text_color="#8D9AAA").grid(row=0, column=0, padx=15, pady=8, sticky="w")
        self.category_filter_menu = ctk.CTkOptionMenu(filter_frame, values=self.categories, command=self._filter_category, width=140, height=30, fg_color="#1A2530", button_color="#2A3A4A")
        self.category_filter_menu.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.category_filter_menu.set("All")
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search...", height=30, width=150, font=("Segoe UI", 11))
        self.search_entry.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self._apply_filter_and_paginate())
        self.count_label = ctk.CTkLabel(filter_frame, text="0 items", font=("Segoe UI", 11, "bold"), text_color="#5F6B78")
        self.count_label.grid(row=0, column=3, padx=15, pady=8, sticky="e")

        row += 1

        # --- Knowledge List ---
        list_frame = ctk.CTkFrame(self.main_container, fg_color="#131A22", corner_radius=10)
        list_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        list_frame.grid_columnconfigure(0, weight=1)

        self.list_container = ctk.CTkScrollableFrame(list_frame, fg_color="transparent", height=200)
        self.list_container.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.list_container.grid_columnconfigure(0, weight=1)

        # --- Pagination ---
        pagination_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        pagination_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        pagination_frame.grid_columnconfigure(0, weight=1)
        pagination_frame.grid_columnconfigure(1, weight=0)
        pagination_frame.grid_columnconfigure(2, weight=0)
        pagination_frame.grid_columnconfigure(3, weight=0)
        pagination_frame.grid_columnconfigure(4, weight=1)

        self.prev_btn = ctk.CTkButton(pagination_frame, text="◀", width=36, height=28, fg_color="#2A3A4A", hover_color="#3B4A5A", command=self._prev_page)
        self.prev_btn.grid(row=0, column=1, padx=5)
        self.page_label = ctk.CTkLabel(pagination_frame, text="1/1", font=("Segoe UI", 11), text_color="#8D9AAA")
        self.page_label.grid(row=0, column=2, padx=10)
        self.next_btn = ctk.CTkButton(pagination_frame, text="▶", width=36, height=28, fg_color="#2A3A4A", hover_color="#3B4A5A", command=self._next_page)
        self.next_btn.grid(row=0, column=3, padx=5)

        self._show_placeholder()

    # ============================================================
    # TRENDING TOPICS & SMART SUGGESTIONS HANDLERS
    # ============================================================
    
    def _on_topic_click(self, idx):
        """Handle topic button click — search by topic."""
        if idx < len(self.trending_topics):
            topic = self.trending_topics[idx]
            topic_name = topic.get('name', '')
            if topic_name:
                self.search_entry.delete(0, "end")
                self.search_entry.insert(0, topic_name)
                self._apply_filter_and_paginate()

    def _on_suggestion_click(self, idx):
        """Handle suggestion button click — ask question."""
        if idx < len(self.smart_suggestions):
            question = self.smart_suggestions[idx]
            self._qa_entry.delete(0, "end")
            self._qa_entry.insert(0, question)
            self._ask_knowledge()

    # ============================================================
    # ADD KNOWLEDGE
    # ============================================================
    
    def _on_textbox_focus(self, event):
        if self.add_textbox.get("1.0", "end-1c").strip() == KNOWLEDGE_TEXT_PLACEHOLDER:
            self.add_textbox.delete("1.0", "end")

    def _add_knowledge_from_active_tab(self):
        tab = self.add_tabview.get()
        category = self.add_category_menu.get()

        if tab == "📝 Text":
            text = self.add_textbox.get("1.0", "end-1c").strip()
            if not text or text == KNOWLEDGE_TEXT_PLACEHOLDER:
                self._safe_configure(self._add_status_label, text="⚠️ Enter text!", text_color="#EF4444")
                return
            self._add_knowledge_common(text, category)

        elif tab == "🌐 URL":
            url = self.url_entry.get().strip()
            if not url:
                self._safe_configure(self._add_status_label, text="⚠️ Enter URL!", text_color="#EF4444")
                return
            self._fetch_and_extract_from_url()

        elif tab == "📊 Raw":
            raw = self.raw_textbox.get("1.0", "end-1c").strip()
            if not raw or raw == KNOWLEDGE_RAW_PLACEHOLDER:
                self._safe_configure(self._add_status_label, text="⚠️ Enter data!", text_color="#EF4444")
                return
            self._process_raw_data()

    def _add_knowledge_common(self, content: str, category: str):
        if not content:
            return
        try:
            from core.knowledge import knowledge
            if knowledge and hasattr(knowledge, 'add'):
                item_id = knowledge.add(
                    content=content[:KNOWLEDGE_MAX_CONTENT_LENGTH],
                    category=category.lower(),
                    type="fact",
                    tags=[category.lower(), "manual"],
                    confidence=50.0,
                    importance=0.5
                )
                if item_id:
                    self._safe_configure(self._add_status_label, text=f"✅ Added! ID: {item_id}", text_color="#22C55E")
                    self.update_data()
                else:
                    self._safe_configure(self._add_status_label, text="❌ Failed.", text_color="#EF4444")
            else:
                self._safe_configure(self._add_status_label, text="❌ Knowledge module unavailable!", text_color="#EF4444")
        except Exception as e:
            logger.error(f"[Knowledge] Add error: {e}")
            self._safe_configure(self._add_status_label, text=f"❌ Error: {str(e)[:60]}", text_color="#EF4444")

    # ============================================================
    # URL & RAW PROCESSING
    # ============================================================
    
    def _fetch_and_extract_from_url(self):
        url = self.url_entry.get().strip()
        if not url:
            self._safe_configure(self._url_status_label, text="⚠️ Enter URL!", text_color="#EF4444")
            return

        self.url_fetch_button.configure(state="disabled", text="⏳...")
        self._safe_configure(self._url_status_label, text="🔄 Fetching...", text_color="#F59E0B")

        def fetch_task():
            try:
                raw = fetch_url_content(url)
                if len(raw) < KNOWLEDGE_MIN_CONTENT_LENGTH:
                    self.after(0, lambda: self._safe_configure(self._url_status_label, text="⚠️ Content too short.", text_color="#EF4444"))
                    return

                content = self._clean_content(raw)
                if len(content) < 50:
                    self.after(0, lambda: self._safe_configure(self._url_status_label, text="⚠️ No informative content.", text_color="#EF4444"))
                    return

                category = self.add_category_menu.get()
                self.after(0, lambda: self._add_knowledge_common(content, category))
                self.after(0, lambda: self._safe_configure(self._url_status_label, text=f"✅ Success! {len(content)} chars.", text_color="#22C55E"))
                self.after(0, lambda: self.url_entry.delete(0, "end"))

            except Exception as e:
                self.after(0, lambda: self._safe_configure(self._url_status_label, text=f"❌ {str(e)[:60]}", text_color="#EF4444"))
            finally:
                self.after(0, lambda: self.url_fetch_button.configure(state="normal", text="🚀 Fetch"))

        threading.Thread(target=fetch_task, daemon=True).start()

    def _process_raw_data(self):
        raw = self.raw_textbox.get("1.0", "end-1c").strip()
        if not raw or raw == KNOWLEDGE_RAW_PLACEHOLDER:
            self._safe_configure(self._raw_status_label, text="⚠️ Enter data!", text_color="#EF4444")
            return

        self.raw_process_button.configure(state="disabled", text="⏳...")
        self._safe_configure(self._raw_status_label, text="🔄 Processing...", text_color="#F59E0B")

        def parse_task():
            try:
                parsed = parse_raw_data(raw)
                if parsed:
                    category = self.add_category_menu.get()
                    content = f"[Raw Data] {parsed}"
                    self.after(0, lambda: self._add_knowledge_common(content, category))
                    self.after(0, lambda: self._safe_configure(self._raw_status_label, text=f"✅ Success! {len(parsed)} chars.", text_color="#22C55E"))
                    self.after(0, lambda: self.raw_textbox.delete("1.0", "end"))
                else:
                    self.after(0, lambda: self._safe_configure(self._raw_status_label, text="⚠️ No valid data.", text_color="#EF4444"))
            except Exception as e:
                self.after(0, lambda: self._safe_configure(self._raw_status_label, text=f"❌ {str(e)[:60]}", text_color="#EF4444"))
            finally:
                self.after(0, lambda: self.raw_process_button.configure(state="normal", text="⚙️ Parse"))

        threading.Thread(target=parse_task, daemon=True).start()

    # ============================================================
    # Q&A
    # ============================================================
    
    def _ask_knowledge(self):
        if self._is_destroyed:
            return

        question = self._qa_entry.get().strip()
        if not question:
            return

        self._qa_response.configure(state="normal")
        self._qa_response.delete("1.0", "end")
        self._qa_response.insert("1.0", f"🔍 Searching: '{question}'\n\n")
        self._qa_button.configure(state="disabled", text="⏳...")

        try:
            from core.knowledge import knowledge
            results = []

            if knowledge is not None:
                for method_name in ['search', 'find', 'get']:
                    if hasattr(knowledge, method_name):
                        try:
                            meth = getattr(knowledge, method_name)
                            if method_name == 'search':
                                try:
                                    res = meth(query=question, limit=10)
                                except:
                                    try:
                                        res = meth(query=question, max_results=10)
                                    except:
                                        res = meth(question)
                            else:
                                res = meth(question)
                            if res:
                                if isinstance(res, list):
                                    results = res
                                elif isinstance(res, dict):
                                    results = [res]
                                break
                        except Exception:
                            continue

            normalized_results = []
            for item in results:
                if isinstance(item, dict):
                    normalized_results.append(item)
                else:
                    normalized = self._normalize_item(item)
                    if normalized.get('content'):
                        normalized_results.append(normalized)

            if not normalized_results and self.knowledge_items:
                keywords = question.lower().split()
                scored = []
                for item in self.knowledge_items:
                    content = item.get('content', '').lower()
                    score = sum(1 for kw in keywords if kw in content)
                    if score > 0:
                        scored.append((score, item))
                scored.sort(key=lambda x: x[0], reverse=True)
                normalized_results = [item for _, item in scored[:5]]

            if normalized_results:
                self._qa_response.insert("end", "📚 Found:\n\n")
                keywords = question.lower().split()

                for i, item in enumerate(normalized_results, 1):
                    content = item.get('content', '')
                    confidence = item.get('confidence', 0)
                    category = item.get('category', 'general')

                    sentences = re.split(r'[.!?]', content)
                    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

                    relevant = []
                    for sent in sentences:
                        sent_lower = sent.lower()
                        kw_count = sum(1 for kw in keywords if kw in sent_lower)
                        if kw_count > 0:
                            relevant.append((kw_count, sent))

                    relevant.sort(key=lambda x: x[0], reverse=True)
                    best_sentences = [sent for _, sent in relevant[:2]]

                    if not best_sentences:
                        for sent in sentences:
                            if len(sent) > 40:
                                best_sentences.append(sent)
                                if len(best_sentences) >= 2:
                                    break

                    if not best_sentences:
                        best_sentences = [content[:150] + "..."]

                    answer = '. '.join(best_sentences)
                    if len(answer) > 300:
                        answer = answer[:300] + "..."

                    source = ""
                    url_match = re.search(r'(https?://[^\s]{10,})', content)
                    if url_match:
                        url = url_match.group(1)
                        if len(url) < 80:
                            source = f" (Source: {url})"

                    self._qa_response.insert(
                        "end",
                        f"{i}. [{category.upper()}] {answer}{source}\n   (Confidence: {confidence:.0f}%)\n\n"
                    )
            else:
                self._qa_response.insert("end", "😕 No relevant knowledge found.\n\n💡 Tips:\n• Use specific keywords\n• Add knowledge via the form above")

        except Exception as e:
            logger.error(f"[Knowledge] Q&A error: {e}")
            self._qa_response.insert("end", f"❌ Error: {str(e)[:100]}")

        self._qa_response.configure(state="disabled")
        self._qa_entry.delete(0, "end")
        self._qa_button.configure(state="normal", text="🔍 Ask")

    # ============================================================
    # PAGINATION & FILTER
    # ============================================================
    
    def _apply_filter_and_paginate(self):
        category = "All"
        if self._safe_widget_exists(self.category_filter_menu):
            category = self.category_filter_menu.get()

        search_query = ""
        if self._safe_widget_exists(self.search_entry):
            search_query = self.search_entry.get().strip().lower()

        items = self.knowledge_items

        if category != "All":
            items = [i for i in items if i.get('category', '').lower() == category.lower()]

        if search_query:
            items = [i for i in items if search_query in i.get('content', '').lower()]

        self.filtered_items = items
        total = len(items)
        self.total_pages = max(1, (total + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE)

        if self.current_page >= self.total_pages:
            self.current_page = self.total_pages - 1
        if self.current_page < 0:
            self.current_page = 0

        self._update_list_page()
        self._update_pagination_controls()

    def _update_list_page(self):
        if self._is_destroyed:
            return

        try:
            for w in self.list_container.winfo_children():
                w.destroy()
        except:
            pass

        start = self.current_page * self.ITEMS_PER_PAGE
        end = min(start + self.ITEMS_PER_PAGE, len(self.filtered_items))
        page_items = self.filtered_items[start:end]

        if not page_items:
            label = ctk.CTkLabel(
                self.list_container,
                text=KNOWLEDGE_NO_RESULTS_TEXT,
                font=("Segoe UI", 13),
                text_color="#5F6B78"
            )
            label.pack(padx=20, pady=30)
            return

        icons = KNOWLEDGE_CATEGORY_ICONS

        for i, item in enumerate(page_items):
            try:
                frame = ctk.CTkFrame(
                    self.list_container,
                    fg_color="#1A2430" if i % 2 == 0 else "transparent",
                    corner_radius=4
                )
                frame.pack(fill="x", padx=5, pady=2)

                content = item.get('content', 'No content')[:100] + "..."
                cat = item.get('category', 'general')
                conf = item.get('confidence', 0)
                icon = icons.get(cat, '📄')

                label = ctk.CTkLabel(
                    frame,
                    text=f"{icon} [{cat.upper()}] {content} (conf: {conf:.0f}%)",
                    font=("Segoe UI", 11),
                    text_color="#E8EDF2",
                    anchor="w"
                )
                label.pack(padx=10, pady=5, fill="x")

            except Exception as e:
                logger.debug(f"List item error: {e}")

    def _update_pagination_controls(self):
        if self._safe_widget_exists(self.prev_btn):
            self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        if self._safe_widget_exists(self.next_btn):
            self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")
        if self._safe_widget_exists(self.page_label):
            self.page_label.configure(text=f"{self.current_page+1}/{self.total_pages}")
        if self._safe_widget_exists(self.count_label):
            self.count_label.configure(text=f"{len(self.filtered_items)} items")

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_list_page()
            self._update_pagination_controls()

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_list_page()
            self._update_pagination_controls()

    def _filter_category(self, category):
        self.current_page = 0
        self._apply_filter_and_paginate()

    # ============================================================
    # UPDATE DATA
    # ============================================================
    
    def update_data(self):
        if not self.is_running or self._is_destroyed:
            return

        try:
            if not self.winfo_exists():
                self.is_running = False
                return
        except:
            self.is_running = False
            return

        try:
            self.update_count += 1
            self._collect_data()
            self._update_ui()
            self.is_connected = True
            self.success_count += 1
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            logger.error(f"[Knowledge] Update error: {e}")
            if self._safe_widget_exists(self.knowledge_status):
                self.knowledge_status.set_status(False)

        if self.is_running and not self._is_destroyed:
            try:
                self.after(self.update_interval, self.update_data)
            except:
                pass

    # ============================================================
    # COLLECT DATA
    # ============================================================
    
    def _collect_data(self):
        self.knowledge_items = []
        self.trending_topics = []
        self.smart_suggestions = []
        self.knowledge_stats = {}

        # 1. Dari Core Knowledge
        try:
            from core.knowledge import knowledge
            if knowledge:
                if hasattr(knowledge, 'stats'):
                    stats = knowledge.stats()
                    if stats:
                        self.knowledge_stats = {
                            "total": getattr(stats, 'total', 0),
                            "states": getattr(stats, 'state_count', 0),
                            "avg_confidence": getattr(stats, 'avg_confidence', 0),
                            "active": getattr(stats, 'active', 0),
                            "archived": getattr(stats, 'archived', 0),
                        }

                if hasattr(knowledge, 'all'):
                    items = knowledge.all()
                    if items:
                        for item in items[:KNOWLEDGE_MAX_ITEMS_DISPLAY]:
                            try:
                                normalized = self._normalize_item(item)
                                if normalized.get('content'):
                                    self.knowledge_items.append(normalized)
                            except:
                                continue
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"[Knowledge] Core error: {e}")

        # 2. Generate Trending Topics dari Knowledge Items
        all_words = []
        for item in self.knowledge_items:
            content = item.get('content', '')
            # Ambil kata-kata penting (min 4 karakter)
            words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
            all_words.extend(words)

        # Hitung frekuensi
        word_counts = Counter(all_words)
        # Filter kata umum (stopwords)
        stopwords = {'this', 'that', 'with', 'from', 'have', 'will', 'what', 'when', 'where', 'which', 'would', 'could', 'should', 'your', 'about', 'after', 'before', 'between', 'during', 'without', 'through', 'among', 'upon', 'because', 'since', 'until', 'while'}
        for sw in stopwords:
            word_counts.pop(sw, None)

        # Ambil top 4
        top_words = word_counts.most_common(4)
        self.trending_topics = [
            {"name": word, "count": count} for word, count in top_words if count > 1
        ]

        # 3. Generate Smart Suggestions dari Knowledge Items
        if self.knowledge_items:
            # Ambil item dengan confidence tinggi
            sorted_items = sorted(self.knowledge_items, key=lambda x: x.get('confidence', 0), reverse=True)
            high_confidence = [item for item in sorted_items if item.get('confidence', 0) > 60][:3]
            
            suggestions = []
            for item in high_confidence:
                content = item.get('content', '')
                # Ambil kalimat pertama sebagai pertanyaan
                sentences = re.split(r'[.!?]', content)
                for sent in sentences:
                    sent = sent.strip()
                    if len(sent) > 30:
                        # Buat pertanyaan
                        if 'bitcoin' in sent.lower() or 'crypto' in sent.lower():
                            suggestions.append("Tell me about Bitcoin / Crypto")
                        elif 'market' in sent.lower():
                            suggestions.append("How is the market doing?")
                        elif 'pattern' in sent.lower():
                            suggestions.append("What patterns are detected?")
                        else:
                            # Ambil 5 kata pertama sebagai topik
                            words = sent.split()[:5]
                            suggestions.append(f"What is {' '.join(words)}?")
                        break
            
            # Fallback suggestions
            if not suggestions:
                suggestions = [
                    "What is the latest market trend?",
                    "Tell me about Bitcoin",
                    "What patterns are forming?",
                    "Summarize recent knowledge"
                ]
            
            self.smart_suggestions = suggestions[:4]
        else:
            self.smart_suggestions = [
                "What is the latest market trend?",
                "Tell me about Bitcoin",
                "What patterns are forming?",
                "Summarize recent knowledge"
            ]

    # ============================================================
    # UPDATE UI
    # ============================================================
    
    def _update_ui(self):
        if self._is_destroyed:
            return

        total = self.knowledge_stats.get('total', 0)
        has_data = total > 0 or len(self.knowledge_items) > 0

        if self._safe_widget_exists(self.knowledge_status):
            self.knowledge_status.set_status(has_data)

        if self._safe_widget_exists(self.total_items_card):
            self.total_items_card.update_value(str(total))

        if self._safe_widget_exists(self.pattern_count_card):
            self.pattern_count_card.update_value(str(len(self.trending_topics)))

        if self._safe_widget_exists(self.insight_count_card):
            categories = set(item.get('category', 'general') for item in self.knowledge_items)
            self.insight_count_card.update_value(str(len(categories)))

        avg_conf = self.knowledge_stats.get('avg_confidence', 0)
        if self._safe_widget_exists(self.confidence_avg_card):
            self.confidence_avg_card.update_value(f"{avg_conf:.0f}%")

        # ============================================================
        # UPDATE TRENDING TOPICS
        # ============================================================
        if self.trending_topics:
            for i, btn in enumerate(self.topic_buttons):
                if i < len(self.trending_topics):
                    topic = self.trending_topics[i]
                    btn.configure(
                        text=f"🔥 {topic['name']} ({topic['count']})",
                        state="normal"
                    )
                    btn.grid()
                else:
                    btn.grid_remove()
        else:
            # Show empty state
            for btn in self.topic_buttons:
                btn.grid_remove()
            self.topics_empty_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        if self._safe_widget_exists(self.topic_count_label):
            self.topic_count_label.configure(text=f"{len(self.trending_topics)} topics")

        # ============================================================
        # UPDATE SMART SUGGESTIONS
        # ============================================================
        for i, btn in enumerate(self.suggestion_buttons):
            if i < len(self.smart_suggestions):
                btn.configure(
                    text=f"💡 {self.smart_suggestions[i]}",
                    state="normal"
                )
                btn.grid()
            else:
                btn.grid_remove()

        # Apply filter & paginate
        self._apply_filter_and_paginate()

        if self._safe_widget_exists(self.last_update_label):
            self.last_update_label.configure(
                text=f"Last update: {datetime.now().strftime('%H:%M:%S')}"
            )

    # ============================================================
    # LIFECYCLE
    # ============================================================
    
    def set_bot(self, bot):
        self.bot = bot

    def refresh(self):
        if not self._is_destroyed:
            self.update_data()

    def stop(self):
        self.is_running = False

    def on_show(self):
        self.is_running = True
        self._is_destroyed = False
        self.update_data()

    def destroy(self):
        if self._is_destroyed:
            return
        self._is_destroyed = True
        self.is_running = False
        self.knowledge_items = []
        self.trending_topics = []
        self.smart_suggestions = []
        self.knowledge_stats = {}
        try:
            super().destroy()
        except:
            pass


# ============================================================
# END OF KNOWLEDGE.PY
# ============================================================