# 05 — Simulation & walking-policy training options for the microduck on THIS machine

**Machine under evaluation:** Windows 11 Home 23H2 (build 22631), Intel i5-13420H, 24 GB RAM, NVIDIA GeForce RTX 3050 **6 GB Laptop GPU**, NVIDIA driver **546.18**, WSL2 present (only `docker-desktop` distro), Python 3.13 on Windows.
**Robot:** BDX-style biped, 14× Feetech STS3215 (Open Duck Mini v2 layout: 5 DoF per leg + 4 head/neck), PETG on a Bambu P1S.
**Date of research:** 2026-09-26. Every number below carries a URL; anything I could not verify is marked **[UNVERIFIED]**.

---

## TL;DR — decision

| Question | Answer |
|---|---|
| Can this laptop run Isaac Sim 4.5 / 5.x / 6.x + Isaac Lab? | **No.** Official minimum is RTX 3070 / 8 GB (4.5) and RTX 4080 / 16 GB (5.1 and 6.0); driver minimum on Windows is 580.88 (5.1). We have 6 GB and driver 546.18. WSL2 is explicitly unsupported (no Vulkan). |
| Can it run Isaac Gym Preview (legacy)? | **No, and don't try.** Ubuntu 18.04/20.04 only, Python 3.6–3.8, deprecated and unsupported. |
| Can it run MuJoCo Playground / MJX + Brax PPO (what Open Duck Mini uses)? | **Yes, inside WSL2.** JAX has no native-Windows CUDA; WSL2 CUDA is "experimental" but is the standard path. Driver 546.18 satisfies JAX's CUDA-12 wheel minimum (>= 525) and NVIDIA's WSL minimum (R495+). |
| Recommended stack | **WSL2 Ubuntu-24.04 + `jax[cuda12]` + MuJoCo/MJX + fork of `Open_Duck_Playground` with our own MJCF**, reference motions from `Open_Duck_reference_motion_generator` (placo — Linux wheels only, another reason for WSL2), ONNX export → `Open_Duck_Mini_Runtime`-style Python runtime on the robot. |
| Expected training time on the 3050 | Open Duck Mini v2 300 M-step run measured **1 h 11 min at 68,700 steps/s on an RTX 3090**. Scaling by raw FP32/bandwidth (3050 Laptop ≈ 1/5–1/6.4 of a 3090) gives **≈ 9–14 k steps/s → roughly 6–9 h for 300 M steps, 3–4.5 h for the runner's default 150 M steps** **[ESTIMATE — must be measured; assumes 8192 envs fit in 6 GB]**. |
| ROS 2 | **Not required** — Open Duck's runtime is plain Python (rustypot + onnxruntime + BNO055). If you want ROS: **Jazzy Jalisco (LTS, EOL May 2029) on Ubuntu 24.04 in WSL2**, with a small URDF + `robot_state_publisher` + policy node + `feetech_ros2_driver` stack (plan in §4). |
| First thing to do | Update the NVIDIA driver to a current Game Ready build (>= 580.88). It costs nothing and removes the "driver older than ptxas" JIT slow-down, unblocks `jax[cuda13]`, Warp CUDA-13 wheels, etc. |

---

## 1. Official requirements vs. this laptop

### 1.1 NVIDIA Isaac Sim + Isaac Lab

