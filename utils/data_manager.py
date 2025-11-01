import json
import os
from datetime import datetime
from typing import Dict, Any

class DataManager:
    def __init__(self):
        self.results_dir = "results"
        self.ensure_results_directory()
    
    def ensure_results_directory(self):
        """Create results directory if it doesn't exist"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def save_results(self, data: Dict[str, Any], filename: str = None) -> str:
        """Save investigation results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"investigation_{timestamp}.json"
        
        filepath = os.path.join(self.results_dir, filename)
        
        # Add timestamp to data
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_results(self, filename: str) -> Dict[str, Any]:
        """Load investigation results from JSON file"""
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_all_results(self) -> list:
        """Get list of all result files"""
        if not os.path.exists(self.results_dir):
            return []
        
        return [f for f in os.listdir(self.results_dir) if f.endswith('.json')]
