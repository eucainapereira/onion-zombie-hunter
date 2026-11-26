"""Suíte Completa de Testes Unitários para o Motor FinOps e Roteador REST.

Executável com a biblioteca padrão:
    python3 -m unittest discover -s src
"""

import json
import unittest

from engine import run_finops_scan
from handler import lambda_handler
from pricing import (
    calculate_alb_cost,
    calculate_ebs_cost,
    calculate_eip_cost,
    calculate_health_score,
    calculate_nat_cost,
    calculate_snapshot_cost,
    generate_remediation_plans,
)


class TestPricingAndScore(unittest.TestCase):
    """Testes da matriz tarifária oficial AWS US East e FinOps Health Score."""

    def test_ebs_costs(self):
        # gp3: 100 GB * 0.08 = $8.00
        monthly, annual = calculate_ebs_cost("gp3", 100)
        self.assertEqual(monthly, 8.00)
        self.assertEqual(annual, 96.00)

        # gp2: 200 GB * 0.10 = $20.00
        monthly_gp2, annual_gp2 = calculate_ebs_cost("gp2", 200)
        self.assertEqual(monthly_gp2, 20.00)
        self.assertEqual(annual_gp2, 240.00)

    def test_eip_cost(self):
        # 1 EIP: 730 * 0.005 = 3.65
        monthly, annual = calculate_eip_cost()
        self.assertEqual(monthly, 3.65)
        self.assertEqual(annual, 43.80)

    def test_nat_cost(self):
        # 1 NAT Gateway: 730 * 0.045 = 32.85
        monthly, annual = calculate_nat_cost()
        self.assertEqual(monthly, 32.85)
        self.assertEqual(annual, 394.20)

    def test_snapshot_cost(self):
        # 200 GB: 200 * 0.05 = 10.00
        monthly, annual = calculate_snapshot_cost(200)
        self.assertEqual(monthly, 10.00)
        self.assertEqual(annual, 120.00)

    def test_alb_cost(self):
        # 1 ALB: 730 * 0.0225 = 16.43
        monthly, annual = calculate_alb_cost()
        self.assertEqual(monthly, 16.43)
        self.assertEqual(annual, 197.10)

    def test_health_score_calculation(self):
        # Score inicial sem zumbis = 100
        self.assertEqual(calculate_health_score([]), 100)

        # 1 CRITICAL (-20), 1 HIGH (-10), 1 MEDIUM (-5) = 100 - 35 = 65
        findings = [
            {"severity": "CRITICAL"},
            {"severity": "HIGH"},
            {"severity": "MEDIUM"},
        ]
        self.assertEqual(calculate_health_score(findings), 65)

        # Muitas penalidades devem limitar no piso de 0
        many_findings = [{"severity": "CRITICAL"}] * 10
        self.assertEqual(calculate_health_score(many_findings), 0)

    def test_remediation_plan_snapshot_safeguard(self):
        findings = [
            {
                "rule_id": "ZH-EBS-001",
                "resource_id": "vol-12345678",
                "resource_type": "ebs_volume",
            }
        ]
        plans = generate_remediation_plans(findings, 96.00)
        cli_script = plans["aws_cli_scripts"][0]
        # Deve conter salvaguarda prévia de snapshot
        self.assertIn("create-snapshot", cli_script)
        self.assertIn("--volume-id vol-12345678", cli_script)
        self.assertIn("aws ec2 delete-volume --volume-id vol-12345678", cli_script)
        self.assertIn("terraform destroy -target=aws_ebs_volume.volume_vol_12345678", plans["terraform_hcl"][0])


