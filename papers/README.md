# 论文清单（Edgecsi-project）

本项目主题：**基于 WiFi 信道状态信息（CSI）的室内无设备感知与行为识别**。
本目录汇总相关论文：完整 BibTeX 见 [`references.bib`](references.bib)，关键论文 PDF 见 [`pdf/`](pdf/)。

## 一、综述 / 教程（先读这些建立全貌）

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Yousefi et al., *A Survey on Behavior Recognition Using WiFi CSI*, IEEE Comm. Mag. | 2017 | 最早的系统性综述，介绍 CSI 感知原理与流程 | [1708.07129.pdf](pdf/1708.07129.pdf)（arXiv 开放版） |
| Tan et al., *A Survey of Commodity WiFi Sensing in 10 Years* | 2021 | 近十年商用 WiFi 感知的现状、挑战与机会 | [2111.07038.pdf](pdf/2111.07038.pdf) |
| Yang et al., *SenseFi: A Library and Benchmark on Deep-Learning-Empowered WiFi Human Sensing* | 2022 | 开源库 + 基准，**建议作为代码起点** | [2207.07859.pdf](pdf/2207.07859.pdf) |
| Radwan et al., *A Tutorial-cum-Survey on Self-Supervised Learning for Wi-Fi Sensing* | 2025 | 自监督学习用于 WiFi 感知的趋势与展望（前沿方法） | [2506.12052.pdf](pdf/2506.12052.pdf) |

## 二、经典奠基

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Wang et al., *CARM: Understanding and Modeling of WiFi Signal Based HAR*, MobiCom | 2015 | CSI 速度模型 + 活动识别的奠基工作 | — |
| Zhang et al., *WiSpeed: Statistical Electromagnetic Approach for Device-Free Speed Estimation* | 2017 | 速度估计与统计电磁模型 | [1712.00348.pdf](pdf/1712.00348.pdf) |
| Ma et al., *SignFi: Sign Language Recognition Using WiFi*, IMWUT | 2018 | 手语识别（276 类细粒度） | — |
| Zheng et al., *Zero-Effort Cross-Domain Gesture Recognition with Wi-Fi (Widar)*, MobiSys | 2019 | 跨域手势识别，Widar3.0 前身 | — |

## 三、预处理 / 相位净化

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Diaz et al., *Channel Phase Processing in Wireless Networks for HAR* | 2023 | 相位净化（去线性相位）用于活动识别 | [2303.16873.pdf](pdf/2303.16873.pdf) |
| Rhodes et al., *WiRM: Respiration Monitoring Using Conjugate CSI* | 2025 | 共轭相乘（CSI ratio）抗时变相位误差 | [2507.23419.pdf](pdf/2507.23419.pdf) |
| Hanahara et al., *Frame-Capture-Based CSI Recomposition (Firmware-Agnostic)* | 2021 | 与固件无关的 CSI 重构 | [2110.15660.pdf](pdf/2110.15660.pdf) |

## 四、数据集 / 基准

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Zhu et al., *CSI-Bench: Large-Scale In-the-Wild Dataset for Multi-task WiFi Sensing* | 2025 | 大规模多任务感知基准，**必读以定位 SOTA** | [2505.21866.pdf](pdf/2505.21866.pdf) |
| Yang et al., *MM-Fi: Multi-Modal Non-Intrusive 4D Human Dataset* | 2023 | WiFi+mmWave+LiDAR+RGB 多模态数据集 | [2305.10345.pdf](pdf/2305.10345.pdf) |
| Huang et al., *WiMANS: Benchmark for WiFi-based Multi-user Activity Sensing* | 2024 | 多用户活动基准 | [2402.09430.pdf](pdf/2402.09430.pdf) |
| Euchner et al., *ESPARGOS: Phase-Coherent WiFi CSI Datasets* | 2024 | 相位相干的 CSI 数据集 | [2408.16377.pdf](pdf/2408.16377.pdf) |
| Wang et al., *Wi-Fi Sensing Tool Release: 802.11ax CSI from Commercial AP* | 2025 | 802.11ax 商业 AP 提取 CSI 工具 | [2506.16957.pdf](pdf/2506.16957.pdf) |

## 五、深度学习模型与方法

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Showmik et al., *PCA-based Wavelet CNN for CSI HAR* | 2022 | PCA + 小波 CNN | [2212.13161.pdf](pdf/2212.13161.pdf) |
| Khan et al., *Contactless HAR using Deep Learning with SDR* | 2023 | 软件无线电 + 深度学习的接触式/非接触式 HAR | — |
| Yang et al., *EfficientFi: Lightweight WiFi Sensing via CSI Compression* | 2022 | 轻量化/边缘感知 | [2204.04138.pdf](pdf/2204.04138.pdf) |
| Strohmayer et al., *WiFlexFormer: Efficient WiFi-Based Person-Centric Sensing* | 2024 | Transformer 架构 | [2411.04224.pdf](pdf/2411.04224.pdf) |
| Hou et al., *RFBoost: Deep WiFi Sensing via Physical Data Augmentation* | 2024 | 物理数据增强 | [2410.07230.pdf](pdf/2410.07230.pdf) |
| Wang et al., *WiFi Sensing via Reservoir Computing* | 2026 | 储备池计算（轻量时序建模） | — |

## 六、跨域 / 泛化（难点热点）

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Strohmayer et al., *DATTA: Domain-Adversarial Test-Time Adaptation* | 2024 | 测试时域适应 | [2411.13284.pdf](pdf/2411.13284.pdf) |
| Strohmayer et al., *Data Augmentation for Cross-Domain WiFi CSI HAR* | 2024 | 跨域数据增强 | [2401.00964.pdf](pdf/2401.00964.pdf) |
| Hasanzadeh et al., *DoRF: Doppler Radiance Fields for Robust HAR* | 2025 | 多普勒辐射场 | [2507.12132.pdf](pdf/2507.12132.pdf) |
| Radwan et al., *MU-SHOT-Fi: Self-Supervised Multi-User Wi-Fi Sensing* | 2026 | 多用户无源域适应 | — |
| Wang et al., *Robust Cross-Domain WiFi Fall Detection (Physics-Driven Transformer)* | 2026 | 跌倒检测 + 跨域 | [2605.00869.pdf](pdf/2605.00869.pdf) |

## 七、手势 / 身份 / 其它

| 引用 | 年份 | 说明 | PDF |
|---|---|---|---|
| Islam et al., *Wi-Fringe: Text Semantics in Named Gesture Recognition* | 2019 | 手势识别 | — |
| Avola et al., *Wi-Fi Passive Person Re-Identification based on CSI* | 2019 | 身份重识别 | — |
| Kong et al., *CIRSense: Rethinking WiFi Sensing with Channel Impulse Response* | 2025 | 用 CIR（而非 CFR）做感知 | — |
| Chen et al., *The Universal Language of CSI: Unifying Wireless Sensing Across Devices* | 2026 | 跨设备/跨环境统一表征 | — |

---

## 使用建议

1. **先读综述**（第一组 4 篇）建立全貌；
2. **定任务与数据集**：优先 CSI-Bench（多任务）或 UT-HAR（入门）；
3. **代码起点**：SenseFi 开源库；
4. **创新方向**：重点看"跨域/泛化"与"自监督"两组；
5. 全部引用可直接用 [`references.bib`](references.bib) 导入 Zotero / LaTeX。

> 注：表中"PDF —"表示该文为 IEEE/ACM 正式发表版本（非开放获取），可通过 DOI 从出版社获取；
> 其余 arXiv 版本 PDF 已下载到 `pdf/` 目录。
