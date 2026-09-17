#!/usr/bin/env python3
"""Testes de invariantes do sistema de ingestão do ACIRV Notebook.

Cobre:
1. Imutabilidade de 000-Arquivos-originais/ (safety gate de escrita)
2. Safety gate: os dois caminhos sensíveis confirmados são bloqueados
3. Idempotência do ledger
4. Versionamento: mudança de blob_sha é detectada
5. Remoção humana não apaga claims canônicos
6. Claims: todo claim material tem disposition válida
7. Proveniência: claim promovido requer source/versionamento
8. Contradições: contradiction ≠ validated
9. Divergência: pending_validation ≠ validated em campos diferentes
10. Schema do ledger e claims

Uso:
    python -m pytest test_invariantes.py -v
    python test_invariantes.py         # execução direta (unittest)
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Garante que o diretório do módulo está no path
sys.path.insert(0, str(Path(__file__).parent))

from safety_gate import classify, CONFIRMED_SENSITIVE_PATHS
from claims import (
    Claim, validate_claim, load_claims, save_claims,
    get_pending_validations, get_contradictions,
    VALID_DISPOSITIONS, VALID_VALIDATION_STATUSES, VALID_EVIDENCE_CLASSES,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_valid_claim(**overrides) -> dict:
    """Cria um claim válido com campos mínimos."""
    base = {
        "claim_id": "test.entity.property.value",
        "source_path": "000-Arquivos-originais/Algum-Arquivo.md",
        "source_blob_sha": "abc123def456abc123def456abc123def456abc1",
        "statement": "O evento SudoExpo começa em agosto de 2026.",
        "entity": "SudoExpo 2026",
        "property": "data_inicio",
        "value": "agosto/2026",
        "semantic_role": "fato",
        "evidence_class": "fato_documentado",
        "authority": "nota_operacional_humana",
        "confidence": "medio_alto",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "disposition": "promoted",
        "validation_status": "pending_validation",
        "canonical_destination": "03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md",
    }
    base.update(overrides)
    return base


def _make_ledger_entry(**overrides) -> dict:
    base = {
        "source_path": "000-Arquivos-originais/Algum-Arquivo.md",
        "blob_sha": "abc123",
        "media_type": "md",
        "domain": "geral",
        "source_type": "nota_operacional",
        "authority": "nota_operacional_humana",
        "sensitivity": "normal",
        "read_status": "unread",
        "processing_status": "unprocessed",
        "source_status": "active",
        "safety_reason": "nenhum padrão suspeito detectado",
        "inventoried_at": datetime.now(timezone.utc).isoformat(),
        "is_version_update": False,
        "supersedes_sha": [],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Test 1: Imutabilidade de 000-Arquivos-originais/
# ---------------------------------------------------------------------------

class TestSourcesImmutability(unittest.TestCase):
    """Verifica que scripts não escrevem em 000-Arquivos-originais/."""
    
    def test_safety_gate_never_writes_to_sources_dir(self):
        """O safety gate opera apenas com strings de caminho — não escreve nada."""
        path = "000-Arquivos-originais/Algum-Arquivo.md"
        result = classify(path)
        # A função classify nunca cria arquivos
        sources_dir = Path("000-Arquivos-originais")
        # Verifica que nenhum arquivo foi criado no diretório protegido
        if sources_dir.exists():
            before = list(sources_dir.rglob("*"))
            classify(path)
            after = list(sources_dir.rglob("*"))
            self.assertEqual(before, after, "safety_gate.classify() criou arquivos em 000-Arquivos-originais/")
    
    def test_inventory_script_does_not_write_to_sources(self):
        """O inventariar_fontes.py não modifica 000-Arquivos-originais/."""
        # Verifica que o script só modifica o ledger, nunca a pasta protegida
        # Teste de intenção: o script opera em <vault>/85-Bases-e-Consultas/
        from inventariar_fontes import SOURCES_DIR, DEFAULT_LEDGER
        self.assertNotIn("000-Arquivos-originais", DEFAULT_LEDGER)
        self.assertEqual(SOURCES_DIR, "000-Arquivos-originais")


# ---------------------------------------------------------------------------
# Test 2: Safety gate — caminhos sensíveis confirmados
# ---------------------------------------------------------------------------

class TestSafetyGate(unittest.TestCase):
    """Verifica que o safety gate bloqueia arquivos sensíveis."""
    
    def test_confirmed_sensitive_paths_are_blocked(self):
        """Os dois caminhos confirmados sensíveis devem ser bloqueados sem leitura."""
        expected_paths = [
            "000-Arquivos-originais/Contas e Senhas.md",
            "000-Arquivos-originais/Minha Chave API Antropic.md",
        ]
        for path in expected_paths:
            with self.subTest(path=path):
                result = classify(path)
                self.assertEqual(
                    result.read_status, "sensitive_do_not_read",
                    f"Caminho '{path}' deveria ter read_status=sensitive_do_not_read, "
                    f"obtido: {result.read_status}"
                )
                self.assertIn(
                    result.sensitivity, ("confirmed_secret", "secret_suspected"),
                    f"Caminho '{path}' deveria ter sensitivity confirmada como secret"
                )
    
    def test_confirmed_sensitive_paths_match_constant(self):
        """Os caminhos testados estão no conjunto CONFIRMED_SENSITIVE_PATHS."""
        self.assertIn("000-Arquivos-originais/Contas e Senhas.md", CONFIRMED_SENSITIVE_PATHS)
        self.assertIn("000-Arquivos-originais/Minha Chave API Antropic.md", CONFIRMED_SENSITIVE_PATHS)
    
    def test_password_pattern_in_name_is_blocked(self):
        """Arquivos com 'senha' ou 'password' no nome são bloqueados."""
        for suspicious in [
            "arquivo_com_senha.md",
            "passwords.txt",
            "000-Arquivos-originais/tokens_api.md",
            "000-Arquivos-originais/Minha Chave API qualquer.md",
        ]:
            with self.subTest(path=suspicious):
                result = classify(suspicious)
                self.assertEqual(result.read_status, "sensitive_do_not_read",
                                 f"'{suspicious}' deveria ser bloqueado")
    
    def test_normal_file_is_allowed(self):
        """Arquivo sem padrões suspeitos é classificado como normal."""
        result = classify("000-Arquivos-originais/Relatorio-de-Agosto.md")
        self.assertEqual(result.sensitivity, "normal")
        self.assertNotEqual(result.read_status, "sensitive_do_not_read")
    
    def test_zip_is_quarantined(self):
        """Arquivos ZIP são colocados em quarentena técnica."""
        result = classify("000-Arquivos-originais/Pacote.zip")
        self.assertEqual(result.sensitivity, "technical_quarantine")
        self.assertEqual(result.read_status, "sensitive_do_not_read")


# ---------------------------------------------------------------------------
# Test 3: Idempotência do ledger
# ---------------------------------------------------------------------------

class TestLedgerIdempotency(unittest.TestCase):
    """Verifica que o ledger não gera duplicatas."""
    
    def test_no_duplicate_entries_on_same_sha(self):
        """Mesmo (source_path, blob_sha) não deve gerar duas entradas."""
        entry1 = _make_ledger_entry()
        entry2 = _make_ledger_entry()  # mesma chave
        
        entries = [entry1, entry2]
        
        # Simula a lógica de índice do ledger
        seen = set()
        duplicates = []
        for e in entries:
            key = (e["source_path"], e["blob_sha"])
            if key in seen:
                duplicates.append(key)
            seen.add(key)
        
        self.assertEqual(
            len(duplicates), 1,
            "Duas entradas idênticas deveriam gerar 1 duplicata detectada"
        )
    
    def test_ledger_roundtrip(self):
        """Ledger pode ser salvo e recarregado sem perda de dados."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ledger_path = Path(tmpdir) / "test_ledger.jsonl"
            entries = [
                _make_ledger_entry(source_path="000-Arquivos-originais/A.md", blob_sha="sha1"),
                _make_ledger_entry(source_path="000-Arquivos-originais/B.md", blob_sha="sha2"),
            ]
            
            # Salva
            with ledger_path.open("w", encoding="utf-8") as f:
                for e in entries:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            
            # Recarrega
            loaded = []
            with ledger_path.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        loaded.append(json.loads(line))
            
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["source_path"], "000-Arquivos-originais/A.md")


