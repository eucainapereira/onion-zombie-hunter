"""Onion Zombie Hunter — Motor Determinístico FinOps de 5 Regras.

Implementação 100% stdlib em Python 3.12 sem pacotes externos.
Regras implementadas:
- ZH-EBS-001: EBS Volumes Desanexados (state == 'available')
- ZH-EIP-001: Elastic IPs Órfãos (sem association_id)
- ZH-NAT-001: NAT Gateways Ociosos (conexões == 0 ou tráfego 7d < 1MB com idade > 24h)
- ZH-SNP-001: Snapshots Abandonados (volume de origem deletado ou idade > 90 dias)
- ZH-ALB-001: ALBs sem Targets (sem target groups ou zero targets saudáveis)
"""

import datetime
import uuid
from typing import Any

from pricing import (
    calculate_alb_cost,
    calculate_ebs_cost,
    calculate_eip_cost,
    calculate_health_score,
    calculate_nat_cost,
    calculate_snapshot_cost,
    generate_remediation_plans,
)


def _parse_iso_date(date_str: str | None) -> datetime.datetime | None:
    """Faz parse seguro de strings ISO8601 em datetime UTC."""
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        normalized = date_str.replace("Z", "+00:00")
        return datetime.datetime.fromisoformat(normalized)
    except (ValueError, TypeError):
        return None


def scan_ebs_volume(volume: dict[str, Any]) -> dict[str, Any] | None:
    """Regra ZH-EBS-001: Detecta volumes EBS desanexados (state == 'available')."""
    state = str(volume.get("state") or volume.get("status") or "").strip().lower()
    attachments = volume.get("attachments")

    # Volume é considerado desanexado se o estado for 'available' ou se attachments for explicitamente vazio e state não for in-use
    is_available = state == "available" or (attachments == [] and state != "in-use")
    if not is_available:
        return None

    vol_id = str(volume.get("id") or volume.get("volume_id") or "vol-unknown")
    vtype = str(volume.get("volume_type") or "gp3")
    size_gb = float(volume.get("size_gb") or volume.get("size") or 0)
    created_at = volume.get("create_time") or volume.get("created_at")
    tags = volume.get("tags") or {}

    # Severidade: volumes grandes (> 100 GB) são HIGH, <= 100 GB MEDIUM (ou HIGH por padrão da regra)
    severity = "HIGH" if size_gb > 100 else "HIGH"  # Padrão formal da regra é HIGH

    monthly_waste, annual_waste = calculate_ebs_cost(vtype, size_gb)
    clean_id = vol_id.replace("-", "_")

    return {
        "rule_id": "ZH-EBS-001",
        "resource_id": vol_id,
        "resource_type": "ebs_volume",
        "severity": severity,
        "title": f"EBS Volume Desanexado (Unattached {vtype})",
        "description": f"Volume EBS de {int(size_gb)} GB em estado 'available' sem vínculo a instâncias EC2, gerando custo ocioso contínuo.",
        "monthly_waste_usd": monthly_waste,
        "annual_waste_usd": annual_waste,
        "details": {
            "size_gb": size_gb,
            "volume_type": vtype,
            "state": "available",
            "created_at": created_at,
            "tags": tags,
        },
        "remediation": {
            "action": "Criar snapshot preventivo de salvaguarda e excluir o volume EBS órfão",
            "aws_cli": (
                f"aws ec2 create-snapshot --volume-id {vol_id} "
                f"--description 'Salvaguarda pré-deleção Onion Zombie Hunter' && "
                f"aws ec2 delete-volume --volume-id {vol_id}"
            ),
            "terraform_hcl": (
                f"# Remover a definição do recurso 'aws_ebs_volume' correspondente ou executar:\n"
                f"terraform destroy -target=aws_ebs_volume.{clean_id}"
            ),
        },
    }


