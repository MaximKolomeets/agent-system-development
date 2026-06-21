#!/usr/bin/env python3
"""Генерирует docs/agent-system/cloud/ из manifest orchestrator_context_bundle."""

from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml"
README_NAME = "README.md"


@dataclass
class BundleEntry:
    path: str
    cloud_flatname: str


@dataclass
class BundleConfig:
    generated_dir: str
    max_files: int
    files: list[BundleEntry]


def _strip(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_bundle(text: str) -> BundleConfig:
    generated_dir = ""
    max_files = 25
    files: list[BundleEntry] = []
    current: dict[str, str] | None = None
    in_bundle = False
    in_files = False

    for line in text.splitlines():
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*$", line):
            if current:
                files.append(_entry_from_raw(current))
                current = None
            in_bundle = line.strip() == "orchestrator_context_bundle:"
            in_files = False
            continue

        if not in_bundle:
            continue

        match = re.match(r"  ([a-z_]+):\s*(.*)$", line)
        if match:
            key, raw_value = match.groups()
            value = _strip(raw_value)
            if key == "files":
                in_files = True
            elif key == "generated_dir":
                generated_dir = value
                in_files = False
            elif key == "max_files" and value:
                max_files = int(value)
                in_files = False
            else:
                in_files = False
            continue

        if not in_files:
            continue

        match = re.match(r"    - path:\s*(.+)$", line)
        if match:
            if current:
                files.append(_entry_from_raw(current))
            current = {"path": _strip(match.group(1))}
            continue

        match = re.match(r"      cloud_flatname:\s*(.+)$", line)
        if match and current is not None:
            current["cloud_flatname"] = _strip(match.group(1))

    if current:
        files.append(_entry_from_raw(current))

    if not generated_dir:
        raise ValueError("orchestrator_context_bundle.generated_dir is missing")
    if not files:
        raise ValueError("orchestrator_context_bundle.files is empty")

    return BundleConfig(generated_dir=generated_dir, max_files=max_files, files=files)


def _entry_from_raw(raw: dict[str, str]) -> BundleEntry:
    path = raw.get("path", "")
    if not path:
        raise ValueError("Bundle entry without path")
    flatname = raw.get("cloud_flatname") or Path(path).name
    validate_flatname(flatname)
    return BundleEntry(path=path, cloud_flatname=flatname)


def validate_flatname(flatname: str) -> None:
    if not flatname or "/" in flatname or "\\" in flatname or flatname in {".", ".."}:
        raise ValueError(f"Invalid cloud_flatname: {flatname!r}")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", flatname):
        raise ValueError(f"cloud_flatname contains unsupported characters: {flatname!r}")


def validate_bundle(config: BundleConfig) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for entry in config.files:
        source = ROOT / entry.path
        if not source.is_file():
            errors.append(f"Missing bundle source file: {entry.path}")
        previous = seen.get(entry.cloud_flatname)
        if previous:
            errors.append(f"cloud_flatname collision: {entry.cloud_flatname} for {previous} and {entry.path}")
        seen[entry.cloud_flatname] = entry.path

    # README входит в лимит загрузки, потому что архитектор обычно грузит cloud/ целиком.
    total_cloud_files = len(config.files) + 1
    if total_cloud_files > config.max_files:
        errors.append(f"Cloud bundle has {total_cloud_files} files, limit is {config.max_files}")
    return errors


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def freshness() -> tuple[str, str]:
    origin_developer = git_output("rev-parse", "--verify", "origin/developer")
    if origin_developer:
        base = git_output("merge-base", "HEAD", "origin/developer") or origin_developer
    else:
        base = git_output("rev-parse", "HEAD")
    asof = git_output("show", "-s", "--format=%cI", base)
    return asof, base


def render_readme(config: BundleConfig, asof: str, developer_head_sha: str) -> bytes:
    lines: list[str] = [
        "# Orchestrator Context Cloud Bundle",
        "",
        "AUTO-GENERATED — не править руками; регенерировать через `python docs/agent-system/tools/gen_cloud_bundle.py`.",
        "",
        "## Freshness",
        "",
        f"- asof: `{asof}`",
        f"- developer_head_sha: `{developer_head_sha}`",
        f"- file_count_including_readme: `{len(config.files) + 1}`",
        "",
        "## Контракт",
        "",
        "- Источник состава: `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle`.",
        "- Каждый файл ниже является flat copy текущего repo content из origin path.",
        "- Проверка drift: `python docs/agent-system/tools/gen_cloud_bundle.py --check`.",
        "",
        "## Состав",
        "",
        "| origin path | cloud filename |",
        "| --- | --- |",
    ]
    for entry in config.files:
        lines.append(f"| `{entry.path}` | `{entry.cloud_flatname}` |")

    lines.extend(
        [
            "",
            "## Upload how-to",
            "",
            "### ChatGPT / browser upload",
            "",
            "1. Открыть `docs/agent-system/cloud/`.",
            "2. Загрузить все файлы из папки целиком, если интерфейс допускает текущий `file_count_including_readme`.",
            "3. Если нужен incremental refresh, загрузить только изменённые flat-файлы из per-task handoff и этот `README.md`.",
            "",
            "### Google Drive for Desktop",
            "",
            "1. Архитектор настраивает Google Drive for Desktop в своей пользовательской сессии.",
            "2. Создаёт папку Drive, например `Agent System / orchestrator-context-cloud`.",
            "3. Копирует содержимое `docs/agent-system/cloud/` в эту папку штатными средствами ОС.",
            "4. Проверяет в Drive UI, что количество файлов совпадает с `file_count_including_readme`.",
            "",
            "### rclone template",
            "",
            "Engine не выполняет авторизацию и не создаёт token files. Команды ниже — шаблон для архитектора после самостоятельной настройки remote:",
            "",
            "```text",
            "rclone config",
            "rclone copy docs/agent-system/cloud/ <drive-remote>:orchestrator-context-cloud --dry-run",
            "rclone copy docs/agent-system/cloud/ <drive-remote>:orchestrator-context-cloud",
            "```",
            "",
            "`<drive-remote>` — имя remote, созданное архитектором локально. Credentials/tokens не хранить в repository.",
            "",
        ]
    )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def expected_snapshot(config: BundleConfig) -> dict[str, bytes]:
    asof, developer_head_sha = freshness()
    snapshot: dict[str, bytes] = {}
    for entry in config.files:
        snapshot[entry.cloud_flatname] = (ROOT / entry.path).read_bytes()
    snapshot[README_NAME] = render_readme(config, asof, developer_head_sha)
    return dict(sorted(snapshot.items()))


def cloud_dir(config: BundleConfig) -> Path:
    return ROOT / config.generated_dir


def write_snapshot(config: BundleConfig, snapshot: dict[str, bytes]) -> None:
    output_dir = cloud_dir(config)
    output_dir.mkdir(parents=True, exist_ok=True)

    for existing in output_dir.iterdir():
        if existing.is_dir():
            raise RuntimeError(f"Unexpected subdirectory in flat cloud bundle: {existing}")
        if existing.name not in snapshot:
            existing.unlink()

    for name, content in snapshot.items():
        (output_dir / name).write_bytes(content)


def check_snapshot(config: BundleConfig, snapshot: dict[str, bytes]) -> int:
    errors = 0
    output_dir = cloud_dir(config)
    actual_files = {path.name: path for path in output_dir.iterdir()} if output_dir.exists() else {}
    expected_names = set(snapshot)

    extra = sorted(set(actual_files) - expected_names)
    missing = sorted(expected_names - set(actual_files))
    if extra or missing:
        errors += 1
        print("Cloud bundle file set drift detected:", file=sys.stderr)
        for name in missing:
            print(f"- missing: {name}", file=sys.stderr)
        for name in extra:
            print(f"- extra: {name}", file=sys.stderr)

    for name in sorted(expected_names & set(actual_files)):
        actual = actual_files[name].read_bytes()
        expected = snapshot[name]
        if actual == expected:
            continue
        errors += 1
        print(f"Cloud bundle content drift detected: {name}", file=sys.stderr)
        print(_byte_diff(actual, expected, str(actual_files[name]), f"regenerated {name}"), file=sys.stderr)

    return 1 if errors else 0


def _byte_diff(actual: bytes, expected: bytes, fromfile: str, tofile: str) -> str:
    actual_text = actual.decode("utf-8", errors="replace").splitlines(keepends=True)
    expected_text = expected.decode("utf-8", errors="replace").splitlines(keepends=True)
    return "".join(difflib.unified_diff(actual_text, expected_text, fromfile=fromfile, tofile=tofile))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate docs/agent-system/cloud/ from orchestrator_context_bundle.")
    parser.add_argument("--check", action="store_true", help="Check cloud bundle drift and source file existence.")
    args = parser.parse_args(argv)

    config = parse_bundle(MANIFEST.read_text(encoding="utf-8"))
    validation_errors = validate_bundle(config)
    if validation_errors:
        for error in validation_errors:
            print(error, file=sys.stderr)
        return 1

    snapshot = expected_snapshot(config)
    if args.check:
        return check_snapshot(config, snapshot)

    write_snapshot(config, snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
