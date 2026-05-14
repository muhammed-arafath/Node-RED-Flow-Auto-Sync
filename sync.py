#!/usr/bin/env python3
"""
🔄 Node-RED Flow Auto-Sync - FINAL VERSION
Main (Auth): enter  ip101:1880 → Client: enter  ip44:1880
"""

import requests
import sys
import time

MAIN = "http://enter  ip101:1880"
CLIENT = "http://enter  ip44:1880"
FLOW = "Wansa AC"
USER = "arafath"
PASS = "ND!13bo@"

def get_bearer_token(node_red_url, username, password):
    """Get Bearer token"""
    try:
        login_url = f"{node_red_url}/auth/token"
        data = {"client_id": "node-red-admin", "grant_type": "password", 
                "scope": "*", "username": username, "password": password}
        
        r = requests.post(login_url, json=data, timeout=10)
        
        if r.status_code == 200:
            token = r.json().get('access_token')
            if token:
                return token
        return None
    except:
        return None

def sync(main_token):
    """Sync flows"""
    print("="*70)
    print("🔄 NODE-RED FLOW SYNC")
    print("="*70)
    print(f"Main:   {MAIN}")
    print(f"Client: {CLIENT}")
    print(f"Flow:   {FLOW}\n")
    
    main_headers = {"Authorization": f"Bearer {main_token}"}
    
    try:
        # Get Main flows
        print("1️⃣  Fetching Main flows...")
        r = requests.get(f"{MAIN}/flows", headers=main_headers, timeout=10)
        r.raise_for_status()
        main_flows = r.json()
        print(f"   ✅ Got {len(main_flows)} items\n")
        
        # Find Wansa AC flow
        print(f"2️⃣  Finding '{FLOW}' flow...")
        flow_tab = None
        for f in main_flows:
            if f.get('type') == 'tab' and f.get('label') == FLOW:
                flow_tab = f
                break
        
        if not flow_tab:
            print(f"   ❌ Flow not found!\n")
            return False
        
        # Extract nodes in this flow
        flow_id = flow_tab['id']
        flow_items = [flow_tab]
        
        for item in main_flows:
            if item.get('z') == flow_id:
                flow_items.append(item)
        
        for item in main_flows:
            if not item.get('z') and item.get('type') in ['mqtt-broker', 'rmdevice', 'global-config']:
                flow_items.append(item)
        
        print(f"   ✅ Extracted {len(flow_items)} items\n")
        
        # Get current client flows
        print("3️⃣  Getting Client flows...")
        r = requests.get(f"{CLIENT}/flows", timeout=10)
        r.raise_for_status()
        current_flows = r.json()
        print(f"   ✅ Got {len(current_flows)} items\n")
        
        # Merge flows
        print("4️⃣  Preparing payload...")
        existing_ids = {item['id'] for item in flow_items}
        merged_flows = [item for item in current_flows if item['id'] not in existing_ids]
        merged_flows.extend(flow_items)
        
        print(f"   ✅ Merged {len(merged_flows)} items\n")
        
        # Push to Client
        print("5️⃣  Pushing to Client...")
        r = requests.post(f"{CLIENT}/flows", json=merged_flows, timeout=10)
        
        # Accept 200, 201, 204 as success
        if r.status_code in [200, 201, 204]:
            print(f"   ✅ Synced!\n")
            print("="*70)
            print("✅ SYNC COMPLETED SUCCESSFULLY!")
            print(f"   Synced {len(flow_items)} items")
            print(f"   Status: {r.status_code} OK")
            print("="*70 + "\n")
            return True
        else:
            print(f"   ❌ Failed: {r.status_code}\n")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)[:80]}\n")
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Node-RED Flow Auto-Sync')
    parser.add_argument('--user', default=USER)
    parser.add_argument('--password', default=PASS)
    parser.add_argument('--watch', action='store_true', help='Watch mode')
    parser.add_argument('--interval', type=int, default=10, help='Interval seconds')
    
    args = parser.parse_args()
    
    print("\n🔐 Getting token...\n")
    
    main_token = get_bearer_token(MAIN, args.user, args.password)
    if not main_token:
        print("❌ Cannot get token\n")
        sys.exit(1)
    
    print("✅ Token obtained\n")
    
    if args.watch:
        print(f"👁️  WATCH MODE - Every {args.interval}s (Ctrl+C to stop)\n")
        try:
            count = 0
            while True:
                count += 1
                print(f"[Sync #{count}] {time.strftime('%H:%M:%S')}")
                sync(main_token)
                print(f"⏳ Next in {args.interval}s...\n")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 Watch mode stopped\n")
            sys.exit(0)
    else:
        success = sync(main_token)
        sys.exit(0 if success else 1)
