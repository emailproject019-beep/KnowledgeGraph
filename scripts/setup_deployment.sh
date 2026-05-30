#!/bin/bash

# KnowledgeGraph Somnia Testnet Deployment Setup Script

set -e

echo "=========================================="
echo "KnowledgeGraph Somnia Testnet Setup"
echo "=========================================="
echo ""

# Step 1: Check prerequisites
echo "Step 1: Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting."; exit 1; }
echo "✓ Prerequisites met (Python 3, Docker, Docker Compose)"
echo ""

# Step 2: Setup Python environment
echo "Step 2: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Step 3: Install Python dependencies
echo "Step 3: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 4: Setup environment variables
echo "Step 4: Setting up environment configuration..."
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please configure .env with:"
    echo "  - SOMNIA_RPC_URL=https://testnet.somnia.network"
    echo "  - PRIVATE_KEY=your_wallet_private_key"
    echo "  - WALLET_ADDRESS=your_wallet_address"
    exit 1
fi

# Validate required env vars
required_vars=("PRIVATE_KEY" "WALLET_ADDRESS" "SOMNIA_RPC_URL")
for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env; then
        echo "ERROR: Missing required environment variable: $var"
        exit 1
    fi
done
echo "✓ Environment configuration verified"
echo ""

# Step 5: Start Docker services
echo "Step 5: Starting Docker services (Neo4j, Kafka, Zookeeper)..."
docker-compose up -d
echo "✓ Docker services started"
echo ""

# Step 6: Wait for services to be ready
echo "Step 6: Waiting for services to be ready..."
echo "  - Waiting for Neo4j (bolt://localhost:7687)..."
for i in {1..30}; do
    if nc -z localhost 7687 2>/dev/null; then
        echo "  ✓ Neo4j is ready"
        break
    fi
    echo "    Attempt $i/30..."
    sleep 2
done

echo "  - Waiting for Kafka (localhost:9092)..."
for i in {1..30}; do
    if nc -z localhost 9092 2>/dev/null; then
        echo "  ✓ Kafka is ready"
        break
    fi
    echo "    Attempt $i/30..."
    sleep 2
done
echo ""

# Step 7: Create Kafka topics
echo "Step 7: Creating Kafka topics..."
docker exec knowledge-graph-kafka kafka-topics --create \
    --topic knowledge-graph \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists 2>/dev/null || true
echo "✓ Kafka topics created"
echo ""

echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Services are running:"
echo "  - Neo4j: bolt://localhost:7687 (user: neo4j, password: password)"
echo "  - Neo4j Browser: http://localhost:7474"
echo "  - Kafka: localhost:9092"
echo ""
echo "Next steps:"
echo "1. Update .env with your testnet wallet credentials"
echo "2. Verify your wallet has testnet funds from faucet"
echo "3. Deploy smart contract: npm run deploy:testnet"
echo "4. Update config.py with deployed contract address"
echo "5. Run: bash scripts/start_deployment.sh"
echo ""
