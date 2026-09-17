#!/usr/bin/env python3
"""Suíte de testes de integração e invariantes para o Sistema de Ingestão e Paridade.

Executa testes reais com repositórios Git temporários (fixtures) para garantir:
1. Primeira inventariação determinística
2. Segunda execução 100% idempotente (0 novos, 0 alterados, 0 diffs)
3. Alteração de blob SHA (nova versão vinculada por supersedes_sha)
4. Remoção humana de arquivos (deleted_by_human)
5. Isolamento pré-leitura de arquivos sensíveis (Safety Gate)
6. Parsing estrito de JSONL corrompido (ValueError explícito com linha)
7. Detecção de claim_id duplicado
8. Detecção de referências de claims órfãs (supersedes, contradicts, duplicates)
9. Detecção de nota canônica de destino inexistente
10. Resolução determinística de anchors (headings e block IDs)
11. Validez de fonte revisada com 0 claims novos (reviewed_no_material_change)
12. Desacoplamento de fontes primárias e validação humana
13. Geração reproduzível do relatório de cobertura
14. Snapshot runtime de imutabilidade de 000-Arquivos-originais/
15. Validação de IDs de máquina ASCII estritos

Uso:
    python -m pytest test_invariantes.py -v
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
import pytest

from safety_gate import classify, CONFIRMED_SENSITIVE_PATHS
from inventariar_fontes import (
    run as run_inventory, load_ledger, save_ledger,
    SOURCES_DIR, DEFAULT_LEDGER
)
from claims import (
    load_claims, save_claims, validate_claims_dataset,
    validate_claim_schema, normalize_anchor_slug, extract_file_anchors
)
from validar_invariantes import (
    take_sources_snapshot, check_runtime_immutability,
    check_safety_gate_known_secrets, check_ledger_integrity,
    check_claims_referential_integrity, check_contradictions_not_validated
)
from relatorio_cobertura import generate_coverage_data, render_markdown_report


@pytest.fixture
def temp_git_vault(tmp_path: Path) -> Path:
    """Cria um repositório Git temporário estruturado para testes de integração."""
    vault = tmp_path / "ACIRV-Notebook"
    vault.mkdir()

    # Estrutura de pastas
    (vault / SOURCES_DIR).mkdir()
    (vault / "01-Estrategia-e-Marca").mkdir()
    (vault / "03-Projetos-Campanhas-e-Eventos").mkdir()
    (vault / "04-Conteudo-Canais-e-Imprensa").mkdir()
    (vault / "05-Metricas-e-Decisao").mkdir()
    (vault / "85-Bases-e-Consultas").mkdir()

    # Git init
    subprocess.run(["git", "init"], cwd=vault, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Test Agent"], cwd=vault, capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "test@acirv.org"], cwd=vault, capture_output=True, check=True)

    # Arquivos normais em 000-Arquivos-originais/
    f1 = vault / SOURCES_DIR / "Relatorio_Agosto.md"
    f1.write_text("# Relatório Agosto 2026\nVisualizações: 3.340.052\n", encoding="utf-8")

    f2 = vault / SOURCES_DIR / "Mudancas_Cronograma.md"
    f2.write_text("# Cronograma\nConecta: 11/09 07h30\n", encoding="utf-8")

    # Arquivo sensível
    f_sec = vault / SOURCES_DIR / "Contas e Senhas.md"
    f_sec.write_text("senha_secreta_123", encoding="utf-8")

    # Nota canônica
    note1 = vault / "03-Projetos-Campanhas-e-Eventos" / "SudoExpo-2026.md"
    note1.write_text("# SudoExpo-2026\n\n## Datas e cronograma\nRealização em setembro.\n^cronograma\n", encoding="utf-8")

    # Commit inicial
    subprocess.run(["git", "add", "."], cwd=vault, capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=vault, capture_output=True, check=True)

    return vault


class TestIntegrationPipeline:
    """Testes de integração cobrindo os 15 cenários de garantia determinística."""

    def test_1_first_inventory(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        stats = run_inventory(temp_git_vault, ledger_path)

        assert stats["total_fontes"] == 3
        assert stats["new_entries"] == 3
        assert ledger_path.exists()

        ledger = load_ledger(ledger_path)
        assert len(ledger) == 3

    def test_2_second_execution_idempotency(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        run_inventory(temp_git_vault, ledger_path)

        content_before = ledger_path.read_text(encoding="utf-8")

        # Segunda execução sem alterações
        stats2 = run_inventory(temp_git_vault, ledger_path)
        content_after = ledger_path.read_text(encoding="utf-8")

        assert stats2["new_entries"] == 0
        assert stats2["updated_entries"] == 0
        assert content_before == content_after, "Segunda execução produziu diff no ledger JSONL!"

    def test_3_blob_change_detection(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        run_inventory(temp_git_vault, ledger_path)

        # Edita arquivo existente
        f1 = temp_git_vault / SOURCES_DIR / "Relatorio_Agosto.md"
        f1.write_text("# Relatório Agosto 2026 V2\nVisualizações: 4.000.000\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=temp_git_vault, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "Edit file"], cwd=temp_git_vault, capture_output=True, check=True)

        stats2 = run_inventory(temp_git_vault, ledger_path)
        assert stats2["updated_entries"] == 1

        ledger = load_ledger(ledger_path)
        entries_f1 = [e for (p, s), e in ledger.items() if p == f"000-Arquivos-originais/Relatorio_Agosto.md"]
        assert len(entries_f1) == 2, "Novo blob deve preservar versão anterior no ledger!"
        newest = [e for e in entries_f1 if e.get("is_version_update")][0]
        assert len(newest["supersedes_sha"]) == 1

    def test_4_human_deletion_detection(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        run_inventory(temp_git_vault, ledger_path)

        # Remove arquivo no Git
        subprocess.run(["git", "rm", f"{SOURCES_DIR}/Mudancas_Cronograma.md"], cwd=temp_git_vault, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "Delete file"], cwd=temp_git_vault, capture_output=True, check=True)

        stats2 = run_inventory(temp_git_vault, ledger_path)
        assert stats2["deleted_detected"] == 1

        ledger = load_ledger(ledger_path)
        deleted_entries = [e for e in ledger.values() if e.get("source_status") == "deleted_by_human"]
        assert len(deleted_entries) == 1

    def test_5_sensitive_file_blocking(self, temp_git_vault: Path):
        res = classify("000-Arquivos-originais/Contas e Senhas.md")
        assert res.read_status == "sensitive_do_not_read"
        assert res.sensitivity == "confirmed_secret"

    def test_6_corrupt_jsonl_raises_exception(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text('{"source_path": "000-Arquivos-originais/A.md", "blob_sha": "abc"}\n{invalid_json_line}\n', encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            load_ledger(ledger_path)
        assert "linha 2" in str(exc_info.value).lower()

    def test_7_duplicate_claim_id_detection(self, temp_git_vault: Path):
        claims = [
            {"claim_id": "test.id.1", "statement": "A", "entity": "E", "property": "P", "value": "V",
             "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
             "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "pending_validation",
             "validation_status": "pending_validation"},
            {"claim_id": "test.id.1", "statement": "B", "entity": "E", "property": "P", "value": "V2",
             "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
             "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "pending_validation",
             "validation_status": "pending_validation"}
        ]
        errs = validate_claims_dataset(temp_git_vault, claims)
        assert any("duplicado" in e.lower() for e in errs)

    def test_8_orphan_claim_ref_detection(self, temp_git_vault: Path):
        claims = [
            {"claim_id": "test.id.1", "statement": "A", "entity": "E", "property": "P", "value": "V",
             "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
             "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "pending_validation",
             "validation_status": "pending_validation", "supersedes": ["non.existent.id"]}
        ]
        errs = validate_claims_dataset(temp_git_vault, claims)
        assert any("inexistente" in e.lower() for e in errs)

    def test_9_non_existent_destination_detection(self, temp_git_vault: Path):
        claims = [
            {"claim_id": "test.id.1", "statement": "A", "entity": "E", "property": "P", "value": "V",
             "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
             "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "promoted",
             "validation_status": "not_required",
             "supporting_sources": [{"source_path": "000-Arquivos-originais/Relatorio_Agosto.md", "source_blob_sha": "abc"}],
             "canonical_destination": "03-Projetos/Inexistente.md"}
        ]
        errs = validate_claims_dataset(temp_git_vault, claims)
        assert any("não existe" in e.lower() for e in errs)

    def test_10_anchor_verification(self, temp_git_vault: Path):
        dest_file = temp_git_vault / "03-Projetos-Campanhas-e-Eventos" / "SudoExpo-2026.md"
        anchors = extract_file_anchors(dest_file)
        assert "datas-e-cronograma" in anchors
        assert "cronograma" in anchors

    def test_11_reviewed_source_with_zero_claims_is_valid(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        run_inventory(temp_git_vault, ledger_path)

        ledger = load_ledger(ledger_path)
        matching_keys = [k for k in ledger.keys() if k[0] == "000-Arquivos-originais/Relatorio_Agosto.md"]
        assert len(matching_keys) > 0
        key = matching_keys[0]
        ledger[key]["review_status"] = "reviewed_no_material_change"
        save_ledger(ledger_path, list(ledger.values()))

        # Deve validar sem exceções
        errs = check_ledger_integrity(ledger_path)
        assert len(errs) == 0

    def test_12_disentangled_human_validation_schema(self, temp_git_vault: Path):
        claim = {
            "claim_id": "test.ascii.id",
            "supporting_sources": [{"source_path": "000-Arquivos-originais/Relatorio_Agosto.md", "source_blob_sha": "a"*40}],
            "statement": "Declaração", "entity": "Entidade", "property": "prop", "value": "val",
            "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
            "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "promoted",
            "validation_status": "validated", "validation_source": "human_validation",
            "validation_record": "validacao_humana_2026_09_17", "validated_at": "2026-09-17T14:21:00-03:00",
            "canonical_destination": "03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md",
            "destination_anchor": "datas-e-cronograma"
        }
        errs = validate_claim_schema(claim)
        assert len(errs) == 0

    def test_13_real_report_generation(self, temp_git_vault: Path):
        ledger_path = temp_git_vault / DEFAULT_LEDGER
        claims_path = temp_git_vault / "85-Bases-e-Consultas" / "Claims-Canonicos.jsonl"
        run_inventory(temp_git_vault, ledger_path)

        data = generate_coverage_data(temp_git_vault, ledger_path, claims_path)
        md = render_markdown_report(data)
        assert "Relatório de Cobertura e Paridade" in md
        assert "Processable Source Coverage" in md

    def test_14_runtime_immutability_snapshot(self, temp_git_vault: Path):
        before = take_sources_snapshot(temp_git_vault)
        after = take_sources_snapshot(temp_git_vault)

        errs = check_runtime_immutability(before, after)
        assert len(errs) == 0

    def test_15_ascii_claim_id_strict_validation(self, temp_git_vault: Path):
        claim = {
            "claim_id": "test.com.acento.orçamento",
            "statement": "A", "entity": "E", "property": "P", "value": "V",
            "semantic_role": "fato", "evidence_class": "fato_documentado", "authority": "registro_primario",
            "confidence": "alto", "observed_at": "2026-09-17T00:00:00Z", "disposition": "pending_validation",
            "validation_status": "pending_validation"
        }
        errs = validate_claim_schema(claim)
        assert any("ascii" in e.lower() for e in errs)
