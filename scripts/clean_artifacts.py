"""产物清理 — 同一主版本号下只保留最新 N 个（默认 2）。

用法:
    python clean_artifacts.py --dir products --keep 2 --pattern "FanControl_v*.zip"
    python clean_artifacts.py --dir docs --keep 2 --pattern "v*/" --group-major
    python clean_artifacts.py --dir installer --keep 2 --pattern "FanControl_Setup_v*.exe"

规则:
    - 按文件名中的版本号排序（x.y.z），保留最新的 keep 个
    - --group-major: 按主版本号分组，每组保留 keep 个（默认保留最新 keep 组内最新）
    - 目录模式（--pattern "v*/"）对匹配的目录递归删除
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

VERSION_RE = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")


def version_key(name: str) -> tuple[int, int, int]:
    m = VERSION_RE.search(name)
    if not m:
        return (0, 0, 0)
    return tuple(int(x) for x in m.groups())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True, help="目标目录")
    ap.add_argument("--keep", type=int, default=2, help="保留数量（默认 2）")
    ap.add_argument("--pattern", default="*", help="文件名 glob（默认全部）")
    ap.add_argument("--group-major", action="store_true",
                    help="按主版本号分组保留（每组保留最新 keep 个）")
    args = ap.parse_args()

    d = Path(args.dir)
    if not d.exists():
        print(f"目录不存在: {d}")
        return 1

    is_dir_pattern = args.pattern.endswith("/")
    pat = args.pattern.rstrip("/")
    items = [p for p in d.iterdir()
             if (p.is_dir() if is_dir_pattern else p.is_file())
             and p.match(pat)]
    if not items:
        print(f"无匹配项: {d} 匹配 {args.pattern}")
        return 0

    if args.group_major:
        groups: dict[int, list[Path]] = {}
        for p in items:
            m = VERSION_RE.search(p.name)
            major = int(m.group(1)) if m else 0
            groups.setdefault(major, []).append(p)
        to_delete: list[Path] = []
        for major, members in sorted(groups.items()):
            members.sort(key=lambda p: version_key(p.name))
            to_delete.extend(members[:-args.keep])
            if members[:-args.keep]:
                print(f"主版本 {major}: 保留 {len(members[-args.keep:])} 个，"
                      f"删除 {len(members[:-args.keep])} 个")
    else:
        items.sort(key=lambda p: version_key(p.name))
        to_delete = items[:-args.keep]
        if to_delete:
            print(f"保留 {len(items[-args.keep:])} 个: "
                  + ", ".join(p.name for p in items[-args.keep:]))

    for p in to_delete:
        if p.is_dir():
            shutil.rmtree(p)
            print(f"  删目录: {p}")
        else:
            p.unlink()
            print(f"  删文件: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
