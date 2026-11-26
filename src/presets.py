"""Onion Zombie Hunter — Presets Realistas de Demonstração FinOps.

Fornece cenários pré-configurados prontos para auditoria imediata no motor
e consumo em 1 clique na interface web.
"""

from typing import Any

PRESETS_DATA: dict[str, dict[str, Any]] = {
    "startup_waste": {
        "id": "startup_waste",
        "name": "Startup em Crescimento Rápido (Desperdício Ocioso Típico)",
        "description": "Volumes EBS esquecidos após deploys, EIPs órfãos e um NAT Gateway inativo em VPC de staging.",
        "resource_counts": {
            "ebs_volumes": 2,
            "elastic_ips": 2,
            "nat_gateways": 1,
            "snapshots": 1,
            "load_balancers": 0,
        },
        "inventory": {
            "ebs_volumes": [
                {
                    "id": "vol-0a1b2c3d4e5f67890",
                    "size_gb": 100,
                    "volume_type": "gp3",
                    "state": "available",
                    "create_time": "2026-08-15T10:00:00Z",
                    "tags": {
                        "Environment": "staging",
                        "Project": "legacy-app",
                    },
                },
                {
                    "id": "vol-0f9e8d7c6b5a43210",
                    "size_gb": 50,
                    "volume_type": "gp2",
                    "state": "available",
                    "create_time": "2026-09-01T12:00:00Z",
                    "tags": {
                        "Environment": "dev",
                        "Project": "experiment",
                    },
                },
            ],
            "elastic_ips": [
                {
                    "allocation_id": "eipalloc-0123456789abcdef0",
                    "public_ip": "54.210.10.45",
                    "association_id": None,
                    "tags": {
                        "Name": "dev-bastion-ip",
                    },
                },
                {
                    "allocation_id": "eipalloc-0fedcba9876543210",
                    "public_ip": "52.86.99.12",
                    "association_id": None,
                    "tags": {
                        "Name": "staging-api-old",
                    },
                },
            ],
            "nat_gateways": [
                {
                    "id": "nat-0987654321fedcba0",
                    "state": "available",
                    "vpc_id": "vpc-0a1b2c3d",
                    "bytes_processed_last_7d": 0,
                    "active_connections": 0,
                    "tags": {
                        "Environment": "staging",
                    },
                },
            ],
            "snapshots": [
                {
                    "id": "snap-0123456789abcdef0",
                    "volume_id": "vol-deleted99999",
                    "volume_size_gb": 200,
                    "start_time": "2025-11-01T08:00:00Z",
                    "source_volume_exists": False,
                    "tags": {
                        "Owner": "ex-contractor",
                    },
                },
            ],
            "load_balancers": [],
        },
    },
    "enterprise_sprawl": {
        "id": "enterprise_sprawl",
        "name": "Corporativo com Sprawl de Ambientes (Desperdício Severo)",
        "description": "Múltiplos ALBs vazios, NAT Gateways ociosos em dev e gigabytes em snapshots órfãos.",
        "resource_counts": {
            "ebs_volumes": 5,
            "elastic_ips": 4,
            "nat_gateways": 2,
            "snapshots": 6,
            "load_balancers": 2,
        },
        "inventory": {
            "ebs_volumes": [
                {
                    "id": "vol-ent001",
                    "size_gb": 500,
                    "volume_type": "gp3",
                    "state": "available",
                    "create_time": "2026-05-10T00:00:00Z",
                    "tags": {"Dept": "DataAnalytics"},
                },
                {
                    "id": "vol-ent002",
                    "size_gb": 200,
                    "volume_type": "gp2",
                    "state": "available",
                    "create_time": "2026-06-11T00:00:00Z",
                    "tags": {"Dept": "BI-Team"},
                },
                {
                    "id": "vol-ent003",
                    "size_gb": 1000,
                    "volume_type": "io1",
                    "state": "available",
                    "create_time": "2026-04-01T00:00:00Z",
                    "tags": {"Dept": "Database-Archive"},
                },
                {
                    "id": "vol-ent004",
                    "size_gb": 80,
                    "volume_type": "gp3",
                    "state": "available",
                    "create_time": "2026-07-20T00:00:00Z",
                    "tags": {"Dept": "CI-CD-Old"},
                },
                {
                    "id": "vol-ent005",
                    "size_gb": 300,
                    "volume_type": "standard",
                    "state": "available",
                    "create_time": "2026-03-15T00:00:00Z",
                    "tags": {"Dept": "Legacy-FileServer"},
                },
            ],
            "elastic_ips": [
                {
                    "allocation_id": "eipalloc-ent01",
                    "public_ip": "3.210.15.1",
                    "association_id": None,
                    "tags": {"Env": "qa-1"},
                },
                {
                    "allocation_id": "eipalloc-ent02",
                    "public_ip": "3.210.15.2",
                    "association_id": None,
                    "tags": {"Env": "qa-2"},
                },
                {
                    "allocation_id": "eipalloc-ent03",
                    "public_ip": "3.210.15.3",
                    "association_id": None,
                    "tags": {"Env": "dev-cluster"},
                },
                {
                    "allocation_id": "eipalloc-ent04",
                    "public_ip": "3.210.15.4",
                    "association_id": None,
                    "tags": {"Env": "sandbox"},
                },
            ],
            "nat_gateways": [
                {
                    "id": "nat-ent-us-east-1a",
                    "state": "available",
                    "vpc_id": "vpc-corp-qa",
                    "bytes_processed_last_7d": 0,
                    "active_connections": 0,
                    "tags": {"Environment": "QA"},
                },
                {
                    "id": "nat-ent-us-east-1b",
                    "state": "available",
                    "vpc_id": "vpc-corp-dev",
                    "bytes_processed_last_7d": 0,
                    "active_connections": 0,
                    "tags": {"Environment": "Dev"},
                },
            ],
            "snapshots": [
                {
                    "id": "snap-ent01",
                    "volume_id": "vol-del-01",
                    "volume_size_gb": 500,
                    "source_volume_exists": False,
                    "start_time": "2025-01-01T00:00:00Z",
                },
                {
                    "id": "snap-ent02",
                    "volume_id": "vol-del-02",
                    "volume_size_gb": 200,
                    "source_volume_exists": False,
                    "start_time": "2025-02-01T00:00:00Z",
                },
                {
                    "id": "snap-ent03",
                    "volume_id": "vol-del-03",
                    "volume_size_gb": 100,
                    "source_volume_exists": False,
                    "start_time": "2025-03-01T00:00:00Z",
                },
                {
                    "id": "snap-ent04",
                    "volume_id": "vol-del-04",
                    "volume_size_gb": 150,
                    "source_volume_exists": False,
                    "start_time": "2025-04-01T00:00:00Z",
                },
                {
                    "id": "snap-ent05",
                    "volume_id": "vol-del-05",
                    "volume_size_gb": 250,
                    "source_volume_exists": False,
                    "start_time": "2025-05-01T00:00:00Z",
                },
                {
                    "id": "snap-ent06",
                    "volume_id": "vol-del-06",
                    "volume_size_gb": 80,
                    "source_volume_exists": False,
                    "start_time": "2025-06-01T00:00:00Z",
                },
            ],
            "load_balancers": [
                {
                    "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/ent-alb-qa/11111111",
                    "name": "ent-alb-qa",
                    "type": "application",
                    "target_groups": [
                        {
                            "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/tg-qa-empty/22222222",
                            "registered_targets_count": 0,
                            "healthy_targets_count": 0,
                        }
                    ],
                },
                {
                    "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/ent-alb-poc/33333333",
                    "name": "ent-alb-poc",
                    "type": "application",
                    "target_groups": [],
                },
            ],
        },
    },
    "dev_sandbox_leak": {
        "id": "dev_sandbox_leak",
        "name": "Sandbox de Desenvolvimento Esquecido",
        "description": "Volumes EBS de instâncias de teste deletadas e EIPs não liberados.",
        "resource_counts": {
            "ebs_volumes": 3,
            "elastic_ips": 1,
            "nat_gateways": 0,
            "snapshots": 2,
            "load_balancers": 1,
        },
        "inventory": {
            "ebs_volumes": [
                {
                    "id": "vol-sbx-01",
                    "size_gb": 120,
                    "volume_type": "gp3",
                    "state": "available",
                },
                {
                    "id": "vol-sbx-02",
                    "size_gb": 50,
                    "volume_type": "gp2",
                    "state": "available",
                },
                {
                    "id": "vol-sbx-03",
                    "size_gb": 30,
                    "volume_type": "gp3",
                    "state": "available",
                },
            ],
            "elastic_ips": [
                {
                    "allocation_id": "eipalloc-sbx-01",
                    "public_ip": "54.198.22.8",
                    "association_id": None,
                },
            ],
            "nat_gateways": [],
            "snapshots": [
                {
                    "id": "snap-sbx-01",
                    "volume_id": "vol-lost-01",
                    "volume_size_gb": 80,
                    "source_volume_exists": False,
                },
                {
                    "id": "snap-sbx-02",
                    "volume_id": "vol-lost-02",
                    "volume_size_gb": 60,
                    "source_volume_exists": False,
                },
            ],
            "load_balancers": [
                {
                    "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/sbx-alb-idle/44444444",
                    "name": "sbx-alb-idle",
                    "type": "application",
                    "target_groups": [
                        {
                            "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/tg-sbx/55555555",
                            "registered_targets_count": 0,
                            "healthy_targets_count": 0,
                        }
                    ],
                },
            ],
        },
    },
    "clean_slate": {
        "id": "clean_slate",
        "name": "Ambiente 100% Otimizado (Clean Slate)",
        "description": "Conta em total conformidade FinOps sem nenhum recurso zumbi ou desperdício ocioso.",
        "resource_counts": {
            "ebs_volumes": 0,
            "elastic_ips": 0,
            "nat_gateways": 0,
            "snapshots": 0,
            "load_balancers": 0,
        },
        "inventory": {
            "ebs_volumes": [
                {
                    "id": "vol-prod-active",
                    "size_gb": 250,
                    "volume_type": "gp3",
                    "state": "in-use",
                    "attachments": [{"instance_id": "i-0123456789abcdef0"}],
                }
            ],
            "elastic_ips": [
                {
                    "allocation_id": "eipalloc-prod-active",
                    "public_ip": "54.210.200.1",
                    "association_id": "eipassoc-0a1b2c3d4e5f67890",
                    "instance_id": "i-0123456789abcdef0",
                }
            ],
            "nat_gateways": [
                {
                    "id": "nat-prod-active",
                    "state": "available",
                    "vpc_id": "vpc-prod",
                    "bytes_processed_last_7d": 524288000,
                    "active_connections": 128,
                }
            ],
            "snapshots": [
                {
                    "id": "snap-prod-recent",
                    "volume_id": "vol-prod-active",
                    "volume_size_gb": 250,
                    "source_volume_exists": True,
                    "tags": {"Retention": "30-days"},
                }
            ],
            "load_balancers": [
                {
                    "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/prod-alb/66666666",
                    "name": "prod-alb",
                    "type": "application",
                    "target_groups": [
                        {
                            "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/prod-tg/77777777",
                            "registered_targets_count": 4,
                            "healthy_targets_count": 4,
                        }
                    ],
                }
            ],
        },
    },
}

