"""文档编译脚本 — Markdown → LaTeX → PDF（中文）。

用法:
    python build_docs.py <md文件> [副标题]

流程: pandoc --standalone --toc → xelatex ×3（中文必需 xelatex）
依赖: pandoc + MiKTeX/TeX Live（xelatex）
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_NAME = sys.argv[1] if len(sys.argv) > 1 else "spec.md"
SUB_TITLE = sys.argv[2] if len(sys.argv) > 2 else MD_NAME.replace(".md", "")

MD_FILE = BASE / MD_NAME
TEX_FILE = BASE / MD_NAME.replace(".md", ".tex")
PDF_FILE = BASE / MD_NAME.replace(".md", ".pdf")

DOC_TITLE = "<项目名>"
DOC_VERSION = "vX.Y"
DOC_DATE = "<YYYY-MM-DD>"
DOC_STATUS = "已完成"

PANDOC_ARGS = [
    "--standalone", "--toc", "--toc-depth=2",
    "--number-sections",
    "--syntax-highlighting=pygments",
    "-V", "documentclass=ctexart",
    "-V", "geometry=left=2cm,right=2cm,top=2.5cm,bottom=2.5cm",
    "-V", "mainfont=SimHei",
    "-V", "monofont=Courier New",
    "-V", f"title={DOC_TITLE}",
    "-V", f"subtitle={SUB_TITLE}",
    "-V", f"date={DOC_DATE}",
    "-V", f"version={DOC_VERSION}",
    "-V", f"status={DOC_STATUS}",
    "-V", "colorlinks=true",
    "-V", "linkcolor=blue",
    "-V", "urlcolor=blue",
    "-V", "toccolor=blue",
    "-V", "header-includes=\\usepackage{booktabs}",
    "--pdf-engine=xelatex",
    "-o", str(TEX_FILE),
    str(MD_FILE),
]


def run(cmd: list[str]) -> bool:
    print(f"  $ {' '.join(cmd[:2])}...")
    try:
        return subprocess.run(cmd, check=True).returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"  失败 (rc={e.returncode})")
        return False
    except FileNotFoundError:
        print("  未找到命令（检查 pandoc/xelatex 是否安装）")
        return False


def main() -> int:
    if not MD_FILE.exists():
        print(f"MD 文件不存在: {MD_FILE}")
        return 1
    print("=== Step 1: pandoc → tex ===")
    if not run(["pandoc", *PANDOC_ARGS]):
        return 1
    print("=== Step 2: xelatex ×3 ===")
    for i in range(1, 4):
        print(f"  Pass {i}:")
        if not run(["xelatex", "-interaction=nonstopmode", str(TEX_FILE)]):
            return 1
    if not PDF_FILE.exists():
        print("PDF 未生成")
        return 1
    print(f"✓ PDF: {PDF_FILE.name} ({PDF_FILE.stat().st_size // 1024} KB)")
    # 清理辅助文件，保留 .tex
    for ext in [".aux", ".log", ".out", ".toc"]:
        p = PDF_FILE.with_suffix(ext)
        p.unlink(missing_ok=True)
    print("=== Step 3: cleanup ===")
    print("OK (retained .tex)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
