# 🔄 Node-RED Flow Auto-Sync

Automatic synchronization of Node-RED flows between Main (with authentication) and Client (no authentication) instances.

**Main Node-RED** (192.168.1.xx:1880) → **Client Node-RED** (192.168.1.xx:1880)

---

## ✨ Features

- ✅ **Automatic Flow Sync** - Sync flows with a single command
- ✅ **Bearer Token Authentication** - Secure authentication support
- ✅ **Watch Mode** - Continuous background synchronization
- ✅ **Easy Setup** - Simple Python script, no complex configuration
- ✅ **Preserves Everything** - All nodes, wires, configs, and automations
- ✅ **Fast Deployment** - 2-3 seconds per sync
- ✅ **Production Ready** - Error handling and retry logic included

---

## 🎯 Use Cases

- Synchronize flows between office server and remote client
- Backup flows automatically
- Continuous development and deployment
- Multi-instance Node-RED management
- Flow version control and distribution

---

## 📋 Requirements

- Python 3.7+
- `requests` library
- Node-RED instances (Main and Client)
- Network access between instances

---

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Configure

Edit `sync.py` and update:

```python
MAIN = "http://192.168.1.xx:1880"      # Your Main Node-RED URL
CLIENT = "http://192.168.1.xx:1880"     # Your Client Node-RED URL
FLOW = "Wansa AC"                        # Flow name to sync
USER = "arafath"                         # Username
PASS = "ND!13bo@"                        # Password
```

---

## 📖 Usage

### One-Time Sync

```bash
python3 sync.py
```

**Output:**
```
🔐 Getting token...
✅ Token obtained

🔄 NODE-RED FLOW SYNC
...
✅ SYNC COMPLETED SUCCESSFULLY!
   Synced 61 items
   Status: 204 OK
```

---

### Continuous Watch Mode (Every 10 seconds)

```bash
python3 sync.py --watch --interval 10
```

Press `Ctrl+C` to stop.

---

### Every 5 Seconds

```bash
python3 sync.py --watch --interval 5
```

---

### Custom Flow Name

```bash
python3 sync.py --flow "Other Flow Name"
```

---

### Custom Credentials

```bash
python3 sync.py --user "admin" --password "mypassword"
```

---

## 🔄 How It Works

```
1. Get Bearer token from Main Node-RED
2. Fetch all flows from Main
3. Extract target flow (Wansa AC)
4. Get current flows from Client
5. Merge flows (remove old, add new)
6. Push merged flows to Client
7. ✅ Sync complete!
```

---

## 📊 What Gets Synced

✅ **Nodes**
- Inject nodes with timing settings
- Function nodes with code
- MQTT nodes with configurations
- Link nodes
- Debug nodes
- All custom nodes

✅ **Connections**
- All node wires
- Message routing
- Link references

✅ **Configuration**
- MQTT broker settings
- Device configurations
- Global settings

✅ **Automation**
- Cron schedules
- Repeat intervals
- Timing settings

---

## 🔐 Authentication

### Main Node-RED (Bearer Token)

Main Node-RED uses Bearer token authentication:

```python
Authorization: Bearer <token>
```

The script automatically:
1. Sends username/password to `/auth/token` endpoint
2. Gets Bearer token
3. Uses token for all subsequent API calls

### Client Node-RED

Client can have:
- **No authentication** (recommended for internal network)
- **Same authentication** as Main (optional)

The script detects and handles both cases.

---

## 🐳 Docker Support (Optional)

If you want to run in Docker:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY sync.py .
RUN pip install requests

CMD ["python3", "sync.py", "--watch", "--interval", "10"]
```

Build and run:

```bash
docker build -t nodered-sync .
docker run --network host nodered-sync
```

---

## 📈 Advanced Usage

### Schedule with Cron (Every 5 minutes)

```bash
crontab -e
```

Add:

```cron
*/5 * * * * cd /path/to/SimpleFlow1 && python3 sync.py >> sync.log 2>&1
```

---

### Background Service (Linux)

Create `/etc/systemd/system/nodered-sync.service`:

```ini
[Unit]
Description=Node-RED Flow Auto-Sync
After=network.target

[Service]
Type=simple
User=nodered
WorkingDirectory=/home/nodered/SimpleFlow1
ExecStart=/usr/bin/python3 sync.py --watch --interval 10
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nodered-sync
sudo systemctl start nodered-sync
sudo systemctl status nodered-sync
```

---

### Check Logs

```bash
# View logs
cat sync.log

# Tail logs in real-time
tail -f sync.log

# Last 10 syncs
grep "SYNC COMPLETED" sync.log | tail -10
```

---

## 🆘 Troubleshooting

### Error: "Connection refused"

**Solution:** Check if Node-RED instances are running and accessible:

```bash
curl http://192.168.1.xx:1880/flows
curl http://192.168.1.xx:1880/flows
```

---

### Error: "Cannot get token"

**Solution:** Verify username and password are correct:

```bash
python3 sync.py --user "arafath" --password "ND!13bo@"
```

---

### Error: "Flow not found"

**Solution:** Check exact flow name in Main Node-RED and update `FLOW` variable:

```python
FLOW = "Exact Flow Name"  # Case-sensitive!
```

---

### Error: "401 Unauthorized"

**Solution:** Bearer token might be expired or invalid:

1. Check credentials
2. Verify Main Node-RED authentication is enabled
3. Restart Main Node-RED

---

## 📊 Sync Statistics

The script outputs detailed information:

```
1️⃣  Fetching Main flows...
   ✅ Got 143 items

2️⃣  Finding 'Wansa AC' flow...
   ✅ Extracted 61 items

3️⃣  Getting Client flows...
   ✅ Got 433 items

4️⃣  Preparing payload...
   ✅ Merged 433 items

5️⃣  Pushing to Client...
   ✅ Synced!

Status: 204 OK
```

---

## 🔧 Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `MAIN` | `http://192.168.1.xx:1880` | Main Node-RED URL |
| `CLIENT` | `http://192.168.1.xx:1880` | Client Node-RED URL |
| `FLOW` | `Wansa AC` | Flow name to sync |
| `USER` | `arafath` | Username |
| `PASS` | `ND!13bo@` | Password |

---

## 💡 Tips & Best Practices

1. **Always test first** - Run one-time sync before continuous mode
2. **Monitor logs** - Keep logs for debugging
3. **Use appropriate intervals** - 10-60 seconds is reasonable
4. **Backup flows** - Keep Node-RED backups
5. **Network security** - Use HTTPS in production
6. **Authentication** - Enable auth on both instances for security

---

## 🎯 Real-World Workflow

```bash
# 1. Edit flows in Main Node-RED
# 2. Run sync
python3 sync.py

# 3. Client gets instant update
# ✅ Flow synced!

# Or for continuous development:
python3 sync.py --watch --interval 30
```

---

## 📝 Project Structure

```
SimpleFlow1/
├── sync.py           # Main sync script
├── README.md         # This file
├── LICENSE           # MIT License
├── .gitignore        # Git ignore file
└── examples/
    └── docker-compose.yml  # Docker example (optional)
```

---

