#!/bin/bash
# Test runner script for OSRS Tool Hub

set -e

echo "🧪 Running OSRS Tool Hub Test Suite"
echo "===================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if poetry is available
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}⚠ Poetry not found. Using pytest directly.${NC}"
    PYTEST_CMD="pytest"
else
    echo -e "${BLUE}📦 Using Poetry to run tests${NC}"
    PYTEST_CMD="poetry run pytest"
fi

# Parse command line arguments
TEST_TYPE="${1:-all}"
VERBOSE="${2:-}"

case "$TEST_TYPE" in
    "all")
        echo -e "${BLUE}Running all tests...${NC}"
        $PYTEST_CMD backend/tests/ -v
        ;;
    "e2e")
        echo -e "${BLUE}Running E2E tests...${NC}"
        $PYTEST_CMD backend/tests/test_e2e_*.py -v -m "not slow"
        ;;
    "integration")
        echo -e "${BLUE}Running integration tests...${NC}"
        $PYTEST_CMD backend/tests/test_integration_*.py -v
        ;;
    "flipping")
        echo -e "${BLUE}Running flipping tests...${NC}"
        $PYTEST_CMD backend/tests/test_e2e_flipping.py backend/tests/test_flipping.py -v
        ;;
    "gear")
        echo -e "${BLUE}Running gear tests...${NC}"
        $PYTEST_CMD backend/tests/test_e2e_gear.py -v
        ;;
    "slayer")
        echo -e "${BLUE}Running slayer tests...${NC}"
        $PYTEST_CMD backend/tests/test_e2e_slayer.py backend/tests/test_slayer.py -v
        ;;
    "unit")
        echo -e "${BLUE}Running unit tests...${NC}"
        $PYTEST_CMD backend/tests/ -v -m "unit"
        ;;
    "coverage")
        echo -e "${BLUE}Running tests with coverage...${NC}"
        echo -e "${YELLOW}Note: pytest-cov must be installed for coverage reports${NC}"
        if command -v poetry &> /dev/null; then
            if poetry run pytest --help | grep -q "\-\-cov"; then
                poetry run pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term
                echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
            else
                echo -e "${YELLOW}⚠ pytest-cov not installed. Install with: poetry add --group dev pytest-cov${NC}"
                echo -e "${BLUE}Running tests without coverage...${NC}"
                poetry run pytest backend/tests/ -v
            fi
        else
            if pytest --help | grep -q "\-\-cov"; then
                pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term
                echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}"
            else
                echo -e "${YELLOW}⚠ pytest-cov not installed. Install with: pip install pytest-cov${NC}"
                echo -e "${BLUE}Running tests without coverage...${NC}"
                pytest backend/tests/ -v
            fi
        fi
        ;;
    *)
        echo "Usage: $0 [all|e2e|integration|flipping|gear|slayer|unit|coverage]"
        echo ""
        echo "Test types:"
        echo "  all         - Run all tests (default)"
        echo "  e2e         - Run end-to-end tests"
        echo "  integration - Run integration tests"
        echo "  flipping    - Run flipping-related tests"
        echo "  gear        - Run gear-related tests"
        echo "  slayer      - Run slayer-related tests"
        echo "  unit        - Run unit tests only"
        echo "  coverage    - Run tests with coverage report"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Tests completed!${NC}"
