"""
Stats Tab - Usage statistics and analytics with beautiful charts
"""
import customtkinter as ctk
from components.glass_card import GlassCard
from assets.styles import *
from datetime import datetime, timedelta
import random


class StatsTab(ctk.CTkFrame):
    """Statistics tab showing usage analytics"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._build_ui()
        self._load_mock_stats()
    
    def _build_ui(self):
        """Build stats tab layout"""
        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=BG_GLASS,
            scrollbar_button_hover_color=BG_GLASS_HOVER
        )
        scroll.pack(fill="both", expand=True, padx=PADDING_LG, pady=PADDING_LG)
        
        # Title
        title_label = ctk.CTkLabel(
            scroll,
            text="Statistics",
            font=(FONT_FAMILY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, PADDING_LG))
        
        # Summary cards row
        summary_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(0, PADDING_LG))
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.stat_cards = {}
        stats = [
            ("total", "Total Transcriptions", "0", ACCENT_PRIMARY),
            ("words", "Total Words", "0", ACCENT_SECONDARY),
            ("success", "Success Rate", "0%", ACCENT_SUCCESS),
            ("today", "Today", "0", ACCENT_WARNING)
        ]
        
        for i, (key, label, value, color) in enumerate(stats):
            card = self._create_stat_card(summary_frame, label, value, color)
            card.grid(row=0, column=i, padx=PADDING_XS, sticky="ew")
            self.stat_cards[key] = card
        
        # Activity section
        self._build_activity_section(scroll)
        
        # Most used modes section
        self._build_modes_section(scroll)
        
        # Recent activity timeline
        self._build_timeline_section(scroll)
    
    def _create_stat_card(self, parent, title, value, accent_color):
        """Create a single stat card with animated number"""
        card = GlassCard(parent, hover_enabled=False)
        card.configure(height=120)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        title_label.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_XS))
        
        # Value with accent color
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=(FONT_FAMILY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD),
            text_color=accent_color,
            anchor="w"
        )
        value_label.pack(anchor="w", padx=PADDING_LG, pady=(0, PADDING_LG))
        
        # Store reference to value label
        card.value_label = value_label
        return card
    
    def _build_activity_section(self, parent):
        """Build activity chart section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=PADDING_LG, pady=(PADDING_LG, PADDING_MD))
        
        title = ctk.CTkLabel(
            header,
            text="📊 Activity Overview",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(side="left")
        
        period = ctk.CTkLabel(
            header,
            text="Last 7 days",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY,
            fg_color=BG_DARKER,
            corner_radius=RADIUS_SM,
            padx=PADDING_MD,
            pady=4
        )
        period.pack(side="right")
        
        # Simple bar chart (ASCII-style for now)
        chart_frame = ctk.CTkFrame(section, fg_color="transparent")
        chart_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_LG))
        
        # Mock data for 7 days
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        values = [12, 8, 15, 20, 10, 5, 18]
        max_val = max(values)
        
        for i, (day, val) in enumerate(zip(days, values)):
            bar_container = ctk.CTkFrame(chart_frame, fg_color="transparent")
            bar_container.pack(side="left", fill="both", expand=True, padx=2)
            
            # Bar
            bar_height = int((val / max_val) * 120) if max_val > 0 else 0
            bar = ctk.CTkFrame(
                bar_container,
                fg_color=ACCENT_PRIMARY if val == max(values) else BG_GLASS_ACTIVE,
                corner_radius=RADIUS_SM,
                width=40,
                height=bar_height
            )
            bar.pack(side="bottom", pady=(0, PADDING_XS))
            
            # Value label
            val_label = ctk.CTkLabel(
                bar_container,
                text=str(val),
                font=(FONT_FAMILY, FONT_SIZE_SM, FONT_WEIGHT_MEDIUM),
                text_color=TEXT_PRIMARY if val == max(values) else TEXT_SECONDARY
            )
            val_label.pack(side="bottom", pady=(0, PADDING_XS))
            
            # Day label
            day_label = ctk.CTkLabel(
                bar_container,
                text=day,
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY
            )
            day_label.pack(side="bottom")
    
    def _build_modes_section(self, parent):
        """Build most used modes section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🎯 Most Used Modes",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_MD))
        
        # Mode usage bars
        modes = [
            ("Vibe Coder", 85, ACCENT_PRIMARY),
            ("Casual Chatter", 15, ACCENT_SECONDARY)
        ]
        
        for mode_name, percentage, color in modes:
            mode_frame = ctk.CTkFrame(section, fg_color="transparent")
            mode_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
            
            # Mode name and percentage
            label_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
            label_frame.pack(fill="x", pady=(0, PADDING_XS))
            
            name_label = ctk.CTkLabel(
                label_frame,
                text=mode_name,
                font=(FONT_FAMILY, FONT_SIZE_MD),
                text_color=TEXT_PRIMARY
            )
            name_label.pack(side="left")
            
            pct_label = ctk.CTkLabel(
                label_frame,
                text=f"{percentage}%",
                font=(FONT_FAMILY, FONT_SIZE_MD, FONT_WEIGHT_MEDIUM),
                text_color=color
            )
            pct_label.pack(side="right")
            
            # Progress bar background
            bar_bg = ctk.CTkFrame(
                mode_frame,
                fg_color=BG_DARKER,
                corner_radius=RADIUS_SM,
                height=8
            )
            bar_bg.pack(fill="x")
            
            # Progress bar fill
            bar_fill = ctk.CTkFrame(
                bar_bg,
                fg_color=color,
                corner_radius=RADIUS_SM,
                height=8,
                width=int(600 * percentage / 100)  # Assume 600px max width
            )
            bar_fill.pack(side="left")
        
        # Spacer
        ctk.CTkLabel(section, text="").pack(pady=PADDING_SM)
    
    def _build_timeline_section(self, parent):
        """Build recent activity timeline"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="⏱️ Recent Activity",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_MD))
        
        # Timeline items
        activities = [
            ("5 minutes ago", "Transcribed 120 words in Vibe Coder mode"),
            ("15 minutes ago", "Transcribed 95 words in Casual Chatter mode"),
            ("1 hour ago", "Transcribed 145 words in Vibe Coder mode"),
            ("2 hours ago", "Transcribed 78 words in Vibe Coder mode")
        ]
        
        for time, description in activities:
            item_frame = ctk.CTkFrame(section, fg_color="transparent")
            item_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_SM))
            
            # Timeline dot
            dot = ctk.CTkFrame(
                item_frame,
                fg_color=ACCENT_PRIMARY,
                corner_radius=RADIUS_FULL,
                width=8,
                height=8
            )
            dot.pack(side="left", padx=(0, PADDING_MD), pady=PADDING_XS)
            
            # Content
            content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            content_frame.pack(side="left", fill="x", expand=True)
            
            time_label = ctk.CTkLabel(
                content_frame,
                text=time,
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY
            )
            time_label.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(
                content_frame,
                text=description,
                font=(FONT_FAMILY, FONT_SIZE_MD),
                text_color=TEXT_PRIMARY
            )
            desc_label.pack(anchor="w")
        
        # Spacer
        ctk.CTkLabel(section, text="").pack(pady=PADDING_SM)
    
    def _load_mock_stats(self):
        """Load mock statistics data"""
        # Update summary cards
        self.stat_cards["total"].value_label.configure(text="47")
        self.stat_cards["words"].value_label.configure(text="5,240")
        self.stat_cards["success"].value_label.configure(text="96%")
        self.stat_cards["today"].value_label.configure(text="8")
    
    def refresh_stats(self):
        """Refresh statistics from storage (for future integration)"""
        # TODO: Calculate stats from data_storage.py
        # - Total transcriptions
        # - Total words (sum of text_length)
        # - Success rate (paste_success percentage)
        # - Today's count (filter by date)
        # - Activity by day
        # - Mode usage distribution
        pass
