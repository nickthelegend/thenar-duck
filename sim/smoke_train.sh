#!/usr/bin/env bash
# Smoke test of the Open Duck Playground training pipeline on this GPU (stock open_duck_mini_v2 robot).
LOG=/mnt/d/Project/thenar-duck/sim/smoke_train.log
exec > >(tee -a "$LOG") 2>&1
echo "=== smoke_train start $(date) ==="
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/Open_Duck_Playground" || exit 1
source .venv/bin/activate
export XLA_PYTHON_CLIENT_MEM_FRACTION=0.85
export TF_FORCE_GPU_ALLOW_GROWTH=true
export JAX_DEFAULT_MATMUL_PRECISION=highest
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
start=$(date +%s)
python playground/open_duck_mini_v2/runner.py --task flat_terrain_backlash --num_timesteps ${1:-2000000}
rc=$?
end=$(date +%s)
echo "runner exit $rc after $((end-start)) s"
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
ls -la checkpoints 2>/dev/null | tail -5
echo "=== smoke_train DONE rc=$rc $(date) ==="
