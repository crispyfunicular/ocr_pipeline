#!/usr/bin/env bash
#
# setup.sh — Set up the OCR pipeline environment
#
# Usage:
#   ./setup.sh                  # Base setup (venv + Python deps + API key check)
#   ./setup.sh --with-enhance   # Also install enhancement tools (PyTorch, DocRes, ResShift)
#
# This script:
#   1. Creates a Python virtual environment (.venv)
#   2. Installs Python dependencies from requirements.txt
#   3. Checks API key configuration
#
# With --with-enhance, it additionally:
#   4. Installs enhancement Python packages (requirements-enhance.txt)
#   5. Installs PyTorch with CUDA support
#   6. Clones DocRes repository and downloads model weights
#   7. Clones ResShift / PreP-OCR and downloads model weights
#

set -euo pipefail

# ── Parse arguments ───────────────────────────────────
WITH_ENHANCE=false
for arg in "$@"; do
    case "$arg" in
        --with-enhance) WITH_ENHANCE=true ;;
        -h|--help)
            echo "Usage: ./setup.sh [--with-enhance]"
            echo ""
            echo "Options:"
            echo "  --with-enhance   Install image enhancement tools"
            echo "                   (PyTorch+CUDA, DocRes, ResShift)"
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: ./setup.sh [--with-enhance]"
            exit 1
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$WITH_ENHANCE" = true ]; then
    TOTAL_STEPS=7
else
    TOTAL_STEPS=3
fi

echo "═══════════════════════════════════════════════════"
echo "  🔧 OCR Pipeline — Environment Setup"
if [ "$WITH_ENHANCE" = false ]; then
    echo "     (base only — use --with-enhance for image"
    echo "      enhancement tools)"
fi
echo "═══════════════════════════════════════════════════"

STEP=0

# ── 1. Virtual environment ────────────────────────────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: Virtual environment ──"

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
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: Python dependencies ──"

pip install --upgrade pip -q
pip install -r requirements.txt
echo "  ✅ requirements.txt installed"

# ── 3. API key check ─────────────────────────────────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: API keys ──"

if [ -n "${OPENAI_API_KEY:-}" ]; then
    echo "  ✅ OPENAI_API_KEY is set"
else
    echo "  ⚠️  OPENAI_API_KEY is NOT set"
    echo "     The OCR stage requires an OpenAI API key."
    echo "     Set it with:  export OPENAI_API_KEY='sk-...'"
fi

# ── Enhancement tools (opt-in) ────────────────────────
if [ "$WITH_ENHANCE" = true ]; then

# ── 4. Enhancement Python dependencies ────────────────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: Enhancement Python dependencies ──"

pip install -r requirements-enhance.txt
echo "  ✅ requirements-enhance.txt installed"

# ── 5. PyTorch with CUDA ──────────────────────────────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: PyTorch with CUDA ──"

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

# ── 6. DocRes (AI document restoration) ───────────────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: DocRes setup ──"

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

# ── 7. ResShift / PreP-OCR (diffusion deblurring) ─────
STEP=$((STEP + 1))
echo ""
echo "── Step ${STEP}/${TOTAL_STEPS}: ResShift (PreP-OCR deblurring) setup ──"

RESSHIFT_DIR="resshift"
RESSHIFT_WEIGHTS="$RESSHIFT_DIR/weights"
DEBLUR_CKPT="$RESSHIFT_WEIGHTS/resshift_deblur_prep_ocr.pth"
AUTOENC_CKPT="$RESSHIFT_WEIGHTS/autoencoder_vq_f4.pth"
PREPOCR_CONFIG="$RESSHIFT_DIR/configs/deblur_prepocr.yaml"

if [ -d "$RESSHIFT_DIR" ]; then
    echo "  ✅ ResShift repo already cloned"
else
    echo "  Cloning ResShift..."
    git clone --depth 1 https://github.com/zsyOAOA/ResShift.git "$RESSHIFT_DIR"
    echo "  ✅ ResShift cloned"
