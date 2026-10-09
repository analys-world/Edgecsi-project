#!/usr/bin/env python3
"""viz_csi.py — CSI 可视化分析（Intel 5300 / ESP32 通用）。

用法:
    ~/.dsh/venvs/sci/bin/python viz_csi.py <数据文件> [--fs 采样率] [--out 输出图]

支持输入:
    *.npz  —— 统一中间格式（推荐，由 parse_to_npz.py 生成）
    *.dat  —— Intel 5300 CSI Tool 原始文件（需 csiread）
    *.csv  —— ESP32-CSI-Tool 原始文件（需 pandas）

输出:
    csi_overview.png —— 幅度时序列 + 幅度热力图 + STFT 频谱图
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")  # 无显示环境也能存图
import matplotlib.pyplot as plt
from scipy import signal

# 中文字体（避免图上中文变方框）
plt.rcParams["font.sans-serif"] = [
    "Noto Sans CJK SC", "Noto Sans CJK JP", "WenQuanYi Zen Hei",
    "Droid Sans Fallback", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


# ──────────────────────────────────────────────────────────────────────────────
# 读取
# ──────────────────────────────────────────────────────────────────────────────

def load_npz(path: str):
    d = np.load(path, allow_pickle=True)
    csi = d["csi"]
    ts = d["timestamp"] if "timestamp" in d else np.arange(csi.shape[0], dtype=float)
    rssi = d["rssi"] if "rssi" in d else None
    return csi, ts, rssi


def load_intel(path: str, nrx: int = 3, ntx: int = 2, pl_size: int = 10):
    import csiread
    d = csiread.Intel(path, nrxnum=nrx, ntxnum=ntx, pl_size=pl_size)
    d.read()
    csi = d.get_scaled_csi()  # (packets, rx, tx, 30)
    ts = np.arange(csi.shape[0], dtype=float)
    return csi, ts, None


def load_esp32(path: str):
    import pandas as pd
    df = pd.read_csv(path, header=None, skiprows=0, on_bad_lines="skip")
    # ESP32-CSI-Tool 每行以 CSI_DATA 开头，CSI 数组在行尾
    # 用 pandas 读入后，取数值列中的后半段作为 CSI（兼容性优先）
    num = df.apply(pd.to_numeric, errors="coerce")
    if num.shape[1] < 8:
        raise ValueError("CSV 列数过少，可能不是 ESP32-CSI-Tool 输出")
    # 取最后 64 列中的有效数值作为 CSI（长度视配置而定）
    csi = num.iloc[:, -64:].to_numpy(dtype=float)
    csi = np.nan_to_num(csi)
    ts = np.arange(csi.shape[0], dtype=float)
    return csi, ts, None


def load_any(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".npz":
        return load_npz(path)
    if ext == ".dat":
        return load_intel(path)
    if ext == ".csv":
        return load_esp32(path)
    raise ValueError(f"不支持的格式: {ext}")


# ──────────────────────────────────────────────────────────────────────────────
# 画图
# ──────────────────────────────────────────────────────────────────────────────

def flatten_csi(csi: np.ndarray) -> np.ndarray:
    """(packets, ...) → (packets, subcarriers)。"""
    csi = np.asarray(csi)
    if csi.ndim == 2:
        return csi
    return csi.reshape(csi.shape[0], -1)


def plot_csi(csi, ts, rssi=None, fs=None, title="CSI", out="csi_overview.png",
             max_subcarriers=5):
    csi = flatten_csi(csi)
    amp = np.abs(csi)
    t = np.asarray(ts, dtype=float)
    t = t - t[0]
    if fs is None or fs <= 0:
        fs = (len(t) - 1) / t[-1] if len(t) > 1 and t[-1] > 0 else 1.0
    print(f"[viz] packets={csi.shape[0]} subcarriers={csi.shape[1]} fs≈{fs:.2f} Hz")

    n_panels = 3 + (1 if rssi is not None else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=(12, 3 * n_panels), sharex=False)
    if n_panels == 1:
        axes = [axes]

    # 1) 幅度时序列
    ax = axes[0]
    for k in range(min(max_subcarriers, amp.shape[1])):
        ax.plot(t, amp[:, k], lw=0.8, label=f"sc{k}")
    ax.set_ylabel("|H|")
    ax.set_title(title)
    ax.legend(fontsize=7, ncol=min(max_subcarriers, 5))
    ax.grid(alpha=0.3)

    # 2) 幅度热力图（子载波 × 时间）
    ax = axes[1]
    im = ax.imshow(amp.T, aspect="auto", origin="lower",
                   extent=[t[0], t[-1], 0, amp.shape[1]], cmap="viridis")
    ax.set_ylabel("subcarrier")
    ax.set_title("幅度热力图 (subcarrier × time)")
    plt.colorbar(im, ax=ax, label="|H|")

    # 3) STFT 频谱图（子载波平均）
    ax = axes[2]
    x = amp.mean(axis=1)
    x = x - x.mean()
    nperseg = int(min(256, max(16, len(x) // 8)))
    f, tt, Z = signal.stft(x, fs=fs, nperseg=nperseg,
                           noverlap=nperseg // 2, window="hann")
    im2 = ax.pcolormesh(t[0] + tt, f, 20 * np.log10(np.abs(Z) + 1e-9), shading="auto")
    ax.set_ylabel("frequency (Hz)")
    ax.set_xlabel("time (s)")
    ax.set_title("STFT 频谱图")
    plt.colorbar(im2, ax=ax, label="dB")

    # 4) 可选 RSSI
    if rssi is not None:
        ax = axes[3]
        ax.plot(t, np.asarray(rssi), lw=0.8, color="tab:red")
        ax.set_ylabel("RSSI (dBm)")
        ax.set_xlabel("time (s)")
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"[viz] 已保存: {out}")
    return out


def main():
    ap = argparse.ArgumentParser(description="CSI 可视化分析")
    ap.add_argument("path", help="输入文件 (.npz / .dat / .csv)")
    ap.add_argument("--fs", type=float, default=0.0, help="采样率 Hz（不填则自动估算）")
    ap.add_argument("--out", default="csi_overview.png", help="输出图片路径")
    ap.add_argument("--title", default=None, help="图标题")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print(f"文件不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    csi, ts, rssi = load_any(args.path)
    title = args.title or os.path.basename(args.path)
    plot_csi(csi, ts, rssi=rssi, fs=args.fs, title=title, out=args.out)


if __name__ == "__main__":
    main()
