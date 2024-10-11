import argparse
import requests
import sys
import urllib3
import concurrent.futures
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from colorama import Fore, Style, init

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_ascii_art():
    ascii_art = """
███████╗██╗   ██╗██████╗ ███████╗███████╗███████╗██╗  ██╗
██╔════╝██║   ██║██╔══██╗██╔════╝██╔════╝██╔════╝██║ ██╔╝
███████╗██║   ██║██████╔╝███████╗█████╗  █████╗  █████╔╝ 
╚════██║██║   ██║██╔══██╗╚════██║██╔══╝  ██╔══╝  ██╔═██╗ 
███████║╚██████╔╝██████╔╝███████║███████╗███████╗██║  ██╗
╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝══╝  ══╝
                                               by Adarsh SR
"""
    print(ascii_art)

def path_fuzzer(url, wordlist, timeout=5, verbose=False, threads=10, delay=0, save_file=None, status_filter=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Retry strategy
        retry_strategy = Retry(
            total=3,  # Number of retries
            backoff_factor=1,  # Delay between retries
            status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        # Ensure the URL ends without a slash to avoid double slashes
        if url.endswith('/'):
            base_url = url[:-1]
        else:
            base_url = url

        with open(wordlist, 'r') as f:
            paths = [line.strip() for line in f]

        results = []
        status_filter = status_filter or [200, 301, 302, 403]

        def check_path(path):
            full_url = f"{base_url}/{path}"
            if verbose:
                print(f"Trying URL: {full_url}")
            try:
                response = http.get(full_url, headers=headers, timeout=timeout, verify=False)

                # Color-code based on status code
                if 200 <= response.status_code < 300:
                    color = Fore.GREEN  # Success
                elif 300 <= response.status_code < 400:
                    color = Fore.BLUE  # Redirection
                elif 400 <= response.status_code < 500:
                    color = Fore.YELLOW  # Client error
                else:
                    color = Fore.RED  # Server error

                if response.status_code in status_filter:
                    result = f"{color}[+] Found valid path ({response.status_code}): {full_url}{Style.RESET_ALL}"
                    print(result)
                    results.append(result)

            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Error connecting to {full_url}: {e}{Style.RESET_ALL}")

            # Delay between requests to avoid rate-limiting
            if delay > 0:
                time.sleep(delay)

        # Use threading to parallelize the path fuzzing process
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            # Execute check_path for each path without a progress bar
            for _ in executor.map(check_path, paths):
                pass  # Simply iterating through to ensure all tasks are completed

        # Save the results to a file if specified
        if save_file:
            with open(save_file, 'w') as f:
                for result in results:
                    f.write(result + '\n')
            print(f"Results saved to {save_file}")

    except FileNotFoundError:
        print(f"Wordlist file '{wordlist}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_ascii_art()
    
    parser = argparse.ArgumentParser(description="Path Fuzzer")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show every attempted URL)")
    parser.add_argument("-T", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between requests in seconds (default: 0)")
    parser.add_argument("-s", "--save", type=str, help="Save results to a file")
    parser.add_argument("--status", type=int, nargs="+", default=[200, 301, 302, 403], help="Filter output by status codes (default: 200, 301, 302, 403)")
    args = parser.parse_args()
    
    path_fuzzer(args.url, args.wordlist, timeout=args.timeout, verbose=args.verbose, threads=args.threads, delay=args.delay, save_file=args.save, status_filter=args.status)