class TestFinOpsRulesEngine(unittest.TestCase):
    """Testes determinísticos das 5 regras de detecção de recursos zumbis."""

    def test_zh_ebs_001_unattached_detected(self):
        inventory = {
            "ebs_volumes": [
                {"id": "vol-unattached", "size_gb": 100, "volume_type": "gp3", "state": "available"},
                {"id": "vol-attached", "size_gb": 50, "volume_type": "gp3", "state": "in-use"},
            ]
        }
        res = run_finops_scan(inventory)
        self.assertEqual(res["summary"]["total_zombies_found"], 1)
        self.assertEqual(res["findings"][0]["rule_id"], "ZH-EBS-001")
        self.assertEqual(res["findings"][0]["resource_id"], "vol-unattached")

    def test_zh_eip_001_unassociated_detected(self):
        inventory = {
            "elastic_ips": [
                {"allocation_id": "eipalloc-orphan", "public_ip": "1.2.3.4", "association_id": None},
                {"allocation_id": "eipalloc-used", "public_ip": "5.6.7.8", "association_id": "eipassoc-123"},
            ]
        }
        res = run_finops_scan(inventory)
        self.assertEqual(res["summary"]["total_zombies_found"], 1)
        self.assertEqual(res["findings"][0]["rule_id"], "ZH-EIP-001")
        self.assertEqual(res["findings"][0]["resource_id"], "eipalloc-orphan")

    def test_zh_nat_001_idle_detected_with_grace_period(self):
        inventory = {
            "nat_gateways": [
                # NAT com mais de 24h sem conexões e 0 bytes -> zumbi
                {
                    "id": "nat-idle",
                    "state": "available",
                    "vpc_id": "vpc-01",
                    "bytes_processed_last_7d": 0,
                    "active_connections": 0,
                    "create_time": "2026-01-01T00:00:00Z",
                },
                # NAT com tráfego normal -> não é zumbi
                {
                    "id": "nat-active",
                    "state": "available",
                    "vpc_id": "vpc-02",
                    "bytes_processed_last_7d": 50000000,
                    "active_connections": 10,
                    "create_time": "2026-01-01T00:00:00Z",
                },
                # NAT recém-criado (< 24h) com 0 bytes -> NÃO deve ser detectado (carência)
                {
                    "id": "nat-newly-created",
                    "state": "available",
                    "vpc_id": "vpc-03",
                    "bytes_processed_last_7d": 0,
                    "active_connections": 0,
                    "create_time": "2026-11-26T18:00:00Z",  # Horário recente
                },
            ]
        }
        res = run_finops_scan(inventory)
        self.assertEqual(res["summary"]["total_zombies_found"], 1)
        self.assertEqual(res["findings"][0]["rule_id"], "ZH-NAT-001")
        self.assertEqual(res["findings"][0]["resource_id"], "nat-idle")

    def test_zh_snp_001_orphaned_snapshot_detected(self):
        inventory = {
            "snapshots": [
                # Volume base deletado
                {
                    "id": "snap-orphan",
                    "volume_id": "vol-deleted",
                    "volume_size_gb": 100,
                    "source_volume_exists": False,
                },
                # Volume existe e recente
                {
                    "id": "snap-valid",
                    "volume_id": "vol-active",
                    "volume_size_gb": 50,
                    "source_volume_exists": True,
                    "start_time": "2026-11-20T00:00:00Z",
                },
            ]
        }
        res = run_finops_scan(inventory)
        self.assertEqual(res["summary"]["total_zombies_found"], 1)
        self.assertEqual(res["findings"][0]["rule_id"], "ZH-SNP-001")
        self.assertEqual(res["findings"][0]["resource_id"], "snap-orphan")

    def test_zh_alb_001_empty_targets_detected(self):
        inventory = {
            "load_balancers": [
                # ALB sem target groups
                {
                    "arn": "arn:aws:alb:1",
                    "name": "alb-empty-tg",
                    "type": "application",
                    "target_groups": [],
                },
                # ALB com targets saudáveis
                {
                    "arn": "arn:aws:alb:2",
                    "name": "alb-healthy",
                    "type": "application",
                    "target_groups": [{"registered_targets_count": 2, "healthy_targets_count": 2}],
                },
            ]
        }
        res = run_finops_scan(inventory)
        self.assertEqual(res["summary"]["total_zombies_found"], 1)
        self.assertEqual(res["findings"][0]["rule_id"], "ZH-ALB-001")
        self.assertEqual(res["findings"][0]["resource_id"], "arn:aws:alb:1")


