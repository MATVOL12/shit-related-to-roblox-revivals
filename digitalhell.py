import requests
import base64
import os
from datetime import datetime
import re
import uuid

def generate_job_id():
    return f"JOB_{uuid.uuid4().hex[:32]}"

def send_soap_request():  #fuck i hate my life
    # Make sure RCCService is running on this port
    url = "http://localhost:64989"
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': 'http://roblox.com/OpenJobEx',
        'Connection': 'keep-alive'
    }
    
    save_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'thumbnails')
    os.makedirs(save_dir, exist_ok=True)
    
    # Check if directory is writable
    if not os.access(save_dir, os.W_OK):
        print(f"Error: Directory {save_dir} is not writable.")
        return
    
    request_path = os.path.expanduser('~/Downloads/request.xml')
    if not os.path.exists(request_path):
        print(f"Error: {request_path} does not exist.")
        return
    
    with open(request_path, 'r') as file:
        soap_template = file.read()  #i dont fucking understand whats going on
    
    try:
        # Generate new job ID for each attempt
        job_id = generate_job_id()
        soap_request = soap_template.replace('JOB_dddHedrNVI9Bn46WCsqZofEXJ023RYghLl', job_id)
        
        print(f"Sending request to: {url}")
        print(f"Headers: {headers}")
        
        response = requests.post(
            url, 
            data=soap_request, 
            headers=headers,
            timeout=120  # Increased timeout to 2 minutes
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            match = re.search(r'<ns1:value>([^<]+)</ns1:value>', response.text)
            if match:
                image_data = base64.b64decode(match.group(1))
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'avatar_thumbnail_{timestamp}.png'
                filepath = os.path.join(save_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                print(f"Thumbnail saved as: {filepath}")
            else:
                print("No image data found in response")
                print("Response content:")
                print(response.text)
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print("Response content:")
            print(response.text)
                
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print("Please ensure RCCService is running and the port is correct")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except Exception as e:
        print(f"Error: {e}")
        if 'response' in locals():
            print("Full response:")
            print(response.text)

if __name__ == "__main__":  #please kill me
    send_soap_request()
