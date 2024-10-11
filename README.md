# Subseek

Subseek is a simple path fuzzing tool written in Python that discovers valid paths on a target website using a customizable wordlist. It features support for configurable timeouts, verbosity, threading, and status code filtering.

## Features

- Path Fuzzing: Test multiple paths against a target URL
- Threading: Perform concurrent requests for faster processing
- Configurable Timeout: Set custom request timeouts
- Status Code Filtering: Filter results by HTTP status codes
- Verbose Mode: Enable detailed output for every attempted URL
- Result Saving: Save successful paths to a file

## Requirements

- Python 3.x
- `requests`
- `colorama`

## Installation

```bash
git clone https://github.com/Adarsh-S-R/subseek.git
cd subseek
```

## Usage

```bash
python subseek.py -u <target_url> -w <path_to_wordlist> [options]
```

## Options

| Option | Description |
|--------|-------------|
| `-u, --url` | Target URL (e.g., https://example.com) [required] |
| `-w, --wordlist` | Path to the wordlist file [required] |
| `-t, --timeout` | Request timeout in seconds (default: 5) |
| `-v, --verbose` | Enable verbose output |
| `-T, --threads` | Number of threads to use (default: 10) |
| `-d, --delay` | Delay between requests in seconds (default: 0) |
| `-s, --save` | Save results to a file |
| `--status` | Filter output by status codes (default: 200, 301, 302, 403) |

## Example Usage

```bash
# Basic usage
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt

# Verbose output
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt -v

# Custom timeout
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt -t 10

# Specify threads
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt -T 5

# Add delay between requests
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt -d 1

# Save results
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt -s results.txt

# Filter by status codes
python subseek.py -u http://testphp.vulnweb.com -w wordlist.txt --status 200 403
```

Author: **[Adarsh SR](https://github.com/Adarsh-S-R)**

Contact: For questions, suggestions, or contributions, feel free to reach out.
