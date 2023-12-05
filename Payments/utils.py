# utils.py

import base64
from django.conf import settings

def get_vtpass_basic_auth():
    username = settings.VT_PASS_USERNAME  # Update with the actual setting name
    password = settings.VT_PASS_PASSWORD  # Update with the actual setting name
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('utf-8')
    base64_auth = base64.b64encode(auth_bytes).decode('utf-8')
    return f"Basic {base64_auth}"
def generate_request_id():
    import datetime
    import pytz
    # Get the current date and time in Africa/Lagos timezone (GMT+1)
    lagos_timezone = pytz.timezone('Africa/Lagos')
    current_datetime = datetime.datetime.now(lagos_timezone)
    
    # Format the date and time as YYYYMMDDHHII
    formatted_datetime = current_datetime.strftime('%Y%m%d%H%M')
    
    # Concatenate with additional alphanumeric characters
    request_id = formatted_datetime + 'ad8ef08acd8fc0f'  # You can change this part as desired
    
    # Ensure the Request ID is at least 12 characters long and numeric
    if len(request_id) < 12:
        raise ValueError("Request ID must be 12 characters or more.")
    if not request_id[:12].isdigit():
        raise ValueError("First 12 characters of Request ID must be numeric.")
    
    return request_id