# Mapeamento de apelidos e aliases comuns (ex: do prompt da Camada 4)
PRESET_ALIASES: dict[str, str] = {
    "startup_waste": "startup_waste",
    "saas_startup_sprawl": "startup_waste",
    "saas-startup-sprawl": "startup_waste",
    "enterprise_sprawl": "enterprise_sprawl",
    "enterprise_finops_leak": "enterprise_sprawl",
    "enterprise-finops-leak": "enterprise_sprawl",
    "dev_sandbox_leak": "dev_sandbox_leak",
    "clean_slate": "clean_slate",
    "clean_well_architected": "clean_slate",
    "clean-well-architected": "clean_slate",
}


def get_presets_catalog() -> list[dict[str, Any]]:
    """Retorna o catálogo de presets conforme especificado na Seção 8.2 do README.md."""
    catalog = []
    for p in PRESETS_DATA.values():
        catalog.append({
            "id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "resource_counts": p["resource_counts"],
        })
    return catalog


def get_preset_inventory(preset_identifier: str) -> dict[str, Any] | None:
    """Busca o inventário de um preset por ID ou alias normalizado."""
    if not preset_identifier:
        return None

    norm = preset_identifier.strip().lower().replace(" ", "_")
    canonical_id = PRESET_ALIASES.get(norm, norm)

    if canonical_id in PRESETS_DATA:
        return PRESETS_DATA[canonical_id]["inventory"]

    return None
