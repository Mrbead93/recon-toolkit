# ReconX — Unified Recon Framework

A professional recon and enumeration toolkit built entirely
in Python on an unrooted Android phone (Samsung Z Fold 7)
running Termux.

## Tools

### Port Scanner
Threaded TCP port scanner with DNS resolution, semaphore
limiting, service detection, colour output and auto-saved
timestamped reports. Built across 4 versions from raw
sockets up.

### OSINT Username Tool
Multi-platform username recon tool covering 12 platforms
including GitHub, GitLab, Reddit, Twitter, Instagram,
TikTok, LinkedIn, npm, PyPI, HackerNews and more.
Pulls full profile data where APIs allow.

### Network Mapper
Threaded subnet scanner using dual ICMP and TCP detection
to discover live hosts. Includes service banner grabbing,
open port detection per host and full network reports.
Built across 4 versions.

### Automation Toolkit
Termux:API powered phone automation including battery
monitor with threshold alerts, network watchdog with
live notifications and a daily system report with
persistent logging.

### Shodan Recon Tool
Direct Shodan API integration for public IP intelligence.
Returns geolocation, ISP, open ports, service banners
and CVE vulnerabilities without using the broken CLI.

### ReconX Framework
Unified 10-module framework tying all tools together
into a single menu-driven interface.

## ReconX Modules

| Option | Module                        | Description                              |
|--------|-------------------------------|------------------------------------------|
| 1      | Port Scanner                  | Threaded TCP scan with service detection |
| 2      | OSINT Username Lookup         | 9 platform simultaneous search           |
| 3      | Shodan IP Recon               | CVE detection and IP intelligence        |
| 4      | DNS Recon                     | Subdomain brute force and reverse DNS    |
| 5      | Full Target Report            | Automated multi-phase recon sweep        |
| 6      | Deep Recon                    | Subdomain enum, DNS brute, email harvest |
| 7      | HTTP Fingerprinter            | WAF, tech stack, security header grading |
| 8      | SMB Enumerator                | NetBIOS, signing check, vuln assessment  |
| 9      | CVE Vulnerability Scanner     | Live NVD queries with CVSS scoring       |
| 10     | Web App Recon                 | Directory busting and parameter fuzzing  |

## Launch

```bash
python3 ~/projects/reconx/reconx.py
