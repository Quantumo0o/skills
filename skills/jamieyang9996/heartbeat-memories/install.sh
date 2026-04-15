#!/bin/bash

# HBM Memory System Installer for macOS and Linux
# Version: 1.0.0
# Date: April 15, 2026

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  HBM Memory System - Installer${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check operating system
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_NAME="Linux" ;;
    Darwin*)    OS_NAME="macOS" ;;
    *)          OS_NAME="UNKNOWN:${OS}" ;;
esac

echo -e "${BLUE}[1/6] Detecting system...${NC}"
echo "Operating System: ${OS_NAME}"

# Check Python
echo -e "${BLUE}[2/6] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "Python not found!"
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python@3.9"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(${PYTHON_CMD} -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(${PYTHON_CMD} -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(${PYTHON_CMD} -c "import sys; print(sys.version_info.minor)")

if [ ${PYTHON_MAJOR} -lt 3 ] || ([ ${PYTHON_MAJOR} -eq 3 ] && [ ${PYTHON_MINOR} -lt 8 ]); then
    print_error "Python 3.8 or higher required (found ${PYTHON_VERSION})"
    exit 1
fi

print_status "Python ${PYTHON_VERSION} detected"

# Install/upgrade pip
echo -e "${BLUE}[3/6] Setting up Python environment...${NC}"
print_status "Upgrading pip..."
${PYTHON_CMD} -m pip install --upgrade pip --quiet

# Install dependencies
echo -e "${BLUE}[4/6] Installing Python dependencies...${NC}"
REQUIRED_PACKAGES=("chromadb" "sentence-transformers" "pandas" "numpy" "requests" "tqdm")

for package in "${REQUIRED_PACKAGES[@]}"; do
    print_status "Installing ${package}..."
    ${PYTHON_CMD} -m pip install ${package} --quiet
done

# Create directory structure
echo -e "${BLUE}[5/6] Creating directory structure...${NC}"
DIRECTORIES=(
    "memory/目标记忆库"
    "memory/会话记忆库"
    "memory/版本记忆库"
    "memory/经验记忆库"
    "memory/情感记忆库"
    "memory/心跳回忆"
    "memory/语义搜索_db"
    "memory/RAG"
    "scripts"
    "references"
    "models/all-MiniLM-L6-v2/sentence-transformers/all-MiniLM-L6-v2"
)

for dir in "${DIRECTORIES[@]}"; do
    mkdir -p "${dir}"
    print_status "Created: ${dir}"
done

# Download model
echo -e "${BLUE}[6/6] Downloading pre-trained model...${NC}"
print_status "Downloading all-MiniLM-L6-v2 model (this may take a few minutes)..."
if ${PYTHON_CMD} -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('models/all-MiniLM-L6-v2/sentence-transformers/all-MiniLM-L6-v2')" 2>/dev/null; then
    print_status "Model downloaded successfully"
    MODEL_DIM=$(${PYTHON_CMD} -c "from sentence_transformers import SentenceTransformer; import sys; sys.path.insert(0, '.'); model = SentenceTransformer('models/all-MiniLM-L6-v2/sentence-transformers/all-MiniLM-L6-v2'); print(model.get_sentence_embedding_dimension())" 2>/dev/null || echo "384")
    print_status "Model dimension: ${MODEL_DIM}"
else
    print_warning "Model download failed (network issue or disk space)"
    print_warning "You can download it manually later using:"
    echo "  ${PYTHON_CMD} scripts/local_memory_system_v2.py"
fi

# Finalize
echo
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}           INSTALLATION COMPLETE!${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo -e "${BLUE}What's next?${NC}"
echo "  1. Test the system:"
echo "     ${PYTHON_CMD} scripts/local_memory_system_v2.py"
echo "  2. Try adding a memory:"
echo "     add_exp \"Test Problem\" \"Test Solution\" --highlight"
echo "  3. Search your memories:"
echo "     search \"test\""
echo
echo -e "${BLUE}Quick Commands:${NC}"
echo "  ${PYTHON_CMD} scripts/local_memory_system_v2.py           # Start interactive CLI"
echo "  cat memory/会话记忆库/\$(date +%Y-%m-%d).md          # View today's conversations"
echo "  cat memory/目标记忆库/GOALS.md                      # View your goals"
echo
echo -e "${BLUE}Documentation:${NC}"
echo "  README.md          - Complete user guide"
echo "  SKILL.md           - OpenClaw skill definition"
echo "  references/        - Detailed documentation"
echo
echo -e "${BLUE}Need help?${NC}"
echo "  Check references/MEMORY.md for system overview"
echo "  Review the installation log above for any warnings"
echo

# Create a quick test script
cat > test_install.sh << 'EOF'
#!/bin/bash
echo "Testing HBM Memory System installation..."
python3 scripts/local_memory_system_v2.py --help 2>/dev/null && echo "✓ CLI tool works" || echo "✗ CLI tool not working"
[ -f "memory/目标记忆库/GOALS.md" ] && echo "✓ Directory structure OK" || echo "✗ Directory structure incomplete"
echo "Test complete!"
EOF
chmod +x test_install.sh

print_status "Created test script: ./test_install.sh"
echo
echo -e "${YELLOW}Run './test_install.sh' to verify your installation.${NC}"