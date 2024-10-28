import os
from datetime import datetime
import xml.etree.ElementTree as ET
from typing import Any, Union, Dict

class OrderArchiver:
    """Utility for archiving order responses"""
    
    def __init__(self, archive_dir: str = "pttavm_logs"):
        self.archive_dir = archive_dir
        os.makedirs(archive_dir, exist_ok=True)
    
    def archive_response(self, response: Union[str, Dict], prefix: str = "pttavm_orders_response") -> str:
        """Archive API response as XML"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.xml"
        filepath = os.path.join(self.archive_dir, filename)
        
        if isinstance(response, str):
            # If response is already XML string, save directly
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response)
        else:
            # Convert dictionary response to XML and save
            root = ET.Element("response")
            self._dict_to_xml(response, root)
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
        
        return filepath
    
    def archive_request(self, request: str, prefix: str = "pttavm_orders_request") -> str:
        """Archive API request XML"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.xml"
        filepath = os.path.join(self.archive_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(request)
            
        return filepath
    
    def _dict_to_xml(self, data: Any, parent: ET.Element):
        """Convert dictionary to XML elements"""
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, str(key))
                self._dict_to_xml(value, child)
        elif isinstance(data, (list, tuple)):
            for item in data:
                child = ET.SubElement(parent, "item")
                self._dict_to_xml(item, child)
        else:
            parent.text = str(data)
