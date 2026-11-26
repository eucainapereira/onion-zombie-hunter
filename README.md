# Onion Zombie Hunter — Cloud FinOps Waste Sweeper 🧟‍♂️💸

> **Auditor e Varredor Determinístico de Recursos Zumbis e Desperdício Ocioso na AWS**  
> *100% Serverless nativo, Scale-to-Zero permanente sob AWS Free Tier e Governança Rigorosa de FinOps.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![AWS Architecture](https://img.shields.io/badge/AWS-Serverless-orange.svg)](https://aws.amazon.com/)
[![Runtime: Python 3.12](https://img.shields.io/badge/Python-3.12%20Stdlib-green.svg)](https://www.python.org/)
[![IaC: Terraform](https://img.shields.io/badge/IaC-Terraform%201.5%2B-purple.svg)](https://www.terraform.io/)
[![FinOps: Scale--to--Zero](https://img.shields.io/badge/FinOps-Scale--to--Zero-success.svg)](https://www.finops.org/)

---

## 1. Visão Geral

O **Onion Zombie Hunter** é uma solução de auditoria e governança financeira em nuvem (*Cloud FinOps*) de alta precisão, desenvolvida especificamente para identificar, quantificar e remediar **recursos zumbis ociosos e esquecidos** em ambientes Amazon Web Services (AWS).

Em ecossistemas ágeis de DevOps e Cloud Computing, desenvolvedores e pipelines provisionam e descartam infraestruturas com alta rotatividade. No entanto, o processo de decomissão muitas vezes é imperfeito: discos são desanexados mas nunca deletados, IPs elásticos perdem suas instâncias e passam a ser tarifados por hora, NAT Gateways de ambientes desativados continuam faturando 24x7, snapshots de volumes há muito extintos acumulam-se no S3 e balanceadores de carga vazios continuam drenando orçamentos corporativos.

O **Onion Zombie Hunter** atua como um varredor cirúrgico que:
- Executa **5 regras de detecção determinística FinOps** de alta fidelidade.
- Calcula instantaneamente o **rombo financeiro mensal e anual projetado (em USD)**.
- Gera um indicador unificado de saúde financeira (**FinOps Health Score de 0 a 100**).
- Fornece planos de remediação automatizados com **scripts AWS CLI dotados de salvaguardas prévias de snapshot** e **blocos de código Terraform HCL**.
- Opera sob o paradigma estrito de **Scale-to-Zero**, mantendo um custo fixo de **US$ 0.00/mês em ociosidade**.

---

## 2. O Problema de Negócio e o Rombo Financeiro FinOps

### O Fenômeno do "Zombie Cloud Waste"
Estudos da FinOps Foundation e de grandes consultorias de cloud apontam que entre **25% e 35% do gasto total em infraestrutura pública de nuvem é desperdiçado** em recursos superdimensionados ou completamente ociosos. Os recursos zumbis são particularmente perigosos porque:
1. **Passam despercebidos por métricas de CPU/Memória:** Um volume EBS desanexado tem 0% de uso de CPU, um IP desassociado não gera alertas de tráfego e um NAT Gateway sem pacotes não aciona limites do CloudWatch.
2. **Cobrança Ininterrupta 24x7:** Serviços como NAT Gateways e ALBs faturam taxa horária fixa independentemente do tráfego.
3. **Efeito Acumulativo Silencioso:** Dezenas de volumes órfãos e centenas de gigabytes em snapshots antigos drenam silenciosamente milhares de dólares todos os anos sem produzir nenhum valor para o negócio.

### Anatomia dos 5 Grandes Vazamentos de Nuvem na AWS

```
+----------------------------------------------------------------------------------------------------+
|                                    ROMBO FINANCEIRO TÍPICO ANUAL                                   |
|                                                                                                    |
|   NAT Gateway Ocioso (1 unidade sem tráfego)       ---------->  US$  394.20 / ano                  |
|   NAT Gateways Ociosos (Multi-AZ, 3 unidades)      ---------->  US$ 1,182.60 / ano                  |
|   Application Load Balancer (ALB sem Targets)      ---------->  US$  197.10 / ano                  |
|   Volume EBS gp3 Desanexado (1x 200 GB)            ---------->  US$  192.00 / ano                  |
|   Elastic IP Órfão (2x endereços desassociados)    ---------->  US$   87.60 / ano                  |
|   Snapshots Abandonados (5x 100 GB s/ volume base) ---------->  US$  300.00 / ano                  |
|                                                                                                    |
|   TOTAL DESPERDIÇADO EM UM SANDBOX ESQUECIDO:     ---------->  US$ 2,353.50+ / ano                |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Arquitetura da Solução (100% Serverless & Scale-to-Zero)

O **Onion Zombie Hunter** foi projetado seguindo a regra inegociável de **FinOps Scale-to-Zero**: a própria ferramenta de combate ao desperdício **nunca deve gerar custos ociosos**.

### Princípios Rigorosos de Governança de Infraestrutura:
- **Proibição Expressa:** É terminantemente proibido o provisionamento de recursos com custo fixo ou ocioso na infraestrutura da ferramenta (tais como instâncias EC2, clusters Amazon EKS, instâncias de banco de dados Amazon RDS, clusters ElastiCache ou NAT Gateways dedicados).
- **Arquitetura Enxuta Tripartite:** Toda a aplicação reside exclusivamente em três serviços gerenciados sem servidor:
  1. **Amazon S3 Static Website:** Hospedagem da Single Page Application (HTML5, CSS3, Vanilla JS).
  2. **Amazon API Gateway HTTP API v2:** Roteamento com latência submilisegundo, CORS global habilitado e custo até 70% inferior a APIs REST tradicionais.
  3. **AWS Lambda (Python 3.12 Stdlib):** Computação orientada a eventos, com execução estritamente baseada na biblioteca padrão do Python (**sem dependências pip externas**), eliminando falhas de empacotamento, vulnerabilidades de cadeia de suprimentos e layers inchadas.

### Diagrama de Arquitetura

```mermaid
flowchart TD
    subgraph Client["Camada do Cliente (Navegador Web)"]
        Browser["Usuário / Engenheiro FinOps / SRE<br/>(Interface Web SPA)"]
    end

    subgraph AWS_Cloud["AWS Cloud (Região us-east-1 / us-east-2)"]
        subgraph Frontend_Layer["1. Camada de Apresentação (Scale-to-Zero)"]
            S3["Amazon S3 Static Website<br/><code>onion-zh-frontend-&lt;account&gt;-&lt;region&gt;</code><br/><i>HTML5 / Modern Dark CSS / Vanilla JS</i>"]
        end

        subgraph Ingress_Layer["2. Ponto de Entrada & Roteamento"]
            APIGW["Amazon API Gateway HTTP API v2<br/><code>onion-zh-api</code><br/><i>CORS: Allow-Origin * | Proxy Integrations</i>"]
        end

        subgraph Backend_Layer["3. Motor de Auditoria FinOps (Python 3.12)"]
            Lambda["AWS Lambda Function<br/><code>onion-zh-engine</code><br/><i>Python 3.12 Runtime | Stdlib Only</i>"]
            
            subgraph RulesEngine["5 Regras Determinísticas FinOps"]
                R1["<b>ZH-EBS-001</b><br/>EBS Volumes Desanexados"]
                R2["<b>ZH-EIP-001</b><br/>Elastic IPs Órfãos"]
                R3["<b>ZH-NAT-001</b><br/>NAT Gateways Ociosos"]
                R4["<b>ZH-SNP-001</b><br/>Snapshots Abandonados"]
                R5["<b>ZH-ALB-001</b><br/>ALBs sem Targets"]
            end

            subgraph DataSources["Fontes de Análise"]
                Presets["Presets Realistas de Demonstração<br/>(startup_waste, enterprise_sprawl, ...)"]
                LiveInv["Inventário JSON Submetido<br/>(AWS Resource Payload)"]
            end
        end

        subgraph Observability["4. Observabilidade & Logs"]
            CW["Amazon CloudWatch Logs<br/><code>/aws/lambda/onion-zh-engine</code><br/><i>Retenção Rígida: 7 dias</i>"]
        end
    end

    Browser -->|1. Carrega SPA via HTTP/HTTPS| S3
    Browser -->|2. GET /health & GET /presets| APIGW
    Browser -->|3. POST /scan (Preset ou Inventário)| APIGW
    APIGW -->|4. Proxy Event| Lambda
    Lambda --> DataSources
    DataSources --> RulesEngine
    RulesEngine -->|5. Calcula Score & Desperdício USD| Lambda
    Lambda -.->|Logs de Execução (Zero Custo Extra)| CW
    Lambda -->|6. JSON Response Padronizado| APIGW
    APIGW -->|7. Resposta HTTP 200 OK| Browser
```

---

## 4. Convenção Canônica de Nomenclatura (`onion-zh-*`)

Para assegurar governança, rastreabilidade e evitar conflitos em ambientes compartilhados da AWS, **todos** os recursos provisionados utilizam obrigatoriamente o prefixo canônico **`onion-zh-*`**:

| Recurso AWS | Identificador / Padrão de Nomenclatura | Finalidade Técnica |
| :--- | :--- | :--- |
| **S3 Bucket (Frontend)** | `onion-zh-frontend-<account_id>-<region>` | Hospedagem dos assets estáticos da SPA (`index.html`, `styles.css`, `app.js`). |
| **API Gateway (HTTP API)**| `onion-zh-api` | Endpoint HTTP API v2 com integração AWS_PROXY e CORS habilitado. |
| **Lambda Function** | `onion-zh-engine` | Função serveless em Python 3.12 contendo o motor de regras FinOps. |
| **IAM Role (Lambda)** | `onion-zh-lambda-role` | Role com permissão de assunção (`sts:AssumeRole`) para o serviço Lambda. |
| **IAM Policy (Lambda)** | `onion-zh-lambda-policy` | Política de menor privilégio para envio de logs ao CloudWatch. |
| **CloudWatch Log Group** | `/aws/lambda/onion-zh-engine` | Grupo de logs de execução com retenção máxima mandatória de **7 dias**. |

---

## 5. As 5 Regras de Detecção Determinística FinOps

As regras operam de forma puramente determinística sobre os metadados dos recursos da AWS:

```
+--------------------------------------------------------------------------------------------------------+
|                                    MATRIZ DE REGRAS DETERMINÍSTICAS                                    |
+------------+---------------------------+----------+---------------------------------+----------------+
| Código     | Nome da Regra             | Gravidade| Condição Lógica de Disparo      | Custo Base     |
+------------+---------------------------+----------+---------------------------------+----------------+
| ZH-EBS-001 | EBS Volumes Desanexados   | HIGH     | state == 'available'            | $0.08/GB-mês   |
| ZH-EIP-001 | Elastic IPs Órfãos        | MEDIUM   | association_id == null          | $0.005/hora    |
| ZH-NAT-001 | NAT Gateways Ociosos      | CRITICAL | bytes_7d == 0 & connections == 0| $0.045/hora    |
| ZH-SNP-001 | Snapshots Abandonados     | HIGH     | source_volume_exists == false   | $0.05/GB-mês   |
| ZH-ALB-001 | ALBs sem Targets          | HIGH     | registered_targets_count == 0   | $0.0225/hora   |
+------------+---------------------------+----------+---------------------------------+----------------+
```

### 1. `ZH-EBS-001` — EBS Volumes Desanexados (Unattached Volumes)
- **Critério:** Volumes EBS com estado `available` (não associados a nenhuma instância EC2 ativa).
- **Racional:** Quando uma instância EC2 é encerrada sem a diretiva `DeleteOnTermination`, o volume persiste no storage da AWS, gerando cobrança proporcional ao tamanho e tipo provisionado.
- **Fórmula de Custo:**
  - `gp3`: Tamanho (GB) × US$ 0.08 / mês
  - `gp2`: Tamanho (GB) × US$ 0.10 / mês
  - `io1` / `io2`: Tamanho (GB) × US$ 0.125 / mês (+ custo de IOPS provisionado)
  - `standard` / `st1` / `sc1`: Tamanho (GB) × US$ 0.045 / mês

### 2. `ZH-EIP-001` — Elastic IPs Órfãos (Unassociated EIPs)
- **Critério:** Endereços IPv4 elásticos (`eipalloc-*`) que possuem `association_id == null` ou `instance_id == null`.
- **Racional:** A AWS penaliza financeiramente a reserva de endereços IPv4 públicos que não estão vinculados a uma interface de rede ou instância ativa, cobrando US$ 0.005 por hora ociosa.
- **Fórmula de Custo:** US$ 0.005/hora × 730 horas = **US$ 3.65 / mês (US$ 43.80 / ano)** por endereço órfão.

### 3. `ZH-NAT-001` — NAT Gateways Ociosos (Idle NAT Gateways)
- **Critério:** NAT Gateway em estado `available` cujo tráfego de dados nos últimos 7 dias (`bytes_processed_last_7d`) seja igual a 0 e o número de conexões ativas seja 0.
- **Racional:** Um dos maiores geradores de desperdício invisível. Mantido frequentemente ativo em sub-redes de staging ou testes inativos. Possui taxa horária de US$ 0.045/hora mesmo sem processar pacotes.
- **Fórmula de Custo:** US$ 0.045/hora × 730 horas = **US$ 32.85 / mês (US$ 394.20 / ano)** por unidade ociosa. Em arquiteturas Multi-AZ com 3 NAT Gateways: **US$ 98.55 / mês (US$ 1,182.60 / ano)**.

### 4. `ZH-SNP-001` — Snapshots Abandonados (Orphaned Snapshots)
- **Critério:** Snapshots EBS cujo volume de origem já foi completamente deletado da conta (`source_volume_exists == false`), ou snapshots sem tags de retenção com mais de 90 dias de idade.
- **Racional:** Backups manuais ou snapshots pontuais de volumes temporários ficam armazenados no S3 sem política de ciclo de vida (DLM) e continuam sendo tarifados indefinidamente.
- **Fórmula de Custo:** Tamanho do Volume Base (GB) × US$ 0.05 / mês. Um snapshot de 200 GB abandonado custa **US$ 10.00 / mês (US$ 120.00 / ano)**.

### 5. `ZH-ALB-001` — Application Load Balancers sem Targets (Empty ALBs)
- **Critério:** ALBs com status `active` cujos Target Groups associados possuem `registered_targets_count == 0` ou `healthy_targets_count == 0`.
- **Racional:** Balanceadores criados para testes ou deixados para trás após migrações de containers/EC2 cobram taxa horária de US$ 0.0225/hora mais unidades de capacidade (LCU) mesmo sem encaminhar nenhuma requisição.
- **Fórmula de Custo:** US$ 0.0225/hora × 730 horas = **US$ 16.43 / mês (US$ 197.10 / ano)** por balanceador vazio.

---

## 6. Algoritmo do FinOps Health Score (0 a 100)

O **FinOps Health Score** é uma métrica normalizada que expressa a saúde orçamentária do ambiente:

$$\text{Score} = \max\left(0, 100 - \sum \text{Penalidades}\right)$$

### Pesos de Penalidade por Recurso Zumbi:
- **Gravidade CRÍTICA (`CRITICAL`):** -20 pontos (ex: NAT Gateway ocioso sem tráfego).
- **Gravidade ALTA (`HIGH`):** -10 pontos (ex: ALB vazio, Snapshot abandonado > 50 GB, Volume EBS > 100 GB).
- **Gravidade MÉDIA (`MEDIUM`):** -5 pontos (ex: Elastic IP órfão, Volume EBS ≤ 100 GB).
- **Gravidade BAIXA (`LOW`):** -2 pontos.

### Faixas de Classificação:
- **90 – 100:** 🟢 **Excelente / Otimizado** — Ambiente em estrita conformidade FinOps.
- **75 – 89:** 🟡 **Bom / Atenção Moderada** — Pequenos resíduos detectados; remediação recomendada.
- **50 – 74:** 🟠 **Risco FinOps Elevado** — Rombo orçamentário relevante; ação corretiva necessária.
- **0 – 49:** 🔴 **Crítico / Desperdício Severo** — Múltiplos recursos caros ociosos drenando o orçamento.

---

## 7. Matriz de Precificação AWS (Infraestrutura da Aplicação vs. Recursos Detectados)

### 7.1. Custo de Operação da Solução (Scale-to-Zero)

Todos os componentes operam integralmente dentro da camada perpétua do **AWS Free Tier**:

| Componente | Nível de Serviço | Custo Fixo Ocioso | Custo sob Uso Médio (10.000 scans/mês) |
| :--- | :--- | :--- | :--- |
| **Amazon S3 (SPA)** | 5 MB de storage, < 1.000 requisições GET | **US$ 0.00** | < US$ 0.01 / mês |
| **Amazon API Gateway** | HTTP API v2 (1M requisições gratuitas/mês) | **US$ 0.00** | **US$ 0.00** (coberto pelo Free Tier) |
| **AWS Lambda** | Python 3.12 (128 MB RAM, ~80ms de runtime) | **US$ 0.00** | **US$ 0.00** (coberto pelos 3.2M seg grátis) |
| **Amazon CloudWatch** | Log Group com retenção de 7 dias | **US$ 0.00** | < US$ 0.01 / mês |
| **TOTAL MENSAL ESTIMADO** | **Solução 100% Serverless** | **US$ 0.00 / mês** | **< US$ 0.02 / mês** |
| **TOTAL ANUAL ESTIMADO** | **Solução 100% Serverless** | **US$ 0.00 / ano** | **< US$ 0.24 / ano** |

### 7.2. Tabela de Precificação de Recursos Zumbis Detectados

| Código da Regra | Recurso AWS | Preço Unitário Oficial AWS | Custo Mensal Projetado | Custo Anual Projetado |
| :--- | :--- | :--- | :--- | :--- |
| `ZH-EBS-001` | Volume EBS gp3 (100 GB) | US$ 0.080 / GB-mês | **US$ 8.00** | **US$ 96.00** |
| `ZH-EBS-001` | Volume EBS gp2 (200 GB) | US$ 0.100 / GB-mês | **US$ 20.00** | **US$ 240.00** |
| `ZH-EIP-001` | Elastic IP Órfão (1 IP) | US$ 0.005 / hora | **US$ 3.65** | **US$ 43.80** |
| `ZH-NAT-001` | NAT Gateway Ocioso (1 AZ) | US$ 0.045 / hora | **US$ 32.85** | **US$ 394.20** |
| `ZH-NAT-001` | NAT Gateways Ociosos (3 AZs)| US$ 0.135 / hora | **US$ 98.55** | **US$ 1,182.60** |
| `ZH-SNP-001` | Snapshot Órfão (100 GB) | US$ 0.050 / GB-mês | **US$ 5.00** | **US$ 60.00** |
| `ZH-ALB-001` | ALB sem Targets (1 unidade)| US$ 0.0225 / hora | **US$ 16.43** | **US$ 197.10** |

---

## 8. Contrato Exato de API (HTTP API v2)

A API aceita e responde no formato `application/json` e implementa cabeçalhos CORS completos (`Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, POST, OPTIONS`, `Access-Control-Allow-Headers: Content-Type`).

### 8.1. `GET /health`
Verifica a saúde operacional da função Lambda e do motor de regras.

#### Requisição
```http
GET /health HTTP/1.1
Host: <api_id>.execute-api.<region>.amazonaws.com
```

#### Resposta (HTTP 200 OK)
```json
{
  "status": "healthy",
  "service": "onion-zombie-hunter",
  "engine_version": "1.0.0",
  "timestamp": "2026-11-26T18:45:00Z",
  "uptime_status": "operational",
  "rules_loaded": 5
}
```

---

### 8.2. `GET /presets`
Retorna os cenários demonstrativos predefinidos com dados de inventário simulados para demonstração imediata no frontend.

#### Requisição
```http
GET /presets HTTP/1.1
Host: <api_id>.execute-api.<region>.amazonaws.com
```

#### Resposta (HTTP 200 OK)
```json
{
  "presets": [
    {
      "id": "startup_waste",
      "name": "Startup em Crescimento Rápido (Desperdício Ocioso Típico)",
      "description": "Volumes EBS esquecidos após deploys, EIPs órfãos e um NAT Gateway inativo em VPC de staging.",
      "resource_counts": {
        "ebs_volumes": 2,
        "elastic_ips": 2,
        "nat_gateways": 1,
        "snapshots": 1,
        "load_balancers": 0
      }
    },
    {
      "id": "enterprise_sprawl",
      "name": "Corporativo com Sprawl de Ambientes (Desperdício Severo)",
      "description": "Múltiplos ALBs vazios, NAT Gateways ociosos em dev e gigabytes em snapshots órfãos.",
      "resource_counts": {
        "ebs_volumes": 5,
        "elastic_ips": 4,
        "nat_gateways": 2,
        "snapshots": 6,
        "load_balancers": 2
      }
    },
    {
      "id": "dev_sandbox_leak",
      "name": "Sandbox de Desenvolvimento Esquecido",
      "description": "Volumes EBS de instâncias de teste deletadas e EIPs não liberados.",
      "resource_counts": {
        "ebs_volumes": 3,
        "elastic_ips": 1,
        "nat_gateways": 0,
        "snapshots": 2,
        "load_balancers": 1
      }
    },
    {
      "id": "clean_slate",
      "name": "Ambiente 100% Otimizado (Clean Slate)",
      "description": "Conta em total conformidade FinOps sem nenhum recurso zumbi ou desperdício ocioso.",
      "resource_counts": {
        "ebs_volumes": 0,
        "elastic_ips": 0,
        "nat_gateways": 0,
        "snapshots": 0,
        "load_balancers": 0
      }
    }
  ]
}
```

---

### 8.3. `POST /scan`
Executa o motor analítico de FinOps. Suporta **duas modalidades de entrada**:
1. **Por Preset:** `{"preset": "startup_waste"}`
2. **Por Inventário Customizado:** `{"inventory": { ... }}`

#### Modalidade A: Requisição com Preset
```json
{
  "preset": "startup_waste"
}
```

#### Modalidade B: Requisição com Inventário Completo
```json
{
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
          "Project": "legacy-app"
        }
      }
    ],
    "elastic_ips": [
      {
        "allocation_id": "eipalloc-0123456789abcdef0",
        "public_ip": "54.210.10.45",
        "association_id": null,
        "tags": {
          "Name": "dev-bastion-ip"
        }
      }
    ],
    "nat_gateways": [
      {
        "id": "nat-0987654321fedcba0",
        "state": "available",
        "vpc_id": "vpc-0a1b2c3d",
        "bytes_processed_last_7d": 0,
        "active_connections": 0,
        "tags": {
          "Environment": "dev"
        }
      }
    ],
    "snapshots": [
      {
        "id": "snap-0123456789abcdef0",
        "volume_id": "vol-deleted99999",
        "volume_size_gb": 200,
        "start_time": "2025-11-01T08:00:00Z",
        "source_volume_exists": false,
        "tags": {
          "Owner": "ex-contractor"
        }
      }
    ],
    "load_balancers": [
      {
        "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/onion-zh-dummy-alb/50dc6c495c0c9188",
        "name": "onion-zh-dummy-alb",
        "type": "application",
        "target_groups": [
          {
            "arn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/empty-tg/73e2d6bc24d8a067",
            "registered_targets_count": 0,
            "healthy_targets_count": 0
          }
        ],
        "tags": {
          "Environment": "test"
        }
      }
    ]
  }
}
```

#### Esquema Completo do JSON de Saída (`HTTP 200 OK`)
```json
{
  "scan_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "engine_version": "1.0.0",
  "timestamp": "2026-11-26T18:45:00Z",
  "summary": {
    "finops_health_score": 62,
    "wasted_monthly_usd": 60.93,
    "wasted_annual_usd": 731.16,
    "total_resources_scanned": 5,
    "total_zombies_found": 5,
    "severity_counts": {
      "critical": 1,
      "high": 2,
      "medium": 2,
      "low": 0,
      "info": 0
    },
    "cost_by_category": {
      "ebs": 8.00,
      "eip": 3.65,
      "nat": 32.85,
      "snapshot": 10.00,
      "alb": 16.43
    }
  },
  "findings": [
    {
      "rule_id": "ZH-EBS-001",
      "resource_id": "vol-0a1b2c3d4e5f67890",
      "resource_type": "ebs_volume",
      "severity": "HIGH",
      "title": "EBS Volume Desanexado (Unattached gp3)",
      "description": "Volume EBS de 100 GB em estado 'available' há mais de 30 dias sem vínculo a instâncias EC2, gerando custo ocioso contínuo.",
      "monthly_waste_usd": 8.00,
      "annual_waste_usd": 96.00,
      "details": {
        "size_gb": 100,
        "volume_type": "gp3",
        "state": "available",
        "created_at": "2026-08-15T10:00:00Z",
        "tags": {
          "Environment": "staging",
          "Project": "legacy-app"
        }
      },
      "remediation": {
        "action": "Criar snapshot preventivo de salvaguarda e excluir o volume EBS órfão",
        "aws_cli": "aws ec2 create-snapshot --volume-id vol-0a1b2c3d4e5f67890 --description 'Salvaguarda pré-deleção Onion Zombie Hunter' && aws ec2 delete-volume --volume-id vol-0a1b2c3d4e5f67890",
        "terraform_hcl": "# Remover a definição do recurso 'aws_ebs_volume' correspondente ou executar:\nterraform destroy -target=aws_ebs_volume.legacy_volume"
      }
    },
    {
      "rule_id": "ZH-EIP-001",
      "resource_id": "eipalloc-0123456789abcdef0",
      "resource_type": "elastic_ip",
      "severity": "MEDIUM",
      "title": "Elastic IP Órfão Desassociado",
      "description": "Endereço IPv4 elástico (54.210.10.45) alocado sem associação ativa a nenhuma interface ENI ou instância EC2.",
      "monthly_waste_usd": 3.65,
      "annual_waste_usd": 43.80,
      "details": {
        "public_ip": "54.210.10.45",
        "allocation_id": "eipalloc-0123456789abcdef0",
        "association_id": null
      },
      "remediation": {
        "action": "Liberar imediatamente o endereço IP estático para o pool da AWS",
        "aws_cli": "aws ec2 release-address --allocation-id eipalloc-0123456789abcdef0",
        "terraform_hcl": "# Remover o bloco 'aws_eip' ou executar:\nterraform destroy -target=aws_eip.orphan_eip"
      }
    },
    {
      "rule_id": "ZH-NAT-001",
      "resource_id": "nat-0987654321fedcba0",
      "resource_type": "nat_gateway",
      "severity": "CRITICAL",
      "title": "NAT Gateway Ocioso sem Tráfego",
      "description": "NAT Gateway ativo na VPC vpc-0a1b2c3d com 0 bytes processados e 0 conexões ativas nos últimos 7 dias.",
      "monthly_waste_usd": 32.85,
      "annual_waste_usd": 394.20,
      "details": {
        "vpc_id": "vpc-0a1b2c3d",
        "bytes_processed_last_7d": 0,
        "active_connections": 0
      },
      "remediation": {
        "action": "Deletar o NAT Gateway ocioso e readequar a tabela de rotas da sub-rede privada",
        "aws_cli": "aws ec2 delete-nat-gateway --nat-gateway-id nat-0987654321fedcba0",
        "terraform_hcl": "# Remover o bloco 'aws_nat_gateway' ou executar:\nterraform destroy -target=aws_nat_gateway.idle_nat"
      }
    },
    {
      "rule_id": "ZH-SNP-001",
      "resource_id": "snap-0123456789abcdef0",
      "resource_type": "snapshot",
      "severity": "HIGH",
      "title": "Snapshot Abandonado (Volume de Origem Excluído)",
      "description": "Snapshot de 200 GB vinculado a volume inexistente (vol-deleted99999) sem política ativa de ciclo de vida.",
      "monthly_waste_usd": 10.00,
      "annual_waste_usd": 120.00,
      "details": {
        "volume_size_gb": 200,
        "original_volume_id": "vol-deleted99999",
        "source_volume_exists": false
      },
      "remediation": {
        "action": "Confirmar obsolescência da imagem e deletar o snapshot abandonado",
        "aws_cli": "aws ec2 delete-snapshot --snapshot-id snap-0123456789abcdef0",
        "terraform_hcl": "# Remover o bloco 'aws_ebs_snapshot' ou executar:\nterraform destroy -target=aws_ebs_snapshot.abandoned_snap"
      }
    },
    {
      "rule_id": "ZH-ALB-001",
      "resource_id": "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/onion-zh-dummy-alb/50dc6c495c0c9188",
      "resource_type": "load_balancer",
      "severity": "HIGH",
      "title": "Application Load Balancer sem Targets Registrados",
      "description": "Balanceador de aplicação ativo com target groups vazios (0 instâncias ou containers registrados).",
      "monthly_waste_usd": 16.43,
      "annual_waste_usd": 197.10,
      "details": {
        "alb_name": "onion-zh-dummy-alb",
        "registered_targets_count": 0,
        "healthy_targets_count": 0
      },
      "remediation": {
        "action": "Descomissionar o Load Balancer e seus respectivos Target Groups vazios",
        "aws_cli": "aws elbv2 delete-load-balancer --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/onion-zh-dummy-alb/50dc6c495c0c9188",
        "terraform_hcl": "# Remover o bloco 'aws_lb' ou executar:\nterraform destroy -target=aws_lb.empty_alb"
      }
    }
  ],
  "remediation_plans": {
    "terraform_hcl": [
      "# =========================================================================\n# PLANO DE REMEDIAÇÃO FINOPS VIA TERRAFORM\n# Remova as seguintes definições do seu arquivo de infraestrutura ou destrua:\n# =========================================================================\nterraform destroy -target=aws_ebs_volume.legacy_volume\nterraform destroy -target=aws_eip.orphan_eip\nterraform destroy -target=aws_nat_gateway.idle_nat\nterraform destroy -target=aws_ebs_snapshot.abandoned_snap\nterraform destroy -target=aws_lb.empty_alb"
    ],
    "aws_cli_scripts": [
      "#!/usr/bin/env bash\n# =========================================================================\n# SCRIPT DE REMEDIAÇÃO AUTOMÁTICA COM SALVAGUARDA DE SEGURANÇA PRÉVIA\n# Gerado por Onion Zombie Hunter v1.0.0\n# =========================================================================\nset -euo pipefail\n\necho '[FINOPS] Iniciando remediação de recursos zumbis...'\n\n# 1. EBS Volumes Desanexados (COM SALVAGUARDA MANDATÓRIA DE SNAPSHOT)\necho '[ZH-EBS-001] Criando snapshot de salvaguarda para vol-0a1b2c3d4e5f67890...'\naws ec2 create-snapshot \\\n  --volume-id vol-0a1b2c3d4e5f67890 \\\n  --description 'Salvaguarda preventiva pré-deleção Onion Zombie Hunter'\necho '[ZH-EBS-001] Deletando volume órfão vol-0a1b2c3d4e5f67890...'\naws ec2 delete-volume --volume-id vol-0a1b2c3d4e5f67890\n\n# 2. Elastic IPs Órfãos\necho '[ZH-EIP-001] Liberando Elastic IP ocioso eipalloc-0123456789abcdef0...'\naws ec2 release-address --allocation-id eipalloc-0123456789abcdef0\n\n# 3. NAT Gateways Ociosos\necho '[ZH-NAT-001] Deletando NAT Gateway ocioso nat-0987654321fedcba0...'\naws ec2 delete-nat-gateway --nat-gateway-id nat-0987654321fedcba0\n\n# 4. Snapshots Abandonados\necho '[ZH-SNP-001] Excluindo snapshot abandonado snap-0123456789abcdef0...'\naws ec2 delete-snapshot --snapshot-id snap-0123456789abcdef0\n\n# 5. ALBs sem Targets\necho '[ZH-ALB-001] Deletando Application Load Balancer vazio...'\naws elbv2 delete-load-balancer \\\n  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/onion-zh-dummy-alb/50dc6c495c0c9188\n\necho '[FINOPS] Remediação concluída com sucesso! Economia anual estimada: US$ 731.16'"
    ]
  }
}
```

---

## 9. Árvore Canônica de Diretórios e Arquivos

Esta é a estrutura exata e vinculante de diretórios e arquivos do repositório:

```text
onion-zombie-hunter/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Testes unitários do motor, linter e validação de síntese Terraform
│       └── deploy.yml             # Pipeline de provisionamento Terraform e sync dos assets web S3
├── iam/
│   ├── lambda-policy.json         # Permissões CloudWatch Logs de menor privilégio
│   └── lambda-assume-role.json    # Trust relationship para execução do AWS Lambda
├── src/
│   ├── __init__.py                # Package initializer da aplicação
│   ├── engine.py                  # Motor das 5 regras de detecção determinística FinOps
│   ├── lambda_function.py         # Handler AWS Lambda, roteamento HTTP e cabeçalhos CORS
│   ├── presets.py                 # Conjuntos predefinidos de dados de teste e demonstração
│   └── pricing.py                 # Matriz de precificação FinOps unitária AWS
├── terraform/
│   ├── main.tf                    # Declaração do provider AWS, constraints e backend
│   ├── variables.tf               # Variáveis de entrada (prefix, aws_region, environment)
│   ├── outputs.tf                 # Outputs canônicos: api_url, frontend_url, s3_bucket_name
│   ├── s3.tf                      # Bucket S3 configurado como Website Hosting estático
│   ├── lambda.tf                  # Função Lambda Python 3.12, zip e permissões
│   └── api_gateway.tf             # API Gateway HTTP API v2 com CORS e rotas
├── web/
│   ├── index.html                 # Interface Single Page Application (SPA) responsiva
│   ├── styles.css                 # Design system FinOps (Dark theme moderno e cartões de métrica)
│   └── app.js                     # Consumo da API, renderização de score e gráficos
├── .gitignore                     # Exclusão estrita de arquivos transitórios, estados e segredos
├── LICENSE                        # Licença permissiva MIT (Cainã Pereira, 2026)
└── README.md                      # Contrato arquitetural normativo e documentação técnica
```

---

## 10. Outputs Canônicos do Terraform

O módulo Terraform expõe estritamente os três outputs normativos abaixo:

| Nome do Output | Tipo | Exemplo de Valor | Descrição |
| :--- | :--- | :--- | :--- |
| `api_url` | `string` | `https://p73sp8ai87.execute-api.us-east-1.amazonaws.com` | URL base do Amazon API Gateway HTTP API v2. |
| `frontend_url` | `string` | `http://onion-zh-frontend-123456789012-us-east-1.s3-website.us-east-1.amazonaws.com` | URL pública do Amazon S3 Static Website. |
| `s3_bucket_name` | `string` | `onion-zh-frontend-123456789012-us-east-1` | Nome físico do bucket S3 onde a SPA é implantada. |

---

## 11. Guia de Deploy e Destruição (Lifecycle Operacional)

### 11.1. Pré-requisitos
- **AWS CLI v2** configurada com credenciais válidas (`aws sts get-caller-identity`).
- **Terraform >= 1.5.0** instalado localmente ou no agente de CI/CD.
- **Python 3.12** instalado para execução de testes locais (opcional).

### 11.2. Provisionamento da Infraestrutura com Terraform

```bash
# 1. Navegue até o diretório de infraestrutura
cd terraform/

# 2. Inicialize os providers e módulos
terraform init

# 3. Valide a sintaxe e planeje a execução
terraform validate
terraform plan -out=tfplan

# 4. Aplique a infraestrutura (criação do S3, API Gateway e Lambda)
terraform apply -auto-approve tfplan

# 5. Capture os outputs canônicos gerados
export API_URL=$(terraform output -raw api_url)
export S3_BUCKET=$(terraform output -raw s3_bucket_name)
export FRONTEND_URL=$(terraform output -raw frontend_url)

echo "API Gateway URL: $API_URL"
echo "Frontend S3 URL: $FRONTEND_URL"
echo "S3 Bucket Name:  $S3_BUCKET"
```

### 11.3. Publicação dos Assets Estáticos (Frontend SPA)

```bash
# Retorne à raiz do projeto
cd ..

# Gere o arquivo de configuração dinâmica para o frontend
echo "window.API_URL = '${API_URL}';" > web/config.js

# Sincronize os arquivos estáticos da SPA diretamente para o S3
aws s3 sync web/ s3://${S3_BUCKET}/ \
  --delete \
  --cache-control "max-age=300"

echo "Deploy do Frontend concluído com sucesso em: ${FRONTEND_URL}"
```

### 11.4. Testes de Validação e Smoke Test

```bash
# 1. Healthcheck da API
curl -s "${API_URL}/health" | jq .

# 2. Consulta de Presets Disponíveis
curl -s "${API_URL}/presets" | jq .

# 3. Execução de Varredura FinOps com Preset Demonstrativo
curl -s -X POST "${API_URL}/scan" \
  -H "Content-Type: application/json" \
  -d '{"preset": "startup_waste"}' | jq .
```

### 11.5. Procedimento de Destruição e Limpeza Completa (Teardown)

Para garantir **zero resíduos** na conta da AWS após os testes:

```bash
# 1. Esvazie o bucket S3 (mandatório antes do destroy)
aws s3 rm s3://${S3_BUCKET}/ --recursive

# 2. Destrua todos os recursos gerenciados pelo Terraform
cd terraform/
terraform destroy -auto-approve

echo "Ambiente completamente destruído. Zero custos remanescentes."
```

---

## 12. Governança e Contribuição

Este projeto é governado sob as práticas do **Onion Flow**, garantindo entrega contínua, arquitetura rastreável e conformidade estrita com os padrões abertos da **FinOps Foundation**.

- **Licença:** Código disponibilizado sob a licença [MIT](LICENSE).
- **Autor:** Cainã Pereira (2026).
