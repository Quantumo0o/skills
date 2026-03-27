#!/usr/bin/env python3
"""
Akkualle SEO Audit - Automatisches SEO-Monitoring für akku-alle.de
Mit Memory Integration v2.0
"""

import requests
import json
import sys
from datetime import datetime

# Memory Integration
sys.path.insert(0, '/root/.openclaw/workspace/tools')
from skill_memory import get_secret, log_action

API_URL = "https://akku-alle.de/api/admin"

def get_api_secret():
    """Holt das v9 Secret aus dem Memory"""
    return get_secret("v9") or "akkualle-johny-2026-geheim"

def run_seo_audit():
    """Führt v9.seo.auditAll aus und gibt strukturierten Report zurück"""
    secret = get_api_secret()
    
    response = requests.post(API_URL, json={
        "secret": secret,
        "action": "v9.seo.auditAll"
    })

    if response.status_code != 200:
        log_action("akkualle-seo", "audit_failed", f"HTTP {response.status_code}")
        return None

    data = response.json()
    log_action("akkualle-seo", "audit_complete", f"{len(data.get('issues', []))} issues found")
    return data

def fix_meta_descriptions():
    """Kürzt zu lange META Descriptions auf 155 Zeichen"""
    secret = get_api_secret()
    
    blogs = requests.post(API_URL, json={
        "secret": secret,
        "action": "blog.list",
        "data": {"limit": 100}
    }).json()

    fixed = 0
    for blog in blogs.get('blogs', []):
        excerpt = blog.get('excerpt', '')
        if len(excerpt) > 155:
            new_excerpt = excerpt[:152] + "..."
            requests.post(API_URL, json={
                "secret": secret,
                "action": "blog.update",
                "data": {"id": blog['id'], "excerpt": new_excerpt}
            })
            fixed += 1

    log_action("akkualle-seo", "meta_fixed", f"{fixed} descriptions shortened")
    return fixed

def get_content_gaps():
    """Findet Content-Lücken via v9.content.gaps"""
    secret = get_api_secret()
    
    response = requests.post(API_URL, json={
        "secret": secret,
        "action": "v9.content.gaps"
    })

    return response.json()

if __name__ == "__main__":
    print("🔍 Akkualle SEO Audit (mit Memory)")
    print("=" * 50)

    # Health Check
    health = requests.post(API_URL, json={
        "secret": get_api_secret(),
        "action": "v9.health"
    }).json()

    print(f"📊 DB Stats:")
    print(f"   Scooters: {health.get('db', {}).get('scooters', 0)}")
    print(f"   Blogs: {health.get('db', {}).get('blogs', 0)}")
    print(f"   Knowledge: {health.get('db', {}).get('knowledge', 0)}")

    # SEO Audit
    audit = run_seo_audit()
    if audit:
        issues = audit.get('issues', [])
        print(f"\n⚠️  Issues: {len(issues)}")
        for issue in issues[:10]:
            print(f"   - {issue.get('type')}: {issue.get('message')}")

    print(f"\n✅ Audit abgeschlossen: {datetime.now()}")
