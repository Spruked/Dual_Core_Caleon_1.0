#!/bin/bash

# Dual Core Caleon - Health Check Script
# Usage: ./health-check.sh

set -e

echo "🔍 Dual Core Caleon - Health Check"
echo "=================================="

BASE_URL="http://localhost"
SERVICES=(
    "nginx:$BASE_URL/health"
    "frontend:$BASE_URL/"
    "caleon-port:$BASE_URL/api/health"
    "caleon-core:$BASE_URL/core/health"
    "ollama:$BASE_URL/ollama/api/tags"
)

# Optional services
OPTIONAL_SERVICES=(
    "tts-engine:$BASE_URL/tts/health"
)

check_service() {
    local service=$1
    local url=$2
    local name=$(echo $service | cut -d: -f1)

    echo -n "Checking $name... "

    if curl -s --max-time 10 "$url" > /dev/null 2>&1; then
        echo "✅ OK"
        return 0
    else
        echo "❌ FAILED"
        return 1
    fi
}

FAILED_SERVICES=()

echo "Core Services:"
echo "--------------"
for service in "${SERVICES[@]}"; do
    name=$(echo $service | cut -d: -f1)
    url=$(echo $service | cut -d: -f2)

    if ! check_service "$name" "$url"; then
        FAILED_SERVICES+=("$name")
    fi
done

echo ""
echo "Optional Services:"
echo "------------------"
for service in "${OPTIONAL_SERVICES[@]}"; do
    name=$(echo $service | cut -d: -f1)
    url=$(echo $service | cut -d: -f2)

    if check_service "$name" "$url"; then
        :
    fi
done

echo ""
if [ ${#FAILED_SERVICES[@]} -eq 0 ]; then
    echo "🎉 All core services are healthy!"
    echo ""
    echo "Access your Caleon instance at: http://localhost"
    exit 0
else
    echo "❌ Some services are not healthy:"
    for service in "${FAILED_SERVICES[@]}"; do
        echo "   - $service"
    done
    echo ""
    echo "Check logs with: docker-compose logs [service-name]"
    exit 1
fi