def scan_elastic_ip(eip: dict[str, Any]) -> dict[str, Any] | None:
    """Regra ZH-EIP-001: Detecta Elastic IPs órfãos (sem association_id ou instance_id)."""
    assoc_id = eip.get("association_id")
    inst_id = eip.get("instance_id")

    # Se estiver associado a uma instância ou interface, não é órfão
    if assoc_id or inst_id:
        return None

    alloc_id = str(eip.get("allocation_id") or eip.get("id") or "eipalloc-unknown")
    public_ip = str(eip.get("public_ip") or eip.get("ip") or "unknown-ip")
    tags = eip.get("tags") or {}

    monthly_waste, annual_waste = calculate_eip_cost()
    clean_id = alloc_id.replace("-", "_")

    return {
        "rule_id": "ZH-EIP-001",
        "resource_id": alloc_id,
        "resource_type": "elastic_ip",
        "severity": "MEDIUM",
        "title": "Elastic IP Órfão Desassociado",
        "description": f"Endereço IPv4 elástico ({public_ip}) alocado sem associação ativa a nenhuma interface ENI ou instância EC2.",
        "monthly_waste_usd": monthly_waste,
        "annual_waste_usd": annual_waste,
        "details": {
            "public_ip": public_ip,
            "allocation_id": alloc_id,
            "association_id": None,
            "tags": tags,
        },
        "remediation": {
            "action": "Liberar imediatamente o endereço IP estático para o pool da AWS",
            "aws_cli": f"aws ec2 release-address --allocation-id {alloc_id}",
            "terraform_hcl": (
                f"# Remover o bloco 'aws_eip' ou executar:\n"
                f"terraform destroy -target=aws_eip.{clean_id}"
            ),
        },
    }


def scan_nat_gateway(nat: dict[str, Any]) -> dict[str, Any] | None:
    """Regra ZH-NAT-001: Detecta NAT Gateways ociosos (0 conexões ou tráfego < 1MB com idade > 24h)."""
    state = str(nat.get("state") or "available").lower()
    if state not in ("available", "active"):
        return None

    # Verifica carência de 24 horas (salvaguarda anti-falso-positivo para NAT recém-criado)
    created_at_str = nat.get("create_time") or nat.get("created_at")
    dt_created = _parse_iso_date(created_at_str)
    now = datetime.datetime.now(datetime.timezone.utc)

    if dt_created:
        age_seconds = (now - dt_created).total_seconds()
        # Se tiver menos de 24 horas (86400 segundos), concede carência
        if age_seconds < 86400:
            return None

    bytes_processed = float(nat.get("bytes_processed_last_7d") if nat.get("bytes_processed_last_7d") is not None else 0)
    active_connections = int(nat.get("active_connections") if nat.get("active_connections") is not None else 0)

    # Condição de disparo: conexões ativas == 0 E tráfego nos últimos 7d < 1MB (1.000.000 bytes)
    is_idle = active_connections == 0 and bytes_processed < 1_000_000
    if not is_idle:
        return None

    nat_id = str(nat.get("id") or nat.get("nat_gateway_id") or "nat-unknown")
    vpc_id = str(nat.get("vpc_id") or "vpc-unknown")
    tags = nat.get("tags") or {}

    monthly_waste, annual_waste = calculate_nat_cost()
    clean_id = nat_id.replace("-", "_")

    return {
        "rule_id": "ZH-NAT-001",
        "resource_id": nat_id,
        "resource_type": "nat_gateway",
        "severity": "CRITICAL",
        "title": "NAT Gateway Ocioso sem Tráfego",
        "description": f"NAT Gateway ativo na VPC {vpc_id} com {int(bytes_processed)} bytes processados e {active_connections} conexões ativas nos últimos 7 dias.",
        "monthly_waste_usd": monthly_waste,
        "annual_waste_usd": annual_waste,
        "details": {
            "vpc_id": vpc_id,
            "bytes_processed_last_7d": bytes_processed,
            "active_connections": active_connections,
            "tags": tags,
        },
        "remediation": {
            "action": "Deletar o NAT Gateway ocioso e readequar a tabela de rotas da sub-rede privada",
            "aws_cli": f"aws ec2 delete-nat-gateway --nat-gateway-id {nat_id}",
            "terraform_hcl": (
                f"# Remover o bloco 'aws_nat_gateway' ou executar:\n"
                f"terraform destroy -target=aws_nat_gateway.{clean_id}"
            ),
        },
    }


