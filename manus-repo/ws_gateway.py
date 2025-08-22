"""
ws_gateway.py

A minimal WebSocket gateway that accepts JSON messages from a client and proxies them
to the OpenAI Chat API using the environment OPENAI_API_KEY (or a provided api_key in the
message). This is intentionally simple (non-streaming) so it will work without extra
streaming plumbing; you can extend it later to support streaming tokens.

Usage:
  # start server
  python ws_gateway.py

Client message format (JSON) over websocket:
  {
    "api_key": "optional - use env OPENAI_API_KEY if not provided",
    "model": "gpt-4o-mini",           # optional
    "messages": [ {"role":"user","content":"Hello"} ]
  }

Server response (JSON):
  { "ok": true, "reply": "..." }
  or
  { "ok": false, "error": "..." }

Security: this gateway forwards requests to OpenAI using the provided API key. Keep keys secret.
Bind to localhost or use an SSH tunnel for remote access.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import status
from fastapi.responses import HTMLResponse
import os
import json
import asyncio

try:
    import openai
except Exception:
    openai = None

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ws gateway ready"}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except Exception as e:
                await websocket.send_text(json.dumps({"ok": False, "error": f"invalid json: {e}"}))
                continue

            api_key = data.get('api_key') or os.environ.get('OPENAI_API_KEY') or os.environ.get('OPENAI_API_KEY_LOCAL')
            if not api_key:
                await websocket.send_text(json.dumps({"ok": False, "error": "no OpenAI API key provided (field api_key or OPENAI_API_KEY env)"}))
                continue

            if openai is None:
                await websocket.send_text(json.dumps({"ok": False, "error": "openai package not installed"}))
                continue

            openai.api_key = api_key
            model = data.get('model', 'gpt-4o-mini')
            messages = data.get('messages')
            if not messages:
                await websocket.send_text(json.dumps({"ok": False, "error": "missing messages field"}))
                continue

            # Call OpenAI (simple non-streaming call)
            try:
                resp = openai.ChatCompletion.create(model=model, messages=messages)
                # The exact shape depends on OpenAI library version; be defensive
                choice = None
                if isinstance(resp, dict):
                    choices = resp.get('choices') or []
                    if len(choices) > 0:
                        # handle different response shapes
                        content = choices[0].get('message', {}).get('content') if choices[0].get('message') else choices[0].get('text')
                        choice = content
                else:
                    # Some client libs return objects with .choices
                    try:
                        choice = resp.choices[0].message.content
                    except Exception:
                        choice = str(resp)

                await websocket.send_text(json.dumps({"ok": True, "reply": choice}))
            except Exception as e:
                await websocket.send_text(json.dumps({"ok": False, "error": str(e)}))

    except WebSocketDisconnect:
        return

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8787)
