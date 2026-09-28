#!/usr/bin/env bash
# One-shot environment bootstrap inside the "microduck" WSL2 Ubuntu-24.04 distro.
# Pins follow research/05_sim_training_options.md §3.3 (known-good: jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5).
set -o pipefail
LOG=/mnt/d/Project/thenar-duck/sim/wsl_setup.log
exec > >(tee -a "$LOG") 2>&1
echo "=== wsl_setup start $(date) ==="
step() { echo; echo "### $1  ($(date +%H:%M:%S))"; }

step "apt"
sudo apt-get update -y && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git git-lfs build-essential curl libgl1 libglu1-mesa libegl1 || { echo "APT FAILED"; exit 1; }

step "uv"
if ! command -v uv >/dev/null 2>&1 && [ ! -x "$HOME/.local/bin/uv" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh || { echo "UV INSTALL FAILED"; exit 1; }
fi
export PATH="$HOME/.local/bin:$PATH"
uv --version

step "clone Open_Duck_Playground"
cd "$HOME"
[ -d Open_Duck_Playground ] || git clone --depth 1 https://github.com/apirrone/Open_Duck_Playground || { echo "CLONE FAILED"; exit 1; }
cd Open_Duck_Playground
git log -1 --format='%H %cd %s'

step "venv + pinned deps"
[ -d .venv ] || uv venv --python 3.12 || { echo "VENV FAILED"; exit 1; }
source .venv/bin/activate
uv pip install "jax[cuda12]==0.6.2" "mujoco==3.3.4" "mujoco-mjx==3.3.4" "playground==0.0.5" || { echo "PIN INSTALL FAILED"; exit 1; }
uv pip install -e . || echo "WARN: editable install of Open_Duck_Playground failed (check pyproject)"
uv pip list 2>/dev/null | grep -i -E "^(jax|jaxlib|mujoco|mujoco-mjx|playground|brax|onnx|tensorflow) " || true

step "jax GPU smoke test"
python - <<'PY'
import jax, jax.numpy as jnp, time
print("jax", jax.__version__, "devices:", jax.devices())
x = jnp.ones((4096, 4096)); t = time.time(); (x @ x).block_until_ready(); print("matmul 4096^2 took", round(time.time() - t, 3), "s")
import mujoco; print("mujoco", mujoco.__version__)
from mujoco import mjx; print("mjx ok")
PY

step "clone reference motion generator"
cd "$HOME"
[ -d Open_Duck_reference_motion_generator ] || git clone --depth 1 https://github.com/apirrone/Open_Duck_reference_motion_generator || echo "WARN: refmotion clone failed"
cd Open_Duck_reference_motion_generator 2>/dev/null && git lfs install && git lfs pull || echo "WARN: lfs pull failed"

step "disk"
df -h / | tail -1
echo "=== wsl_setup DONE $(date) ==="