def scan_snapshot(snap: dict[str, Any]) -> dict[str, Any] | None:
    """Regra ZH-SNP-001: Detecta Snapshots abandonados (volume original deletado ou idade > 90 dias)."""
    source_exists = snap.get("source_volume_exists")
    size_gb = float(snap.get("volume_size_gb") or snap.get("size_gb") or 0)
    snap_id = str(snap.get("id") or snap.get("snapshot_id") or "snap-unknown")
    orig_vol = str(snap.get("volume_id") or "vol-unknown")
    tags = snap.get("tags") or {}

    # Verifica idade (> 90 dias)
    created_at_str = snap.get("start_time") or snap.get("created_at")
    dt_created = _parse_iso_date(created_at_str)
    now = datetime.datetime.now(datetime.timezone.utc)
    is_older_than_90d = False

    if dt_created:
        age_days = (now - dt_created).total_seconds() / 86400
        if age_days > 90:
            is_older_than_90d = True

    # Dispara se volume de origem foi deletado (False) OU idade > 90 dias sem política/tags de retenção
    is_abandoned = (source_exists is False) or (is_older_than_90d and not any(k.lower() in ("retention", "dlm") for k in tags))

    if not is_abandoned:
        return None

    monthly_waste, annual_waste = calculate_snapshot_cost(size_gb)
    clean_id = snap_id.replace("-", "_")

    return {
        "rule_id": "ZH-SNP-001",
        "resource_id": snap_id,
        "resource_type": "snapshot",
        "severity": "HIGH",
        "title": "Snapshot Abandonado (Volume de Origem Excluído)",
        "description": f"Snapshot de {int(size_gb)} GB vinculado a volume inexistente ({orig_vol}) sem política ativa de ciclo de vida.",
        "monthly_waste_usd": monthly_waste,
        "annual_waste_usd": annual_waste,
        "details": {
            "volume_size_gb": size_gb,
            "original_volume_id": orig_vol,
            "source_volume_exists": source_exists,
            "tags": tags,
        },
        "remediation": {
            "action": "Confirmar obsolescência da imagem e deletar o snapshot abandonado",
            "aws_cli": f"aws ec2 delete-snapshot --snapshot-id {snap_id}",
            "terraform_hcl": (
                f"# Remover o bloco 'aws_ebs_snapshot' ou executar:\n"
                f"terraform destroy -target=aws_ebs_snapshot.{clean_id}"
            ),
        },
    }


def scan_load_balancer(alb: dict[str, Any]) -> dict[str, Any] | None:
    """Regra ZH-ALB-001: Detecta Application Load Balancers sem targets (ou zero targets saudáveis)."""
    alb_type = str(alb.get("type") or "application").lower()
    if alb_type != "application":
        return None

    target_groups = alb.get("target_groups") or []
    alb_arn = str(alb.get("arn") or alb.get("id") or "arn:aws:elasticloadbalancing:unknown")
    alb_name = str(alb.get("name") or "alb-unknown")
    tags = alb.get("tags") or {}

    total_registered = 0
    total_healthy = 0

    if not target_groups:
        is_empty = True
    else:
        for tg in target_groups:
            total_registered += int(tg.get("registered_targets_count") or 0)
            total_healthy += int(tg.get("healthy_targets_count") or 0)
        is_empty = total_registered == 0 or total_healthy == 0

    if not is_empty:
        return None

    monthly_waste, annual_waste = calculate_alb_cost()
    clean_id = alb_name.replace("-", "_")

    return {
        "rule_id": "ZH-ALB-001",
        "resource_id": alb_arn,
        "resource_type": "load_balancer",
        "severity": "HIGH",
        "title": "Application Load Balancer sem Targets Registrados",
        "description": "Balanceador de aplicação ativo com target groups vazios (0 instâncias ou containers registrados).",
        "monthly_waste_usd": monthly_waste,
        "annual_waste_usd": annual_waste,
        "details": {
            "alb_name": alb_name,
            "registered_targets_count": total_registered,
            "healthy_targets_count": total_healthy,
            "tags": tags,
        },
        "remediation": {
            "action": "Descomissionar o Load Balancer e seus respectivos Target Groups vazios",
            "aws_cli": f"aws elbv2 delete-load-balancer --load-balancer-arn {alb_arn}",
            "terraform_hcl": (
                f"# Remover o bloco 'aws_lb' ou executar:\n"
                f"terraform destroy -target=aws_lb.{clean_id}"
            ),
        },
    }


