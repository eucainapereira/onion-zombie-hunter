"""Onion Zombie Hunter — Matriz de Precificação FinOps AWS & Planos de Remediação.

Implementação 100% stdlib em conformidade com o README.md e padrão US East (N. Virginia).
"""

from typing import Any

# Constante de horas mensais oficiais de faturamento da AWS (365 dias / 12 meses * 24 horas = 730 horas)
HOURS_PER_MONTH: int = 730

# Tarifas unitárias oficiais AWS US East (N. Virginia)
EBS_RATES_PER_GB_MONTH: dict[str, float] = {
    "gp3": 0.080,
    "gp2": 0.100,
    "io1": 0.125,
    "io2": 0.125,
    "standard": 0.045,
    "st1": 0.045,
    "sc1": 0.045,
}
EBS_DEFAULT_RATE_PER_GB_MONTH: float = 0.080

EIP_HOURLY_RATE: float = 0.005
NAT_HOURLY_RATE: float = 0.045
ALB_HOURLY_RATE: float = 0.0225
SNAPSHOT_RATE_PER_GB_MONTH: float = 0.050

# Penalidades de FinOps Health Score (README Seção 6)
PENALTY_WEIGHTS: dict[str, int] = {
    "CRITICAL": 20,
    "HIGH": 10,
    "MEDIUM": 5,
    "LOW": 2,
    "INFO": 0,
}


def calculate_ebs_cost(volume_type: str | None, size_gb: float | int) -> tuple[float, float]:
    """Calcula custo mensal e anual para volume EBS desanexado."""
    vtype = (volume_type or "gp3").lower()
    rate = EBS_RATES_PER_GB_MONTH.get(vtype, EBS_DEFAULT_RATE_PER_GB_MONTH)
    size = max(0.0, float(size_gb or 0))
    monthly = round(size * rate, 2)
    annual = round(monthly * 12, 2)
    return monthly, annual


def calculate_eip_cost() -> tuple[float, float]:
    """Calcula custo mensal e anual para Elastic IP órfão."""
    monthly = round(EIP_HOURLY_RATE * HOURS_PER_MONTH, 2)  # 3.65
    annual = round(monthly * 12, 2)  # 43.80
    return monthly, annual


def calculate_nat_cost() -> tuple[float, float]:
    """Calcula custo mensal e anual para NAT Gateway ocioso."""
    monthly = round(NAT_HOURLY_RATE * HOURS_PER_MONTH, 2)  # 32.85
    annual = round(monthly * 12, 2)  # 394.20
    return monthly, annual


def calculate_snapshot_cost(size_gb: float | int) -> tuple[float, float]:
    """Calcula custo mensal e anual para Snapshot abandonado."""
    size = max(0.0, float(size_gb or 0))
    monthly = round(size * SNAPSHOT_RATE_PER_GB_MONTH, 2)
    annual = round(monthly * 12, 2)
    return monthly, annual


def calculate_alb_cost() -> tuple[float, float]:
    """Calcula custo mensal e anual para Application Load Balancer sem targets."""
    monthly = round(ALB_HOURLY_RATE * HOURS_PER_MONTH, 2)  # 16.43
    annual = round(ALB_HOURLY_RATE * HOURS_PER_MONTH * 12, 2)  # 197.10
    return monthly, annual


def calculate_health_score(findings: list[dict[str, Any]]) -> int:
    """Calcula o FinOps Health Score normalizado de 0 a 100.

    Fórmula: max(0, 100 - sum(Penalidades))
    """
    if not findings:
        return 100

    total_penalty = 0
    for finding in findings:
        sev = str(finding.get("severity", "MEDIUM")).upper()
        total_penalty += PENALTY_WEIGHTS.get(sev, 5)

    return max(0, min(100, 100 - total_penalty))


