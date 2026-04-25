# Advanced Jobboard Crawling Engine

A production-grade jobboard crawler with multi-layered anti-blocking technology, proxy rotation, captcha solving, and human-like behavior simulation.

## Quick Start

### Installation

```bash
cd /root/.openclaw/workspace/jobboard-crawler-engine
pip3 install -r requirements.txt
playwright install chromium
```

### Run Crawler

```bash
chmod +x start_crawler.sh
./start_crawler.sh upwork
```

For all platforms:
```bash
./start_crawler.sh all
```

### Test Features

```bash
./start_crawler.sh test-anti-detection
./start_crawler.sh test-proxy-pool
```

## Features

- **Anti-Detection**: Fingerprint spoofing, proxy rotation, stealth mode
- **Proxy Pool**: Auto-discovery, health checking, failover
- **Rate Limiting**: Adaptive backoff, session quotas
- **Captcha Solving**: Auto-detection, 2Captcha, 9LLOK, DeathByCAPTCHA
- **Behavior Simulation**: Human-like typing, scrolling, mouse movements
- **Health Monitoring**: Metrics, IP reputation, analytics
- **Multi-Platform**: Upwork, Freelancer, LinkedIn Jobs

## Configuration

Edit `config/engine_config.json` to configure:
- Platform URLs
- Difficulty levels (easy, medium, hard)
- Proxy settings
- Rate limits
- Captcha provider

## Output

Results saved to `output/crawl_results_[timestamp].json`

## Docker

```bash
docker build -t jobboard-crawler:latest .
docker run -v $(pwd)/config:/app/config -v $(pwd)/output:/app/output jobboard-crawler:latest upwork
```

---

**Author:** Zebedee Korie Nig Ltd
**Date:** 2026-04-21
**Technology:** Python
**Version:** 2.0.0