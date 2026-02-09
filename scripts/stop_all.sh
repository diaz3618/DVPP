#!/bin/bash
# Stop all DVPP applications
# Usage: ./scripts/stop_all.sh

echo "🛑 Stopping all DVPP applications..."

# Stop Docker containers
docker-compose down

# Kill any host Python processes on ports 5000-5007
echo "🔍 Checking for host processes..."
PIDS=$(sudo lsof -ti :5000,:5001,:5002,:5003,:5004,:5005,:5006,:5007 2>/dev/null)
if [ ! -z "$PIDS" ]; then
    echo "  Found processes: $PIDS"
    echo "  Killing host processes..."
    sudo kill -9 $PIDS 2>/dev/null
    echo "  ✓ Host processes killed"
fi

echo "All applications stopped"
echo ""
echo "💡 To remove volumes (delete data): docker-compose down -v"
echo "💡 For complete cleanup: ./scripts/cleanup_all.sh"
