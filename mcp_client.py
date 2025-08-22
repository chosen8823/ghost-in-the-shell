"""
Simple MCP client to interact with the local MCP server.
Usage:
    python mcp_client.py --cmd "echo hello"
    python mcp_client.py --read "path/to/file"
    python mcp_client.py --write "path/to/file" --content "text"

Security:
Set environment variable MCP_API_KEY or edit config/mcp_config.json to match.
"""
import requests
import argparse
import os
from pathlib import Path
import json

CONFIG_PATH = Path("config") / "mcp_config.json"
if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, 'r') as f:
            cfg = json.load(f)
            DEFAULT_HOST = cfg.get('bind_host','127.0.0.1')
            DEFAULT_PORT = cfg.get('bind_port',8008)
    except Exception:
        DEFAULT_HOST = '127.0.0.1'
        DEFAULT_PORT = 8008
else:
    DEFAULT_HOST='127.0.0.1'
    DEFAULT_PORT=8008

API_KEY = os.getenv('MCP_API_KEY') or (cfg.get('api_key') if 'cfg' in locals() else None)
BASE_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"

headers = {}
if API_KEY:
    headers['x-api-key'] = API_KEY


def exec_cmd(cmd, timeout=30):
    r = requests.post(f"{BASE_URL}/exec", json={'cmd':cmd,'timeout':timeout}, headers=headers)
    print(r.json())


def read_file(path):
    r = requests.get(f"{BASE_URL}/file/read", params={'path':path}, headers=headers)
    print(json.dumps(r.json(), indent=2))


def write_file(path, content):
    r = requests.post(f"{BASE_URL}/file/write", json={'path':path,'content':content}, headers=headers)
    print(r.json())


def status():
    r = requests.get(f"{BASE_URL}/status", headers=headers)
    print(r.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', help='Command to execute')
    parser.add_argument('--read', help='Path to read')
    parser.add_argument('--write', help='Path to write')
    parser.add_argument('--content', help='Content to write')
    parser.add_argument('--status', action='store_true')
    args = parser.parse_args()

    if args.status:
        status()
    if args.cmd:
        exec_cmd(args.cmd)
    if args.read:
        read_file(args.read)
    if args.write:
        write_file(args.write, args.content or '')
