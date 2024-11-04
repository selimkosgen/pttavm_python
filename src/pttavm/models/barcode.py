from dataclasses import dataclass
from typing import List, Optional

class BarcodeError(Exception):
    """Barkod işlemi hatası"""
    pass

class ValidationError(BarcodeError):
    """Barkod doğrulama hatası"""
    pass

@dataclass
class BarcodeCheckResult:
    """Barkod kontrol sonucu"""
    barcode: str
    exists: bool
    message: Optional[str] = None

@dataclass
class BulkBarcodeCheck:
    """Toplu barkod kontrol isteği"""
    barcodes: List[str]

    def __post_init__(self):
        if not self.barcodes:
            raise ValidationError("At least one barcode is required")
        if not all(isinstance(barcode, str) for barcode in self.barcodes):
            raise ValidationError("All barcodes must be strings")
        if not all(barcode.strip() for barcode in self.barcodes):
            raise ValidationError("Empty or whitespace-only barcodes are not allowed")
        if len(self.barcodes) > 100:  # API limiti
            raise ValidationError("Maximum 100 barcodes allowed per request") 