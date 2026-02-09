#!/bin/bash
# Start all 8 DVPP applications
# Usage: ./scripts/start_all.sh

echo "Starting all 8 DVPP vulnerable applications..."
echo "⚠️  WARNING: These applications contain intentional security vulnerabilities"
echo "    Only run in isolated lab environments!"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    exit 1
fi

# Start all containers
echo "Building and starting containers..."
docker-compose up -d --build

echo ""
echo "All applications started!"
echo ""
echo "📋 Application URLs:"
echo "   1. SecureDoc (Document Management):  http://localhost:5000"
echo "   2. VulnBlog (Blog/CMS):              http://localhost:5001"
echo "   3. DataViz (Analytics):              http://localhost:5002"
echo "   4. FileShare (File Upload):          http://localhost:5003"
echo "   5. APIGateway (REST API):            http://localhost:5004"
echo "   6. EcomStore (E-commerce):           http://localhost:5005"
echo "   7. ChatApp (Real-time Chat):         http://localhost:5006"
echo "   8. AdminPanel (Admin Dashboard):     http://localhost:5007"
echo ""
echo "View logs: docker-compose logs -f [service_name]"
echo "🛑 Stop all:  docker-compose down"
echo "🗑️  Clean up:  docker-compose down -v"