fi

mkdir -p "$RESSHIFT_WEIGHTS"

if [ -f "$DEBLUR_CKPT" ]; then
    echo "  ✅ PreP-OCR deblur weights already downloaded"
else
    echo "  Downloading PreP-OCR deblur weights (457 MB)..."
    wget -q --show-progress \
        "https://huggingface.co/ShuhaoGuan/prep-ocr-resshift-deblur/resolve/main/resshift_deblur_prep_ocr.pth" \
        -O "$DEBLUR_CKPT"
    echo "  ✅ Deblur weights downloaded ($(du -h "$DEBLUR_CKPT" | cut -f1))"
fi

if [ -f "$AUTOENC_CKPT" ]; then
    echo "  ✅ VQ-VAE autoencoder weights already downloaded"
else
    echo "  Downloading VQ-VAE autoencoder weights..."
    wget -q --show-progress \
        "https://github.com/zsyOAOA/ResShift/releases/download/v2.0/autoencoder_vq_f4.pth" \
        -O "$AUTOENC_CKPT"
    echo "  ✅ Autoencoder weights downloaded ($(du -h "$AUTOENC_CKPT" | cut -f1))"
fi

# Create local config with corrected paths
SCRIPT_ABS_DIR="$(cd "$SCRIPT_DIR" && pwd)"
cat > "$PREPOCR_CONFIG" <<YAML
trainer:
  target: trainer.TrainerDifIRLPIPS

model:
  target: models.unet.UNetModelSwin
  ckpt_path: ${SCRIPT_ABS_DIR}/${DEBLUR_CKPT}
  params:
    image_size: 64
    in_channels: 3
    model_channels: 160
    out_channels: 3
    attention_resolutions: [64,32,16,8]
    dropout: 0
    channel_mult: [1, 2, 2, 4]
    num_res_blocks: [2, 2, 2, 2]
    conv_resample: True
    dims: 2
    use_fp16: False
    num_head_channels: 32
    use_scale_shift_norm: True
    resblock_updown: False
    swin_depth: 2
    swin_embed_dim: 192
    window_size: 8
    mlp_ratio: 4
    cond_lq: True
    lq_size: 256

diffusion:
  target: models.script_util.create_gaussian_diffusion
  params:
    sf: 1
    schedule_name: exponential
    schedule_kwargs:
      power: 0.3
    etas_end: 0.99
    steps: 4
    min_noise_level: 0.2
    kappa: 2.0
    weighted_mse: False
    predict_type: xstart
    timestep_respacing: ~
    scale_factor: 1.0
    normalize_input: True
    latent_flag: True

autoencoder:
  target: ldm.models.autoencoder.VQModelTorch
  ckpt_path: ${SCRIPT_ABS_DIR}/${AUTOENC_CKPT}
  tune_decoder: False
  params:
    embed_dim: 3
    n_embed: 8192
    ddconfig:
      double_z: False
      z_channels: 3
      resolution: 256
      in_channels: 3
      out_ch: 3
      ch: 128
      ch_mult:
      - 1
      - 2
      - 4
      num_res_blocks: 2
      attn_resolutions: []
      dropout: 0.0
      padding_mode: zeros
YAML
echo "  ✅ Config written to $PREPOCR_CONFIG"

fi  # end --with-enhance

# ── Done ──────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ Setup complete!"
echo ""
echo "  Activate the environment:"
echo "    source .venv/bin/activate"
echo ""
if [ "$WITH_ENHANCE" = false ]; then
    echo "  To install enhancement tools (PyTorch, DocRes, ResShift):"
    echo "    ./setup.sh --with-enhance"
    echo ""
fi
echo "  Run the pipeline:"
echo "    python pipeline.py run"
echo "    python pipeline.py --help"
echo "═══════════════════════════════════════════════════"
