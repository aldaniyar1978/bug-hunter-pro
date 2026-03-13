#!/usr/bin/env python3
"""
Bug Hunter Pro - AI-Powered Vulnerability Scanner
Author: aldaniyar1978
Description: Automated bug bounty hunting tool with OWASP Top 10 detection
"""

import sys
import argparse
import requests
import json
import yaml
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import groq
import concurrent.futures
import logging
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler()
    ]
)

class BugHunter:
    def __init__(self, config_file='config.yaml'):
        """Initialize Bug Hunter with configuration"""
        self.load_config(config_file)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BugHunterPro/1.0 Security Scanner'
        })
        self.vulnerabilities = []
        self.scanned_urls = set()
        
    def load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            logging.info(f"Configuration loaded from {config_file}")
        except FileNotFoundError:
            logging.warning(f"Config file {config_file} not found, using defaults")
            self.config = self.default_config()
    
    def default_config(self):
        """Return default configuration"""
        return {
            'scan': {
                'timeout': 10,
                'max_threads': 5,
                'max_depth': 3
            },
            'groq': {
                'api_key': '',
                'model': 'mixtral-8x7b-32768'
            },
            'payloads': {
                'xss': [
                    '<script>alert(1)</script>',
                    '"><script>alert(1)</script>',
                    "'><script>alert(1)</script>",
                    '<img src=x onerror=alert(1)>'
                ],
                'sqli': [
                    "' OR '1'='1",
                    "' OR 1=1--",
                    "admin' --",
                    "' UNION SELECT NULL--"
                ]
            }
        }
    
    def banner(self):
        """Display banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║           Bug Hunter Pro - Vulnerability Scanner        ║
║              AI-Powered Bug Bounty Tool                  ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def crawl(self, url, depth=0):
        """Crawl website to find URLs"""
        if depth > self.config['scan']['max_depth'] or url in self.scanned_urls:
            return []
        
        self.scanned_urls.add(url)
        found_urls = [url]
        
        try:
            response = self.session.get(url, timeout=self.config['scan']['timeout'])
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    if next_url not in self.scanned_urls:
                        found_urls.extend(self.crawl(next_url, depth + 1))
        except Exception as e:
            logging.error(f"Error crawling {url}: {str(e)}")
        
        return found_urls
    
    def test_xss(self, url):
        """Test for XSS vulnerabilities"""
        vulnerabilities = []
        
        for payload in self.config['payloads']['xss']:
            try:
                # Test in query parameters
                test_url = f"{url}?test={payload}"
                response = self.session.get(test_url, timeout=self.config['scan']['timeout'])
                
                if payload in response.text:
                    vuln = {
                        'type': 'XSS',
                        'severity': 'High',
                        'url': test_url,
                        'payload': payload,
                        'description': 'Reflected XSS vulnerability detected'
                    }
                    vulnerabilities.append(vuln)
                    logging.warning(f"[XSS] Found at {url}")
            except Exception as e:
                logging.debug(f"Error testing XSS on {url}: {str(e)}")
        
        return vulnerabilities
    
    def test_sqli(self, url):
        """Test for SQL Injection vulnerabilities"""
        vulnerabilities = []
        
        for payload in self.config['payloads']['sqli']:
            try:
                test_url = f"{url}?id={payload}"
                response = self.session.get(test_url, timeout=self.config['scan']['timeout'])
                
                # Check for SQL error messages
                sql_errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'oracle']
                if any(error in response.text.lower() for error in sql_errors):
                    vuln = {
                        'type': 'SQL Injection',
                        'severity': 'Critical',
                        'url': test_url,
                        'payload': payload,
                        'description': 'SQL Injection vulnerability detected'
                    }
                    vulnerabilities.append(vuln)
                    logging.warning(f"[SQLi] Found at {url}")
            except Exception as e:
                logging.debug(f"Error testing SQLi on {url}: {str(e)}")
        
        return vulnerabilities
    
    def scan_url(self, url):
        """Scan a single URL for vulnerabilities"""
        print(f"{Fore.YELLOW}[*] Scanning: {url}{Style.RESET_ALL}")
        
        vulns = []
        vulns.extend(self.test_xss(url))
        vulns.extend(self.test_sqli(url))
        
        self.vulnerabilities.extend(vulns)
        return vulns
    
    def scan(self, target_url):
        """Main scanning function"""
        self.banner()
        print(f"{Fore.GREEN}[+] Starting scan on: {target_url}{Style.RESET_ALL}")
        
        # Crawl website
        print(f"{Fore.CYAN}[*] Crawling website...{Style.RESET_ALL}")
        urls = self.crawl(target_url)
        print(f"{Fore.GREEN}[+] Found {len(urls)} URLs{Style.RESET_ALL}")
        
        # Scan URLs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['scan']['max_threads']) as executor:
            executor.map(self.scan_url, urls)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate vulnerability report"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}SCAN RESULTS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if not self.vulnerabilities:
            print(f"{Fore.GREEN}[+] No vulnerabilities found{Style.RESET_ALL}")
            return
        
        print(f"{Fore.RED}[!] Found {len(self.vulnerabilities)} vulnerabilities{Style.RESET_ALL}\n")
        
        for i, vuln in enumerate(self.vulnerabilities, 1):
            severity_color = Fore.RED if vuln['severity'] == 'Critical' else Fore.YELLOW
            print(f"{severity_color}[{i}] {vuln['type']} - {vuln['severity']}{Style.RESET_ALL}")
            print(f"    URL: {vuln['url']}")
            print(f"    Payload: {vuln['payload']}")
            print(f"    Description: {vuln['description']}\n")
        
        # Save to JSON
        report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.vulnerabilities, f, indent=4)
        print(f"{Fore.GREEN}[+] Report saved to: {report_file}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='Bug Hunter Pro - Vulnerability Scanner')
    parser.add_argument('-u', '--url', required=True, help='Target URL to scan')
    parser.add_argument('-c', '--config', default='config.yaml', help='Configuration file')
    
    args = parser.parse_args()
    
    hunter = BugHunter(config_file=args.config)
    hunter.scan(args.url)

if __name__ == '__main__':
    main()
