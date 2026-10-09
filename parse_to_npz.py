#!/usr/bin/env python3
"""parse_to_npz.py — 把原始 CSI 采集文件转成统一中间格式 .npz。

用法:
    # Intel 5300 (.dat)
    ~/.dsh/venvs/sci/bin/python parse_to_npz.py --link intel --in csi.dat --out out.npz

    # ESP32-CSI-Tool (.csv)
    ~/.dsh/venvs/sci/bin/python parse_to_npz.py --link esp32 --in esp32.csv --out out.npz

统一格式 (.npz) 内容:
    csi        (packets, ..., subcarriers)  complex64
    timestamp  (packets,)                   采集时间戳（Unix 秒）
    rssi       (packets,)                   可选
    meta_json  实验元数据（JSON 字符串）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np


def parse_intel(path: str, nrx: int, ntx: int, pl_size: int):
    import csiread
    d = csiread.Intel(path, nrxnum=nrx, ntxnum=ntx, pl_size=pl_size)
    d.read()
    csi = d.get_scaled_csi()          # (packets, rx, tx, 30)
    rssi = getattr(d, "rssi_a", None)
    ts = np.arange(csi.shape[0], dtype=float)
    return csi, ts, rssi


def parse_esp32(path: str, csi_cols: int):
    import pandas as pd
    df = pd.read_csv(path, header=None, on_bad_lines="skip")
    num = df.apply(pd.to_numeric, errors="coerce")
    csi = np.nan_to_num(num.iloc[:, -csi_cols:].to_numpy(dtype=float))
    ts = np.arange(csi.shape[0], dtype=float)
    return csi, ts, None


def main():
    ap = argparse.ArgumentParser(description="原始 CSI → 统一 .npz")
    ap.add_argument("--link", required=True, choices=["intel", "esp32"])
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nrx", type=int, default=3, help="Intel: 接收天线数")
    ap.add_argument("--ntx", type=int, default=2, help="Intel: 发送天线数")
    ap.add_argument("--pl-size", type=int, default=10, help="Intel: payload 长度")
    ap.add_argument("--csi-cols", type=int, default=64, help="ESP32: 行尾 CSI 列数")
    ap.add_argument("--meta", default="{}", help="额外元数据 JSON")
    args = ap.parse_args()

    if not os.path.exists(args.inp):
        print(f"输入不存在: {args.inp}", file=sys.stderr)
        sys.exit(1)

    if args.link == "intel":
        csi, ts, rssi = parse_intel(args.inp, args.nrx, args.ntx, args.pl_size)
    else:
        csi, ts, rssi = parse_esp32(args.inp, args.csi_cols)

    meta = {
        "link": args.link,
        "source_file": os.path.basename(args.inp),
        "parsed_at": datetime.now().isoformat(timespec="seconds"),
    }
    try:
        meta.update(json.loads(args.meta))
    except json.JSONDecodeError:
        pass

    payload = {"csi": csi.astype(np.complex64), "timestamp": np.asarray(ts, dtype=float),
               "meta_json": json.dumps(meta, ensure_ascii=False)}
    if rssi is not None:
        payload["rssi"] = np.asarray(rssi)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    np.savez_compressed(args.out, **payload)
    print(f"[parse] {args.link}: csi={csi.shape} → {args.out}")


if __name__ == "__main__":
    main()
