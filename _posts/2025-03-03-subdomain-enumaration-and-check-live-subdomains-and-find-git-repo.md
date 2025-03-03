---
title: Subfinder | Subdominator - Subdomain Enumeration httprobe - Check Live Domains and Finding Git Repositories
categories: writeup
tags: ['subdomain']
---

# Subdomain Enumeration with Subfinder & Subdominator, Live Domain Checking with httprobe, and Git Repository Discovery

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/subdomain1.webp" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


## 1. Subfinder - Subdomain Enumeration
Subfinder is a tool to find subdomains by querying various online sources.

Installation:
```bash
# Update system and install Go (if not installed)
sudo apt update
sudo apt install golang-go

# Set Go workspace environment variable (if not set)
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Install Subfinder using Go
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Usage:

Run Subfinder to find subdomains for a domain
```bash
subfinder -d example.com
```

You can also use additional flags for more functionality:

- ``o`` to output results to a file
- ``t`` to set the number of threads for faster enumeration

Example:
```bash
subfinder -d example.com -o subdomains.txt
```

## 2. Subdominator - Subdomain Discovery (Using Google Search)
Subdominator is another tool to find subdomains using Google Search.

### Installation:

Clone Subdominator repo and install dependencies
```bash
git clone https://github.com/gwen001/subdominator.git
cd subdominator
pip install -r requirements.txt
```

### Usage:
```bash
# Use Subdominator to find subdomains
python3 subdominator.py -d example.com
```

## 3. httprobe - Check Live Domains
httprobe is used to check if a subdomain is live (responding to HTTP requests).

Installation:

```bash
# Install httprobe using Go
go install github.com/tomnomnom/httprobe@latest
```
Usage:
```bash
# Check if the domains listed in a file are live
cat subdomains.txt | httprobe
```

This command will take a list of subdomains from the file `subdomains.txt` and check which ones are live.

## 4. httpx - HTTP Probe for Enhanced Domain Scanning
httpx is another tool for checking live domains with additional capabilities like checking for HTTPS, ports, etc.

Installation:
```bash
# Install httpx using Go
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

Usage:
```bash
# Check live subdomains with httpx
cat subdomains.txt | httpx -status-code -title -tech-detect
```

This command checks each subdomain's status code, title, and technology stack.

## 5. Finding Git Repositories
To find Git repositories related to a domain or project, you can search GitHub or GitLab for repositories associated with a given domain. You can also use search engines or specific queries to discover GitHub repositories.

### Using Search Engines (e.g., Google):
Search for GitHub repositories associated with a domain:

```bash
site:github.com example.com
```

This search will show you repositories that might be related to `example.com`.

Using GitHub API (Optional for automation):
You can also use GitHub's API to search repositories programmatically. Here’s an example using `curl`:

```bash
curl "https://api.github.com/search/repositories?q=example.com"
```

This command queries GitHub for repositories containing `example.com`.

## Summary of Commands:

### Subfinder for subdomains:

```bash
subfinder -d example.com
```

### Subdominator for subdomains:

```bash
python3 subdominator.py -d example.com
```

### httprobe to check live domains:

```bash
cat subdomains.txt | httprobe
```

### **httpx** for enhanced live domain scanning:

```bash
cat subdomains.txt | httpx -status-code -title -tech-detect
```

### GitHub API to find Git repositories:

```bash
curl "https://api.github.com/search/repositories?q=example.com"
```

