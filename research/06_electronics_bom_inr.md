# 06 — Microduck electronics + hardware BOM (INR)

**Scope:** priced, India-sourced bill of materials for a BDX-style "microduck" biped built around Feetech STS3215 serial-bus servos only, printed in PETG on a Bambu Lab P1S, with a walking policy run on-board at 50 Hz.
**Reference design:** Open Duck Mini v2 (apirrone) — 14× STS3215 7.4 V, Raspberry Pi Zero 2 W, Waveshare Bus Servo Adapter (A), BNO055, 2×18650 (2S) + BMS + 5 V UBEC, MAX98357A amp, target BOM < US$400 ([README](https://github.com/apirrone/Open_Duck_Mini/blob/v2/README.md), [BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing), [assembly guide](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md)). The v2 BOM sheet totals €398 (€331 "estimated lowest") for the base robot and €432 with the "expression package" (speaker, LEDs, camera).
**Prices checked:** 26 Sep 2026. All INR figures are **inclusive of 18 % GST** unless marked *ex-GST*. electronicscomp.com lists prices ex-GST; where I used them I show the GST-inclusive figure and mark the source. robu.in ships free above ₹999.
**FX used for import comparisons:** ~₹96 / USD (USD/INR 95.96 on 25 Sep 2026, [tradingeconomics](https://tradingeconomics.com/india/currency)).
**Convention:** "verified" = price read from the vendor page/search listing on the date above; "est." = my estimate, clearly labelled; "unverified" = a number I could not confirm.

---

## 0. Headline numbers

| Configuration | Servos | Compute | Total (parts only) | Margin vs ₹50,000 |
|---|---|---|---|---|
| **Minimum viable** | 14× ST3215 7.4 V (robu, ₹2,159) | Pi Zero 2 W (₹2,079, **out of stock everywhere**) | **₹41,787** | +₹8,213 |
| Minimum viable, in-stock compute | same | Pi 3 A+ (₹3,211) | **₹42,919** | +₹7,081 |
| **Recommended** | 14× ST3215 7.4 V | Pi 3 A+ (+ BNO085, 4200 mAh, audio, eyes, foot switches, full insert kit) | **₹47,723** | +₹2,277 |
| **Deluxe** | 16× ST3215 12 V (evelta C018, ₹2,419) | Pi 5 4 GB (₹11,200) + Camera 3 Wide + HAT (A) + 3S | **₹72,446** | **−₹22,446 (over budget)** |

Tools the user may lack (balance charger ₹2,079, heat-set tip ~₹500 unverified, bench 12 V PSU ₹425) add ₹2.5–3.0 k on top.

**Three findings that drive the budget:**
1. **Servos are 63–75 % of every total.** The cheapest verified in-stock STS3215 in India is the Waveshare-branded ST3215 7.4 V at **₹2,159** on robu.in; Feetech-branded 7.4 V at evelta is ₹2,224 (80 in stock). 12 V units cost ₹2,358–2,650. Importing from AliExpress/Seeed does **not** save money once India's 40.4 % duty stack is applied (see §1.3).
2. **Raspberry Pi Zero 2 W is unobtainable in India right now** (all five vendors checked are out of stock; fabtolab shows "expected December 2027"; global substrate shortage). Pi 3 A+ (₹3,211, in stock) is the practical stand-in.
3. **Pi 5 pricing has roughly doubled in India in 2026** (Pi 5 4 GB ₹11,200–14,181 vs ₹5,500–6,200 quoted in Feb 2026 guides) because of the LPDDR4 price rises Raspberry Pi announced on 2 Feb 2026 and again on 1 Apr 2026. A Pi 5 build cannot fit in ₹50 k with 14+ servos.

---

## 1. Servos — Feetech STS3215 (both voltage variants)

Electrical facts used later: operating voltage 6–12.6 V (12 V variant) / 4–7.4 V (7.4 V variant); stall current **2.7 A @ 12 V, 2.5 A @ 7.4 V** ([Waveshare product page](https://www.waveshare.com/st3215-servo.htm)); no-load current 200 mA, connector **5264 / 2.54 mm 3-pin**, 45.2 × 35 × 24.7 mm ([Waveshare wiki](https://www.waveshare.com/wiki/ST3215_Servo)); idle (stopped) current 21 mA and no-load 150 mA @ 6 V ([Feetech datasheet, core-electronics mirror](https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf)); weight 55 ± 1 g, 25T spline, ships with a 15 cm cable ([feetechrc.com](https://www.feetechrc.com/525603.html)). Torque: 19.5 kg·cm @ 7.4 V (C001, 1/345), 30 kg·cm @ 12 V (C018, 1/345).

### 1.1 Indian vendor prices, per servo

| Variant | Vendor | Unit price ₹ (incl. GST) | Stock (26 Sep 2026) | URL | Note |
|---|---|---|---|---|---|
| **7.4 V 19.5 kg·cm** (Waveshare ST3215) | robu.in | **2,159** | In stock | https://robu.in/?s=ST3215+19.5kg&post_type=product (SKU R258500) | Cheapest verified. Same Feetech servo, Waveshare packaging. |
| 7.4 V 19 kg 1/345 (Feetech ST3215) | evelta.com | 2,224.30 (₹1,885 ex-GST) | 80 in stock, ships Mumbai | https://evelta.com/sts3215-7-4v-19kg-dual-axis-ttl-string-servo-motor/ | Feetech-branded; bulk quote available. |
| 7.4 V 1/147 (STS3215-C046) | evelta.com | 2,224.30 | listed | https://evelta.com/feetech/ | Faster/lower-torque ratio — not for legs. |
| **12 V 30 kg·cm** (Waveshare 30KG) | electronicscomp.com | 1,715 *ex-GST* → ≈ 2,024 incl. | listing seen on search page; product page 404 on check | https://www.electronicscomp.com/index.php?route=product/search&search=bus%20servo | **Unverified** — confirm before relying on it. |
| 12 V 30 kg·cm (Waveshare ST3215) | theengineerstore.in | 2,358 | 3–5 day dispatch | https://www.theengineerstore.in/products/waveshare-30kg-serial-bus-servo | |
| 12 V 30 kg·cm (Feetech ST3215-C018) | evelta.com | 2,419 (₹2,050 ex-GST) | listed | https://evelta.com/feetech/ | Feetech-branded. |
| 12 V 30 kg·cm (Waveshare 30KG) | robu.in | 2,599 | In stock | https://robu.in/product/waveshare-30kg-serial-bus-servo/ | |
| 12 V 30 kg·cm | thinkrobotics.com | 2,649.99 | 2–4 weeks | https://thinkrobotics.com/products/st3215-series-serial-bus-servo | |

14 servos: 7.4 V = ₹30,226 (robu) / ₹31,140 (evelta). 12 V = ₹33,012 (theengineerstore) / ₹33,866 (evelta) / ₹36,386 (robu). 16 servos add ₹4,318 (7.4 V) or ₹4,838 (12 V evelta).

### 1.2 LeRobot SO-101 / SO-ARM101 kits as a servo source

| Kit | Vendor | Price ₹ | Contents | Effective ₹/servo | Verdict |
|---|---|---|---|---|---|
| ThinkRobotics LeRobot SO-101 (leader + follower) | thinkrobotics.com | **27,999.99**, in stock | 12× STS3215: follower 6× **12 V 1/345**; leader 6× **7.4 V mixed 1/191, 1/345, 1/147**; 2 driver boards; 5 V 6 A + 12 V 7.5 A PSUs; 4 clamps; printed parts | ₹2,333 before crediting boards/PSUs | Not a clean source of 14 identical leg servos (only 6 are 12 V 1/345; leader servos have wrong ratios). Worth it only if you also want the arm. https://thinkrobotics.com/products/so-arm101-hugging-face-lerobot |
| Seeed SO-ARM101 Pro Servo Motor Kit (no prints) | robu.in | 34,440, backorder | 12 servos + boards + cables | ₹2,870 | Worse than singles. https://robu.in/?s=STS3215&post_type=product |
| Seeed SO-ARM101 Pro Servo Motor Kit | seeedstudio.com | US$249.90 (≈ ₹24,000 + duty ≈ ₹33,700) | as above | ≈ ₹2,800 landed | Not cheaper. https://www.seeedstudio.com/SO-ARM101-Low-Cost-AI-Arm-Kit-p-6426.html |

### 1.3 Import (AliExpress / Seeed / eBay) vs local — duty stack

India duty on servo motors, HSN 85015190: BCD 15 % + AIDC (15 % of BCD) + SWS (10 % of BCD+AIDC) + IGST 18 % = **40.39 % of CIF** ([eximpe HSN 85015190](https://eximpe.com/hsncode-finder/85015190); the task's "~30 %" assumption is too low).

| Source | USD each | 14 pcs + est. US$40 shipping | INR CIF (@96) | + 40.39 % duty | ₹/servo landed |
|---|---|---|---|---|---|
| Seeed STS3215 C001 (10+ price) | $19.00 ([seeed](https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html)) | $306 | ₹29,376 | ₹41,241 | **₹2,946** |
| Waveshare direct | $16.99–21.99 ([waveshare](https://www.waveshare.com/st3215-servo.htm)) | $278–348 | ₹26,700–33,400 | ₹37,500–46,900 | ₹2,680–3,350 |
| eBay 12-pack 7.4 V | $284.99/12 = $23.75 ([ebay](https://www.ebay.com/itm/277573318432)) | — | — | — | ≈ ₹3,200 |
| Feetech "oversea price" | $15 ([feetechrc](https://www.feetechrc.com/2020-05-13_56655.html)) | $250 | ₹24,000 | ₹33,694 | ₹2,407 (best case, no courier fees) |

**Conclusion:** local ₹2,159–2,224 beats every import path; buy in India.

---

## 2. Bus-servo driver / adapter

| Part | Qty | Unit ₹ | Vendor URL | Note |
|---|---|---|---|---|
| **Waveshare Bus Servo Adapter (A)** ("Serial Bus Servo Driver Board") | 1 | **432** (in stock) | https://robu.in/product/waveshare-serial-bus-servo-driver-board-integrates-servo-power-supply-and-control-circuit-applicable-for-st-sc-series-serial-bus-servos/ | UART or USB (jumper), up to 253 servos, 42×33 mm. Rated 9–12.6 V but Waveshare docs state "actually 5–8.4 V can also be input" → works on 2S ([docs.waveshare](https://docs.waveshare.com/Bus_Servo_Adapter_A)). Supports changing servo ID/mode → **doubles as the programmer** ([wiki](https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A))). This is what Open Duck Mini v2 uses. |
| same, other Indian prices | | 499.99 thinkrobotics / 789 rees52 / 439 ex-GST electronicscomp | https://thinkrobotics.com/products/serial-bus-servo-driver , https://rees52.com/products/waveshare-serial-bus-servo-driver-board-all-in-one-servo-driver-board-with-integrated-power-control-for-st-sc-actuators-rs8478 | |
| SmartElex clone of the above | 1 | 509 | https://robu.in/?s=serial+bus+servo+cable&post_type=product | robu house brand. |
| **Waveshare Bus Servo Driver HAT (A)** (ESP32-WROOM-32 + servo bus, Pi HAT) | 1 | **2,099** (in stock) | https://robu.in/product/waveshare-serial-bus-servo-driver-hat-integrates-esp32-and-servo-control-circuit-suitable-for-st-rsbl-series-serial-bus-servos/ | 9–25 V in via XT60/DC jack, powers the Pi from an on-board 5 V buck, talks to Pi over GPIO UART, USB-C ×2, WiFi. Best fit for a **12 V / 3S** build; also the "ESP32 compute" option (§3). |
| Feetech FE-URT-1 (official USB↔TTL/RS485 adapter) | 0–1 | 1,069 (in stock) | https://robu.in/product/fe-urt-1-multi-function-serial-signal-converter-module/ | Interfaces: 3-pin 5264-3AW (SCS/STS). Only needed if you want Feetech's FD debug tool on a separate dongle. FE-URT-2 at evelta ₹1,137 ex-GST (https://evelta.com/feetech/). |
| Waveshare Servo Driver with ESP32 (PWM, 16-ch) | 0 | 1,639 | https://robu.in/product/waveshare-esp32-servo-driver-expansion-board-built-in-wifi-and-bluetooth/ | **PWM servos only — not usable for STS3215.** Listed to avoid a mis-buy. |
| Waveshare Serial Bus Servo DC Buck Adapter 7.2 V | 0–1 | 479 (in stock) | https://robu.in/product/waveshare-serial-bus-servo-dc-buck-adapter-mini-module-design-for-serial-bus-servos-easy-to-use-7-2v-buck-regulator/ | 9–36 V in → 7.2 V, **3 A peak** — only enough for bench programming of one or two 7.4 V servos from a 12 V PSU. |

---

## 3. Compute for a 50 Hz ONNX policy

Open Duck Mini v2 runs its ONNX walking policy on a Pi Zero 2 W at 50 Hz ([runtime repo](https://github.com/apirrone/Open_Duck_Mini_Runtime)); the policy is a small MLP, so anything ≥ Zero 2 W class is sufficient. Compute cost, not capability, decides.

| Board | Vendor | ₹ | Stock | URL | Assessment |
|---|---|---|---|---|---|
| **Raspberry Pi Zero 2 W** | robu.in | 2,079 | **OOS** | https://robu.in/product/raspberry-pi-zero-2-w/ | Reference board. Also OOS at evelta ₹1,748.76 (https://evelta.com/raspberry-pi-zero-2-w/), thingbits ₹1,770 (https://www.thingbits.in/products/raspberry-pi-zero-2-w), silverline ₹1,500 (https://www.silverlineelectronics.in/products/raspberry-pi-zero-2-silverline-india-authorised-distributor), fabtolab ₹1,665 "expected Dec 2027" (https://www.fabtolab.com/raspberry-pi-zero-2-w-rp3a0-1ghz-quad-core-64-bit-arm-cortex-a53-cpu-512mb-sdram-wireless-lan-mini-hdmi-port-micro-usb). Cause: chip-substrate capacity consumed by AI accelerators; RPi expects relief H2-2026 ([raspberry.tips, 14 Sep 2026](https://raspberry.tips/en/raspberrypi-infos/raspberry-pi-zero-2-w-alternative-sold-out)). ThinkRobotics says Indian stock "arrives in waves" at ₹1,500–2,000 ([guide, Feb 2026](https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-zero-2-w-stock-availability-guide-and-smart-buying-strategies-in-india)). |
| **Raspberry Pi 3 Model A+** | robu.in | **3,211** | In stock | https://robu.in/?s=raspberry+pi+3+model+a%2B&post_type=product | Same BCM2837 family as Zero 2 W's RP3A0 but 1.4 GHz, 512 MB, 40-pin, CSI, USB-A; 65×56 mm (bigger than Zero's 65×30). Runs the same 64-bit Pi OS + onnxruntime. electropi ₹3,361.82 incl., 17 in stock (https://www.electropi.in/buy-raspberry-pi-3-model-a-plus-india). **Recommended in-stock choice.** |
| Raspberry Pi 4 B 2 GB / 4 GB | robu.in | 6,449 / 11,469 | OOS / in stock | https://robu.in/product/raspberry-pi-4-model-b-with-2-gb-ram/ , https://robu.in/product/raspberry-pi-4-model-b-with-4-gb-ram/ | Overkill, heavy, hot; 4 GB price inflated by DRAM rises. |
| Raspberry Pi 5 1 GB / 2 GB | robocraze / robu | 5,044 / 7,629 | sold out / OOS | https://robocraze.com/products/official-raspberry-pi-5-model-b-1gb-ram , https://robu.in/?s=raspberry+pi+5+2gb&post_type=product | Cheapest Pi 5 route if they restock. |
| **Raspberry Pi 5 4 GB** | silverline | **11,200** | in stock | https://www.silverlineelectronics.in/products/raspberry-pi-5-model-b-4gb-ram-in-stock | robu ₹13,409 OOS (https://robu.in/product/raspberry-pi-5-model-4gb/), robocraze ₹13,999–14,181 sold out (https://robocraze.com/products/raspberry-pi-5-4gb). Feb-2026 guide range ₹5,500–6,200 is stale ([thinkrobotics](https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-5-price-india-complete-cost-analysis-and-buying-guide)). Needs 5.1 V/5 A: official 27 W PSU ₹1,255, Active Cooler ₹519 (robu Pi 5 page). Only for the deluxe build (Isaac/ROS 2 on-board, camera). |
| Radxa Zero 3W (1/2/4 GB) | thinkrobotics / hubtronics / robodo | from 2,649.99 / 2,599 (2 GB) / 6,536 (4 GB+eMMC) | all OOS | https://thinkrobotics.com/products/radxa-zero-3w , https://hubtronics.in/radxa-zero-3w-2gbram , https://robodo.in/products/radxa-zero-3w-single-board-computer-raspberry-pi-alternative-tiny-rk3566-4-gb-ram-storage | Zero-footprint RK3566; good if it reappears, but weaker software support than Pi. |
| Orange Pi Zero 3 (1 GB) | probots | 3,999 (₹3,389 + GST) | OOS | https://probots.co.in/orange-pi-zero-3-1gb-ram-h618-quad-core-64-bit-development-single-board-computer.html | |
| ESP32 / ESP32-S3 (e.g. the Bus Servo Driver HAT (A) above) | robu | 2,099 (HAT) | in stock | see §2 | ESP32-S3 has 128-bit SIMD and can run a tiny INT8 MLP in well under 20 ms ([Espressif edge-AI workshop](https://developer.espressif.com/workshops/edge-ai-with-esp32-s3/introduction/)), but there is **no Open Duck runtime for it** — you would rewrite the controller, IMU driver and policy I/O in C. Research risk; not recommended for the first robot. |
| microSD 32 GB (SanDisk Ultra) | robu | 1,629 | in stock | https://robu.in/?s=SanDisk+32GB+microSD&post_type=product | Robu price is high; ~₹500 on amazon.in is typical but **unverified** (amazon blocked my fetch). |

**Recommendation:** Pi Zero 2 W if you can catch a restock (set stock alerts at ThinkRobotics/robu); otherwise **Pi 3 A+ (₹3,211)**. Pi 5 only in the deluxe tier.

---

## 4. IMU

| Part | Vendor | ₹ | Stock | URL | Note |
|---|---|---|---|---|---|
| **Bosch BNO055 9-axis board (generic)** | robu.in | **1,439** | in stock (SKU R231480) | https://robu.in/?s=BNO055&post_type=product | On-chip fusion, I²C/UART. Reference IMU for Open Duck Mini. Known Pi issue: BNO055 uses I²C clock stretching → lower the Pi I²C baud (e.g. 10 kHz) or use UART mode. |
| 7Semi BNO055 Qwiic | robu.in | 1,359 | OOS | https://robu.in/product/7semi-bno055-9-dof-absolute-orientation-sensor-breakout-i2c-qwiic/ | |
| DFRobot Fermion BNO055 | robu.in | 1,896 | in stock | https://robu.in/?s=BNO055&post_type=product | |
| Adafruit BNO055 STEMMA QT | robu.in | 4,619 | in stock | same search | Overpriced for this use. |
| **SmartElex BNO085** | robu.in | **2,409** | in stock | https://robu.in/?s=BNO055&post_type=product (SKU R268085) | Better gyro/fusion (SH-2, 400 Hz game-rotation vector) than BNO055; recommended upgrade. |
| Adafruit BNO085 STEMMA QT | robu.in | 3,941 | in stock | https://robu.in/product/adafruit-9-dof-orientation-fusion-bno080-stemma-qt/ | |
| MPU6050 module | electronicscomp | 143.96 (₹122 ex-GST) | 421 in stock | https://www.electronicscomp.com/mpu6050-triple-axis-gyro-accelerometer-module | Cheapest; raw 6-axis, you run your own filter (Madgwick). Fine for a policy that only needs gyro + gravity vector, but drifts/noisier. |
| BMI088 module | — | — | not found at robu/electronicscomp | — | Seeed Grove BMI088 exists abroad; **no verified Indian price**. |

**Recommendation:** BNO055 ₹1,439 (minimum, matches Open Duck code) → BNO085 ₹2,409 (recommended/deluxe).

---

## 5. Power

### 5.1 Sizing (estimate — no measured microduck data found; flagged)

Assumptions: 10 leg servos average ~0.4 A each while walking (between the 0.15–0.2 A no-load and 2.5 A stall figures in §1), 4 head servos ~0.1 A, Pi Zero 2 W/3 A+ ~0.4 A @ 5 V via a UBEC at ~80 % (≈0.35 A at 7.4 V). ≈ **4.8 A average at 7.4 V (~35 W)**; 30 min needs ≈ **2.4 Ah at 2S**. Same power at 3S ≈ 3.2 A → 30 min ≈ 1.6 Ah. Peak: several servos stalling simultaneously → 10–20 A, so use ≥ 20C LiPo or a 20 A BMS and fuse at ~10–15 A. Open Duck Mini v2 itself runs on 2× Molicel P30B 18650 (3000 mAh, 30 A) in a 2S holder ([BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing)).

### 5.2 Parts

| Part | Qty | Unit ₹ | Vendor URL | Note |
|---|---|---|---|---|
| **2S 7.4 V 2200 mAh 45C LiPo (Pro-Range)** | 1 | **1,629** in stock | https://robu.in/?s=2S+2200mAh+lipo&post_type=product | ~27 min at the estimate above; XT60 lead, JST-XH balance, 115 g. 30C version ₹1,399 is OOS (https://robu.in/product/orange-2200mah-2s-30c-60c-lithium-polymer-battery-pack-lipo/). |
| 2S 7.4 V 4200 mAh 35C LiPo (Orange) | 1 | 2,599 in stock | same search | ~50 min; heavier (est. ~220 g, unverified). Used in Recommended. |
| 3S 11.1 V 2200 mAh 35C (Bonka) | 1 | 2,039 in stock | https://robu.in/?s=3S+2200mAh+lipo&post_type=product | For 12 V servos. Pro-Range 3S 2200 30C ₹1,619 / 40C ₹1,679 both OOS (https://robu.in/product/orange-2200mah-3s-30c60c-lithium-polymer-battery-pack-lipo/), 175 g, XT60. |
| 18650 alternative: Samsung INR18650-25R (2500 mAh, 20 A) | 2 | 539 | https://robu.in/product/samsung-inr18650-25r-2500mah-li-ion-battery/ | **OOS at robu**; IndiaMART sellers ₹290–375 (unverified). |
| 18650 ×2 holder with cover + switch | 1 | 59 | https://robu.in/?s=18650+holder&post_type=product | Open-Duck-style pack. |
| 2S 20 A BMS | 1 | 149 | https://robu.in/?s=2S+20A+BMS&post_type=product | Do not use the ₹69 5 A board for this load. |
| USB-C 2S 8.4 V 4 A charger/booster module | 1 | 329 | https://robu.in/?s=2S+lithium+charger+module&post_type=product | Charge the 18650 pack in-robot (Open Duck has a USB-C charge port). |
| Pre-built Pro-Range NMC 18650 2S1P 2500 mAh 3C pack | (alt) | 579 | https://robu.in/?s=18650+2500mAh+cell&post_type=product | Cheapest 2S pack but **3C = 7.5 A max** — marginal for stalls; not recommended. 2S2P 6000 mAh ₹1,259 is a better 18650 option. |
| **UBEC 5 V / 3 A** (5.5–35 V in) | 1 | 269 in stock | https://robu.in/product/ubec-5v-3a/ | 5 V rail for Pi Zero 2 W / 3 A+ (Open Duck uses a UBEC). |
| 5 V 5 A buck (MINI560 Pro / XY-3606 / LM2596-class) | 1 (Pi 5 only) | 89–199 | https://robu.in/?s=5V+5A+buck+converter&post_type=product | Pi 5 wants 5.1 V/5 A; the DFRobot Pi 5 18650 UPS HAT is ₹6,719 (https://robu.in/product/dfrobot-raspberry-pi-5-18650-battery-ups-hat-5-1v-5a/) — too dear. |
| Servo rail | — | — | — | 7.4 V servos: feed battery directly into the Bus Servo Adapter (A) (5–8.4 V OK). 12 V servos: 3S straight into Adapter (A)/HAT (A) (9–12.6 V). |
| XT30 pair (Amass, M+F) | 1–2 | 36 + 32 = 68/pair | https://robu.in/?s=XT30&post_type=product | electronicscomp ₹26 each ex-GST (https://www.electronicscomp.com/index.php?route=product/search&search=xt30). |
| XT60 pairs (Amass, 5 pairs) | 1 pack | 375 (₹318 ex-GST) | https://www.electronicscomp.com/index.php?route=product/search&search=XT60 | Only if using the HAT (A) (XT60 input) / 3S packs. |
| 1S–8S LiPo low-voltage alarm/tester | 1 | 148 (₹125 ex-GST) | https://www.electronicscomp.com/lipo-battery-voltage-tester-india | Plugs into balance lead; set 3.5 V/cell. |
| Rocker switch SPST 6 A / DPST 16 A | 1 | 19 / 59 | https://robu.in/?s=rocker+switch&post_type=product | 6 A AC rating is marginal at 5–8 A DC; the 16 A DPST is safer. |
| Inline fuse holder 5×20 mm + 10 A fuse | 1 | 46 (₹39 ex-GST) | https://www.electronicscomp.com/index.php?route=product/search&search=fuse%20holder | |
| Balance charger (tool) SkyRC iMAX B6 V2 / B6 copy | 1 | 3,099 / 2,079 | https://robu.in/?s=IMAX+B6&post_type=product | Needed for LiPo route; not needed for 18650 + USB-C module route. |
| Bench PSU 12 V 5 A (tool) | 1 | 425 (standard) / 1,049 (Pro-Range) | https://robu.in/?s=12V+5A+adapter&post_type=product | For 12 V servos on the bench; for 7.4 V use the 7.2 V buck adapter (§2) or the battery. |

---

## 6. Camera, audio, LEDs, foot contacts (optional / "expression package")

| Part | Qty | Unit ₹ | Vendor URL | Note |
|---|---|---|---|---|
| Raspberry Pi Camera Module 3 (76°) | 1 | 3,249 in stock | https://robu.in/product/raspberry-pi-camera-module-3/ | Open Duck lists a camera as "not integrated yet". |
| Raspberry Pi Camera Module 3 **Wide** (120°) | 1 | 4,379 (only 4 left) | https://robocraze.com/products/raspberry-pi-camera-module-3-wide | Better for a head-mounted cam. |
| Camera FPC: 500 mm Pi 5 (22-pin) cable | 1 | 372 | robu Pi 5 page (https://robu.in/product/raspberry-pi-5-model-4gb/) | Pi Zero/3A+ use different connectors (Zero: 22-pin mini; 3A+: 15-pin) — ~₹100 cables, unverified. |
| **MAX98357A I²S 3 W amp (SmartElex)** | 1 | **194** in stock | https://robu.in/product/smartelex-i2s-audio-breakout-max98357a/ | DFRobot version ₹442 ex-GST OOS (https://www.electronicscomp.com/dfrobot-max98357-i2s-amplifier-module). |
| Speaker 4 Ω 3 W 40 mm | 1 | 79 in stock | https://roboman.in/product/speaker-4-ohm-3watt-1-6inch-40mm-external-magnet-speaker/ | DFRobot 3 W 8 Ω enclosed ₹519 at robu is the tidy alternative. |
| WS2812B eye LEDs (LilyPad single) | 2 | 49 | https://robu.in/?s=WS2812+stick&post_type=product | electronicscomp single WS2812B module ₹19 ex-GST, 8-LED ring ₹272 ex-GST (https://www.electronicscomp.com/index.php?route=product/search&search=WS2812). Drive from Pi GPIO18 (PWM) with a 3.3→5 V level shift, or from the HAT's ESP32. |
| Foot contact switches (Open Duck uses 4× SS-10 style) | 4 | 197 (Omron SS-10) | https://robu.in/?s=SS-10+micro+switch&post_type=product | Generic KW10/KW11 microswitches are ~₹10–20 each (unverified); optional — the policy can run without contact sensing. |

---

## 7. Fasteners, inserts, bearings, cables, consumables

Open Duck Mini v2 uses M3 heat-set inserts + M3 screws throughout (exact counts marked "TODO" in the guide), Loctite 243 on metal-metal joints, 3 bearings, PLA + TPU feet. For PETG, use M3×4 mm or ×6 mm inserts (PETG softens ~80 °C; set the iron to ~230–250 °C).

| Part | Qty | Unit ₹ | Vendor URL | Note |
|---|---|---|---|---|
| **Heat-set inserts kit M2 + M2.5 + M3, 500 pcs** | 1 | 1,349 in stock (₹1,129 version OOS) | https://robu.in/?s=M2.5+heat+set+insert&post_type=product (SKU R267265) / https://robu.in/product/brass-heat-set-insert-nut-hot-melt-knurled-threaded-m2-m25-m3-500pcs/ | Recommended/deluxe. |
| M3×4 mm brass heat-set insert, 25 pcs | 3 | 91 | https://robu.in/product/m3-x-4-mm-brass-heat-set-knurl-threaded-round-insert-nut-25-pcs/ | Minimum build (M3 only, like Open Duck). M3×6 mm also listed. |
| Heat-set inserts, 10-pack, M2×3 / M2.5×4.5 / M3×4.5 | as needed | 49.99 | https://thinkrobotics.com/products/brass-heat-set-inserts-for-plastic | Handy for M2/M2.5 top-ups. |
| M3×8 button-head SS304, 10 pcs | 1 | 125 | https://robu.in/?s=M3+socket+head+cap+screw&post_type=product | Servo-horn & bracket screws. |
| M3×10 button-head, 10 pcs | 1 | 132 | same | |
| M3×12 button-head, 10 pcs | 1 | 142 | same | |
| EasyMech SS304 M3×16 SHCS, 25 pcs | 1 | 70 | same | Best value M3 pack. |
| M2.5×8 SHCS, 10 pcs (EasyMech) | 1 | 154 | https://robu.in/?s=M2.5+X+8mm+socket&post_type=product | M2.5×8 CSK black-oxide ₹79 also there. |
| M2×8 button-head SS304, 10 pcs | 1 | 74 | https://robu.in/?s=M2+X+6mm+socket&post_type=product | STS3215 horn screws are M2 (ship with servo); M2×6 bolt+nut 12 pcs ₹239. |
| M3 nyloc nuts, 25 pcs | 1 | 78 | https://robu.in/?s=nylon+washer+M3&post_type=product | |
| Nylon washers M3 | — | — | not found at robu / electronicscomp | **Unverified**: ~₹100–200 / 100 pcs on amazon.in or local hardware. Alternative: 3D-print PETG shims, or M3 nylon spacers 10 pcs ₹82 (https://robu.in/?s=M3+plastic+washer&post_type=product). |
| **684ZZ 4×9×4** | 4 (1 pack) | 192 / 4 pcs (robu) or 22.4 each (₹19 ex-GST, electronicscomp) | https://robu.in/product/684-zz-bearing-4x9x4-shielded-miniature-ball-bearings-4pcs/ , https://www.electronicscomp.com/684-zz-bearing-4x9x4-shielded-miniature-ball-bearings | |
| MR115 5×11×4 | — | — | **not stocked** at robu or electronicscomp | Substitute **685ZZ 5×11×5** ₹21.2 (₹18 ex-GST, in stock: https://www.electronicscomp.com/index.php?route=product/search&search=685ZZ) and design the pocket 1 mm deeper; or IndiaMART/amazon.in (unverified). |
| 605ZZ 5×14×5 | — | — | **not stocked** at either | Substitute 625RS 5×16×5 ₹18.9 (₹16 ex-GST) or 695ZZ 5×13×4 (not found); design around 685ZZ/625 instead. |
| 608RS 8×22×7 | as needed | 27 (₹23 ex-GST) | https://www.electronicscomp.com/index.php?route=product/search&search=bearing | Also 694ZZ 4×11×4 ₹18, 696ZZ 6×15×5 ₹16, 686ZZ 6×13×5 ₹59, 606ZZ 6×17×6 ₹24 (all ex-GST). |
| Nylon cable ties 4.8 mm × 120 mm, 100 pcs | 1 | 117 (₹99 ex-GST) | https://www.electronicscomp.com/index.php?route=product/search&search=cable%20tie | 10-packs from ₹11. |
| Silicone wire 18 AWG (power), per m | 2 | 32 | https://robu.in/?s=22+AWG+silicone+wire&post_type=product | 22 AWG ₹17/m and 20 AWG ₹21/m were OOS at robu on the day. |
| Servo bus cables | 14 supplied | 0 | — | Each STS3215 ships with a 15 cm 3-pin cable ([feetechrc](https://www.feetechrc.com/525603.html)); connector is Molex-5264-style 2.5 mm 3-pin ([Waveshare wiki](https://www.waveshare.com/wiki/ST3215_Servo), [FE-URT-1 spec](https://robu.in/product/fe-urt-1-multi-function-serial-signal-converter-module/)). |
| Servo extension / daisy-chain cables (longer runs hip→foot, neck) | ~6 | est. 50 each → 300 | https://www.electronicscomp.com/index.php?route=product/search&search=JST%20XH | **No verified Indian listing of genuine 5264 3-pin cables.** 2.54 mm "Relimate" 3-pin cables (₹6–98 each, ex-GST) physically mate with 5264 headers in practice but verify fit; safest is to crimp your own (5264 housings + 2.5 mm crimps) or order Feetech/Waveshare cables with the servos. |
| JST-XH / Relimate connector assortment | 1 | est. 200 | same | Balance lead, IMU, LEDs, switches. |
| Loctite 243 (Open Duck recommendation) | 1 | unverified (~₹300–500) | — | |

---

## 8. Filament (PETG for P1S)

| Part | Qty | Unit ₹ | Vendor URL | Note |
|---|---|---|---|---|
| **Bambu Lab PETG Basic refill 1 kg** | 3 | **699** in stock | https://robu.in/?s=Bambu+Lab+PETG&post_type=product (SKU R260052/R260054) | Native P1S profile; refill fits the Bambu reusable spool. Cheapest good PETG found. |
| Bambu Lab PETG HF 1 kg on spool | 3 | 1,299 in stock | same search | HF is being discontinued upstream; buy while listed. |
| Bambu Lab PETG Translucent refill | — | 1,149 | same | |
| Sunlu PETG 1 kg | — | 739 in stock | https://robu.in/?s=PETG+filament&post_type=product | Budget option; dry it. |
| eSUN PETG 1 kg | — | 1,099–1,329 (ex-GST) | https://www.electronicscomp.com/index.php?route=product/search&search=PETG | Creality CR-PETG ₹999 ex-GST also listed. |
| TPU for feet (optional; Open Duck uses TPU soles) | 1 | unverified (~₹1,000–1,500) | — | User specified PETG; a TPU sole improves traction — consider later. |

Budget 2–3 kg: the duck body is ~500 g of plastic (Open Duck BOM) but PETG demo iterations, supports and failed prints justify 3 kg.

---

## 9. Tools the user may lack

| Tool | ₹ | Vendor URL | Note |
|---|---|---|---|
| Heat-set insert soldering tips (M2–M8 set, 900M/936 fit) | unverified (amazon.in listings exist; prices hidden to fetch) | https://www.amazon.in/Insert-Sizes-Soldering-Printer-Universal/dp/B0C74NP96Q , https://www.amazon.in/amiciTools-Heat-Insert-Soldering-Printing/dp/B0GFDZ5GL9 | Typical ₹300–800 (est.). A plain conical tip works for M3 in a pinch. Not stocked by robu/thinkrobotics/electronicscomp. |
| Servo programmer / ID setter | 0 extra | — | The Bus Servo Adapter (A) in USB mode sets IDs/modes (Waveshare demo, or Feetech FD software). FE-URT-1 ₹1,069 only if you want a dedicated dongle. |
| LiPo balance charger | 2,079–3,099 | https://robu.in/?s=IMAX+B6&post_type=product | Skip if you go 18650 + USB-C 2S charger module (₹329). |
| Bench 12 V 5 A PSU | 425 | https://robu.in/?s=12V+5A+adapter&post_type=product | 12 V build only. |
| Hex drivers 1.5/2/2.5 mm, crimper for 2.5 mm JST-style crimps, soldering iron | assumed owned | — | |

---

## 10. Three priced configurations

### 10.1 Minimum viable — 14 servos (10 leg + 4 head), Pi Zero 2 W, 7.4 V / 2S

| # | Item | Qty | Unit ₹ | Line ₹ |
|---|---|---|---|---|
| 1 | Waveshare ST3215 7.4 V 19.5 kg·cm (robu) | 14 | 2,159 | 30,226 |
| 2 | Waveshare Bus Servo Adapter (A) | 1 | 432 | 432 |
| 3 | Raspberry Pi Zero 2 W (**OOS** — see 10.1b) | 1 | 2,079 | 2,079 |
| 4 | microSD 32 GB | 1 | 1,629 | 1,629 |
| 5 | BNO055 board | 1 | 1,439 | 1,439 |
| 6 | 2S 2200 mAh 45C LiPo | 1 | 1,629 | 1,629 |
| 7 | LiPo alarm | 1 | 148 | 148 |
| 8 | UBEC 5 V 3 A | 1 | 269 | 269 |
| 9 | XT30 pair | 1 | 68 | 68 |
| 10 | Rocker switch 6 A | 1 | 19 | 19 |
| 11 | Inline fuse holder + fuse | 1 | 46 | 46 |
| 12 | M3×4 heat-set inserts, 25 pcs | 3 | 91 | 273 |
| 13 | Screws (M3×8/10/12 ×10, M3×16 ×25, M2.5×8 ×10, M2×8 ×10) | 1 set | 697 | 697 |
| 14 | M3 nyloc nuts 25 | 1 | 78 | 78 |
| 15 | Bearings: 684ZZ ×4 (₹192) + 685ZZ ×4 (₹85) | 1 set | 277 | 277 |
| 16 | Cable ties 100 pcs | 1 | 117 | 117 |
| 17 | Silicone wire 18 AWG | 2 m | 32 | 64 |
| 18 | Relimate/JST 3-pin cables & connectors (est.) | 1 lot | 200 | 200 |
| 19 | Bambu PETG Basic refill 1 kg | 3 | 699 | 2,097 |
| | **Total** | | | **₹41,787** |
| | Margin to ₹50,000 | | | **+₹8,213** |

10.1b — same build with **Pi 3 A+ (₹3,211)** instead of the unobtainable Zero 2 W: **₹42,919**, margin +₹7,081.
Add tools if lacking: iMAX B6 copy ₹2,079 + insert tip ~₹500 (est.) → ₹44,366 / ₹45,498.

### 10.2 Recommended — 14 servos, Pi 3 A+, BNO085, bigger battery, audio + eyes + foot switches, full insert kit

| # | Item | Qty | Unit ₹ | Line ₹ |
|---|---|---|---|---|
| 1 | Waveshare ST3215 7.4 V (robu) | 14 | 2,159 | 30,226 |
| 2 | Bus Servo Adapter (A) | 1 | 432 | 432 |
| 3 | Raspberry Pi 3 A+ | 1 | 3,211 | 3,211 |
| 4 | microSD 32 GB | 1 | 1,629 | 1,629 |
| 5 | SmartElex BNO085 | 1 | 2,409 | 2,409 |
| 6 | 2S 4200 mAh 35C LiPo | 1 | 2,599 | 2,599 |
| 7 | LiPo alarm | 1 | 148 | 148 |
| 8 | UBEC 5 V 3 A | 1 | 269 | 269 |
| 9 | XT30 pairs | 2 | 68 | 136 |
| 10 | Rocker switch 16 A DPST | 1 | 59 | 59 |
| 11 | Inline fuse holder + fuse | 1 | 46 | 46 |
| 12 | MAX98357A amp | 1 | 194 | 194 |
| 13 | Speaker 4 Ω 3 W | 1 | 79 | 79 |
| 14 | WS2812 eye LEDs | 2 | 49 | 98 |
| 15 | Foot switches Omron SS-10 | 4 | 197 | 788 |
| 16 | Heat-set insert kit M2/M2.5/M3 500 pcs | 1 | 1,349 | 1,349 |
| 17 | Screws (as 10.1 + extra M3×16 ×25) | 1 set | 767 | 767 |
| 18 | M3 nyloc nuts | 1 | 78 | 78 |
| 19 | Bearings (684ZZ, 685ZZ + 608RS/625RS spares) | 1 set | 377 | 377 |
| 20 | Cable ties | 1 | 117 | 117 |
| 21 | Silicone wire 18 AWG 2 m + 22 AWG 3 m | 1 | 115 | 115 |
| 22 | Servo extension cables (est.) | 6 | 50 | 300 |
| 23 | JST/Relimate assortment (est.) | 1 | 200 | 200 |
| 24 | Bambu PETG Basic refill | 3 | 699 | 2,097 |
| | **Total** | | | **₹47,723** |
| | Margin to ₹50,000 | | | **+₹2,277** |

With tools (iMAX B6 ₹2,079 + insert tip ~₹500): ₹50,302 — ₹302 over. Levers: generic foot microswitches instead of Omron (−~₹700), or 2200 mAh pack (−₹970).
Antenna servos as STS3215 (+2 × ₹2,159 = +₹4,318) or a camera (+₹3,249) each push this over ₹50 k — pick one, or use the 9 g PWM servos Open Duck uses for antennas (₹100–150 each, unverified) if the all-STS3215 rule can bend.

### 10.3 Deluxe — 16× 12 V servos, Pi 5 4 GB, Camera 3 Wide, HAT (A), 3S

| # | Item | Qty | Unit ₹ | Line ₹ |
|---|---|---|---|---|
| 1 | Feetech ST3215-C018 12 V 30 kg·cm (evelta) | 16 | 2,419 | 38,704 |
| 2 | Bus Servo Driver HAT (A) (ESP32, powers Pi) | 1 | 2,099 | 2,099 |
| 3 | Raspberry Pi 5 4 GB (silverline) | 1 | 11,200 | 11,200 |
| 4 | Pi 5 Active Cooler | 1 | 519 | 519 |
| 5 | microSD 32 GB | 1 | 1,629 | 1,629 |
| 6 | 5 V 5 A buck (Pi 5 rail) | 1 | 109 | 109 |
| 7 | SmartElex BNO085 | 1 | 2,409 | 2,409 |
| 8 | Camera Module 3 Wide | 1 | 4,379 | 4,379 |
| 9 | Pi 5 camera FPC 500 mm | 1 | 372 | 372 |
| 10 | 3S 2200 mAh 35C LiPo (Bonka) | 1 | 2,039 | 2,039 |
| 11 | LiPo alarm | 1 | 148 | 148 |
| 12 | XT60 pairs (5) | 1 | 375 | 375 |
| 13 | Rocker switch 16 A | 1 | 59 | 59 |
| 14 | Fuse holder + fuse | 1 | 46 | 46 |
| 15 | MAX98357A + speaker | 1 | 273 | 273 |
| 16 | WS2812 eyes | 2 | 49 | 98 |
| 17 | Foot switches Omron SS-10 | 4 | 197 | 788 |
| 18 | Heat-set insert kit 500 pcs | 1 | 1,349 | 1,349 |
| 19 | Screws | 1 set | 767 | 767 |
| 20 | M3 nyloc | 1 | 78 | 78 |
| 21 | Bearings | 1 set | 377 | 377 |
| 22 | Cable ties | 1 | 117 | 117 |
| 23 | Wire | 1 | 115 | 115 |
| 24 | Servo extension cables (est.) | 6 | 50 | 300 |
| 25 | JST assortment (est.) | 1 | 200 | 200 |
| 26 | Bambu PETG HF 1 kg spool | 3 | 1,299 | 3,897 |
| | **Total** | | | **₹72,446** |
| | Margin to ₹50,000 | | | **−₹22,446 (over)** |

Tools (charger, tip, 12 V bench PSU) add ~₹3,000. To pull deluxe back toward ₹50 k: Pi 3 A+ instead of Pi 5 (−₹8,617 incl. cooler/buck), 7.4 V servos (−₹4,160), drop camera (−₹4,751) → ≈ ₹54,900; drop the 2 antenna servos → ≈ ₹50,600.

---

## 11. Biggest cost risks (ranked)

1. **Servo price / availability drift** — 14–16 units × ₹2,159–2,650. Robu's 7.4 V listing was in stock on 26 Sep 2026; evelta shows 80 units. A ₹300 swing per servo is ±₹4,200–4,800 on the total. Buy all 14 in one order from one vendor (bulk quote from evelta/robu).
2. **Servo import duty** — 40.39 % (BCD 15 % + AIDC + SWS + IGST 18 %) makes AliExpress/Seeed landed cost ₹2,400–3,350/servo, i.e. **worse than local**. Courier "customs handling" fees (₹500–1,500, unverified) make it worse still. Do not import.
3. **Raspberry Pi 5 price** — ₹11,200–14,181 for 4 GB in India after RPi's Feb/Apr 2026 memory-driven rises ([RPi, 2 Feb 2026](https://www.raspberrypi.com/news/more-memory-driven-price-rises/), [Tom's Hardware](https://www.tomshardware.com/raspberry-pi/raspberry-pi-5-price-increases-drastically-as-ai-shortage-bites-16gb-version-now-usd205-second-price-increase-in-three-months-over-70-percent-more-expensive-than-original-msrp)). Any Pi 5 build is ≥ ₹60 k.
4. **Raspberry Pi Zero 2 W shortage** — zero Indian stock; alternatives are Pi 3 A+ (₹3,211) or waiting for restock (ThinkRobotics alerts). Do not pay marketplace scalper prices (₹2,500–3,500+).
5. **microSD and small-parts markup at robotics shops** — robu's SanDisk 32 GB is ₹1,629; amazon.in is typically ~₹500 (unverified). Similar for screws (₹12–15 per M3 screw at robu 10-packs vs ₹1–3 at a hardware store).
6. **Bearings not stocked in India in the exact sizes** (MR115, 605ZZ) — design the CAD around 684ZZ / 685ZZ / 608 / 625, which are ₹16–24 each and in stock.
7. **GST/shipping** — evelta and electronicscomp show ex-GST prices; add 18 % and courier (₹60–150 per order, unverified) when comparing.

---

## 12. Open questions

- Exact electronicscomp price for the Waveshare 30KG (12 V) servo: search listing showed ₹1,715 (probably ex-GST → ₹2,024) but the product page returned 404; if real, it is the cheapest 12 V source by ₹330.
- Whether robu's Waveshare-branded ST3215 7.4 V (SKU R258500) is the C001 1/345 ratio (it should be; Waveshare sells only the 1/345 variant) — confirm on the product page before ordering 14.
- Measured walking current of a 14-servo STS3215 biped — the 4.8 A @ 7.4 V figure here is an estimate; a 10-minute bench log with the LiPo alarm/ a USB power meter will size the battery properly.
- Availability windows for Pi Zero 2 W in India (ThinkRobotics says 2–8 week waves) — decide whether to wait or commit to Pi 3 A+.
- Genuine 5264 3-pin servo cable source in India (none found) versus 2.54 mm Relimate substitutes — test fit on one servo first.
- Nylon washers and a heat-set insert tip: no verified Indian robotics-shop price; amazon.in/local hardware.
- Whether the Bus Servo Driver HAT (A)'s 5 V buck can supply a Pi 5 (needs 5 A) — Waveshare does not state its current; a separate 5 V 5 A buck is budgeted.
- 12 V (30 kg·cm) vs 7.4 V (19.5 kg·cm): Open Duck's trained policies and actuator identification assume 7.4 V. Switching to 12 V is a valid torque upgrade (+₹2,800–4,200 for 14, plus 3S battery) but you must re-identify actuator gains in MuJoCo/Isaac.

---

## 13. Sources (all accessed 26 Sep 2026)

Servos: https://robu.in/?s=ST3215+19.5kg&post_type=product · https://robu.in/product/waveshare-30kg-serial-bus-servo/ · https://evelta.com/sts3215-7-4v-19kg-dual-axis-ttl-string-servo-motor/ · https://evelta.com/feetech/ · https://thinkrobotics.com/products/st3215-series-serial-bus-servo · https://www.theengineerstore.in/products/waveshare-30kg-serial-bus-servo · https://www.electronicscomp.com/index.php?route=product/search&search=bus%20servo · https://www.waveshare.com/st3215-servo.htm · https://www.waveshare.com/wiki/ST3215_Servo · https://www.feetechrc.com/525603.html · https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf · https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html · https://www.ebay.com/itm/277573318432
Kits: https://thinkrobotics.com/products/so-arm101-hugging-face-lerobot · https://robu.in/?s=STS3215&post_type=product · https://www.seeedstudio.com/SO-ARM101-Low-Cost-AI-Arm-Kit-p-6426.html
Duty/FX: https://eximpe.com/hsncode-finder/85015190 · https://tradingeconomics.com/india/currency
Drivers: https://robu.in/product/waveshare-serial-bus-servo-driver-board-integrates-servo-power-supply-and-control-circuit-applicable-for-st-sc-series-serial-bus-servos/ · https://docs.waveshare.com/Bus_Servo_Adapter_A · https://www.waveshare.com/wiki/Bus_Servo_Adapter_(A) · https://thinkrobotics.com/products/serial-bus-servo-driver · https://robu.in/product/waveshare-serial-bus-servo-driver-hat-integrates-esp32-and-servo-control-circuit-suitable-for-st-rsbl-series-serial-bus-servos/ · https://robu.in/product/fe-urt-1-multi-function-serial-signal-converter-module/ · https://robu.in/product/waveshare-serial-bus-servo-dc-buck-adapter-mini-module-design-for-serial-bus-servos-easy-to-use-7-2v-buck-regulator/
Compute: https://robu.in/product/raspberry-pi-zero-2-w/ · https://evelta.com/raspberry-pi-zero-2-w/ · https://www.thingbits.in/products/raspberry-pi-zero-2-w · https://www.silverlineelectronics.in/products/raspberry-pi-zero-2-silverline-india-authorised-distributor · https://www.fabtolab.com/raspberry-pi-zero-2-w-rp3a0-1ghz-quad-core-64-bit-arm-cortex-a53-cpu-512mb-sdram-wireless-lan-mini-hdmi-port-micro-usb · https://raspberry.tips/en/raspberrypi-infos/raspberry-pi-zero-2-w-alternative-sold-out · https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-zero-2-w-stock-availability-guide-and-smart-buying-strategies-in-india · https://robu.in/?s=raspberry+pi+3+model+a%2B&post_type=product · https://www.electropi.in/buy-raspberry-pi-3-model-a-plus-india · https://robu.in/product/raspberry-pi-4-model-b-with-4-gb-ram/ · https://robu.in/product/raspberry-pi-4-model-b-with-2-gb-ram/ · https://www.silverlineelectronics.in/products/raspberry-pi-5-model-b-4gb-ram-in-stock · https://robu.in/product/raspberry-pi-5-model-4gb/ · https://robocraze.com/products/raspberry-pi-5-4gb · https://robocraze.com/products/official-raspberry-pi-5-model-b-1gb-ram · https://robu.in/?s=raspberry+pi+5+2gb&post_type=product · https://www.raspberrypi.com/news/more-memory-driven-price-rises/ · https://thinkrobotics.com/blogs/product-reviews-buying-guides/raspberry-pi-5-price-india-complete-cost-analysis-and-buying-guide · https://thinkrobotics.com/products/radxa-zero-3w · https://hubtronics.in/radxa-zero-3w-2gbram · https://robodo.in/products/radxa-zero-3w-single-board-computer-raspberry-pi-alternative-tiny-rk3566-4-gb-ram-storage · https://probots.co.in/orange-pi-zero-3-1gb-ram-h618-quad-core-64-bit-development-single-board-computer.html · https://robu.in/product/dfrobot-raspberry-pi-5-18650-battery-ups-hat-5-1v-5a/ · https://github.com/apirrone/Open_Duck_Mini_Runtime · https://developer.espressif.com/workshops/edge-ai-with-esp32-s3/introduction/
IMU: https://robu.in/?s=BNO055&post_type=product · https://robu.in/product/7semi-bno055-9-dof-absolute-orientation-sensor-breakout-i2c-qwiic/ · https://robu.in/product/adafruit-9-dof-orientation-fusion-bno080-stemma-qt/ · https://www.electronicscomp.com/mpu6050-triple-axis-gyro-accelerometer-module
Power: https://robu.in/?s=2S+2200mAh+lipo&post_type=product · https://robu.in/?s=3S+2200mAh+lipo&post_type=product · https://robu.in/product/orange-2200mah-3s-30c60c-lithium-polymer-battery-pack-lipo/ · https://robu.in/product/orange-2200mah-2s-30c-60c-lithium-polymer-battery-pack-lipo/ · https://robu.in/?s=18650+2500mAh+cell&post_type=product · https://robu.in/product/samsung-inr18650-25r-2500mah-li-ion-battery/ · https://robu.in/?s=18650+holder&post_type=product · https://robu.in/?s=2S+20A+BMS&post_type=product · https://robu.in/?s=2S+lithium+charger+module&post_type=product · https://robu.in/product/ubec-5v-3a/ · https://robu.in/?s=5V+5A+buck+converter&post_type=product · https://robu.in/?s=XT30&post_type=product · https://www.electronicscomp.com/index.php?route=product/search&search=xt30 · https://www.electronicscomp.com/index.php?route=product/search&search=XT60 · https://www.electronicscomp.com/lipo-battery-voltage-tester-india · https://robu.in/?s=rocker+switch&post_type=product · https://www.electronicscomp.com/index.php?route=product/search&search=fuse%20holder · https://robu.in/?s=IMAX+B6&post_type=product · https://robu.in/?s=12V+5A+adapter&post_type=product
Camera/audio/LED: https://robu.in/product/raspberry-pi-camera-module-3/ · https://robocraze.com/products/raspberry-pi-camera-module-3-wide · https://robu.in/product/smartelex-i2s-audio-breakout-max98357a/ · https://www.electronicscomp.com/dfrobot-max98357-i2s-amplifier-module · https://roboman.in/product/speaker-4-ohm-3watt-1-6inch-40mm-external-magnet-speaker/ · https://robu.in/?s=WS2812+stick&post_type=product · https://www.electronicscomp.com/index.php?route=product/search&search=WS2812 · https://robu.in/?s=SS-10+micro+switch&post_type=product
Fasteners/bearings/consumables: https://robu.in/?s=M2.5+heat+set+insert&post_type=product · https://robu.in/product/brass-heat-set-insert-nut-hot-melt-knurled-threaded-m2-m25-m3-500pcs/ · https://robu.in/product/m3-x-4-mm-brass-heat-set-knurl-threaded-round-insert-nut-25-pcs/ · https://thinkrobotics.com/products/brass-heat-set-inserts-for-plastic · https://robu.in/?s=M3+socket+head+cap+screw&post_type=product · https://robu.in/?s=M2.5+X+8mm+socket&post_type=product · https://robu.in/?s=M2+X+6mm+socket&post_type=product · https://robu.in/?s=nylon+washer+M3&post_type=product · https://robu.in/?s=M3+plastic+washer&post_type=product · https://robu.in/product/684-zz-bearing-4x9x4-shielded-miniature-ball-bearings-4pcs/ · https://www.electronicscomp.com/684-zz-bearing-4x9x4-shielded-miniature-ball-bearings · https://www.electronicscomp.com/index.php?route=product/search&search=bearing · https://www.electronicscomp.com/index.php?route=product/search&search=685ZZ · https://www.electronicscomp.com/index.php?route=product/search&search=cable%20tie · https://robu.in/?s=22+AWG+silicone+wire&post_type=product · https://www.electronicscomp.com/index.php?route=product/search&search=JST%20XH
Filament: https://robu.in/?s=Bambu+Lab+PETG&post_type=product · https://robu.in/?s=PETG+filament&post_type=product · https://www.electronicscomp.com/index.php?route=product/search&search=PETG
Tools: https://www.amazon.in/Insert-Sizes-Soldering-Printer-Universal/dp/B0C74NP96Q · https://www.amazon.in/amiciTools-Heat-Insert-Soldering-Printing/dp/B0GFDZ5GL9
Reference design: https://github.com/apirrone/Open_Duck_Mini/blob/v2/README.md · https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md · https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing

---

## Critic additions (2026-09-26, from `07_critic_gaps.md`)

1. **Missing line item: 3 x 6804ZZ bearings (20 x 32 x 7 mm).** The Open Duck BOM's bearing (amazon.fr ASIN B0CXXSVFTV, qty 3) is a **6804ZZ**, confirmed by the CAD mesh (OD 32 / ID 20 / W 7, critic's measurement) — not 684/685/608. §7's 684ZZ + 685ZZ set (Rs 277) does not cover it. 6804ZZ: **not listed at electronicscomp** ([search](https://www.electronicscomp.com/index.php?route=product/search&search=6804)); robu.in unreachable (403); IndiaMART/amazon.in unverified. Budget **Rs 300-600 for 3 [price unverified]** or redesign the pivot around a 608RS (Rs 27, in stock).
2. **§7 correction: STS3215 horn screws are M3, not M2.** The horn centre screw is M3 x 6 and the O20 disc's four holes take M3; the **body** pilot holes take the supplied PA2.0 self-tappers or M2 x 6 machine screws (03 §1.2-1.4). Keep the M2 x 8 pack for the body only if you choose machine screws over the supplied self-tappers.
3. **§7 correction: PETG does not "soften ~80 C".** Bambu PETG Basic Tg = 69 C, HDT = 68 C @ 1.8 MPa (04 §0); the servo's 70 C torque cut-off is the same temperature. Iron temperature for inserts: ~245 C (04 §3.2), not a PETG-softening argument.
4. **Antenna servos (§10.2 open item) are not needed:** the reference robot in `duck.mp4` has no antennae (01 §4), only static black ear pods. So the build is exactly **14 x STS3215, zero PWM servos** — the "all bus servos" rule is satisfied at no cost.
5. **Foot switches (§6) are not optional for the pretrained policy:** the 101-dim observation carries 2 contact bits (02 §6.3, 05 §2.2). Dropping them requires retraining at 99 dims. Keep the Rs 788 line; generic KW10 microswitches (Rs 10-20, unverified) are an acceptable saving if the foot pocket is designed around their body.
6. **BNO085 (§4) costs software, not just Rs 970:** the runtime is `adafruit_bno055`, so a BNO085 needs a new driver and axis re-verification. Phase 1: BNO055 Rs 1,439.
7. **Budget lever — 18650 pack instead of LiPo + balance charger:** holder Rs 59 + 2S 20 A BMS Rs 149 + USB-C 2S charger module Rs 329 = Rs 537 plus 2 x 18650 25-30 A cells (Samsung 25R Rs 539 at robu, OOS; IndiaMART Rs 290-375 **[unverified]**) ~= **Rs 1.1-1.6 k total with in-robot charging**, versus LiPo Rs 1,629-2,599 + iMAX charger Rs 2,079. This is the Open Duck design and it is also what Open Duck builders had to fix (voltage sag -> bus CRC errors with weak cells, 02 §7 #2): buy 25-30 A cells.
8. **Not budgeted anywhere:** (a) **spare servos** — 0 in every table; 2 spares = +Rs 4,318; (b) **teleop input** — the Open Duck runtime expects an Xbox controller over Bluetooth (02 §6.5); Rs 0 with keyboard-over-SSH (the video robot is keyboard-teleoperated), Rs 1.5-4 k for a BT gamepad **[unverified]**; (c) **TPU for soles** Rs 1,000-1,500 **[unverified]** (04 Critic additions item 6); (d) heat-set insert tip ~Rs 500 est.; (e) courier Rs 60-150 per order **[unverified]**.
9. **Pi 3 A+ (§3) is 65 x 56 mm class and needs a different head tray than the Zero 2 W (65 x 30 mm):** the official mechanical drawing is at https://pip-assets.raspberrypi.com/categories/512-raspberry-pi-3-model-a/documents/RP-008330-DS-1-raspberry-pi-3-a-plus-mechanical-drawing.pdf (fetched; vector-only, numbers not machine-readable in this session — **read outline and hole grid off the drawing before CAD**).
10. **§1.1 / §12: robu SKU R258500 variant is still unverified** (robu 403 for the critic too). Safer sequence: buy **2 x C001 from Evelta** (Rs 2,224, variant confirmed, 24 h dispatch), measure no-load speed at 7.4 / 8.4 V and read the max-voltage register, then buy 12 more from the same vendor in one order.
11. **Revised realistic totals (critic's arithmetic on this file's line items):** Minimum-viable with Pi 3 A+, 18650 pack instead of LiPo, +3 x 6804 (Rs 450 est.), +insert tip (Rs 500 est.), +TPU (Rs 1,200 est.): **~Rs 45.5-47 k**. Same + 2 spare servos: **~Rs 50-51.5 k (over)**. The Rs 50 k cap holds only with exactly 14 servos, 18650 power, no camera, no Pi 5 and domestically sourced servos — i.e. the reference design's own choices.