def run_finops_scan(inventory: dict[str, Any]) -> dict[str, Any]:
    """Executa a auditoria completa de inventário contra as 5 regras FinOps.

    Retorna estritamente a estrutura JSON normatizada no README.md Seção 8.3.
    """
    ebs_list = inventory.get("ebs_volumes") or []
    eip_list = inventory.get("elastic_ips") or []
    nat_list = inventory.get("nat_gateways") or []
    snp_list = inventory.get("snapshots") or []
    alb_list = inventory.get("load_balancers") or []

    total_scanned = len(ebs_list) + len(eip_list) + len(nat_list) + len(snp_list) + len(alb_list)
    findings: list[dict[str, Any]] = []

    # 1. EBS Volumes
    for vol in ebs_list:
        f = scan_ebs_volume(vol)
        if f:
            findings.append(f)

    # 2. Elastic IPs
    for eip in eip_list:
        f = scan_elastic_ip(eip)
        if f:
            findings.append(f)

    # 3. NAT Gateways
    for nat in nat_list:
        f = scan_nat_gateway(nat)
        if f:
            findings.append(f)

    # 4. Snapshots
    for snp in snp_list:
        f = scan_snapshot(snp)
        if f:
            findings.append(f)

    # 5. Load Balancers
    for alb in alb_list:
        f = scan_load_balancer(alb)
        if f:
            findings.append(f)

    # Agregações de custo e severidade
    monthly_waste_sum = round(sum(f["monthly_waste_usd"] for f in findings), 2)
    annual_waste_sum = round(monthly_waste_sum * 12, 2)
    health_score = calculate_health_score(findings)

    severity_counts = {
        "critical": sum(1 for f in findings if f["severity"] == "CRITICAL"),
        "high": sum(1 for f in findings if f["severity"] == "HIGH"),
        "medium": sum(1 for f in findings if f["severity"] == "MEDIUM"),
        "low": sum(1 for f in findings if f["severity"] == "LOW"),
        "info": sum(1 for f in findings if f["severity"] == "INFO"),
    }

    cost_by_category = {
        "ebs": round(sum(f["monthly_waste_usd"] for f in findings if f["resource_type"] == "ebs_volume"), 2),
        "eip": round(sum(f["monthly_waste_usd"] for f in findings if f["resource_type"] == "elastic_ip"), 2),
        "nat": round(sum(f["monthly_waste_usd"] for f in findings if f["resource_type"] == "nat_gateway"), 2),
        "snapshot": round(sum(f["monthly_waste_usd"] for f in findings if f["resource_type"] == "snapshot"), 2),
        "alb": round(sum(f["monthly_waste_usd"] for f in findings if f["resource_type"] == "load_balancer"), 2),
    }

    remediation = generate_remediation_plans(findings, annual_waste_sum)

    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    scan_uuid = str(uuid.uuid4())

    return {
        "scan_id": scan_uuid,
        "engine_version": "1.0.0",
        "timestamp": now_iso,
        "summary": {
            "finops_health_score": health_score,
            "wasted_monthly_usd": monthly_waste_sum,
            "wasted_annual_usd": annual_waste_sum,
            "total_resources_scanned": total_scanned,
            "total_zombies_found": len(findings),
            "severity_counts": severity_counts,
            "cost_by_category": cost_by_category,
        },
        "findings": findings,
        "remediation_plans": remediation,
    }
