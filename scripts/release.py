"""发布链助手 — 版本检查 / 提交链校验 / 产物验证。

用法:
    python release.py check-version installer/setup.iss     # 读取当前版本
    python release.py verify products/FanControl_vX.Y.Z_DeployPack.zip  # 验证 zip 完整性
    python release.py verify-installer installer/FanControl_Setup_vX.Y.Zbeta.exe  # 检查 exe
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

VERSION_RE = re.compile(r"#define MyAppVersion \"(\d+\.\d+\.\d+)\"")
SUFFIX_RE = re.compile(r"#define MyAppVersionSuffix \"(\w+)\"")


def read_iss_version(iss: Path) -> str:
    txt = iss.read_text(encoding="utf-8")
    v = VERSION_RE.search(txt)
    s = SUFFIX_RE.search(txt)
    if not v:
        raise ValueError(f"未找到 MyAppVersion: {iss}")
    return v.group(1) + (s.group(1) if s else "")


def check_version(iss: Path):
    print(f"setup.iss 版本: v{read_iss_version(iss)}beta"
          if "beta" not in read_iss_version(iss) else f"setup.iss 版本: v{read_iss_version(iss)}")


def verify_zip(zip_path: Path):
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        print(f"{zip_path.name}: {len(zf.infolist())} 条目, "
              f"完整性 {'OK' if bad is None else 'CORRUPT: ' + str(bad)}")
        for i in zf.infolist():
            print(f"  {i.filename}  {i.file_size//1024}KB")


def verify_installer(exe: Path, min_mb: int = 50):
    if not exe.exists():
        print(f"❌ 不存在: {exe}")
        return 1
    mb = exe.stat().st_size / 1e6
    ok = mb >= min_mb
    print(f"{exe.name}: {mb:.1f}MB {'✓' if ok else f'❌ 小于 {min_mb}MB'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check-version").add_argument("iss")
    vp = sub.add_parser("verify").add_argument("zip")
    ip = sub.add_parser("verify-installer")
    ip.add_argument("exe")
    ip.add_argument("--min-mb", type=int, default=50)
    args = ap.parse_args()

    if args.cmd == "check-version":
        check_version(Path(args.iss))
    elif args.cmd == "verify":
        verify_zip(Path(args.zip))
    elif args.cmd == "verify-installer":
        return verify_installer(Path(args.exe), args.min_mb)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
