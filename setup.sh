#!/usr/bin/env bash
#
# setup.sh — Set up the OCR pipeline environment
#
# Usage:
#   ./setup.sh
#
# This script:
#   1. Creates a Python virtual environment (.venv)
#   2. Installs Python dependencies from requirements.txt
#   3. Installs PyTorch with CUDA support
#   4. Clones DocRes repository and downloads model weights
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════"
echo "  🔧 OCR Pipeline — Environment Setup"
echo "═══════════════════════════════════════════════════"

# ── 1. Virtual environment ────────────────────────────
echo ""
echo "── Step 1/4: Virtual environment ──"

if [ -d ".venv" ]; then
    echo "  ✅ .venv already exists"
else
    echo "  Creating .venv..."
    python3 -m venv .venv
    echo "  ✅ .venv created"
fi

# Activate
source .venv/bin/activate
echo "  Activated: $(which python)"

# ── 2. Python dependencies ────────────────────────────
echo ""
echo "── Step 2/4: Python dependencies ──"

pip install --upgrade pip -q
pip install -r requirements.txt
echo "  ✅ requirements.txt installed"

# ── 3. PyTorch with CUDA ──────────────────────────────
echo ""
echo "── Step 3/4: PyTorch with CUDA ──"

if python -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    echo "  ✅ PyTorch with CUDA already installed"
else
    echo "  Installing PyTorch with CUDA 12.8 support..."
    pip install --index-url https://download.pytorch.org/whl/cu128 \
        torch torchvision -q
    echo "  ✅ PyTorch installed"
fi

# Verify
python -c "import torch; print(f'  PyTorch {torch.__version__} — CUDA: {torch.cuda.is_available()}')"

# ── 4. DocRes (AI document restoration) ───────────────
echo ""
echo "── Step 4/4: DocRes setup ──"

DOCRES_DIR="docres"
WEIGHTS_FILE="$DOCRES_DIR/checkpoints/docres.pkl"

if [ -d "$DOCRES_DIR" ]; then
    echo "  ✅ DocRes repo already cloned"
else
    echo "  Cloning DocRes..."
    git clone --depth 1 https://github.com/ZZZHANG-jx/DocRes.git "$DOCRES_DIR"
    echo "  ✅ DocRes cloned"
fi

if [ -f "$WEIGHTS_FILE" ]; then
    echo "  ✅ DocRes weights already downloaded"
else
    echo "  Downloading DocRes weights from HuggingFace..."
    mkdir -p "$DOCRES_DIR/checkpoints"
    wget -q --show-progress \
        "https://huggingface.co/DaVinciCode/doctra-docres-main/resolve/main/docres.pkl" \
        -O "$WEIGHTS_FILE"
    echo "  ✅ Weights downloaded ($(du -h "$WEIGHTS_FILE" | cut -f1))"
fi

# ── 5. OpenAI API key check ───────────────────────────
echo ""
echo "── Step 5/5: OpenAI API key ──"

if [ -n "${OPENAI_API_KEY:-}" ]; then
    echo "  ✅ OPENAI_API_KEY is set"
else
    echo "  ⚠️  OPENAI_API_KEY is NOT set"
    echo "     The OCR stage requires an OpenAI API key."
    echo "     Set it with:  export OPENAI_API_KEY='sk-...'"
fi

# ── Done ──────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ Setup complete!"
echo ""
echo "  Activate the environment:"
echo "    source .venv/bin/activate"
echo ""
echo "  Run the pipeline:"
echo "    python pipeline.py run"
echo "    python pipeline.py --help"
echo "═══════════════════════════════════════════════════"
