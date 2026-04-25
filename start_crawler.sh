#!/bin/bash
# Jobboard Crawling Engine - Launcher Script

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"
cd "$SCRIPT_DIR"

# Check if config file exists
if [ ! -f "config/engine_config.json" ]; then
    echo "Error: Config file not found at config/engine_config.json"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Jobboard Crawling Engine Launcher"
echo "================================"
echo ""

# Parse command line arguments
PLATFORM="${1:-all}"

echo "Target platform: $PLATFORM"
echo "Configuration: config/engine_config.json"
echo ""

case "$PLATFORM" in
    upwork|freelancer|linkedin-jobs)
        echo "Starting crawl for: $PLATFORM"
        python3 main.py "$PLATFORM"
        ;;
    all)
        echo "Starting crawl for all platforms"
        python3 main.py
        ;;
    test-anti-detection)
        echo "Testing anti-detection features..."
        python3 main.py test-anti-detection
        ;;
    test-proxy-pool)
        echo "Testing proxy pool..."
        python3 main.py test-proxy-pool
        ;;
    --help|--h|-h)
        echo "Usage: ./start_crawler.sh [PLATFORM | all | test-anti-detection | test-proxy-pool]"
        echo ""
        echo "Arguments:"
        echo "  upwork     - Crawl Upwork jobs"
        echo "  freelancer - Crawl Freelancer jobs"
        echo "  linkedin-jobs - Crawl LinkedIn Jobs"
        echo "  all        - Crawl all platforms"
        echo "  test-anti-detection - Test anti-detection features"
        echo "  test-proxy-pool - Test proxy pool"
        exit 0
        ;;
    *)
        echo "Error: Unknown platform or command: $PLATFORM"
        echo "Use --help for usage information"
        exit 1
        ;;
esac

echo ""
echo "Crawl completed."