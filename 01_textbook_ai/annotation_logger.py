#!/usr/bin/env python
"""Annotation logger module - tracks annotation timestamps by ID only"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional

class AnnotationLogger:
    """Simple logger that tracks annotation timestamps by text ID"""
    
    def __init__(self, log_file: str = "annotation_log.csv", verbose: bool = False):
        self.log_file = log_file
        self.verbose = verbose
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self._init_log_file()
    
    def _init_log_file(self):
        """Create log file with headers if it doesn't exist"""
        file_exists = os.path.exists(self.log_file)
        
        if not file_exists:
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'session_id', 'text_id', 'label', 'strategy', 'confidence'
                ])
            if self.verbose:
                print(f"📝 Created new annotation log: {self.log_file}")
    
    def log(self, text_id: str, label: str, strategy: str, confidence: float = 0.0) -> None:
        """Log a single annotation by ID only"""
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                self.session_id,
                text_id,
                label,
                strategy,
                confidence
            ])
        
        if self.verbose:
            print(f"  📝 Logged ID: {text_id} → {label}")
    
    def log_batch(self, items: List[List]) -> None:
        """Log multiple annotations at once (items[0] is text_id)"""
        for item in items:
            if len(item) >= 3 and item[2] and item[2] != "2":
                text_id = item[0] if len(item) > 0 else ""
                label = item[2] if len(item) > 2 else ""
                strategy = item[3] if len(item) > 3 and item[3] else "unknown"
                confidence = item[4] if len(item) > 4 and item[4] else 0.0
                
                self.log(text_id, label, strategy, confidence)
    
