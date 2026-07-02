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
README_NAME = "00_README.md"
README_INFORMATIONAL_LINE_PATTERNS = (
    (r"(?m)^- asof: `[^`\n]*`$", "- asof: `<informational>`"),
    (r"(?m)^- developer_head_sha: `[^`\n]*`$", "- developer_head_sha: `<informational>`"),
)
LANG_BY_EXTENSION = {
    ".json": "json",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
}
CANONICAL_BUNDLE_ORDER = [
    "docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md",
    "docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md",
    "docs/agent-system/templates/TASK_HEADER_COMMON.md",
    "docs/agent-system/BRANCH_POLICY.md",
    "docs/agent-system/ENGINE_JOURNAL_CONTRACT.md",
    "docs/agent-system/CURRENT_STATE.md",
    "docs/agent-system/engine-journal/INDEX.md",
    "docs/agent-system/NEXT_STEPS.md",
    "docs/agent-system/ENGINE_ENTRYPOINT.md",
    "docs/agent-system/PROJECT_FILE_MAP.md",
    "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml",
    "docs/agent-system/REVIEW_AUTOLOOP.md",
    "docs/agent-system/TASK_CONTRACT.md",
    "docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md",
    "docs/agent-system/JOURNAL_FINALIZATION_POLICY.md",
    "docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md",
    "docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md",
    "docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md",
    "docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md",
    "docs/agent-system/LANGUAGE_POLICY.md",
    "docs/agent-system/TIME_ACCOUNTING_POLICY.md",
    "docs/agent-system/COST_TRACKING_POLICY.md",
    "docs/agent-system/METRICS.md",
]


@dataclass
class BundleEntry:
    priority: int
    path: str
    cloud_flatname: str
    category: str

    @property
    def cloud_name(self) -> str:
        source_suffix = Path(self.path).suffix.lower()
        flat_path = Path(self.cloud_flatname)
        flat_base = flat_path.stem if flat_path.suffix else flat_path.name
        if source_suffix and source_suffix != ".md":
            ext_suffix = f"_{source_suffix.lstrip('.').lower()}"
        else:
            ext_suffix = ""
        return f"{self.priority:02d}_{flat_base}{ext_suffix}.md"


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
    raw_files: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_bundle = False
    in_files = False

    for line in text.splitlines():
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*$", line):
            if current:
                raw_files.append(current)
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
                raw_files.append(current)
            current = {"path": _strip(match.group(1))}
            continue

        match = re.match(r"      cloud_flatname:\s*(.+)$", line)
        if match and current is not None:
            current["cloud_flatname"] = _strip(match.group(1))

    if current:
        raw_files.append(current)

    if not generated_dir:
        raise ValueError("orchestrator_context_bundle.generated_dir is missing")
    if not raw_files:
        raise ValueError("orchestrator_context_bundle.files is empty")

    raw_by_path = bundle_files_by_path(raw_files)
    category_by_path = parse_manifest_categories(text)
    files = [
        _entry_from_raw(index, raw, category_by_path)
        for index, raw in enumerate((raw_by_path[path] for path in CANONICAL_BUNDLE_ORDER), start=1)
    ]
    return BundleConfig(generated_dir=generated_dir, max_files=max_files, files=files)


