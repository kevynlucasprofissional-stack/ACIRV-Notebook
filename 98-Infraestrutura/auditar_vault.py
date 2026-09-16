#!/usr/bin/env python3
"""Auditoria estática e não destrutiva de um vault Obsidian.

Verifica estrutura de arquivos, frontmatter YAML, IDs/basenames, wikilinks,
integração aproximada do grafo e referências de arquivos Canvas. O script não
substitui abrir o vault no Obsidian nem valida o comportamento de plugins.

Uso:
    python auditar_vault.py /caminho/do/vault --output relatorio.json

Dependência opcional:
    pip install pyyaml
Sem PyYAML, o script ainda inventaria? Não: ele interrompe com instrução clara.
"""

from __future__ import annotations

import argparse
import hashlib
import fnmatch
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML é necessário. Instale com: pip install pyyaml") from exc

WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
HASH_U_RE = re.compile(r"#U([0-9A-Fa-f]{4})")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
FENCED_CODE_RE = re.compile(r"(?:```|~~~).*?(?:```|~~~)", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
WORD_RE = re.compile(r"\b[\wÀ-ÿ]+\b", re.UNICODE)


def decode_hash_u(value: str) -> str:
    """Decodifica sequências literais #U00e7 sem alterar arquivos."""

    def repl(match: re.Match[str]) -> str:
        try:
            return chr(int(match.group(1), 16))
        except (ValueError, OverflowError):
            return match.group(0)

    return HASH_U_RE.sub(repl, value)


def normalize_path(value: str) -> str:
    value = decode_hash_u(value).replace("\\", "/").strip()
    while value.startswith("./"):
        value = value[2:]
    return str(PurePosixPath(value))


def normalize_basename(value: str) -> str:
    value = decode_hash_u(value).strip().replace("\\", "/")
    value = value.rsplit("/", 1)[-1]
    if value.lower().endswith(".md"):
        value = value[:-3]
    return value.casefold()


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "frontmatter_ausente", text
    raw = match.group(1)
    body = text[match.end() :]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, f"yaml_invalido: {exc}", body
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, "frontmatter_nao_e_mapa", body
    return data, None, body


def split_wikilink(raw: str) -> tuple[str, str | None]:
    """Retorna alvo de arquivo e subpath, ignorando display text."""
    before_display = raw.split("|", 1)[0].strip()
    if "#" in before_display:
        target, subpath = before_display.split("#", 1)
        return target.strip(), subpath.strip() or None
    return before_display, None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_numeric(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "mediana": None, "media": None, "max": None}
    return {
        "min": min(values),
        "mediana": statistics.median(values),
        "media": round(statistics.mean(values), 2),
        "max": max(values),
    }


def audit(root: Path, exclude_patterns: list[str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"O caminho não é uma pasta: {root}")

    exclude_patterns = exclude_patterns or []

    def is_excluded(path: Path) -> bool:
        relative = path.relative_to(root).as_posix()
        return any(fnmatch.fnmatch(relative, pattern) for pattern in exclude_patterns)

    all_files = sorted(p for p in root.rglob("*") if p.is_file() and not is_excluded(p))
    md_files = [p for p in all_files if p.suffix.casefold() == ".md"]
    canvas_files = [p for p in all_files if p.suffix.casefold() == ".canvas"]

    rel = {p: normalize_path(p.relative_to(root).as_posix()) for p in all_files}
    rel_literal = {p: p.relative_to(root).as_posix() for p in all_files}
    path_index = {normalize_path(v).casefold(): p for p, v in rel.items()}

    basename_index: dict[str, list[Path]] = defaultdict(list)
    for path in md_files:
        basename_index[normalize_basename(path.stem)].append(path)

    yaml_errors: list[dict[str, str]] = []
    missing_frontmatter: list[str] = []
    ids: dict[str, list[str]] = defaultdict(list)
    aliases: dict[str, list[str]] = defaultdict(list)
    note_types: Counter[str] = Counter()
    word_counts_by_type: dict[str, list[int]] = defaultdict(list)
    word_counts_by_file: dict[str, int] = {}
    parsed: dict[Path, dict[str, Any]] = {}
    bodies: dict[Path, str] = {}

    for path in md_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            yaml_errors.append({"arquivo": rel_literal[path], "erro": f"utf8_invalido: {exc}"})
            continue
        data, error, body = parse_frontmatter(text)
        bodies[path] = text
        if error:
            if error == "frontmatter_ausente":
                missing_frontmatter.append(rel_literal[path])
            else:
                yaml_errors.append({"arquivo": rel_literal[path], "erro": error})
            data = {}
        parsed[path] = data or {}

        note_id = data.get("id") if data else None
        if note_id:
            ids[str(note_id).casefold()].append(rel_literal[path])

        raw_aliases = data.get("aliases", []) if data else []
        if isinstance(raw_aliases, str):
            raw_aliases = [raw_aliases]
        if isinstance(raw_aliases, list):
            for alias in raw_aliases:
                aliases[str(alias).strip().casefold()].append(rel_literal[path])

        note_type = str((data or {}).get("tipo") or (data or {}).get("type") or "sem_tipo")
        note_types[note_type] += 1
        words = len(WORD_RE.findall(body))
        word_counts_by_type[note_type].append(words)
        word_counts_by_file[rel_literal[path]] = words

    broken_links: list[dict[str, str]] = []
    ambiguous_links: list[dict[str, Any]] = []
    link_occurrences = 0
    distinct_edges: set[tuple[str, str]] = set()
    indegree: Counter[str] = Counter()
    outdegree: Counter[str] = Counter()

    for source in md_files:
        body = FENCED_CODE_RE.sub("", bodies.get(source, ""))
        body = INLINE_CODE_RE.sub("", body)
        source_key = normalize_path(rel[source]).casefold()
        for match in WIKILINK_RE.finditer(body):
            link_occurrences += 1
            raw = match.group(1)
            target, _subpath = split_wikilink(raw)
            if not target:  # referência a heading/bloco na própria nota
                continue

            normalized_target_path = normalize_path(target)
            path_candidates = [normalized_target_path]
            if not normalized_target_path.casefold().endswith(".md"):
                path_candidates.append(normalized_target_path + ".md")

            destination: Path | None = None
            for candidate in path_candidates:
                candidate_key = candidate.casefold()
                if candidate_key in path_index and path_index[candidate_key].suffix.casefold() == ".md":
                    destination = path_index[candidate_key]
                    break

            if destination is None:
                base_key = normalize_basename(target)
                candidates = basename_index.get(base_key, [])
                if len(candidates) == 1:
                    destination = candidates[0]
                elif len(candidates) > 1:
                    ambiguous_links.append({
                        "origem": rel_literal[source],
                        "link": raw,
                        "candidatos": [rel_literal[p] for p in candidates],
                    })
                    continue

            if destination is None:
                broken_links.append({"origem": rel_literal[source], "link": raw})
                continue

            destination_key = normalize_path(rel[destination]).casefold()
            distinct_edges.add((source_key, destination_key))
            outdegree[source_key] += 1
            indegree[destination_key] += 1

    md_keys = {normalize_path(rel[p]).casefold(): p for p in md_files}
    no_inlinks = [rel_literal[p] for key, p in md_keys.items() if indegree[key] == 0]
    no_outlinks = [rel_literal[p] for key, p in md_keys.items() if outdegree[key] == 0]
    isolated = [
        rel_literal[p]
        for key, p in md_keys.items()
        if indegree[key] == 0 and outdegree[key] == 0
    ]

    canvas_errors: list[dict[str, str]] = []
    canvas_file_refs: list[dict[str, str]] = []
    for path in canvas_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            canvas_errors.append({"arquivo": rel_literal[path], "erro": str(exc)})
            continue

        node_ids: set[str] = set()
        for node in data.get("nodes", []):
            node_id = str(node.get("id", ""))
            if not node_id:
                canvas_errors.append({"arquivo": rel_literal[path], "erro": "node_sem_id"})
            elif node_id in node_ids:
                canvas_errors.append({"arquivo": rel_literal[path], "erro": f"node_id_duplicado: {node_id}"})
            node_ids.add(node_id)

            if node.get("type") == "file" and node.get("file"):
                target = normalize_path(str(node["file"]))
                if target.casefold() not in path_index:
                    canvas_file_refs.append({
                        "canvas": rel_literal[path],
                        "referencia": str(node["file"]),
                    })

        for edge in data.get("edges", []):
            edge_id = str(edge.get("id", ""))
            if not edge_id:
                canvas_errors.append({"arquivo": rel_literal[path], "erro": "edge_sem_id"})
            from_node = str(edge.get("fromNode", ""))
            to_node = str(edge.get("toNode", ""))
            if from_node not in node_ids or to_node not in node_ids:
                canvas_errors.append({
                    "arquivo": rel_literal[path],
                    "erro": f"edge_aponta_node_inexistente: {edge_id}",
                })

    encoded_names = [
        rel_literal[p]
        for p in all_files
        if HASH_U_RE.search(rel_literal[p])
    ]
    giant_files = [
        {"arquivo": rel_literal[p], "bytes": p.stat().st_size}
        for p in all_files
        if p.stat().st_size >= 1_000_000
    ]

    duplicate_basenames = {
        key: [rel_literal[p] for p in paths]
        for key, paths in basename_index.items()
        if len(paths) > 1
    }
    duplicate_ids = {key: paths for key, paths in ids.items() if len(paths) > 1}
    duplicate_aliases = {key: paths for key, paths in aliases.items() if len(paths) > 1}

    extension_counts = Counter(p.suffix.casefold() or "[sem_extensao]" for p in all_files)
    type_stats = {
        note_type: {"quantidade": len(values), **summarize_numeric(values)}
        for note_type, values in sorted(word_counts_by_type.items())
    }

    return {
        "ferramenta": "auditar_vault.py",
        "escopo": str(root),
        "exclusoes": exclude_patterns,
        "limitacoes": [
            "Auditoria estática; não abre o Obsidian.",
            "A resolução de links aproxima o comportamento por caminho e basename.",
            "Não executa Dataview, Bases, Templater ou outros plugins.",
            "Não valida semanticamente headings e block IDs.",
        ],
        "metricas": {
            "arquivos_totais": len(all_files),
            "por_extensao": dict(sorted(extension_counts.items())),
            "markdown": len(md_files),
            "canvas": len(canvas_files),
            "frontmatter_ausente": len(missing_frontmatter),
            "erros_yaml_ou_utf8": len(yaml_errors),
            "ids_duplicados": len(duplicate_ids),
            "basenames_duplicados": len(duplicate_basenames),
            "aliases_compartilhados": len(duplicate_aliases),
            "wikilinks_ocorrencias": link_occurrences,
            "arestas_distintas": len(distinct_edges),
            "wikilinks_quebrados": len(broken_links),
            "wikilinks_ambiguos": len(ambiguous_links),
            "sem_links_entrada": len(no_inlinks),
            "sem_links_saida": len(no_outlinks),
            "isoladas": len(isolated),
            "canvas_erros_estruturais": len(canvas_errors),
            "canvas_referencias_arquivo_quebradas": len(canvas_file_refs),
            "nomes_com_hash_u": len(encoded_names),
            "arquivos_maiores_1mb": len(giant_files),
        },
        "notas_por_tipo": dict(sorted(note_types.items())),
        "palavras_por_tipo": type_stats,
        "achados": {
            "frontmatter_ausente": missing_frontmatter,
            "erros_yaml_ou_utf8": yaml_errors,
            "ids_duplicados": duplicate_ids,
            "basenames_duplicados": duplicate_basenames,
            "aliases_compartilhados": duplicate_aliases,
            "wikilinks_quebrados": broken_links,
            "wikilinks_ambiguos": ambiguous_links,
            "sem_links_entrada": no_inlinks,
            "sem_links_saida": no_outlinks,
            "isoladas": isolated,
            "canvas_erros_estruturais": canvas_errors,
            "canvas_referencias_arquivo_quebradas": canvas_file_refs,
            "nomes_com_hash_u": encoded_names,
            "arquivos_maiores_1mb": giant_files,
        },
        "hashes_sha256": {
            rel_literal[p]: sha256(p) for p in all_files
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita estaticamente um vault Obsidian.")
    parser.add_argument("vault", type=Path, help="Pasta raiz do vault")
    parser.add_argument("--output", "-o", type=Path, help="Arquivo JSON de saída")
    parser.add_argument("--pretty", action="store_true", help="Mostra o JSON completo no terminal")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Padrão glob relativo a excluir; pode ser repetido. Ex.: 'Processo/**'",
    )
    args = parser.parse_args()

    try:
        report = audit(args.vault, args.exclude)
    except (OSError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(f"Relatório salvo em: {args.output}")

    metrics = report["metricas"]
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.pretty:
        print(payload)

    blocking = (
        metrics["erros_yaml_ou_utf8"]
        + metrics["ids_duplicados"]
        + metrics["wikilinks_quebrados"]
        + metrics["canvas_erros_estruturais"]
        + metrics["canvas_referencias_arquivo_quebradas"]
    )
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