def generate_remediation_plans(
    findings: list[dict[str, Any]],
    total_annual_waste: float,
) -> dict[str, list[str]]:
    """Gera planos de remediação estruturados em Terraform HCL e AWS CLI.

    Garante salvaguarda mandatória de snapshot antes de deletar qualquer volume EBS.
    """
    if not findings:
        return {
            "terraform_hcl": [
                "# =========================================================================\n"
                "# PLANO DE REMEDIAÇÃO FINOPS VIA TERRAFORM\n"
                "# Nenhuma ação necessária: ambiente 100% otimizado e sem recursos zumbis!\n"
                "# ========================================================================="
            ],
            "aws_cli_scripts": [
                "#!/usr/bin/env bash\n"
                "# =========================================================================\n"
                "# SCRIPT DE REMEDIAÇÃO AUTOMÁTICA COM SALVAGUARDA DE SEGURANÇA PRÉVIA\n"
                "# Gerado por Onion Zombie Hunter v1.0.0\n"
                "# =========================================================================\n"
                "set -euo pipefail\n\n"
                "echo '[FINOPS] Nenhum recurso zumbi detectado. Ambiente em conformidade!'"
            ],
        }

    tf_lines: list[str] = [
        "# =========================================================================",
        "# PLANO DE REMEDIAÇÃO FINOPS VIA TERRAFORM",
        "# Remova as seguintes definições do seu arquivo de infraestrutura ou destrua:",
        "# =========================================================================",
    ]

    cli_header: list[str] = [
        "#!/usr/bin/env bash",
        "# =========================================================================",
        "# SCRIPT DE REMEDIAÇÃO AUTOMÁTICA COM SALVAGUARDA DE SEGURANÇA PRÉVIA",
        "# Gerado por Onion Zombie Hunter v1.0.0",
        "# =========================================================================",
        "set -euo pipefail",
        "",
        "echo '[FINOPS] Iniciando remediação de recursos zumbis...'",
        "",
    ]

    cli_ebs: list[str] = []
    cli_eip: list[str] = []
    cli_nat: list[str] = []
    cli_snp: list[str] = []
    cli_alb: list[str] = []

    for idx, finding in enumerate(findings, start=1):
        rule_id = finding.get("rule_id", "")
        res_id = finding.get("resource_id", f"res-{idx}")
        res_type = finding.get("resource_type", "")
        clean_id = res_id.replace("arn:aws:", "").replace("/", "_").replace(":", "_").replace("-", "_")

        if rule_id == "ZH-EBS-001":
            tf_lines.append(f"terraform destroy -target=aws_ebs_volume.volume_{clean_id}")
            cli_ebs.append(
                f"# EBS Volume Desanexado (COM SALVAGUARDA MANDATÓRIA DE SNAPSHOT)\n"
                f"echo '[ZH-EBS-001] Criando snapshot de salvaguarda para {res_id}...'\n"
                f"aws ec2 create-snapshot \\\n"
                f"  --volume-id {res_id} \\\n"
                f"  --description 'Salvaguarda preventiva pré-deleção Onion Zombie Hunter'\n"
                f"echo '[ZH-EBS-001] Deletando volume órfão {res_id}...'\n"
                f"aws ec2 delete-volume --volume-id {res_id}\n"
            )
        elif rule_id == "ZH-EIP-001":
            tf_lines.append(f"terraform destroy -target=aws_eip.eip_{clean_id}")
            cli_eip.append(
                f"# Elastic IP Órfão\n"
                f"echo '[ZH-EIP-001] Liberando Elastic IP ocioso {res_id}...'\n"
                f"aws ec2 release-address --allocation-id {res_id}\n"
            )
        elif rule_id == "ZH-NAT-001":
            tf_lines.append(f"terraform destroy -target=aws_nat_gateway.nat_{clean_id}")
            cli_nat.append(
                f"# NAT Gateway Ocioso\n"
                f"echo '[ZH-NAT-001] Deletando NAT Gateway ocioso {res_id}...'\n"
                f"aws ec2 delete-nat-gateway --nat-gateway-id {res_id}\n"
            )
        elif rule_id == "ZH-SNP-001":
            tf_lines.append(f"terraform destroy -target=aws_ebs_snapshot.snap_{clean_id}")
            cli_snp.append(
                f"# Snapshot Abandonado\n"
                f"echo '[ZH-SNP-001] Excluindo snapshot abandonado {res_id}...'\n"
                f"aws ec2 delete-snapshot --snapshot-id {res_id}\n"
            )
        elif rule_id == "ZH-ALB-001":
            tf_lines.append(f"terraform destroy -target=aws_lb.alb_{clean_id}")
            cli_alb.append(
                f"# ALB sem Targets\n"
                f"echo '[ZH-ALB-001] Deletando Application Load Balancer vazio...'\n"
                f"aws elbv2 delete-load-balancer \\\n"
                f"  --load-balancer-arn {res_id}\n"
            )
        else:
            tf_lines.append(f"terraform destroy -target=aws_{res_type}.{clean_id}")

    cli_body_sections = []
    if cli_ebs:
        cli_body_sections.append("# 1. EBS Volumes Desanexados (COM SALVAGUARDA MANDATÓRIA DE SNAPSHOT)\n" + "".join(cli_ebs))
    if cli_eip:
        cli_body_sections.append("# 2. Elastic IPs Órfãos\n" + "".join(cli_eip))
    if cli_nat:
        cli_body_sections.append("# 3. NAT Gateways Ociosos\n" + "".join(cli_nat))
    if cli_snp:
        cli_body_sections.append("# 4. Snapshots Abandonados\n" + "".join(cli_snp))
    if cli_alb:
        cli_body_sections.append("# 5. ALBs sem Targets\n" + "".join(cli_alb))

    cli_footer = f"echo '[FINOPS] Remediação concluída com sucesso! Economia anual estimada: US$ {total_annual_waste:.2f}'\n"

    cli_full_script = "\n".join(cli_header) + "\n".join(cli_body_sections) + "\n" + cli_footer

    return {
        "terraform_hcl": ["\n".join(tf_lines)],
        "aws_cli_scripts": [cli_full_script],
    }
