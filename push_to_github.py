"""
GitHub Push Script - EpiClock v4.0
Replit GitHub entegrasyonu kullanarak dosyalari push eder
"""

import os
import base64
import requests
import json
from pathlib import Path

REPO_OWNER = "mortemdulcem"
REPO_NAME = "epi-clock-DNA-mtl-prototype"

def get_github_token():
    """Replit GitHub connector'dan token al"""
    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    
    repl_identity = os.environ.get("REPL_IDENTITY")
    web_repl_renewal = os.environ.get("WEB_REPL_RENEWAL")
    
    if repl_identity:
        x_replit_token = f"repl {repl_identity}"
    elif web_repl_renewal:
        x_replit_token = f"depl {web_repl_renewal}"
    else:
        raise Exception("Replit token bulunamadi")
    
    url = f"https://{hostname}/api/v2/connection?include_secrets=true&connector_names=github"
    
    response = requests.get(url, headers={
        "Accept": "application/json",
        "X_REPLIT_TOKEN": x_replit_token
    })
    
    data = response.json()
    
    if not data.get("items"):
        raise Exception("GitHub baglantisi bulunamadi")
    
    connection = data["items"][0]
    settings = connection.get("settings", {})
    
    token = settings.get("access_token") or settings.get("oauth", {}).get("credentials", {}).get("access_token")
    
    if not token:
        raise Exception("GitHub access token bulunamadi")
    
    return token


def get_files_to_push():
    """Push edilecek dosyalari topla"""
    files = []
    
    important_files = [
        "modules/prisma_nma_standards.py",
        "modules/genomic_api_client.py",
        "modules/real_epigenetic_clocks.py",
        "modules/nps_database_unodc.py",
        "modules/enhanced_disease_detection.py",
        "modules/reference_database_expanded.py",
        "modules/universal_pharmacology_database.py",
        "modules/deep_learning_methylation.py",
        "app.py",
        "replit.md",
        "requirements.txt",
        "pyproject.toml",
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            files.append(file_path)
    
    modules_dir = Path("modules")
    if modules_dir.exists():
        for py_file in modules_dir.glob("*.py"):
            if str(py_file) not in files:
                files.append(str(py_file))
    
    return files


def get_or_create_branch(token, branch="main"):
    """Branch bilgisini al veya olustur"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{branch}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["object"]["sha"]
    
    return None


def get_file_sha(token, path, branch="main"):
    """Mevcut dosyanin SHA'sini al"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}?ref={branch}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("sha")
    
    return None


def push_file(token, file_path, branch="main"):
    """Tek dosyayi push et"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")
    
    existing_sha = get_file_sha(token, file_path, branch)
    
    data = {
        "message": f"Update {file_path} - PRISMA-NMA standards module",
        "content": content,
        "branch": branch
    }
    
    if existing_sha:
        data["sha"] = existing_sha
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    response = requests.put(url, headers=headers, json=data)
    
    return response.status_code in [200, 201], response.json()


def main():
    print("=" * 60)
    print("GITHUB PUSH - EpiClock v4.0")
    print("=" * 60)
    print(f"\nRepo: {REPO_OWNER}/{REPO_NAME}")
    
    try:
        print("\n[1/3] GitHub token aliniyor...")
        token = get_github_token()
        print("  Token alindi")
        
        print("\n[2/3] Dosyalar toplanıyor...")
        files = get_files_to_push()
        print(f"  {len(files)} dosya bulundu")
        
        print("\n[3/3] Dosyalar push ediliyor...")
        success_count = 0
        error_count = 0
        
        for file_path in files:
            success, result = push_file(token, file_path)
            
            if success:
                print(f"  [OK] {file_path}")
                success_count += 1
            else:
                error_msg = result.get("message", "Bilinmeyen hata")
                print(f"  [HATA] {file_path}: {error_msg}")
                error_count += 1
        
        print("\n" + "=" * 60)
        print("SONUC")
        print("=" * 60)
        print(f"  Basarili: {success_count}")
        print(f"  Hatali: {error_count}")
        print(f"\nRepo URL: https://github.com/{REPO_OWNER}/{REPO_NAME}")
        
    except Exception as e:
        print(f"\n[HATA] {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()
