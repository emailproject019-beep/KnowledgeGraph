# KnowledgeGraph Somnia Testnet Deployment Guide

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- `netcat` (nc) for connectivity checks
- A wallet with testnet funds (get from [Somnia Faucet](https://testnet.somnia.network))

## Step 6: Install Dependencies

### 6.1 Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 6.2 Install Required Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies installed:**
- `web3>=6.0.0` - Ethereum blockchain interaction
- `python-dotenv>=1.0.0` - Environment variable management
- `pydantic>=2.0.0` - Data validation
- `pyyaml>=6.0` - Configuration files
- `kafka-python>=2.0.2` - Message queue
- `neo4j>=5.0.0` - Knowledge graph database
- `requests>=2.31.0` - HTTP client

## Step 7: Setup Infrastructure

### 7.1 Configure Environment Variables

Update `.env` file with your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
# Somnia Testnet Configuration
SOMNIA_RPC_URL=https://testnet.somnia.network
PRIVATE_KEY=your_wallet_private_key_here
WALLET_ADDRESS=your_wallet_address_here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Kafka Configuration
QUEUE_BOOTSTRAP_SERVERS=localhost:9092
```

### 7.2 Start Infrastructure Services

**Option A: Automated Setup (Recommended)**

```bash
bash scripts/setup_deployment.sh
```

This script will:
1. Check prerequisites
2. Create and activate virtual environment
3. Install dependencies
4. Validate environment configuration
5. Start Docker services
6. Wait for services to be ready
7. Create Kafka topics

**Option B: Manual Setup**

Start Docker services:

```bash
docker-compose up -d
```

Verify services are running:

```bash
# Neo4j
docker exec knowledge-graph-neo4j neo4j status

# Kafka
docker exec knowledge-graph-kafka kafka-topics --list --bootstrap-server localhost:9092
```

Create Kafka topics:

```bash
docker exec knowledge-graph-kafka kafka-topics --create \
    --topic knowledge-graph \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1 \
    --if-not-exists
```

### 7.3 Verify Services

**Neo4j Browser:** http://localhost:7474
- Username: `neo4j`
- Password: `password`

**Check Kafka connectivity:**

```bash
docker exec knowledge-graph-kafka kafka-console-producer \
    --broker-list localhost:9092 \
    --topic knowledge-graph
```

## Step 8: Run Deployment

### 8.1 Verify Testnet Connectivity

```bash
python3 << 'EOF'
from web3 import Web3
import os

rpc_url = os.getenv("SOMNIA_RPC_URL", "https://testnet.somnia.network")
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    print(f"✓ Connected to Somnia Testnet")
    print(f"  Chain ID: {w3.eth.chain_id}")
    print(f"  Latest Block: {w3.eth.block_number}")
    
    wallet = os.getenv("WALLET_ADDRESS")
    balance = w3.eth.get_balance(wallet)
    print(f"  Wallet Balance: {w3.from_wei(balance, 'ether')} STM")
else:
    print("✗ Failed to connect to Somnia testnet")
EOF
```

### 8.2 Deploy Smart Contract (If Not Done)

```bash
# Install Hardhat dependencies
npm install

# Deploy to Somnia testnet
npm run deploy:testnet
```

Update `config.py` with deployed contract address:

```python
SOMNIA_RPC = "https://testnet.somnia.network"
PROVENANCE_CONTRACT = "0x..."  # Your deployed contract address
PROVENANCE_ABI = [ ... ]  # Your contract ABI
```

### 8.3 Run OrchestratorAgent

**Automated (Recommended):**

```bash
bash scripts/start_deployment.sh
```

This will:
1. Verify all services are running
2. Check testnet connectivity
3. Validate wallet configuration
4. Start the OrchestratorAgent

**Manual:**

```bash
# Set environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Activate virtual environment
source venv/bin/activate

# Run the application
python3 main.py
```

### 8.4 Expected Output

```
========================================
Starting KnowledgeGraph Deployment
========================================

✓ Virtual environment activated
✓ PYTHONPATH set to: /path/to/KnowledgeGraph
Verifying environment configuration...
✓ Wallet Address: 0x...
✓ RPC URL: https://testnet.somnia.network
Verifying Docker services...
✓ Neo4j is running
✓ Kafka is running
✓ Connected to Somnia testnet
  Chain ID: 50312
  Latest block: 12345
  Wallet Balance: 10.5 STM

=========================================
Starting KnowledgeGraph Orchestrator
=========================================

[INFO] Loading OrchestratorAgent...
[INFO] Starting OrchestratorAgent loop...
[INFO] Publishing message to knowledge-graph...
[INFO] Submitting commit to Somnia: merkle_root=0x...
✓ Anchored: 0xtxhash...
```

## Monitoring

### Monitor Somnia Transactions

View your transactions at: https://testnet-explorer.somnia.network

Search for your wallet address or transaction hash.

### Monitor Neo4j

Access Neo4j browser:

```cypher
MATCH (n) RETURN COUNT(n) as node_count
```

### Monitor Kafka

```bash
docker exec knowledge-graph-kafka kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic knowledge-graph \
    --from-beginning
```

## Troubleshooting

### Service Connection Errors

```bash
# Check if Docker services are running
docker ps

# View service logs
docker-compose logs neo4j
docker-compose logs kafka
```

### Web3 Connection Issues

```bash
# Test RPC connectivity
python3 -c "from web3 import Web3; print(Web3(Web3.HTTPProvider('https://testnet.somnia.network')).is_connected())"
```

### Wallet Balance Low

Get testnet funds from: https://testnet.somnia.network/faucet

### Permission Errors

```bash
chmod +x scripts/setup_deployment.sh
chmod +x scripts/start_deployment.sh
```

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Deactivate Python virtual environment
deactivate
```

## Next Steps

1. Configure data ingestion sources
2. Customize extraction agent parameters
3. Set up monitoring and alerting
4. Deploy to production infrastructure

For more information, see [README.md](README.md)