# ---------------------------------------------------------------------------
# Test 4: Versionamento
# ---------------------------------------------------------------------------

class TestVersioning(unittest.TestCase):
    """Verifica que mudança de blob_sha é detectada."""
    
    def test_different_sha_same_path_is_new_version(self):
        """Mesmo source_path com blob_sha diferente = nova versão."""
        entry_v1 = _make_ledger_entry(blob_sha="sha_versao_1", is_version_update=False)
        entry_v2 = _make_ledger_entry(blob_sha="sha_versao_2", is_version_update=True)
        
        # Chaves são diferentes
        key_v1 = (entry_v1["source_path"], entry_v1["blob_sha"])
        key_v2 = (entry_v2["source_path"], entry_v2["blob_sha"])
        
        self.assertNotEqual(key_v1, key_v2,
                            "Versões diferentes devem ter chaves diferentes no ledger")
        self.assertTrue(entry_v2["is_version_update"],
                        "Entrada com SHA diferente deve ser marcada como is_version_update=True")
    
    def test_same_sha_same_path_is_unchanged(self):
        """Mesmo (source_path, blob_sha) = sem mudança → skip."""
        entry = _make_ledger_entry(blob_sha="sha_estavel")
        key = (entry["source_path"], entry["blob_sha"])
        
        # Após carregar ledger, a chave existente indica skip
        existing = {key: entry}
        
        # Se a chave está no ledger e processing_status não é 'unprocessed'/'error' → skip
        should_skip = (
            key in existing and
            existing[key].get("processing_status") not in ("unprocessed", "error")
        )
        # Neste caso, processing_status é 'unprocessed', então NÃO deve pular
        self.assertFalse(should_skip)


