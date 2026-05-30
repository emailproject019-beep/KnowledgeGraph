#!/bin/bash

# KnowledgeGraph Somnia Testnet Deployment Start Script

set -e

echo "=========================================="
echo "Starting KnowledgeGraph Deployment"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: bash scripts/setup_deployment.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✓ Virtual environment activated"
echo "✓ PYTHONPATH set to: $PYTHONPATH"
echo ""

# Verify environment configuration
echo "Verifying environment configuration..."
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    exit 1
fi

source .env

if [ -z "$PRIVATE_KEY" ]; then
    echo "ERROR: PRIVATE_KEY not set in .env"
    exit 1
fi

if [ -z "$WALLET_ADDRESS" ]; then
    echo "ERROR: WALLET_ADDRESS not set in .env"
    exit 1
fi

echo "✓ Wallet Address: $WALLET_ADDRESS"
echo "✓ RPC URL: $SOMNIA_RPC_URL"
echo ""

# Verify Docker services
echo "Verifying Docker services..."
if ! nc -z localhost 7687 2>/dev/null; then
    echo "ERROR: Neo4j is not running!"
    echo "Please run: docker-compose up -d"
    exit 1
fi
echo "✓ Neo4j is running"

if ! nc -z localhost 9092 2>/dev/null; then
    echo "ERROR: Kafka is not running!"
    echo "Please run: docker-compose up -d"
    exit 1
fi
echo "✓ Kafka is running"
echo ""

# Check web3 connectivity
echo "Verifying Somnia testnet connectivity..."
python3 << 'EOF'
import os
from web3 import Web3

rpc_url = os.getenv("SOMNIA_RPC_URL")
try:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if w3.is_connected():
        print(f"✓ Connected to Somnia testnet")
        print(f"  Chain ID: {w3.eth.chain_id}")
        print(f"  Latest block: {w3.eth.block_number}")
    else:
        print("ERROR: Failed to connect to Somnia testnet")
        exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    exit 1
fi
echo ""

# Start the deployment
echo "=========================================="
echo "Starting KnowledgeGraph Orchestrator"
echo "=========================================="
echo ""

python3 main.py