def bundle_files_by_path(raw_files: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    raw_by_path: dict[str, dict[str, str]] = {}
    duplicates: list[str] = []
    for raw in raw_files:
        path = raw.get("path", "")
        if path in raw_by_path:
            duplicates.append(path)
        raw_by_path[path] = raw

    expected = set(CANONICAL_BUNDLE_ORDER)
    actual = set(raw_by_path)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if duplicates or missing or extra:
        parts: list[str] = []
        if duplicates:
            parts.append(f"duplicates: {', '.join(sorted(duplicates))}")
        if missing:
            parts.append(f"missing: {', '.join(missing)}")
        if extra:
            parts.append(f"extra: {', '.join(extra)}")
        raise ValueError("orchestrator_context_bundle.files does not match canonical order set: " + "; ".join(parts))
    return raw_by_path


def parse_manifest_categories(text: str) -> dict[str, str]:
    categories = {
        "source",
        "template",
        "target_generated",
        "history_state",
        "journal",
        "scaffold",
        "generated",
    }
    category_by_path: dict[str, str] = {}
    current: str | None = None
    subkey: str | None = None

    for line in text.splitlines():
        match = re.match(r"  ([a-z_]+):\s*$", line)
        if match:
            name = match.group(1)
            current = name if name in categories else None
            subkey = None
            continue

        if current is None:
            continue

        match = re.match(r"    ([a-z_]+):\s*(.*)$", line)
        if match:
            subkey = match.group(1)
            continue

        if subkey != "files":
            continue

        match = re.match(r"      - path:\s*(.+)$", line)
        if match:
            category_by_path[_strip(match.group(1))] = current
            continue

        match = re.match(r"      - (.+)$", line)
        if match:
            category_by_path[_strip(match.group(1))] = current

    return category_by_path


def _entry_from_raw(priority: int, raw: dict[str, str], category_by_path: dict[str, str]) -> BundleEntry:
    path = raw.get("path", "")
    if not path:
        raise ValueError("Bundle entry without path")
    flatname = raw.get("cloud_flatname") or Path(path).name
    validate_flatname(flatname)
    category = category_for_path(path, category_by_path)
    return BundleEntry(priority=priority, path=path, cloud_flatname=flatname, category=category)


def category_for_path(path: str, category_by_path: dict[str, str]) -> str:
    if path in category_by_path:
        return category_by_path[path]
    for pattern, category in category_by_path.items():
        if pattern.endswith("/**") and path.startswith(pattern[:-3]):
            return category
    return "unlisted"


def validate_flatname(flatname: str) -> None:
    if not flatname or "/" in flatname or "\\" in flatname or flatname in {".", ".."}:
        raise ValueError(f"Invalid cloud_flatname: {flatname!r}")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", flatname):
        raise ValueError(f"cloud_flatname contains unsupported characters: {flatname!r}")


def validate_bundle(config: BundleConfig) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    for expected_priority, entry in enumerate(config.files, start=1):
        source = ROOT / entry.path
        if entry.priority != expected_priority:
            errors.append(f"Priority gap: expected {expected_priority:02d}, got {entry.priority:02d} for {entry.path}")
        if not source.is_file():
            errors.append(f"Missing bundle source file: {entry.path}")
        previous = seen.get(entry.cloud_name)
        if previous:
            errors.append(f"cloud filename collision: {entry.cloud_name} for {previous} and {entry.path}")
        seen[entry.cloud_name] = entry.path
        if not re.fullmatch(r"\d{2}_[A-Za-z0-9._-]+\.md", entry.cloud_name):
            errors.append(f"Invalid numbered cloud filename: {entry.cloud_name}")

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
        "- Все файлы бандла имеют расширение `.md`, чтобы проходить upload-ограничения cloud-оркестратора.",
        "- Нумерация задаёт приоритет: при лимите ниже полного бандла загружать первые N файлов по имени.",
        "- Non-md источники завернуты в fenced-блок с языком исходного формата.",
        "- Проверка drift: `python docs/agent-system/tools/gen_cloud_bundle.py --check`.",
        "",
        "## Приоритетная карта",
        "",
        "| priority | cloud filename | source path | category |",
        "| --- | --- | --- | --- |",
        f"| `00` | `{README_NAME}` | generated bundle guide | generated |",
    ]
    for entry in config.files:
        lines.append(f"| `{entry.priority:02d}` | `{entry.cloud_name}` | `{entry.path}` | `{entry.category}` |")

    lines.extend(
        [
            "",
            "## Частичная загрузка",
            "",
            "Если engine принимает меньше файлов, чем полный бандл, загрузить `00_README.md` и первые N numbered-файлов по лексическому порядку. Двузначный префикс сохраняет правильный порядок при `10+` файлах.",
            "",
            "## Upload how-to",
            "",
            "### Chat UI / browser upload",
            "",
            "1. Открыть `docs/agent-system/cloud/`.",
            "2. Загрузить все `.md` файлы из папки целиком, если интерфейс допускает текущий `file_count_including_readme`.",
            "3. Если нужен incremental refresh, загрузить изменённые numbered-файлы из per-task handoff и этот `00_README.md`.",
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


def render_entry(entry: BundleEntry) -> bytes:
    source = ROOT / entry.path
    suffix = source.suffix.lower()
    if suffix == ".md":
        return source.read_bytes()

    language = LANG_BY_EXTENSION.get(suffix, suffix.lstrip(".") or "text")
    source_text = source.read_text(encoding="utf-8")
    lines = [
        f"# Source: `{entry.path}`",
        "",
        f"```{language}",
        source_text.rstrip(),
        "```",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def expected_snapshot(config: BundleConfig) -> dict[str, bytes]:
    asof, developer_head_sha = freshness()
    snapshot: dict[str, bytes] = {README_NAME: render_readme(config, asof, developer_head_sha)}
    for entry in config.files:
        snapshot[entry.cloud_name] = render_entry(entry)
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

    schema_errors = validate_cloud_schema(actual_files, len(snapshot))
    if schema_errors:
        errors += 1
        print("Cloud bundle filename schema drift detected:", file=sys.stderr)
        for error in schema_errors:
            print(f"- {error}", file=sys.stderr)

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
        actual = normalize_content_for_check(name, actual_files[name].read_bytes())
        expected = normalize_content_for_check(name, snapshot[name])
        if actual == expected:
            continue
        errors += 1
        print(f"Cloud bundle content drift detected: {name}", file=sys.stderr)
        print(_byte_diff(actual, expected, str(actual_files[name]), f"regenerated {name}"), file=sys.stderr)

    return 1 if errors else 0


def validate_cloud_schema(actual_files: dict[str, Path], expected_count: int) -> list[str]:
    errors: list[str] = []
    for name in sorted(actual_files):
        if not name.endswith(".md"):
            errors.append(f"non-md cloud file: {name}")
        if not re.fullmatch(r"\d{2}_[A-Za-z0-9._-]+\.md", name):
            errors.append(f"unnumbered or invalid cloud file: {name}")

    expected_prefixes = {f"{index:02d}" for index in range(expected_count)}
    actual_prefixes = {name[:2] for name in actual_files if re.match(r"^\d{2}_", name)}
    if actual_prefixes != expected_prefixes:
        errors.append(
            "numbering is not continuous: "
            f"expected {', '.join(sorted(expected_prefixes))}; "
            f"actual {', '.join(sorted(actual_prefixes))}"
        )
    return errors


def normalize_content_for_check(name: str, content: bytes) -> bytes:
    content = normalize_eol_for_check(content)
    if name == README_NAME:
        content = normalize_readme_for_check(content)
    return content


def normalize_eol_for_check(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalize_readme_for_check(content: bytes) -> bytes:
    text = normalize_eol_for_check(content).decode("utf-8", errors="replace")
    for pattern, replacement in README_INFORMATIONAL_LINE_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text.encode("utf-8")


def _byte_diff(actual: bytes, expected: bytes, fromfile: str, tofile: str) -> str:
    actual_text = actual.decode("utf-8", errors="replace").splitlines(keepends=True)
    expected_text = expected.decode("utf-8", errors="replace").splitlines(keepends=True)
    return "".join(difflib.unified_diff(actual_text, expected_text, fromfile=fromfile, tofile=tofile))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate numbered .md cloud bundle from orchestrator_context_bundle.")
    parser.add_argument("--check", action="store_true", help="Check cloud bundle drift, source files and numbered .md schema.")
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