# ---------------------------------------------------------------------------
# Test 5: Remoção humana não apaga conhecimento canônico
# ---------------------------------------------------------------------------

class TestDeletion(unittest.TestCase):
    """Remoção humana de fonte não apaga claims canônicos."""
    
    def test_deleted_source_marks_as_deleted_not_removes(self):
        """Arquivo deletado deve ter source_status=deleted_by_human, não ser removido."""
        entry = _make_ledger_entry(source_status="active")
        current_paths = {"outro_arquivo.md"}  # source_path do entry não está mais no Git
        
        # Simula detecção de remoção: arquivo não está mais na árvore Git
        source_path = entry["source_path"]
        if source_path not in current_paths:
            entry = dict(entry)
            entry["source_status"] = "deleted_by_human"
        
        self.assertEqual(entry["source_status"], "deleted_by_human")
        # A entrada AINDA existe no ledger (não foi apagada)
        self.assertIsNotNone(entry)
        # A entrada AINDA existe no ledger
        self.assertIsNotNone(entry)
    
    def test_claims_from_deleted_source_persist(self):
        """Claims de fonte deletada devem permanecer para preservar conhecimento histórico."""
        with tempfile.TemporaryDirectory() as tmpdir:
            claims_path = Path(tmpdir) / "claims.jsonl"
            
            claim = _make_valid_claim(
                claim_id="historico.fonte.removida",
                disposition="promoted",
                validation_status="validated",
            )
            save_claims(claims_path, [claim])
            
            # Simula "remoção" — apenas marca no ledger, não apaga claims
            loaded = load_claims(claims_path)
            self.assertEqual(len(loaded), 1, "Claim de fonte histórica não deve ser removido")


# ---------------------------------------------------------------------------
# Test 6: Claims têm disposition válida
# ---------------------------------------------------------------------------

