"""
Google Cloud Function for Sophiella Orchestrator
Event-driven processing for voice commands and system control
"""
import json
import requests
from google.cloud import functions_v1
from flask import Request

def sophiella_trigger(request: Request):
    """
    HTTP Cloud Function for processing Sophiella events
    
    Args:
        request: Flask request object
        
    Returns:
        JSON response
    """
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Parse request data
        if request.content_type == 'application/json':
            data = request.get_json(silent=True) or {}
        else:
            data = {}
        
        event_type = data.get('type', 'unknown')
        payload = data.get('payload', {})
        
        print(f"📥 Received event: {event_type}")
        
        # Route based on event type
        if event_type == 'voice_command':
            result = process_voice_command(payload)
        elif event_type == 'system_control':
            result = process_system_control(payload)
        elif event_type == 'agent_request':
            result = process_agent_request(payload)
        elif event_type == 'workflow_trigger':
            result = process_workflow_trigger(payload)
        else:
            result = {
                'error': f'Unknown event type: {event_type}',
                'supported_types': ['voice_command', 'system_control', 'agent_request', 'workflow_trigger']
            }
        
        response = {
            'success': True,
            'event_type': event_type,
            'result': result,
            'timestamp': str(datetime.now())
        }
        
        return (json.dumps(response), 200, headers)
        
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e),
            'timestamp': str(datetime.now())
        }
        return (json.dumps(error_response), 500, headers)

def process_voice_command(payload):
    """Process voice command events"""
    command = payload.get('command', '')
    confidence = payload.get('confidence', 0.0)
    
    # Forward to system control server
    try:
        response = requests.post(
            'http://127.0.0.1:5001/voice_command',
            json={'command': command},
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {'error': f'Voice command processing failed: {str(e)}'}

def process_system_control(payload):
    """Process system control events"""
    action = payload.get('action', '')
    target = payload.get('target', '')
    
    if action == 'open_app':
        try:
            response = requests.post(
                'http://127.0.0.1:5001/open_app',
                json={'name': target},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': f'System control failed: {str(e)}'}
    
    return {'error': f'Unknown system action: {action}'}

def process_agent_request(payload):
    """Process AI agent requests"""
    agent_type = payload.get('agent', 'claude')
    message = payload.get('message', '')
    
    # Placeholder for agent integration
    return {
        'agent': agent_type,
        'response': f'Agent {agent_type} integration coming in Stage 4',
        'message': message
    }

def process_workflow_trigger(payload):
    """Process n8n workflow triggers"""
    workflow_id = payload.get('workflow_id', '')
    trigger_data = payload.get('data', {})
    
    # Forward to n8n instance
    try:
        n8n_url = f"http://localhost:5678/webhook/{workflow_id}"
        response = requests.post(
            n8n_url,
            json=trigger_data,
            timeout=30
        )
        return {
            'workflow_id': workflow_id,
            'status': 'triggered',
            'n8n_response': response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {'error': f'Workflow trigger failed: {str(e)}'}

# For local testing
if __name__ == "__main__":
    from datetime import datetime
    
    # Test data
    test_request_data = {
        'type': 'voice_command',
        'payload': {
            'command': 'open vscode',
            'confidence': 0.95
        }
    }
    
    print("🧪 Testing Cloud Function locally...")
    print(f"Input: {json.dumps(test_request_data, indent=2)}")
    
    # Simulate processing
    result = process_voice_command(test_request_data['payload'])
    print(f"Output: {json.dumps(result, indent=2)}")