class TestLambdaHandlerREST(unittest.TestCase):
    """Testes de integração das rotas REST e contratos HTTP da Lambda."""

    def test_get_health(self):
        event = {
            "rawPath": "/health",
            "requestContext": {"http": {"method": "GET"}},
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 200)
        self.assertEqual(res["headers"]["Access-Control-Allow-Origin"], "*")

        body = json.loads(res["body"])
        self.assertEqual(body["status"], "healthy")
        self.assertEqual(body["service"], "onion-zombie-hunter")
        self.assertEqual(body["rules_loaded"], 5)

    def test_get_presets(self):
        event = {
            "rawPath": "/presets",
            "requestContext": {"http": {"method": "GET"}},
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 200)

        body = json.loads(res["body"])
        self.assertIn("presets", body)
        preset_ids = [p["id"] for p in body["presets"]]
        self.assertIn("startup_waste", preset_ids)
        self.assertIn("enterprise_sprawl", preset_ids)
        self.assertIn("clean_slate", preset_ids)

    def test_post_scan_with_preset_startup_waste(self):
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"preset": "startup_waste"}),
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 200)

        body = json.loads(res["body"])
        self.assertIn("scan_id", body)
        self.assertIn("summary", body)
        self.assertIn("findings", body)
        self.assertIn("remediation_plans", body)

        summary = body["summary"]
        self.assertGreater(summary["total_zombies_found"], 0)
        self.assertGreater(summary["wasted_monthly_usd"], 0)

        # Checa presença das seções de remediação
        self.assertIn("terraform_hcl", body["remediation_plans"])
        self.assertIn("aws_cli_scripts", body["remediation_plans"])

    def test_post_scan_with_preset_clean_slate(self):
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"preset": "clean_slate"}),
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 200)

        body = json.loads(res["body"])
        summary = body["summary"]
        self.assertEqual(summary["total_zombies_found"], 0)
        self.assertEqual(summary["wasted_monthly_usd"], 0.0)
        self.assertEqual(summary["finops_health_score"], 100)

    def test_post_scan_preset_aliases(self):
        # Alias 'saas_startup_sprawl' e 'clean_well_architected'
        event1 = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"preset": "saas_startup_sprawl"}),
        }
        res1 = lambda_handler(event1)
        self.assertEqual(res1["statusCode"], 200)

        event2 = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"preset": "clean_well_architected"}),
        }
        res2 = lambda_handler(event2)
        self.assertEqual(res2["statusCode"], 200)
        body2 = json.loads(res2["body"])
        self.assertEqual(body2["summary"]["finops_health_score"], 100)

    def test_cors_options_preflight(self):
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "OPTIONS"}},
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 200)
        self.assertEqual(res["headers"]["Access-Control-Allow-Origin"], "*")
        self.assertIn("POST", res["headers"]["Access-Control-Allow-Methods"])

    def test_not_found_route(self):
        event = {
            "rawPath": "/nonexistent",
            "requestContext": {"http": {"method": "GET"}},
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 404)

    def test_bad_request_invalid_json(self):
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": "{ invalid json content ...",
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 400)

    def test_bad_request_unknown_preset(self):
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": json.dumps({"preset": "unknown_preset_123"}),
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 400)

    def test_payload_too_large(self):
        # Gera body > 512 KB (600 KB)
        big_body = json.dumps({"inventory": {"raw_padding": "A" * 600000}})
        event = {
            "rawPath": "/scan",
            "requestContext": {"http": {"method": "POST"}},
            "body": big_body,
        }
        res = lambda_handler(event)
        self.assertEqual(res["statusCode"], 413)


if __name__ == "__main__":
    unittest.main()
