# 🚀 AngkorSSH SCAN v1.1

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/) 
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/CHEA-MC/AngkorScanBugCDN?style=social)](https://github.com/CHEA-MC/AngkorScanBugCDN/stargazers)

> **Powerful CDN & Subdomain Scanner for Security Researchers**

AngkorScanBugCDN គឺជាឧបករណ៍សម្រាប់ស្រាវជ្រាវសន្តិសុខ (Security Research) ដែលអាច៖  
- ស្កេន CDN IPs (Cloudflare, Bunny.net, Fastly, AWS CloudFront)  
- រក Subdomains សកម្ម  
- ពិនិត្យ Active IPs & Ports (443/HTTPS)  

ប្រើប្រាស់ **multi-threading** ដើម្បីអោយល្បឿនលឿន និងមាន **colored UI** ងាយស្រួលមើល។  

---

## ✨ Features

- 🌐 **CDN Extractor** → ដកបញ្ជី IP ពី CDN ចម្បងៗ  
- 🔍 **IP Scanner** → រក IP ដែលបើក Port 443  
- 🏷️ **Subdomain Scanner** → ពិនិត្យ HTTP/HTTPS របស់ Subdomains  
- 📡 **Domain/IP Reverse Lookup** → ស្វែងរក Subdomains ពី Domain ឬ IP  
- ⚡ **Multi-threading** → ស្កេនលឿន និងប្រសិទ្ធភាពខ្ពស់  
- 🎨 **Colored UI** → អោយប្រើងាយ និងទាន់សម័យ  

---

## 📦 Installation

🔹 On Termux (Android)

Step 1 – Update & Upgrade packages
```bash
pkg update && pkg upgrade -y
```

Step 2 – Install git និង python
```bash
pkg install git python -y
```

Step 3 – Clone Repository
```bash
git clone https://github.com/CHEA-MC/AngkorScanBugCDN.git
```

Step 4 – ចូលទៅក្នុង Folder Project
```bash
cd AngkorScanBugCDN
```
Step 5 – Install Dependencies
```bash
pip install -r requirements.txt
```
## ▶️ Usage

ចូលទៅក្នុង folder រួចរត់៖
```bash
python scan.py
```
---

## 📸 Demo




![AngkorScan Demo](./demo.gif)


---

## ⚠️ Disclaimer

ឧបករណ៍នេះមានគោលបំណង ស្រាវជ្រាវ និងអប់រំ ប៉ុណ្ណោះ។
ការប្រើប្រាស់ខុសច្បាប់ គឺជាការទទួលខុសត្រូវរបស់អ្នកប្រើប្រាស់ផ្ទាល់។