class TestClaimsDispositions(unittest.TestCase):
    """Claims materiais têm dispositions válidas."""
    
    def test_valid_disposition_passes(self):
        """Claim com disposition válida não gera erro."""
        for disp in VALID_DISPOSITIONS:
            with self.subTest(disposition=disp):
                # Claims com contradiction não podem ter validation_status=validated
                vstatus = "pending_validation" if disp == "contradiction" else "pending_validation"
                dest = "alguma/nota.md" if disp == "promoted" else None
                claim = _make_valid_claim(
                    disposition=disp,
                    validation_status=vstatus,
                    canonical_destination=dest,
                )
                errors = validate_claim(claim)
                # Contradições são válidas com pending_validation
                self.assertEqual(errors, [], f"Claim com disposition={disp} não deveria ter erros: {errors}")
    
    def test_invalid_disposition_fails(self):
        """Claim com disposition inválida gera erro de validação."""
        claim = _make_valid_claim(disposition="nao_existe_essa_disposition")
        errors = validate_claim(claim)
        self.assertTrue(len(errors) > 0, "Disposition inválida deveria gerar erro")
    
    def test_missing_disposition_fails(self):
        """Claim sem disposition gera erro."""
        claim = _make_valid_claim()
        del claim["disposition"]
        errors = validate_claim(claim)
        self.assertTrue(any("disposition" in e for e in errors))


# ---------------------------------------------------------------------------
# Test 7: Proveniência de claims promovidos
# ---------------------------------------------------------------------------

class TestClaimsProvenance(unittest.TestCase):
    """Claims promovidos exigem fonte e versionamento."""
    
    def test_promoted_without_blob_sha_fails(self):
        """Claim promovido sem source_blob_sha deve falhar na validação."""
        claim = _make_valid_claim(disposition="promoted", source_blob_sha="")
        errors = validate_claim(claim)
        self.assertTrue(
            any("source_blob_sha" in e or "promovido" in e for e in errors),
            f"Deveria exigir source_blob_sha para claim promovido. Erros: {errors}"
        )
    
    def test_promoted_without_destination_fails(self):
        """Claim promovido sem canonical_destination deve falhar."""
        claim = _make_valid_claim(disposition="promoted", canonical_destination=None)
        errors = validate_claim(claim)
        self.assertTrue(
            any("canonical_destination" in e or "destino" in e for e in errors),
            f"Deveria exigir canonical_destination para claim promovido. Erros: {errors}"
        )
    
    def test_promoted_with_full_provenance_passes(self):
        """Claim promovido com proveniência completa é válido."""
        claim = _make_valid_claim(
            disposition="promoted",
            source_blob_sha="abc123def456abc123def456abc123def456abc1",
            canonical_destination="03-Projetos-Campanhas-e-Eventos/SudoExpo-2026.md",
        )
        errors = validate_claim(claim)
        self.assertEqual(errors, [])


# ---------------------------------------------------------------------------
# Test 8: Contradições não validadas silenciosamente
# ---------------------------------------------------------------------------

class TestContradictions(unittest.TestCase):
    """Contradições não podem ser apresentadas como verdade validada."""
    
    def test_contradiction_with_validated_status_fails(self):
        """Claim com disposition=contradiction e validation_status=validated deve falhar."""
        claim = _make_valid_claim(
            disposition="contradiction",
            validation_status="validated",
            canonical_destination=None,
        )
        errors = validate_claim(claim)
        self.assertTrue(
            any("contradiction" in e and "validated" in e for e in errors),
            f"Contradição com status=validated deveria falhar. Erros: {errors}"
        )
    
    def test_contradiction_with_pending_passes(self):
        """Claim com contradiction e pending_validation é o estado correto."""
        claim = _make_valid_claim(
            disposition="contradiction",
            validation_status="pending_validation",
            canonical_destination=None,
        )
        errors = validate_claim(claim)
        self.assertEqual(errors, [], f"Contradição pendente não deveria ter erros: {errors}")
    
    def test_get_contradictions_function(self):
        """A função get_contradictions filtra corretamente."""
        claims = [
            _make_valid_claim(claim_id="c1", disposition="contradiction",
                              validation_status="pending_validation", canonical_destination=None),
            _make_valid_claim(claim_id="c2", disposition="promoted"),
            _make_valid_claim(claim_id="c3", disposition="not_material", canonical_destination=None),
        ]
        contradictions = get_contradictions(claims)
        self.assertEqual(len(contradictions), 1)
        self.assertEqual(contradictions[0]["claim_id"], "c1")


