import re
import logging

logger = logging.getLogger(__name__)

def normalize_phone_number(number: str) -> str:
    """
    Normalize phone number to E.164 format (digits only, no +).
    
    Rules:
    - Remove all non-digit characters.
    - Remove leading '0's.
    - If length is 10, prepend '91' (India default).
    - If length is 12 and starts with '91', keep as is.
    - Start with '91' if it looks like an Indian number.
    
    Returns:
        str: Normalized numeric string (e.g., "919876543210")
    
    Raises:
        ValueError: If number is invalid/malformed.
    """
    if not number:
        raise ValueError("Phone number is empty")

    # Remove all non-digit characters
    digits = "".join(filter(str.isdigit, str(number)))
    
    # Remove leading zeros
    digits = digits.lstrip('0')
    
    # Logic for Indian numbers (most common case for this app)
    if len(digits) == 10:
        return f"91{digits}"
    
    if len(digits) == 12 and digits.startswith("91"):
        return digits
        
    # Validation: E.164 generally 10-15 digits
    if len(digits) < 10 or len(digits) > 15:
        raise ValueError(f"Invalid phone number length: {len(digits)}")
        
    return digits
