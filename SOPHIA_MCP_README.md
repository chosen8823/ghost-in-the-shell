# Sophia MCP (Minimal) — Local Terminal & System Control

This folder provides a minimal, secure MCP HTTP server and client so Sophia can
be given authorized local-terminal and system-control capabilities.

IMPORTANT SECURITY NOTES
- This server can execute shell commands and write files on the host. Treat the
  API key as a secret.
- Default binding is `127.0.0.1` (localhost) — use an SSH tunnel or `ngrok`
  if you need remote access. Do NOT expose directly to the public internet.
- `allow_dangerous` is `false` by default to protect the host from destructive
  commands (e.g., `rm -rf /`). Enable only if you understand the risks.

Quick start (PowerShell)
```powershell
# 1) Ensure virtualenv is active
& ".\.venv\Scripts\Activate.ps1"

# 2) Install requirements
python -m pip install -r sophia_cloud_infrastructure\requirements.txt

# 3) Edit config\mcp_config.json and set a strong api_key
notepad config\mcp_config.json

# 4) Start the server
python mcp_server.py

# 5) From another machine, create an SSH tunnel (on remote machine):
#    ssh -L 8008:127.0.0.1:8008 user@your-windows-ip
#    Then run the client locally on remote machine pointing to 127.0.0.1:8008

# 6) Or use ngrok to expose a secure tunnel (NOT recommended for production):
#    ngrok http 8008

# 7) Use the client
python mcp_client.py --status
python mcp_client.py --cmd "echo hello"
python mcp_client.py --read "C:\path\to\file.txt"
```

Security checklist
- [ ] Set a strong `api_key` in `config/mcp_config.json` or set env `MCP_API_KEY`.

Advanced options
Installer script

There is a convenience PowerShell installer `install_sophia_full_access.ps1` in the repo root.
 - It generates a cryptographically-strong API key and writes `config/mcp_config.json` with `allow_dangerous=true`.
 - It can open a Windows Firewall rule when run as Administrator (`-Expose`).
 - Use `-StartNow` to start the MCP server immediately in a new PowerShell window.
 - The installer prints the generated API key; keep it secret or rotate it after provisioning.

Quick verification checklist (PowerShell)

1. Run the installer (generate API key, enable full access):

```powershell
PowerShell -ExecutionPolicy Bypass -File .\install_sophia_full_access.ps1 -StartNow
```

2. Confirm `config\mcp_config.json` contains the generated key and `allow_dangerous: true`:

```powershell
Get-Content .\config\mcp_config.json | ConvertFrom-Json
```

3. Verify the server is reachable locally:

```powershell
python mcp_client.py --host 127.0.0.1 --port 8008 --api-key <PASTE_API_KEY> --status
```

4. (Optional) Create an SSH tunnel from remote machine and run client there:

```bash
# on remote (linux/mac)
ssh -L 8008:127.0.0.1:8008 user@<windows-ip>
# then on remote machine
python mcp_client.py --host 127.0.0.1 --port 8008 --api-key <PASTE_API_KEY> --status
```