| Isaac Sim version | Min GPU | Min VRAM | Min RAM | Min driver (Windows / Linux) | Source |
|---|---|---|---|---|---|
| **4.5.0** | GeForce RTX 3070 | **8 GB** | 32 GB | (not captured) | 4.5.0 requirements page ([docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/requirements.html](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/requirements.html) — the page 404'd to my fetcher but its table is quoted in search results); corroborated by NVIDIA staff in [IsaacSim discussion #423](https://github.com/isaac-sim/IsaacSim/discussions/423) ("minimum GPU requirement increased from RTX 3070 (version 4.5) to RTX 4080") and by an NVIDIA moderator on the [forum](https://forums.developer.nvidia.com/t/gpu-requirement/305727) ("Minimum: GeForce RTX 3070 with 8GB VRAM; Recommended: RTX 4080 16 GB; Ideal: RTX 6000 Ada 48 GB"). |
| **5.1.0** | GeForce RTX 4080 | **16 GB** | 32 GB | **580.88 / 580.65.06** | [docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html) |
| **6.0 (latest)** | GeForce RTX 4080 | **16 GB** | 32 GB | **595.97 / 595.58.03** | [docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) ("GPUs with less than 16GB VRAM may be insufficient …") |
| **Isaac Lab (main)** | — | "16 GB or more" | "32 GB or more" | Windows 580.88 recommended; Linux 580.65.06+ | [isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html) — also: Isaac Sim 5.x needs Python 3.11, 4.x needs 3.10; support for Isaac Sim <= 4.2 dropped |
| **Isaac Lab 2.1 (for Isaac Sim 4.5)** | — | 16 GB VRAM recommended | 32 GB | — | [isaac-sim.github.io/IsaacLab/v2.1.0/…](https://isaac-sim.github.io/IsaacLab/v2.1.0/source/setup/installation/index.html) |

**Verdict for RTX 3050 6 GB laptop: does not qualify for any Isaac Sim release.**
- 6 GB < 8 GB (4.5 minimum) < 16 GB (5.x/6.x minimum). Driver 546.18 < 580.88.
- NVIDIA staff say the minimum is "the lowest spec GPU tested … not a hard technical limitation" ([discussion #423](https://github.com/isaac-sim/IsaacSim/discussions/423)), and an NVIDIA moderator states "The RTX renderer alone needs up to ~7 GB, so on 8 GB you have very little headroom … The 16 GB minimum is real once scenes get realistic" ([forum: is 8 GB enough for Isaac Sim 5.1](https://forums.developer.nvidia.com/t/is-8gb-vram-enough-for-basic-isaac-sim-5-1-usage/373600)).
- Community data point: someone trained Isaac Lab tasks headless on an **8 GB RTX 4060 laptop** (Isaac Sim 5.1, 32 GB RAM, Windows) but only after crashes without `--headless` and by starting at `num_envs=20` ([tech-multiverse.com](https://tech-multiverse.com/projects/yes-you-can-train-robots-in-isaac-lab-on-an-rtx-4060/)). Nobody documents 6 GB.
- **WSL2 is not an option for Isaac:** "We currently do not support WSL2 and Xvfb … Vulkan is not supported on WSL" ([NVIDIA forum 278252](https://forums.developer.nvidia.com/t/isaac-sim-x86-64-headless-docker-wsl2-support/278252)); the Isaac Sim ROS docs also say Cyclone DDS is "Linux only … Windows WSL2 is not supported at this time" ([Isaac Sim 5.1 ROS install](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_ros.html)).
- Disk: 50 GB SSD minimum for Isaac Sim alone ([5.1.0 requirements](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html)).

### 1.2 Isaac Gym Preview (legacy)

- Status: "This is legacy software. Developers may download and continue to use it, but it is no longer supported." Superseded by Isaac Lab. Latest = Preview 4 ([developer.nvidia.com/isaac-gym](https://developer.nvidia.com/isaac-gym)).
- Prerequisites (Preview 4 docs, mirrored): "Ubuntu 18.04 or 20.04", "Python 3.6, 3.7 or 3.8", "Minimum NVIDIA driver version: Linux: 470" ([docs.robotsfan.com/isaacgym/install.html](https://docs.robotsfan.com/isaacgym/install.html)). The Preview-2 README mirror says "Minimum NVIDIA driver version: 460.32" ([jmcoholich/isaacgym](https://github.com/jmcoholich/isaacgym)).
- The often-quoted "Pascal or later GPU with at least 8 GB VRAM" line appears only in secondary sources in my searches **[UNVERIFIED against an official page]**. NVIDIA's own answer to VRAM questions was "The more environments you try to use, the more VRAM you need"; a user with a 4 GB RTX 3050 laptop could not run the examples at all ([forum 205734](https://forums.developer.nvidia.com/t/gpu-memory-requirement-for-running-isaac-gym/205734)).
- **Verdict:** no Windows, no WSL2 (Vulkan), Python <= 3.8, unsupported. Do not use. Note that `Open_Duck_reference_motion_generator` still emits an Isaac-Gym-format output — ignore it.

### 1.3 Genesis

- `pip install genesis-world`, "Requires Python>=3.10,<3.14"; runs on **Linux, macOS, Windows**; backends CUDA, ROCm, Apple Metal, Vulkan, x86, ARM64; **PyTorch must be installed first** ([GitHub README](https://github.com/Genesis-Embodied-AI/Genesis), [installation docs](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html)). Windows 11 + WSL2 troubleshooting notes exist in the docs.
- Speed claim (v0.2.1 README): "over 43 million FPS when simulating a Franka robotic arm with a single RTX 4090 (430,000 times faster than real-time)" ([README @ v0.2.1](https://raw.githubusercontent.com/Genesis-Embodied-AI/Genesis/v0.2.1/README.md)).
- Locomotion tutorial: Unitree Go2 with `pip install tensorboard rsl-rl-lib==2.2.4`, `python examples/locomotion/go2_train.py`, "This is NOT a comprehensive locomotion policy training pipeline" ([docs v0.4.3](https://genesis-world.readthedocs.io/en/v0.4.3/user_guide/getting_started/locomotion.html)). The "< 26 seconds on an RTX 4090" claim appears in search snippets of older doc versions but not on the v0.4.3 page I fetched **[UNVERIFIED for current version]**.
- **No official VRAM minimum is published.** Verdict: *technically runs natively on Windows on this GPU* (PyTorch has Windows CUDA wheels), so it is the best **native-Windows fallback**, but it is not what Open Duck uses, its MJCF import fidelity for our servo model is unproven, and rsl_rl PPO + Genesis on 6 GB is untested by anyone I could find.

### 1.4 MuJoCo Playground / MJX (JAX)

- Requirements: Python >= 3.10, CUDA 12 via `jax[cuda12]`; install: `uv venv --python 3.12`, `uv pip install -U "jax[cuda12]" --index-url https://pypi.org/simple`, `uv --no-config sync --all-extras` ([mujoco_playground README](https://github.com/google-deepmind/mujoco_playground)). Setup instructions are Linux/macOS; Windows GPU is not possible because JAX has no Windows CUDA build (§3.1).
- Ampere note (our GPU is Ampere): "Users with NVIDIA Ampere architecture GPUs (e.g., RTX 30 and 40 series) may experience reproducibility issues" → `export JAX_DEFAULT_MATMUL_PRECISION=highest` ([same README](https://github.com/google-deepmind/mujoco_playground)).
- MJX design/perf: designed for "all compute hardware supported by the XLA compiler"; on CPU MJX-JAX "can be 10x slower than MuJoCo"; single humanoid at batch 8192 on an A100: "950K steps per second"; MJX-Warp "resolves key performance bottlenecks … around contacts and constraints" ([mujoco.readthedocs.io/en/stable/mjx.html](https://mujoco.readthedocs.io/en/stable/mjx.html)).
- Paper numbers: Berkeley Humanoid flat-ground joystick "under 15 minutes … on two RTX 4090"; Go1 flat "within 5 minutes (2x RTX 4090)"; A100 throughput 120,145 steps/s (Berkeley Humanoid), 417,451 steps/s (Go1) ([arXiv 2502.08844](https://arxiv.org/html/2502.08844)).
- Playground also supports `--impl warp` (MuJoCo Warp backend, beta) but "Training still leverages JAX PPO" → still needs JAX-CUDA → still WSL2 ([playground discussion #197](https://github.com/google-deepmind/mujoco_playground/discussions/197)).
- **No published VRAM minimum.** Verdict: **qualifies, in WSL2**; VRAM headroom on 6 GB must be measured (see §3.4).

### 1.5 Brax

- `pip install brax` (or conda-forge). "Training on NVidia GPU is supported, but you must first install CUDA, CuDNN, and JAX with GPU support." Brax now tells you to use MJX / MuJoCo Warp for physics and keep Brax for the RL algorithms ([google/brax README](https://github.com/google/brax)). Open Duck uses exactly this: Brax PPO on MJX physics.

### 1.6 MuJoCo Warp / Newton / mjlab (the "native Windows?" question)

- NVIDIA Warp ships wheels for **Windows x86-64** and Linux (CPU + CUDA), Python >= 3.10, `pip install warp-lang` ([nvidia.github.io/warp/installation.html](https://nvidia.github.io/warp/installation.html)). Newton (built on Warp): "Linux (x86-64, aarch64), Windows (x86-64), or macOS (CPU only)", "NVIDIA GPU (Maxwell or newer), driver **545 or newer** (CUDA 12)", "No local CUDA Toolkit installation required" ([newton README](https://raw.githubusercontent.com/newton-physics/newton/main/README.md)). Driver 546.18 clears 545 — barely.
- `pip install mujoco-warp`; "NVIDIA GPU is required"; IMPLICITFAST integrator, PGS solver and plugin actuators unsupported ([mujoco_warp README](https://github.com/google-deepmind/mujoco_warp)). A Windows 11 access-violation issue (#8) was closed without comment — Windows status is **unclear** ([issue #8](https://github.com/google-deepmind/mujoco_warp/issues/8)).
- mjlab = "Isaac Lab's manager-based API with MuJoCo Warp", "requires an NVIDIA GPU for training. macOS is supported for evaluation only", `uv run train Mjlab-Velocity-Flat-Unitree-G1 --env.scene.num-envs 4096`; Windows not mentioned ([mujocolab/mjlab](https://github.com/mujocolab/mjlab)).
- rsl_rl (PyTorch PPO used by mjlab/Isaac Lab/Genesis): `pip install rsl-rl-lib`, Python >= 3.9 ([leggedrobotics/rsl_rl](https://github.com/leggedrobotics/rsl_rl)).
- PyTorch publishes Windows CUDA wheels, e.g. `torch-2.14.0+cu126-cp312-cp312-win_amd64.whl` ([download.pytorch.org/whl/cu126/torch](https://download.pytorch.org/whl/cu126/torch/)).

---

## 2. The Open Duck Mini v2 pipeline, exactly

Open Duck Mini v2 = "~42 cm tall", "BOM cost should be under $400", Raspberry Pi Zero 2W onboard, RL via MuJoCo Playground ([Open_Duck_Mini README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/README.md)). BOM sheet: **14× Feetech STS3215 7.4 V / 19 kg·cm (€14 each = €196)**, Waveshare Bus Servo Adapter (A) €5, BNO055 IMU €40, Pi Zero 2W €26.08, 2× Molicel INR18650-P30B + 2S BMS, 4× SS-10 feet switches, total **€398.10** ("lowest" €331.10) ([BOM Google Sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing)).

### 2.1 Step A — reference motions: `Open_Duck_reference_motion_generator` (placo)

Placo-based gait generator that produces imitation targets ([repo](https://github.com/apirrone/Open_Duck_reference_motion_generator)). Commands from the README:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo apt install git-lfs
uv run scripts/auto_waddle.py -j8 --duck open_duck_mini_v2 --sweep --output_dir recordings   # -j = parallel jobs; --sweep = all combos in auto_gait.json (dx, dy, dtheta, frequency ranges); --num N = random motions
uv run scripts/fit_poly.py --ref_motion recordings/          # -> polynomial_coefficients.pkl
uv run scripts/plot_poly_fit.py --coefficients polynomial_coefficients.pkl
uv run scripts/replay_motion.py -f recordings/<file>.json
uv run open_duck_reference_motion_generator/gait_playground.py
```

Outputs `recordings/*.json` and `polynomial_coefficients.pkl`; supports `--duck go_bdx | open_duck_mini | open_duck_mini_v2`. **placo has Linux (manylinux 2.28, x86-64/arm64) and macOS wheels only — no Windows wheels** ([PyPI placo 0.9.26](https://pypi.org/project/placo/)) → this step alone forces WSL2 (or Linux).

### 2.2 Step B — training: `Open_Duck_Playground` (MJX + Brax PPO, joystick env, imitation reward)

README commands ([repo](https://github.com/apirrone/Open_Duck_Playground)):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# copy polynomial_coefficients.pkl into playground/<robot>/data/ and set USE_IMITATION_REWARD=True in joystick.py
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain_backlash --num_timesteps 300000000
uv run tensorboard --logdir=<yourlogdir>
uv run playground/open_duck_mini_v2/mujoco_infer.py -o <path_to_.onnx>
```

- `pyproject.toml`: `requires-python >= 3.11`; deps `jax[cuda12]>=0.5.0`, `jaxlib>=0.5.0`, `playground>=0.0.3`, `onnxruntime>=1.20.1`, `tensorflow>=2.18.0`, `tf2onnx>=1.16.1`, `mediapy`, `pygame`, `framesviewer` ([pyproject](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/pyproject.toml)). **There is no `uv.lock` in the repo** ([root listing](https://api.github.com/repos/apirrone/Open_Duck_Playground/contents/)) → versions drift; pin them (see §3.3).
- Runner CLI defaults: `--num_timesteps 150000000`, `--env joystick`, `--task flat_terrain`, `--output_dir checkpoints`, `--restore_checkpoint_path` ([runner.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/runner.py)). Tasks map to `scene_flat_terrain.xml`, `scene_rough_terrain.xml`, `scene_flat_terrain_backlash.xml`, `scene_rough_terrain_backlash.xml` ([constants.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/constants.py)).
- PPO hyper-parameters are inherited from `mujoco_playground.config.locomotion_params.brax_ppo_config("BerkeleyHumanoidJoystickFlatTerrain")` ([common/runner.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/runner.py)): base `num_envs=8192, batch_size=256, unroll_length=20, num_minibatches=32, num_updates_per_batch=4, discounting=0.97, learning_rate=3e-4, max_grad_norm=1.0, normalize_observations=True`; Berkeley-Humanoid overrides `num_timesteps=150M, num_evals=15, clipping_epsilon=0.2, entropy_cost=0.005`, policy/value MLP `(512, 256, 128)`, value uses `privileged_state` ([locomotion_params.py](https://raw.githubusercontent.com/google-deepmind/mujoco_playground/main/mujoco_playground/config/locomotion_params.py)).
- Env config (`joystick.py`): `ctrl_dt=0.02` (50 Hz), `sim_dt=0.002`, `episode_length=1000`, `action_scale=0.25`, `soft_joint_pos_limit_factor=0.95`, `max_motor_velocity=5.24` rad/s with `USE_MOTOR_SPEED_LIMITS=True`, commands `lin_vel_x ∈ [-0.15, 0.15]`, `lin_vel_y ∈ [-0.2, 0.2]`, `ang_vel_yaw ∈ [-1, 1]`, pushes every 5–10 s of magnitude 0.1–1.0; obs = noisy gyro, noisy accelerometer, command, joint angles, joint velocities, last 3 actions, motor targets, foot contacts, imitation phase; termination = gravity-z < 0 or NaN ([joystick.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/joystick.py)).
- Domain randomization (`common/randomize.py`) and reward weights: see §5.
- ONNX export happens automatically at each eval checkpoint inside `policy_params_fn` → `export_onnx(...)` writing `{output_dir}/{date}_{step}.onnx`; the exporter rebuilds the MLP in Keras, bakes observation mean/std normalisation into the graph, converts with `tf2onnx` (opset 11), output tensor `continuous_actions` ([export_onnx.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/export_onnx.py), [common/runner.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/runner.py)).

**Reported training time / GPU (the only hard number I found):** "300M-step walking run … 1 h 11 min at 68,700 steps/s on an RTX 3090"; that build log used `jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5` for training and `jax 0.11.1 / mujoco 3.12.0 / playground 0.2.0` for inference ([soyeon24/open-duck-mini-v2-build](https://github.com/soyeon24/open-duck-mini-v2-build)). A blog reproduction says 300 M steps "usually takes several hours" without naming the GPU ([dev.to/frankfu](https://dev.to/frankfu/understanding-reinforcement-learning-through-openduck-1if0)). The Open Duck READMEs themselves give no GPU/time.

### 2.3 Step C — deployment: `Open_Duck_Mini_Runtime` (Pi Zero 2W, no ROS)

```bash
git clone https://github.com/apirrone/Open_Duck_Mini_Runtime && cd Open_Duck_Mini_Runtime
git checkout v2
pip install -e .
python3 scripts/check_motors.py
python3 mini_bdx_runtime/mini_bdx_runtime/raw_imu.py
cd scripts/ && python find_soft_offsets.py          # -> ~/duck_config.json (copy example_config.json)
cd scripts/ && python v2_rl_walk_mujoco.py --onnx_model_path <path_to>/BEST_WALK_ONNX_2.onnx
```
([README v2](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/README.md)). Tested on "Raspberry Pi Zero 2W" with Raspberry Pi OS Lite 64-bit (Pi 5 works with `lgpio`); a pre-built image v0.2.3 exists; Xbox controller over Bluetooth; udev rule `SUBSYSTEM=="usb-serial", DRIVER=="ftdi_sio", ATTR{latency_timer}="1"`.
- Control loop: `control_freq=50` Hz, `action_scale=0.25`, `motor_targets = init_pos + action * 0.25`, 3-step action history, `pid=[30, 0, 0]` default in the walk script, head motors `kp=8`; logs "Policy control budget exceeded by …" when the loop overruns; optional `LowPassActionFilter` ([v2_rl_walk_mujoco.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/v2_rl_walk_mujoco.py)).
- Servo interface: `rustypot.feetech(usb_port, 1000000)` (1 Mbps), IDs 10–14 right leg, 20–24 left leg, 30–33 neck/head; `set_kps`/`set_kds` written to the servos; HWI defaults `kps = 32`, `kds = 0`, low-torque `kps = 2`; per-tick `write_goal_position`, `read_present_position`, `read_present_velocity` ([rustypot_position_hwi.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/rustypot_position_hwi.py)). rustypot 1.9.0 ships wheels for Windows/macOS/Linux x86-64/arm64/armv7, CPython 3.10–3.14 ([PyPI](https://pypi.org/project/rustypot/)).
- IMU: `adafruit_bno055.BNO055_I2C`, daemon thread, 50 Hz, quaternion out; comment `# TODO filter spikes` ([imu.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/imu.py)).
- `LowPassActionFilter(control_freq, cutoff_frequency=30.0)`: `alpha = (1/fc) / (1/f_ctrl + 1/fc)`, `y = alpha*y_prev + (1-alpha)*u` ([rl_utils.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/rl_utils.py)).

### 2.4 Time estimate for the RTX 3050 6 GB laptop

| | RTX 3090 (measured host) | RTX 3050 6 GB Laptop (ours) |
|---|---|---|
| CUDA cores | 10,496 ([TechPowerUp](https://www.techpowerup.com/271497/nvidia-geforce-rtx-3090-and-3080-specifications-leaked)) | 2,048, GA107, boost ~1,375 MHz (1,057–1,740 MHz depending on TGP) ([TechPowerUp DB](https://www.techpowerup.com/gpu-specs/?q=3050), [TechPowerUp news](https://www.techpowerup.com/280451/nvidia-geforce-rtx-3050-3050-ti-laptop-gpu-specifications-performance-leaked)) |
| FP32 | ~35.6 TFLOPS | ~5.6–7.1 TFLOPS (2048 × 2 × clock) |
| Memory BW | 936 GB/s | 168 GB/s (96-bit GDDR6) ([videocardz.net](https://videocardz.net/nvidia-geforce-rtx-3050-6gb-mobile)) |
| Ratio | 1 | **≈ 1/5 – 1/6.4** |

68,700 steps/s ÷ (5 … 6.4) ≈ **10.7–13.7 k steps/s**, minus laptop thermal throttling → call it **9–14 k steps/s**. Then: 150 M steps ≈ 3–4.6 h; 300 M steps ≈ 6–9 h; plus a few minutes of XLA JIT per run. **[ESTIMATE]** — the scaling assumes MJX throughput scales with GPU compute, that 8192 envs fit in 6 GB (Open Duck has only 14 DoF and 4 foot contacts, so the MJX state is small, but unmeasured) and that the CPU-side Brax PPO update does not dominate. Measure with a 2 M-step smoke run first; if OOM, halve `num_envs` (4096 keeps batch math intact) at roughly proportional cost in wall-clock.

---

## 3. Recommended stack for this machine (and exact install)

### 3.1 Why WSL2 + JAX-CUDA, not native Windows

- JAX platform table: **Windows x86_64 → NVIDIA GPU "No"; Windows WSL2 → NVIDIA GPU "Experimental"**; "these pip installations do not work with Windows" ([docs.jax.dev installation](https://docs.jax.dev/en/latest/installation.html)). So MJX/Brax/Playground on GPU is WSL2-only in 2026.
- placo (reference motions) has no Windows wheels ([PyPI](https://pypi.org/project/placo/)).
- CUDA on WSL2 needs only the Windows driver: "R495 and later windows will have CUDA support for WSL 2", "This is the only driver you need to install. Do not install any Linux display driver in WSL", WSL kernel >= 4.19.121 (5.10.16.3+ recommended); if you do install a toolkit inside WSL use the "WSL-Ubuntu" package and only `cuda-toolkit-12-x`, never `cuda`/`cuda-drivers`; limitations: no full Unified Memory, limited pinned memory ([CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)).
- Driver 546.18 check: CUDA 12.3 Update 1 requires Windows >= 546.12 ([CUDA release notes table](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)), so 546.18 exposes CUDA 12.3.x. Minor-version compatibility covers the whole CUDA 12.x family for drivers ">= 525" ("Driver Range >= 525 to < 580" per the same page). JAX: CUDA-12 wheels "built with CUDA 12.3, compatible with CUDA >= 12.1", cuDNN >= 9.10.2, "driver version must be >= 525 for CUDA 12 on Linux, and >= 580 for CUDA 13" ([JAX install](https://docs.jax.dev/en/latest/installation.html), [changelog 0.11.2 / 0.6.0](https://docs.jax.dev/en/latest/changelog.html)). **→ `jax[cuda12]` works with 546.18; `jax[cuda13]` does not.**
- Known nuisance with an old driver: "The NVIDIA driver's CUDA version is 12.x which is older than the ptxas CUDA version … XLA is disabling parallel compilation, which may slow down compilation" ([jax discussion #20156](https://github.com/jax-ml/jax/discussions/20156)) — harmless, only slower JIT. Fix = update the driver.
- Native-Windows alternatives exist but none reproduces Open Duck's pipeline: Genesis + rsl_rl (PyTorch, Windows OK, §1.3); Newton/Warp (Windows OK, driver >= 545, §1.6) + mujoco_warp (Windows status unclear) + rsl_rl; plain CPU MuJoCo + PyTorch PPO (MJX on CPU is ~10× slower than MuJoCo; a vectorised CPU MuJoCo env at 50 Hz control / 2 ms physics would need a hand-written multiprocess env — throughput on this i5 **[UNMEASURED]**).

### 3.2 Install steps (Windows side)

```powershell
# PowerShell as Administrator
wsl --update
wsl --list --online
wsl --install -d Ubuntu-24.04          # ([learn.microsoft.com/…/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install))
wsl --set-default-version 2
wsl --set-default Ubuntu-24.04
```
Optional `%UserProfile%\.wslconfig` (defaults: memory = 50 % of Windows RAM, swap = 25 %, all logical processors) ([wsl-config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config)):
```ini
[wsl2]
memory=16GB
processors=8
swap=8GB
```
Then `wsl --shutdown` and reopen. Enable systemd in `/etc/wsl.conf` (`[boot] systemd=true`) if you plan to run ROS 2 daemons.

**Update the NVIDIA driver first** (GeForce Game Ready, any build >= 580.88 — that is the version Isaac Lab recommends on Windows and what one Isaac user had to downgrade *to* from 591.86 ([tech-multiverse](https://tech-multiverse.com/projects/yes-you-can-train-robots-in-isaac-lab-on-an-rtx-4060/))). Not strictly required for `jax[cuda12]`, but it removes the ptxas warning and future-proofs Warp/JAX-CUDA-13.

### 3.3 Install steps (inside Ubuntu-24.04)

```bash
nvidia-smi                                   # must list the GPU and the Windows driver; if not, WSL GPU passthrough is broken
sudo apt update && sudo apt install -y git git-lfs build-essential curl
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc

# --- training repo (fork it first, then clone your fork) ---
git clone https://github.com/apirrone/Open_Duck_Playground && cd Open_Duck_Playground
uv venv --python 3.12 && source .venv/bin/activate      # JAX 0.11 dropped Python 3.11; Windows' 3.13 is irrelevant here
# Known-good pins from the RTX 3090 run (jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5):
uv pip install "jax[cuda12]==0.6.2" "mujoco==3.3.4" "mujoco-mjx==3.3.4" "playground==0.0.5"
uv pip install -e .                                      # pulls tensorflow / tf2onnx / onnxruntime for export + mujoco_infer
python -c "import jax; print(jax.devices())"             # expect [CudaDevice(id=0)]

# --- reference motion generator (separate venv, placo is Linux-only) ---
cd ~ && git clone https://github.com/apirrone/Open_Duck_reference_motion_generator && cd Open_Duck_reference_motion_generator
git lfs pull
uv run scripts/auto_waddle.py -j8 --duck open_duck_mini_v2 --sweep --output_dir recordings
uv run scripts/fit_poly.py --ref_motion recordings/
cp polynomial_coefficients.pkl ~/Open_Duck_Playground/playground/open_duck_mini_v2/data/

# --- train ---
cd ~/Open_Duck_Playground
export XLA_PYTHON_CLIENT_MEM_FRACTION=0.85      # JAX pre-allocates 75 % by default; leave room for TF's exporter
export TF_FORCE_GPU_ALLOW_GROWTH=true           # TF grabbed 1.5 GB on someone's GPU during ONNX export (Open_Duck_Playground issue #19)
export JAX_DEFAULT_MATMUL_PRECISION=highest     # optional: Ampere TF32 reproducibility note in Playground README
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain_backlash --num_timesteps 2000000   # smoke test: fits? steps/s?
uv run playground/open_duck_mini_v2/runner.py --task flat_terrain_backlash --num_timesteps 150000000
uv run tensorboard --logdir=checkpoints
uv run playground/open_duck_mini_v2/mujoco_infer.py -o checkpoints/<stamp>_<step>.onnx
```
JAX memory flags: default "preallocate 75% of the total GPU memory"; `XLA_PYTHON_CLIENT_PREALLOCATE=false`, `XLA_PYTHON_CLIENT_MEM_FRACTION=.XX`, `XLA_PYTHON_CLIENT_ALLOCATOR=platform` ([docs.jax.dev gpu_memory_allocation](https://docs.jax.dev/en/latest/gpu_memory_allocation.html)). Alternative "latest" pin set that the same build log used for inference: `jax 0.11.1 / mujoco 3.12.0 / playground 0.2.0` — API drift between playground 0.0.5 and 0.2.0 is a real risk for the Open Duck fork (no lockfile), so try the old pins first.

Our own robot: copy `playground/open_duck_mini_v2/` → `playground/microduck/`, replace the MJCF (`xmls/`), joint/sensor names in `constants.py`, and the reward config in `joystick.py`, exactly as the README's "adding a new robot" section says; generate a `--duck microduck` config in the reference-motion generator (it needs the URDF + placo kinematics of our legs).

### 3.4 Disk / VRAM / pitfalls

- Disk: Ubuntu-24.04 WSL image ≈ 2 GB; JAX-CUDA pip wheels (cuBLAS, cuDNN, NCCL, nvcc) ≈ 3–4 GB; TensorFlow ≈ 1 GB; budget **~10 GB** on the drive holding `%LocalAppData%\wsl` **[approximate, my estimate]**. Isaac Sim would have needed 50 GB.
- VRAM: no published number for Open Duck at 8192 envs. Smoke-test; if OOM → `num_envs=4096`. Watch that TensorFlow (used only for export) does not also claim VRAM (issue #19 shows `Created device … GPU:0 with 1513 MB memory` on an RTX 5060 Ti, [issue](https://github.com/apirrone/Open_Duck_Playground/issues/19)).
- Old driver: ptxas-newer-than-driver warning → slower compile only. `jax[cuda13]` will refuse (needs >= 580).
- CPU: JAX now requires AVX2/FMA (Haswell+) — the i5-13420H is fine ([changelog](https://docs.jax.dev/en/latest/changelog.html)).
- WSL RAM: with 24 GB physical, WSL defaults to 12 GB; Brax PPO with 8192 envs and TensorBoard is fine there, but set `memory=16GB` if you also run the MuJoCo viewer.
- USB serial (Waveshare adapter) into WSL2 for `mujoco_infer`-style real-robot tests: install `usbipd-win` (`winget install --interactive --exact dorssel.usbipd-win`), then `usbipd list`, `usbipd bind --busid <id>` (admin), `usbipd attach --wsl --busid <id>`, verify with `lsusb` inside WSL ([learn.microsoft.com connect-usb](https://learn.microsoft.com/en-us/windows/wsl/connect-usb)). Otherwise drive servos from native Windows Python with rustypot (Windows wheels exist).
- Viewer / GUI: WSLg gives you OpenGL windows for `mujoco_infer.py`; performance is adequate for a 14-DoF model.

---

## 4. ROS 2 angle

- **Distro:** ROS 2 **Jazzy Jalisco** — LTS, released May 2024, supported until May 2029, Tier-1 on Ubuntu Noble 24.04 (amd64, arm64) and Windows 10 (VS2019); Python >= 3.8. Kilted Kaiju (May 2025–Nov 2026) is non-LTS and also targets Noble ([REP-2000](https://raw.githubusercontent.com/ros-infrastructure/rep/master/rep-2000.rst)). Jazzy on Ubuntu-24.04 inside WSL2 is the right pick; Humble (22.04) would force a second distro.
- **Install (Ubuntu 24.04):** ([ros2_documentation jazzy: Ubuntu-Install-Debs + _Apt-Repositories](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst))
```bash
sudo apt install software-properties-common && sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update && sudo apt install ros-dev-tools ros-jazzy-desktop   # or ros-jazzy-ros-base on the robot
source /opt/ros/jazzy/setup.bash
```
- **Is ROS needed?** No. The Open Duck runtime is a single Python process: rustypot → servos, adafruit_bno055 → IMU, onnxruntime → policy, pygame/Xbox → commands. The policy loop is 50 Hz on a Pi Zero 2W (512 MB RAM). Ubuntu (26.04 LTS page) lists the Pi Zero 2 W as supported ([ubuntu.com/download/raspberry-pi](https://ubuntu.com/download/raspberry-pi)), but running the ROS 2 graph + DDS on 512 MB alongside a 50 Hz servo loop is not something anyone documents — if you want ROS on the robot, plan a Pi 5 (Open Duck runtime already supports Pi 5) **[my judgement]**.
- **Minimal ROS 2 package plan (if you want "ROS" for visualisation, logging and future autonomy):**
  1. `microduck_description` — URDF/xacro exported from SolidWorks (SW2URDF) + STL meshes; launch `robot_state_publisher` + `joint_state_publisher_gui`; RViz config. Also the MJCF for training is derived from the same URDF (MuJoCo's `compile` of URDF, then hand-add the `sts3215` actuator class from §5).
  2. `microduck_hw` — either the ros2_control hardware interface `feetech_ros2_driver` (released for Humble, Jazzy, Kilted, Lyrical, Rolling; repo `ros-physical-ai/feetech_ros2_driver`) ([index.ros.org](https://index.ros.org/p/feetech_ros2_driver/)), or a 50 Hz Python node wrapping rustypot that publishes `sensor_msgs/JointState` and subscribes to `std_msgs/Float64MultiArray` position targets (+ kp/kd service). Alternative: `Ar-Ray-code/feetech_scs_ros2_driver`.
  3. `microduck_imu` — BNO055 → `sensor_msgs/Imu` (any I2C BNO055 ROS 2 driver; verify Jazzy availability before committing **[not verified]**).
  4. `microduck_policy` — onnxruntime node: subscribes IMU + joint states + `geometry_msgs/Twist` (`cmd_vel`), keeps the same 3-action history / phase clock as `v2_rl_walk_mujoco.py`, publishes targets at exactly 50 Hz using a monotonic timer; parameters `action_scale=0.25`, `kp=32`, `kd=0`.
  5. `microduck_teleop` — `joy` → `teleop_twist_joy` with the same velocity limits as training (±0.15 m/s x, ±0.2 m/s y, ±1 rad/s yaw).
  6. `microduck_bringup` — launch files for sim (MuJoCo viewer replaying the ONNX) and real.
  DDS/latency note: keep hardware I/O and the policy in one process (or use intra-process comms) — the Open Duck loop already logs budget overruns at 50 Hz on the Pi.
- Isaac Sim's ROS 2 bridge is irrelevant here (Isaac is out); MuJoCo has no official ROS 2 bridge, so the sim-side "ROS" is limited to replaying policies in the MuJoCo viewer.

---

## 5. Sim-to-real checklist for an STS3215-actuated biped

### 5.1 Actuator model (what Open Duck ships)

| Item | Sim (MJCF) | Real (runtime) | Source |
|---|---|---|---|
| Actuator type | MuJoCo `position` actuator, class `sts3215`, `kp="13.37"` (plain model) / `kp="17.11"` (backlash model), `kv="0.0"`, `forcerange="-3.23 3.23"` N·m, `inheritrange="1"` | Servo internal position loop; P register = 32 (HWI default) / 30 (walk script default), D = 0, head joints P = 8 | [open_duck_mini_v2.xml](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml), [open_duck_mini_v2_backlash.xml](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2_backlash.xml), [rustypot_position_hwi.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/rustypot_position_hwi.py), [v2_rl_walk_mujoco.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/v2_rl_walk_mujoco.py) |
| Joint dynamics (class `sts3215`) | `damping="0.56"`, `frictionloss="0.068"`, `armature="0.027"`; base class adds `frictionloss="0.1"`, `armature="0.005"` (which one wins depends on class nesting — read the XML) | — | same XML |
| Solver | `iterations="1"`, `ls_iterations="5"`, `eulerdamp` disabled, timestep 0.002 s, control 0.02 s | 50 Hz loop | XML + joystick.py |
| Velocity limit | targets rate-limited: `clip(target, prev ± 5.24 rad/s × dt)` | STS3215 12 V no-load "0.222 sec/60° (45 RPM)" = 4.71 rad/s ([Waveshare wiki](https://www.waveshare.com/wiki/ST3215_Servo)); 7.4 V variant speed **[UNVERIFIED — not on any page I could fetch]** | joystick.py |
| Torque limit | ±3.23 N·m (= 32.9 kg·cm) | 7.4 V STS3215: stall 19.5 kg·cm (1.91 N·m), rated 5 kg·cm ([Seeed](https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html)); 12 V variant: stall 30 kg·cm, rated 10 kg·cm, stall current 2.7 A ([Feetech](https://www.feetechrc.com/525603.html)); measured ~35 kg·cm stall at 12 V ([Robo9 test](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/)) | — |
| Backlash | passive `*_backlash` joint per actuated joint: `range ±0.008727 rad (±0.5°)`, `damping 0.01`, `armature 0.01`, `frictionloss 0` | measured backlash **~0.87°** vs datasheet <= 0.5°; repeatability ~0.17° (≈2 encoder counts) ([Robo9](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/)) | backlash XML |
| Encoder | — | 12-bit magnetic, 4096 counts/turn (0.088°), 1 Mbps half-duplex TTL ([Feetech](https://www.feetechrc.com/525603.html), [Waveshare](https://www.waveshare.com/wiki/ST3215_Servo)) | — |
| Action → target | `target = default_pose + 0.25 × action`, actions clipped by joint range × 0.95 | identical (`init_pos + action*0.25`), optional 30 Hz first-order low-pass | joystick.py, rl_utils.py |

**Actions for the microduck:**
1. Set `forcerange` to the servo you actually buy: ~1.9 N·m for the 7.4 V/2S variant, ~2.9 N·m for 12 V/3S. Open Duck's ±3.23 N·m is above the 7.4 V stall — a policy that leans on that margin will stall real servos. **[Open question — see §6]**
2. Keep `kp` in sim as an identified quantity, not a datasheet number: Open Duck's 13.37/17.11 N·m/rad ↔ servo P=32 mapping is not documented anywhere I found; re-identify on our leg (step response with the real servo and a known inertia; fit MuJoCo `kp`, `damping`, `frictionloss`, `armature`).
3. Widen the backlash range to at least ±0.9° (measured) and randomise it.
4. Keep the target-rate limiter (`max_motor_velocity`) but set it from the measured no-load speed at the voltage you run.
5. Thermal: at 12 V a static 15 kg·cm load reached 48 °C and stabilised; continuous oscillation hit 60 °C at 50 min and 71 °C at ~110 min, where "the motor exhibits issues"; a 20 kg·cm dynamic load triggered overload protection after a few cycles ([Robo9](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/)). Keep the `torques` penalty and log servo temperature/current (the STS3215 reports both) during real walks.

### 5.2 Latency and timing

- Sim: policy acts every 20 ms on a state that is exactly 20 ms old (no extra delay in `joystick.py`). Real: 1 Mbps sync-read of 14 positions + 14 velocities + sync-write per tick over FTDI USB serial (`latency_timer=1`), BNO055 over I2C at 50 Hz on a separate thread with a 1-deep queue, onnxruntime inference, Python overhead — the runtime prints "Policy control budget exceeded by …" when > 20 ms ([v2_rl_walk_mujoco.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/v2_rl_walk_mujoco.py), [README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/README.md)).
- Checklist: measure the real loop time on the Pi with the full sensor set; if it is not comfortably < 20 ms, add a 1-step action delay (randomised 0–1 steps) in the env or drop to 40 Hz in both sim and real; use the 3-action history already in the observation (it lets the policy infer delay).
- Set the FTDI `latency_timer` udev rule (above); with the Waveshare Bus Servo Adapter (A) confirm it enumerates as `ftdi_sio` / `ttyACM0` (runtime default port is `/dev/ttyACM0`).

### 5.3 IMU

- Sim observation noise (uniform scales): `gyro=0.1`, `accelerometer=0.05`, `gravity=0.1`, joint pos `hip 0.03 / knee 0.05 / ankle 0.08` rad, `joint_vel=2.5` rad/s ([joystick.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/joystick.py)).
- Real: BNO055 fusion quaternion, spikes not filtered (`TODO filter spikes`), pitch bias and `upside_down` mounting handled in config; calibrate and run `raw_imu.py` before every session ([imu.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/imu.py)).
- Checklist: mount orientation identical to the MJCF `<site>` used for the `gyro`/`accelerometer` sensors; randomise IMU mounting tilt (±2–3°) and add a bias term in sim; clip real gyro spikes; verify sign conventions by tilting the robot and comparing `mujoco_infer.py` vs real observation vectors side by side (the fastest way to catch frame errors).

### 5.4 Domain randomisation (Open Duck `common/randomize.py`)

Floor friction U(0.5, 1.0); `dof_frictionloss × U(0.9, 1.1)`; `dof_armature × U(1.0, 1.05)`; CoM offset U(−0.05, 0.05) m per axis; every body mass × U(0.9, 1.1); torso mass + U(−0.1, 0.1) kg; initial joint pos + U(−0.03, 0.03) rad; actuator `kp × U(0.9, 1.1)` with the bias term (`kd`) kept proportional; comments show earlier, wider ranges (friction 0.4–1.0, torso ±0.2 kg, kp 0.8–1.2) ([randomize.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/randomize.py)). Plus pushes (every 5–10 s, 0.1–1.0 magnitude) and the `flat_terrain_backlash` / `rough_terrain_backlash` scenes.

Reward weights: `tracking_lin_vel 2.5`, `tracking_ang_vel 6.0`, `torques −1e-3`, `action_rate −0.5`, `stand_still −0.2`, `alive 20.0`, `imitation 1.0`, `tracking_sigma 0.01` ([joystick.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/joystick.py)).

**Add for the microduck:** PETG parts are heavier and stiffer than PLA — re-export masses/inertias from SolidWorks with PETG density, then keep the ±10 % mass randomisation; randomise backlash range (0.3–1.0°), a 0–1 step action delay, foot friction down to 0.4 (PETG feet on tile), and battery-voltage-dependent `kp`/`forcerange` (2S sags from 8.4 to 6.4 V).

### 5.5 Deployment loop

1. `mujoco_infer.py -o model.onnx` in sim (WSLg window) — verify the ONNX reproduces the JAX policy.
2. `check_motors.py` → `find_soft_offsets.py` → `duck_config.json` (offsets, IMU orientation).
3. Robot suspended: run the walk script, compare obs vectors and target trajectories against sim logs.
4. On the ground, low speed commands first; log servo temp/current/voltage; stop at 60 °C.

---

## 6. Open questions

1. **7.4 V STS3215 no-load speed** — needed for `max_motor_velocity`; only the 12 V figure (0.222 s/60°) is published on pages I could reach.
2. **VRAM at 8192 envs** for a 14-DoF MJX model on 6 GB — unmeasured; fallback 4096.
3. **Real throughput on the 3050** — the 9–14 k steps/s figure is a compute-ratio extrapolation from one RTX 3090 data point.
4. **Which STS3215 variant / bus voltage the microduck uses** (7.4 V/2S like Open Duck vs 12 V/3S) — drives `forcerange`, speed limit and BOM.
5. **Servo P-register ↔ MuJoCo `kp` mapping** (32 ↔ 13.37/17.11 N·m/rad) — undocumented; must be re-identified for our leg geometry.
6. **Version drift** — `Open_Duck_Playground` has no lockfile; will it still import against `playground 0.2.0` / `jax 0.11.x`? Start with the 0.0.5/0.6.2 pins.
7. **mujoco_warp on native Windows** — issue #8 closed silently; unknown whether a Windows-native Warp + rsl_rl path is viable today.
8. **ROS host** — Pi Zero 2W (Open Duck) cannot reasonably host ROS 2; Pi 5 adds cost and mass.
9. **Driver update side-effects** — confirm the laptop OEM ships a >= 580.88 Game Ready driver for this RTX 3050 6 GB SKU.
10. **Isaac Sim 4.5 page** — the official 4.5.0 requirements URL returned 404 to my fetcher; the RTX 3070 / 8 GB figure is corroborated by NVIDIA staff posts but should be re-checked in a browser.

---

## Sources (all URLs used)

- Isaac Sim requirements: [latest (6.0)](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), [5.1.0](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html), [4.5.0 (404 to fetcher)](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/requirements.html); [Isaac Lab main](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html), [Isaac Lab v2.1.0](https://isaac-sim.github.io/IsaacLab/v2.1.0/source/setup/installation/index.html); [IsaacSim discussion #423](https://github.com/isaac-sim/IsaacSim/discussions/423); [forum 305727](https://forums.developer.nvidia.com/t/gpu-requirement/305727); [forum 373600](https://forums.developer.nvidia.com/t/is-8gb-vram-enough-for-basic-isaac-sim-5-1-usage/373600); [forum 278252 (WSL2)](https://forums.developer.nvidia.com/t/isaac-sim-x86-64-headless-docker-wsl2-support/278252); [Isaac Sim 5.1 ROS install](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/install_ros.html); [tech-multiverse RTX 4060](https://tech-multiverse.com/projects/yes-you-can-train-robots-in-isaac-lab-on-an-rtx-4060/)
- Isaac Gym: [developer.nvidia.com/isaac-gym](https://developer.nvidia.com/isaac-gym), [docs mirror install](https://docs.robotsfan.com/isaacgym/install.html), [jmcoholich/isaacgym](https://github.com/jmcoholich/isaacgym), [forum 205734](https://forums.developer.nvidia.com/t/gpu-memory-requirement-for-running-isaac-gym/205734)
- Genesis: [GitHub](https://github.com/Genesis-Embodied-AI/Genesis), [README v0.2.1](https://raw.githubusercontent.com/Genesis-Embodied-AI/Genesis/v0.2.1/README.md), [install docs](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html), [locomotion v0.4.3](https://genesis-world.readthedocs.io/en/v0.4.3/user_guide/getting_started/locomotion.html)
- MuJoCo/MJX/Playground/Brax/Warp: [mujoco_playground](https://github.com/google-deepmind/mujoco_playground), [Playground paper](https://arxiv.org/html/2502.08844), [locomotion_params.py](https://raw.githubusercontent.com/google-deepmind/mujoco_playground/main/mujoco_playground/config/locomotion_params.py), [playground discussion #197](https://github.com/google-deepmind/mujoco_playground/discussions/197), [MJX docs](https://mujoco.readthedocs.io/en/stable/mjx.html), [MJWarp docs](https://mujoco.readthedocs.io/en/latest/mjwarp/), [mujoco_warp](https://github.com/google-deepmind/mujoco_warp), [mujoco_warp issue #8](https://github.com/google-deepmind/mujoco_warp/issues/8), [brax](https://github.com/google/brax), [Warp install](https://nvidia.github.io/warp/installation.html), [Newton README](https://raw.githubusercontent.com/newton-physics/newton/main/README.md), [mjlab](https://github.com/mujocolab/mjlab), [rsl_rl](https://github.com/leggedrobotics/rsl_rl), [PyTorch cu126 wheels](https://download.pytorch.org/whl/cu126/torch/)
- JAX / CUDA / WSL: [JAX install](https://docs.jax.dev/en/latest/installation.html), [JAX changelog](https://docs.jax.dev/en/latest/changelog.html), [JAX GPU memory](https://docs.jax.dev/en/latest/gpu_memory_allocation.html), [jax discussion #20156](https://github.com/jax-ml/jax/discussions/20156), [CUDA on WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html), [CUDA release notes (driver table)](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html), [WSL install](https://learn.microsoft.com/en-us/windows/wsl/install), [.wslconfig](https://learn.microsoft.com/en-us/windows/wsl/wsl-config), [usbipd](https://learn.microsoft.com/en-us/windows/wsl/connect-usb)
- Open Duck: [Open_Duck_Mini README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/README.md), [BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing), [Open_Duck_Playground](https://github.com/apirrone/Open_Duck_Playground), [pyproject](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/pyproject.toml), [joystick.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/joystick.py), [randomize.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/randomize.py), [common/runner.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/runner.py), [runner.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/runner.py), [constants.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/constants.py), [open_duck_mini_v2.xml](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml), [backlash xml](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2_backlash.xml), [export_onnx.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/export_onnx.py), [issue #19](https://github.com/apirrone/Open_Duck_Playground/issues/19), [reference motion generator](https://github.com/apirrone/Open_Duck_reference_motion_generator), [Runtime README v2](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/README.md), [v2_rl_walk_mujoco.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/v2_rl_walk_mujoco.py), [rustypot_position_hwi.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/rustypot_position_hwi.py), [imu.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/imu.py), [rl_utils.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/rl_utils.py), [soyeon24 build log (RTX 3090 timing)](https://github.com/soyeon24/open-duck-mini-v2-build), [dev.to/frankfu](https://dev.to/frankfu/understanding-reinforcement-learning-through-openduck-1if0), [PyPI rustypot](https://pypi.org/project/rustypot/), [PyPI placo](https://pypi.org/project/placo/)
- STS3215: [Feetech 12 V page](https://www.feetechrc.com/525603.html), [Waveshare ST3215 wiki](https://www.waveshare.com/wiki/ST3215_Servo), [Seeed 7.4 V](https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html), [Robo9 backlash/torque test](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/), [feetech_ros2_driver](https://index.ros.org/p/feetech_ros2_driver/), [feetech_scs_ros2_driver](https://github.com/Ar-Ray-code/feetech_scs_ros2_driver)
- ROS 2: [REP-2000](https://raw.githubusercontent.com/ros-infrastructure/rep/master/rep-2000.rst), [Jazzy Ubuntu install (docs source)](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst), [Ubuntu on Raspberry Pi](https://ubuntu.com/download/raspberry-pi)
- GPUs: [RTX 3090 specs (TechPowerUp)](https://www.techpowerup.com/271497/nvidia-geforce-rtx-3090-and-3080-specifications-leaked), [RTX 3050 Laptop specs (TechPowerUp)](https://www.techpowerup.com/280451/nvidia-geforce-rtx-3050-3050-ti-laptop-gpu-specifications-performance-leaked), [RTX 3050 6 GB Mobile (videocardz.net)](https://videocardz.net/nvidia-geforce-rtx-3050-6gb-mobile)

---

## Critic additions (2026-09-26, from `07_critic_gaps.md`)

1. **Open question 1 (7.4 V no-load speed) is answered in `03_sts3215.md` §2.1** from the Feetech ST-3215-C001 datasheet: **0.192 s/60 deg = 52 RPM = 5.45 rad/s at 7.4 V**; 0.238 s/60 deg = 4.40 rad/s at 6 V; 12 V C018 0.222 s/60 deg = 4.71 rad/s. BAM's identified `max_velocity` is 5.07-5.30 rad/s (02 §2.4), and Open Duck's 5.24 rad/s limiter is exactly the firmware speed register ceiling 3400 steps/s x 2 pi / 4096 = 5.215 rad/s. **But** two 2026 builders measured only ~2.7 rad/s on retail C001 units ([Open_Duck_Mini issue #48](https://github.com/apirrone/Open_Duck_Mini/issues/48)). Action: measure no-load speed on the first two servos at 7.4 V and 8.4 V and set `max_motor_velocity` to the measured value. Note also (02 §6.5) that the runtime has the 5.24 rad/s clip **commented out**, so the real robot is limited only by the physical servo — keep the limiter in sim at the measured value.
2. **Open question 5 (P register <-> MuJoCo kp) is documented, not derived:** maintainer in [Open_Duck_Mini issue #20](https://github.com/apirrone/Open_Duck_Mini/issues/20): "the 17.8 in mujoco corresponds to 32 in the motors firmware units" (~0.556 N.m/rad per P unit, critic's arithmetic). The shipped Playground XML uses kp 13.37 (plain) / 17.11 (backlash); `joints_properties.xml` uses 17.8. Still re-identify on our leg (§5.1 action 2) because the mapping depends on the identified friction/armature.
3. **`forcerange` decision (open question 4 / §5.1 action 1):** for C001 @ 2S set **+/-1.9 N.m** and retrain; soyeon24's fork doubled the real-limit walking speed (0.057 -> 0.130 m/s) by retraining at +/-1.86 (02 §2.4). Do not reuse the stock +/-3.23 XML.
4. **Pin set (open question 6):** two community pin sets exist — `jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5` (this file, soyeon24's full 300 M-step 3090 run) and `jax[cuda12]==0.8.0 + playground==0.0.5` (02 §6.4, [Playground issue #25](https://github.com/apirrone/Open_Duck_Playground/issues/25), fixes the `mujoco_playground._src.collision` import). The JAX install page still ships CUDA-12 wheels for driver >= 525 and says only "at some point in the future we will drop CUDA 12 support" ([docs.jax.dev](https://docs.jax.dev/en/latest/installation.html)), so both work with driver 546.18. Start with the soyeon24 triple (only one with a documented complete training run); fall back to 0.8.0 on the import error; commit a `uv.lock`.
5. **VRAM guesses differ across files** (02 §8: mem fraction 0.6, envs 2048-4096; this file: 0.85, 8192 -> 4096). Both are unmeasured; the 2 M-step smoke test decides. Run the TensorFlow ONNX exporter on CPU (`CUDA_VISIBLE_DEVICES=""` for the export step, or `TF_FORCE_GPU_ALLOW_GROWTH=true`).
6. **Foot-contact bits are not optional** (contradicts 06 §6): the 101-dim observation includes 2 foot contacts (§2.2, 02 §6.3). Either fit the SS-10 switches (budgeted, Rs 788) or retrain with a 99-dim observation.
7. **IMU:** 06 recommends a BNO085, but the runtime uses `adafruit_bno055` with raw gyro + accel; a BNO085 needs `adafruit_bno08x` and re-checked axis conventions. Phase 1: BNO055.
8. **SolidWorks -> URDF/MJCF path (§4 item 1):** the latest official SolidWorks URDF exporter release is **v1.6.1, stated compatibility "SolidWorks 2021"** (v1.6.0: 2020) ([releases page](https://github.com/ros/solidworks_urdf_exporter/releases)); the user's SolidWorks version is unknown. Fallback that reproduces Open Duck's pipeline exactly: STEP -> free Onshape document -> `onshape-to-robot` -> MJCF (02 §6.1). Phase-1 recommendation: keep the Open Duck MJCF and only overwrite masses/inertias with SolidWorks PETG values (`sim2real.md` already overrides masses with slicer estimates).
9. **Answer for the user's "ROS or even Isaac" request, stated plainly:** Isaac Sim/Lab cannot run on this laptop (6 GB VRAM < 8 GB for 4.5, < 16 GB for 5.x/6.0; driver 546.18 < 580.88; WSL2 unsupported). ROS 2 Jazzy is optional and desktop/WSL2-only (RViz, logging); the robot runs the plain-Python Open Duck runtime.