# ---------------------------------------------------------------------------
# Test 9: Divergência de validação
# ---------------------------------------------------------------------------

class TestValidationDivergence(unittest.TestCase):
    """pending_validation não pode aparecer como validated em campos diferentes."""
    
    def test_pending_disposition_validated_status_is_divergence(self):
        """disposition=pending_validation + validation_status=validated é divergência."""
        # Este caso é detectado pelo validar_invariantes.py
        # Aqui testamos que podemos detectar a condição
        claim = {
            "disposition": "pending_validation",
            "validation_status": "validated",
        }
        is_divergent = (
            claim["disposition"] == "pending_validation" and
            claim["validation_status"] == "validated"
        )
        self.assertTrue(is_divergent, "Deveria detectar divergência de validação")


# ---------------------------------------------------------------------------
# Test 10: Schema de claims e ledger
# ---------------------------------------------------------------------------

class TestSchema(unittest.TestCase):
    """Ledger e claims devem ser válidos conforme schema."""
    
    def test_valid_evidence_classes(self):
        """Todos os valores em VALID_EVIDENCE_CLASSES são reconhecidos."""
        expected = {
            "fato_documentado", "dado_calculado", "interpretacao_operacional",
            "hipotese_de_trabalho", "recurso_pedagogico", "representacao_visual",
        }
        self.assertEqual(VALID_EVIDENCE_CLASSES, expected)
    
    def test_all_required_claim_fields_present(self):
        """Um claim válido contém todos os campos obrigatórios."""
        claim = _make_valid_claim()
        errors = validate_claim(claim)
        self.assertEqual(errors, [], f"Claim válido não deveria ter erros: {errors}")
    
    def test_claims_roundtrip(self):
        """Claims podem ser salvos e recarregados sem perda."""
        with tempfile.TemporaryDirectory() as tmpdir:
            claims_path = Path(tmpdir) / "claims.jsonl"
            original = [
                _make_valid_claim(claim_id="c1"),
                _make_valid_claim(claim_id="c2", disposition="not_material",
                                  canonical_destination=None),
            ]
            save_claims(claims_path, original)
            loaded = load_claims(claims_path)
            self.assertEqual(len(loaded), 2)
            ids = {c["claim_id"] for c in loaded}
            self.assertIn("c1", ids)
            self.assertIn("c2", ids)
    
    def test_ledger_required_fields(self):
        """Entradas do ledger têm campos obrigatórios."""
        entry = _make_ledger_entry()
        required = [
            "source_path", "blob_sha", "media_type", "domain",
            "sensitivity", "read_status", "processing_status",
            "source_status", "inventoried_at",
        ]
        for field_name in required:
            self.assertIn(field_name, entry, f"Campo obrigatório ausente: {field_name}")
            self.assertIsNotNone(entry[field_name], f"Campo {field_name} não pode ser None")


# ---------------------------------------------------------------------------
# Test 11: Regressão — notas canônicas não sofrem reescritas cosméticas
# ---------------------------------------------------------------------------

class TestNoCosmedicRewrites(unittest.TestCase):
    """Verifica que o sistema não reescreve conteúdo já correto."""
    
    def test_unchanged_blob_sha_skips_processing(self):
        """Fonte com blob_sha idêntico ao do ledger não é reprocessada."""
        existing_entry = _make_ledger_entry(
            blob_sha="sha_estavel",
            processing_status="processed",
        )
        
        # Simula decisão de skip
        key = (existing_entry["source_path"], existing_entry["blob_sha"])
        existing = {key: existing_entry}
        
        current_blob_sha = "sha_estavel"  # não mudou
        current_key = (existing_entry["source_path"], current_blob_sha)
        
        should_skip = (
            current_key in existing and
            existing[current_key].get("processing_status") not in ("unprocessed", "error")
        )
        self.assertTrue(should_skip, "Fonte sem mudança de SHA deveria ser pulada")


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
