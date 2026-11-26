/**
 * Onion Zombie Hunter — Aplicação Frontend Single Page (SPA)
 * 100% Vanilla JS sem bibliotecas externas.
 */

(function () {
  "use strict";

  // URL Base da API definida via config.js ou fallback seguro
  const API_BASE = (window.API_URL || "").trim().replace(/\/+$/, "");

  // Presets locais em memória para preenchimento imediato no editor
  const LOCAL_PRESETS = {
    startup_waste: {
      ebs_volumes: [
        {
          id: "vol-0a1b2c3d4e5f67890",
          size_gb: 100,
          volume_type: "gp3",
          state: "available",
          create_time: "2026-08-15T10:00:00Z",
          tags: { Environment: "staging", Project: "legacy-app" },
        },
        {
          id: "vol-0f9e8d7c6b5a43210",
          size_gb: 50,
          volume_type: "gp2",
          state: "available",
          create_time: "2026-09-01T12:00:00Z",
          tags: { Environment: "dev", Project: "experiment" },
        },
      ],
      elastic_ips: [
        {
          allocation_id: "eipalloc-0123456789abcdef0",
          public_ip: "54.210.10.45",
          association_id: null,
          tags: { Name: "dev-bastion-ip" },
        },
        {
          allocation_id: "eipalloc-0fedcba9876543210",
          public_ip: "52.86.99.12",
          association_id: null,
          tags: { Name: "staging-api-old" },
        },
      ],
      nat_gateways: [
        {
          id: "nat-0987654321fedcba0",
          state: "available",
          vpc_id: "vpc-0a1b2c3d",
          bytes_processed_last_7d: 0,
          active_connections: 0,
          create_time: "2026-01-01T00:00:00Z",
          tags: { Environment: "staging" },
        },
      ],
      snapshots: [
        {
          id: "snap-0123456789abcdef0",
          volume_id: "vol-deleted99999",
          volume_size_gb: 200,
          start_time: "2025-11-01T08:00:00Z",
          source_volume_exists: false,
          tags: { Owner: "ex-contractor" },
        },
      ],
      load_balancers: [],
    },

    enterprise_sprawl: {
      ebs_volumes: [
        { id: "vol-ent001", size_gb: 500, volume_type: "gp3", state: "available" },
        { id: "vol-ent002", size_gb: 200, volume_type: "gp2", state: "available" },
        { id: "vol-ent003", size_gb: 1000, volume_type: "io1", state: "available" },
        { id: "vol-ent004", size_gb: 80, volume_type: "gp3", state: "available" },
        { id: "vol-ent005", size_gb: 300, volume_type: "standard", state: "available" },
      ],
      elastic_ips: [
        { allocation_id: "eipalloc-ent01", public_ip: "3.210.15.1", association_id: null },
        { allocation_id: "eipalloc-ent02", public_ip: "3.210.15.2", association_id: null },
        { allocation_id: "eipalloc-ent03", public_ip: "3.210.15.3", association_id: null },
        { allocation_id: "eipalloc-ent04", public_ip: "3.210.15.4", association_id: null },
      ],
      nat_gateways: [
        {
          id: "nat-ent-us-east-1a",
          state: "available",
          vpc_id: "vpc-corp-qa",
          bytes_processed_last_7d: 0,
          active_connections: 0,
          create_time: "2026-01-01T00:00:00Z",
        },
        {
          id: "nat-ent-us-east-1b",
          state: "available",
          vpc_id: "vpc-corp-dev",
          bytes_processed_last_7d: 0,
          active_connections: 0,
          create_time: "2026-01-01T00:00:00Z",
        },
      ],
      snapshots: [
        { id: "snap-ent01", volume_id: "vol-del-01", volume_size_gb: 500, source_volume_exists: false },
        { id: "snap-ent02", volume_id: "vol-del-02", volume_size_gb: 200, source_volume_exists: false },
        { id: "snap-ent03", volume_id: "vol-del-03", volume_size_gb: 100, source_volume_exists: false },
        { id: "snap-ent04", volume_id: "vol-del-04", volume_size_gb: 150, source_volume_exists: false },
        { id: "snap-ent05", volume_id: "vol-del-05", volume_size_gb: 250, source_volume_exists: false },
        { id: "snap-ent06", volume_id: "vol-del-06", volume_size_gb: 80, source_volume_exists: false },
      ],
      load_balancers: [
        {
          arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/ent-alb-qa/11111111",
          name: "ent-alb-qa",
          type: "application",
          target_groups: [
            {
              arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/tg-qa-empty/22222222",
              registered_targets_count: 0,
              healthy_targets_count: 0,
            },
          ],
        },
        {
          arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/ent-alb-poc/33333333",
          name: "ent-alb-poc",
          type: "application",
          target_groups: [],
        },
      ],
    },

    clean_slate: {
      ebs_volumes: [
        {
          id: "vol-prod-active",
          size_gb: 250,
          volume_type: "gp3",
          state: "in-use",
          attachments: [{ instance_id: "i-0123456789abcdef0" }],
        },
      ],
      elastic_ips: [
        {
          allocation_id: "eipalloc-prod-active",
          public_ip: "54.210.200.1",
          association_id: "eipassoc-0a1b2c3d4e5f67890",
          instance_id: "i-0123456789abcdef0",
        },
      ],
      nat_gateways: [
        {
          id: "nat-prod-active",
          state: "available",
          vpc_id: "vpc-prod",
          bytes_processed_last_7d: 524288000,
          active_connections: 128,
          create_time: "2026-01-01T00:00:00Z",
        },
      ],
      snapshots: [
        {
          id: "snap-prod-recent",
          volume_id: "vol-prod-active",
          volume_size_gb: 250,
          source_volume_exists: true,
          tags: { Retention: "30-days" },
        },
      ],
      load_balancers: [
        {
          arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/prod-alb/66666666",
          name: "prod-alb",
          type: "application",
          target_groups: [
            {
              arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/prod-tg/77777777",
              registered_targets_count: 4,
              healthy_targets_count: 4,
            },
          ],
        },
      ],
    },
  };

  // Estado da aplicação
  let currentActiveTab = "cli";
  let lastScanResult = null;

  // Elementos do DOM
  const editor = document.getElementById("inventory-editor");
  const editorFeedback = document.getElementById("editor-feedback");
  const btnRunScan = document.getElementById("btn-run-scan");
  const btnFormatJson = document.getElementById("btn-format-json");
  const btnClearJson = document.getElementById("btn-clear-json");

  const btnPresetStartup = document.getElementById("btn-preset-startup");
  const btnPresetEnterprise = document.getElementById("btn-preset-enterprise");
  const btnPresetClean = document.getElementById("btn-preset-clean");

  const apiStatusBadge = document.getElementById("api-status-badge");
  const apiStatusText = document.getElementById("api-status-text");

  const scanMeta = document.getElementById("scan-meta");
  const kpiScore = document.getElementById("kpi-score");
  const kpiScoreBadge = document.getElementById("kpi-score-badge");
  const scoreProgressFill = document.getElementById("score-progress-fill");
  const kpiMonthly = document.getElementById("kpi-monthly");
  const kpiAnnual = document.getElementById("kpi-annual");
  const kpiZombies = document.getElementById("kpi-zombies");
  const kpiTotalScanned = document.getElementById("kpi-total-scanned");
  const severityMiniBreakdown = document.getElementById("severity-mini-breakdown");

  const catEbs = document.getElementById("cat-ebs");
  const catEip = document.getElementById("cat-eip");
  const catNat = document.getElementById("cat-nat");
  const catSnapshot = document.getElementById("cat-snapshot");
  const catAlb = document.getElementById("cat-alb");

  const findingsTbody = document.getElementById("findings-tbody");
  const findingsCountBadge = document.getElementById("findings-count-badge");

  const tabCli = document.getElementById("tab-cli");
  const tabTf = document.getElementById("tab-tf");
  const scriptCodeDisplay = document.getElementById("script-code-display");
  const btnCopyScript = document.getElementById("btn-copy-script");

  // Sanitização estrita contra XSS
  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Verifica status da API remota
  async function checkApiHealth() {
    if (!API_BASE) {
      if (apiStatusBadge) {
        apiStatusBadge.className = "api-badge online";
        apiStatusText.textContent = "Modo Local / Standalone";
      }
      return;
    }

    try {
      const resp = await fetch(`${API_BASE}/health`, { method: "GET" });
      if (resp.ok) {
        apiStatusBadge.className = "api-badge online";
        apiStatusText.textContent = "API Conectada";
      } else {
        apiStatusBadge.className = "api-badge offline";
        apiStatusText.textContent = "API Degradada";
      }
    } catch (err) {
      apiStatusBadge.className = "api-badge offline";
      apiStatusText.textContent = "API Offline";
    }
  }

  // Carrega Preset no Editor
  function loadPreset(presetKey) {
    const data = LOCAL_PRESETS[presetKey];
    if (data) {
      editor.value = JSON.stringify(data, null, 2);
      clearEditorFeedback();

      // Atualiza botões ativos
      document.querySelectorAll(".preset-card").forEach((card) => card.classList.remove("active"));
      const btn = document.querySelector(`[data-preset="${presetKey}"]`);
      if (btn) btn.classList.add("active");

      // Executa o scan automaticamente para visualização instantânea
      executeScan();
    }
  }

  // Feedback do Editor
  function showEditorFeedback(msg, isError = true) {
    editorFeedback.textContent = msg;
    editorFeedback.className = isError ? "editor-feedback error" : "editor-feedback";
  }

  function clearEditorFeedback() {
    editorFeedback.textContent = "";
    editorFeedback.className = "editor-feedback";
  }

  // Renderização dos Resultados na Interface
  function renderScanResults(data) {
    lastScanResult = data;
    const summary = data.summary || {};
    const findings = data.findings || [];
    const remediation = data.remediation_plans || {};

    // 1. Meta
    scanMeta.textContent = `Scan ID: ${data.scan_id || "N/A"} • Versão: ${data.engine_version || "1.0.0"} • Timestamp: ${data.timestamp || "N/A"}`;

    // 2. Score
    const score = Number(summary.finops_health_score ?? 100);
    kpiScore.textContent = score;
    scoreProgressFill.style.width = `${Math.max(0, Math.min(100, score))}%`;

    if (score >= 90) {
      kpiScoreBadge.className = "score-badge excellent";
      kpiScoreBadge.textContent = "🟢 Excelente / Otimizado";
      scoreProgressFill.style.backgroundColor = "var(--color-success)";
    } else if (score >= 75) {
      kpiScoreBadge.className = "score-badge good";
      kpiScoreBadge.textContent = "🟡 Bom / Atenção Moderada";
      scoreProgressFill.style.backgroundColor = "var(--color-warning)";
    } else if (score >= 50) {
      kpiScoreBadge.className = "score-badge warning";
      kpiScoreBadge.textContent = "🟠 Risco FinOps Elevado";
      scoreProgressFill.style.backgroundColor = "#fb923c";
    } else {
      kpiScoreBadge.className = "score-badge critical";
      kpiScoreBadge.textContent = "🔴 Crítico / Desperdício Severo";
      scoreProgressFill.style.backgroundColor = "var(--color-danger)";
    }

    // 3. Custos Mensal e Anual
    kpiMonthly.textContent = Number(summary.wasted_monthly_usd || 0).toFixed(2);
    kpiAnnual.textContent = Number(summary.wasted_annual_usd || 0).toFixed(2);

    // 4. Totais e Breakdown de Severidade
    const totalZombies = Number(summary.total_zombies_found || 0);
    const totalScanned = Number(summary.total_resources_scanned || 0);
    kpiZombies.textContent = totalZombies;
    kpiTotalScanned.textContent = `/ ${totalScanned} auditados`;

    const sevCounts = summary.severity_counts || {};
    severityMiniBreakdown.innerHTML = `
      <span class="sev-tag critical">${sevCounts.critical || 0} Críticos</span>
      <span class="sev-tag high">${sevCounts.high || 0} Altos</span>
      <span class="sev-tag medium">${sevCounts.medium || 0} Médios</span>
    `;

    // 5. Categorias de Custo
    const catCosts = summary.cost_by_category || {};
    catEbs.textContent = `US$ ${Number(catCosts.ebs || 0).toFixed(2)}`;
    catEip.textContent = `US$ ${Number(catCosts.eip || 0).toFixed(2)}`;
    catNat.textContent = `US$ ${Number(catCosts.nat || 0).toFixed(2)}`;
    catSnapshot.textContent = `US$ ${Number(catCosts.snapshot || 0).toFixed(2)}`;
    catAlb.textContent = `US$ ${Number(catCosts.alb || 0).toFixed(2)}`;

    // 6. Tabela de Achados
    findingsCountBadge.textContent = `${findings.length} zumbis detectados`;

    if (findings.length === 0) {
      findingsTbody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center text-success" style="padding: 2rem 1rem;">
            ✨ Parabéns! Nenhum recurso zumbi ou desperdício ocioso foi detectado neste inventário. Ambiente 100% conforme FinOps!
          </td>
        </tr>
      `;
    } else {
      let rowsHtml = "";
      findings.forEach((f) => {
        const sevClass = String(f.severity || "medium").toLowerCase();
        const ruleId = escapeHtml(f.rule_id);
        const resId = escapeHtml(f.resource_id);
        const resType = escapeHtml(f.resource_type);
        const title = escapeHtml(f.title);
        const desc = escapeHtml(f.description);
        const monthly = Number(f.monthly_waste_usd || 0).toFixed(2);
        const annual = Number(f.annual_waste_usd || 0).toFixed(2);
        const action = escapeHtml(f.remediation?.action || "Remover recurso");

        rowsHtml += `
          <tr>
            <td><span class="badge-rule">${ruleId}</span></td>
            <td><span class="badge-sev ${sevClass}">${escapeHtml(f.severity)}</span></td>
            <td>
              <div class="res-id">${resId}</div>
              <div class="res-type">${resType}</div>
            </td>
            <td>
              <strong>${title}</strong>
              <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">${desc}</div>
            </td>
            <td>
              <div class="waste-amount">US$ ${monthly} <span style="font-size:0.75rem;font-weight:normal;">/mês</span></div>
              <div class="waste-annual-sub">US$ ${annual} /ano</div>
            </td>
            <td><span class="remediation-action">${action}</span></td>
          </tr>
        `;
      });
      findingsTbody.innerHTML = rowsHtml;
    }

    // 7. Atualiza Script de Remediação
    updateScriptViewer();
  }

  // Atualiza Código Exibido no Visualizador
  function updateScriptViewer() {
    if (!lastScanResult || !lastScanResult.remediation_plans) {
      scriptCodeDisplay.textContent = "# Execute uma varredura para visualizar os planos de remediação.";
      return;
    }

    const plans = lastScanResult.remediation_plans;
    if (currentActiveTab === "cli") {
      const cliScripts = plans.aws_cli_scripts || [];
      scriptCodeDisplay.textContent = cliScripts.join("\n\n") || "# Nenhum comando necessário.";
    } else {
      const tfScripts = plans.terraform_hcl || [];
      scriptCodeDisplay.textContent = tfScripts.join("\n\n") || "# Nenhuma alteração necessária.";
    }
  }

  // Execução do Scan (API Remota ou Motor Local Standalone)
  async function executeScan() {
    const rawText = editor.value.trim();
    if (!rawText) {
      showEditorFeedback("O editor de inventário está vazio. Cole um JSON ou selecione um preset.");
      return;
    }

    let parsedInventory;
    try {
      parsedInventory = JSON.parse(rawText);
    } catch (err) {
      showEditorFeedback(`Erro de sintaxe JSON: ${err.message}`);
      return;
    }

    clearEditorFeedback();
    btnRunScan.disabled = true;
    btnRunScan.innerHTML = `<span class="btn-icon">⏳</span> Analisando...`;

    try {
      let resultData = null;

      // Se API_BASE estiver configurado, tenta chamada HTTP POST /scan
      if (API_BASE) {
        try {
          const resp = await fetch(`${API_BASE}/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ inventory: parsedInventory }),
          });

          if (resp.ok) {
            resultData = await resp.json();
          } else {
            console.warn("API remota retornou status não-200. Utilizando motor determinístico local...");
          }
        } catch (fetchErr) {
          console.warn("Falha de rede ao conectar à API remota. Utilizando fallback determinístico...", fetchErr);
        }
      }

      // Se não obteve da API remota, executa motor determinístico local no navegador (offline-first)
      if (!resultData) {
        resultData = simulateLocalFinOpsScan(parsedInventory);
      }

      renderScanResults(resultData);
    } catch (err) {
      showEditorFeedback(`Erro durante a varredura: ${err.message}`);
    } finally {
      btnRunScan.disabled = false;
      btnRunScan.innerHTML = `<span class="btn-icon">🚀</span> Executar Scan FinOps`;
    }
  }

  // Motor FinOps Determinístico Local (Fallback 100% idêntico às 5 regras Python)
  function simulateLocalFinOpsScan(inventory) {
    const ebsList = inventory.ebs_volumes || [];
    const eipList = inventory.elastic_ips || [];
    const natList = inventory.nat_gateways || [];
    const snpList = inventory.snapshots || [];
    const albList = inventory.load_balancers || [];

    const totalScanned = ebsList.length + eipList.length + natList.length + snpList.length + albList.length;
    const findings = [];

    // 1. ZH-EBS-001
    ebsList.forEach((vol) => {
      const state = String(vol.state || vol.status || "").toLowerCase();
      const attachments = vol.attachments;
      const isAvailable = state === "available" || (attachments && attachments.length === 0 && state !== "in-use");

      if (isAvailable) {
        const id = vol.id || vol.volume_id || "vol-unknown";
        const size = Number(vol.size_gb || vol.size || 0);
        const vtype = String(vol.volume_type || "gp3").toLowerCase();
        let rate = 0.08;
        if (vtype === "gp2") rate = 0.10;
        else if (vtype.startsWith("io")) rate = 0.125;
        else if (vtype === "standard" || vtype === "st1" || vtype === "sc1") rate = 0.045;

        const monthly = Math.round(size * rate * 100) / 100;
        const annual = Math.round(monthly * 12 * 100) / 100;

        findings.push({
          rule_id: "ZH-EBS-001",
          resource_id: id,
          resource_type: "ebs_volume",
          severity: "HIGH",
          title: `EBS Volume Desanexado (Unattached ${vtype})`,
          description: `Volume EBS de ${size} GB em estado 'available' sem vínculo a instâncias EC2, gerando custo ocioso contínuo.`,
          monthly_waste_usd: monthly,
          annual_waste_usd: annual,
          remediation: {
            action: "Criar snapshot preventivo de salvaguarda e excluir o volume EBS órfão",
            aws_cli: `aws ec2 create-snapshot --volume-id ${id} --description 'Salvaguarda preventiva pré-deleção Onion Zombie Hunter' && aws ec2 delete-volume --volume-id ${id}`,
            terraform_hcl: `terraform destroy -target=aws_ebs_volume.${id.replace(/-/g, "_")}`,
          },
        });
      }
    });

    // 2. ZH-EIP-001
    eipList.forEach((eip) => {
      if (!eip.association_id && !eip.instance_id) {
        const allocId = eip.allocation_id || "eipalloc-unknown";
        const ip = eip.public_ip || "unknown-ip";
        const monthly = 3.65;
        const annual = 43.80;

        findings.push({
          rule_id: "ZH-EIP-001",
          resource_id: allocId,
          resource_type: "elastic_ip",
          severity: "MEDIUM",
          title: "Elastic IP Órfão Desassociado",
          description: `Endereço IPv4 elástico (${ip}) alocado sem associação ativa a nenhuma interface ENI ou instância EC2.`,
          monthly_waste_usd: monthly,
          annual_waste_usd: annual,
          remediation: {
            action: "Liberar imediatamente o endereço IP estático para o pool da AWS",
            aws_cli: `aws ec2 release-address --allocation-id ${allocId}`,
            terraform_hcl: `terraform destroy -target=aws_eip.${allocId.replace(/-/g, "_")}`,
          },
        });
      }
    });

    // 3. ZH-NAT-001
    natList.forEach((nat) => {
      const state = String(nat.state || "available").toLowerCase();
      if (state === "available" || state === "active") {
        const bytes = Number(nat.bytes_processed_last_7d ?? 0);
        const conns = Number(nat.active_connections ?? 0);
        if (conns === 0 && bytes < 1000000) {
          const natId = nat.id || "nat-unknown";
          const vpcId = nat.vpc_id || "vpc-unknown";
          const monthly = 32.85;
          const annual = 394.20;

          findings.push({
            rule_id: "ZH-NAT-001",
            resource_id: natId,
            resource_type: "nat_gateway",
            severity: "CRITICAL",
            title: "NAT Gateway Ocioso sem Tráfego",
            description: `NAT Gateway ativo na VPC ${vpcId} com ${bytes} bytes processados e ${conns} conexões ativas nos últimos 7 dias.`,
            monthly_waste_usd: monthly,
            annual_waste_usd: annual,
            remediation: {
              action: "Deletar o NAT Gateway ocioso e readequar a tabela de rotas da sub-rede privada",
              aws_cli: `aws ec2 delete-nat-gateway --nat-gateway-id ${natId}`,
              terraform_hcl: `terraform destroy -target=aws_nat_gateway.${natId.replace(/-/g, "_")}`,
            },
          });
        }
      }
    });

    // 4. ZH-SNP-001
    snpList.forEach((snp) => {
      const sourceExists = snp.source_volume_exists;
      if (sourceExists === false) {
        const snapId = snp.id || "snap-unknown";
        const origVol = snp.volume_id || "vol-unknown";
        const size = Number(snp.volume_size_gb || 0);
        const monthly = Math.round(size * 0.05 * 100) / 100;
        const annual = Math.round(monthly * 12 * 100) / 100;

        findings.push({
          rule_id: "ZH-SNP-001",
          resource_id: snapId,
          resource_type: "snapshot",
          severity: "HIGH",
          title: "Snapshot Abandonado (Volume de Origem Excluído)",
          description: `Snapshot de ${size} GB vinculado a volume inexistente (${origVol}) sem política ativa de ciclo de vida.`,
          monthly_waste_usd: monthly,
          annual_waste_usd: annual,
          remediation: {
            action: "Confirmar obsolescência da imagem e deletar o snapshot abandonado",
            aws_cli: `aws ec2 delete-snapshot --snapshot-id ${snapId}`,
            terraform_hcl: `terraform destroy -target=aws_ebs_snapshot.${snapId.replace(/-/g, "_")}`,
          },
        });
      }
    });

    // 5. ZH-ALB-001
    albList.forEach((alb) => {
      const tgs = alb.target_groups || [];
      let totalTargets = 0;
      tgs.forEach((tg) => {
        totalTargets += Number(tg.registered_targets_count || 0);
      });

      if (tgs.length === 0 || totalTargets === 0) {
        const arn = alb.arn || alb.name || "alb-unknown";
        const monthly = 16.43;
        const annual = 197.10;

        findings.push({
          rule_id: "ZH-ALB-001",
          resource_id: arn,
          resource_type: "load_balancer",
          severity: "HIGH",
          title: "Application Load Balancer sem Targets Registrados",
          description: "Balanceador de aplicação ativo com target groups vazios (0 instâncias ou containers registrados).",
          monthly_waste_usd: monthly,
          annual_waste_usd: annual,
          remediation: {
            action: "Descomissionar o Load Balancer e seus respectivos Target Groups vazios",
            aws_cli: `aws elbv2 delete-load-balancer --load-balancer-arn ${arn}`,
            terraform_hcl: `terraform destroy -target=aws_lb.${String(alb.name || "empty_alb").replace(/-/g, "_")}`,
          },
        });
      }
    });

    // Agregações
    const monthlySum = Math.round(findings.reduce((acc, f) => acc + f.monthly_waste_usd, 0) * 100) / 100;
    const annualSum = Math.round(monthlySum * 12 * 100) / 100;

    let penalties = 0;
    findings.forEach((f) => {
      if (f.severity === "CRITICAL") penalties += 20;
      else if (f.severity === "HIGH") penalties += 10;
      else if (f.severity === "MEDIUM") penalties += 5;
      else if (f.severity === "LOW") penalties += 2;
    });

    const score = Math.max(0, 100 - penalties);

    // Remediation Scripts
    const cliCommands = findings.map((f) => f.remediation.aws_cli);
    const cliScript = [
      "#!/usr/bin/env bash",
      "# =========================================================================",
      "# SCRIPT DE REMEDIAÇÃO AUTOMÁTICA COM SALVAGUARDA DE SEGURANÇA PRÉVIA",
      "# Gerado por Onion Zombie Hunter v1.0.0",
      "# =========================================================================",
      "set -euo pipefail",
      "",
      "echo '[FINOPS] Iniciando remediação de recursos zumbis...'",
      "",
      cliCommands.join("\n"),
      "",
      `echo '[FINOPS] Remediação concluída com sucesso! Economia anual estimada: US$ ${annualSum.toFixed(2)}'`,
    ].join("\n");

    const tfScript = [
      "# =========================================================================",
      "# PLANO DE REMEDIAÇÃO FINOPS VIA TERRAFORM",
      "# Remova as seguintes definições do seu arquivo de infraestrutura ou destrua:",
      "# =========================================================================",
      ...findings.map((f) => f.remediation.terraform_hcl),
    ].join("\n");

    return {
      scan_id: "local-" + Math.random().toString(36).substring(2, 10),
      engine_version: "1.0.0",
      timestamp: new Date().toISOString(),
      summary: {
        finops_health_score: score,
        wasted_monthly_usd: monthlySum,
        wasted_annual_usd: annualSum,
        total_resources_scanned: totalScanned,
        total_zombies_found: findings.length,
        severity_counts: {
          critical: findings.filter((f) => f.severity === "CRITICAL").length,
          high: findings.filter((f) => f.severity === "HIGH").length,
          medium: findings.filter((f) => f.severity === "MEDIUM").length,
          low: 0,
          info: 0,
        },
        cost_by_category: {
          ebs: Math.round(findings.filter((f) => f.resource_type === "ebs_volume").reduce((a, b) => a + b.monthly_waste_usd, 0) * 100) / 100,
          eip: Math.round(findings.filter((f) => f.resource_type === "elastic_ip").reduce((a, b) => a + b.monthly_waste_usd, 0) * 100) / 100,
          nat: Math.round(findings.filter((f) => f.resource_type === "nat_gateway").reduce((a, b) => a + b.monthly_waste_usd, 0) * 100) / 100,
          snapshot: Math.round(findings.filter((f) => f.resource_type === "snapshot").reduce((a, b) => a + b.monthly_waste_usd, 0) * 100) / 100,
          alb: Math.round(findings.filter((f) => f.resource_type === "load_balancer").reduce((a, b) => a + b.monthly_waste_usd, 0) * 100) / 100,
        },
      },
      findings: findings,
      remediation_plans: {
        terraform_hcl: [tfScript],
        aws_cli_scripts: [cliScript],
      },
    };
  }

  // Event Listeners
  btnPresetStartup.addEventListener("click", () => loadPreset("startup_waste"));
  btnPresetEnterprise.addEventListener("click", () => loadPreset("enterprise_sprawl"));
  btnPresetClean.addEventListener("click", () => loadPreset("clean_slate"));

  btnRunScan.addEventListener("click", executeScan);

  btnFormatJson.addEventListener("click", () => {
    try {
      const obj = JSON.parse(editor.value);
      editor.value = JSON.stringify(obj, null, 2);
      clearEditorFeedback();
    } catch (err) {
      showEditorFeedback(`JSON inválido: ${err.message}`);
    }
  });

  btnClearJson.addEventListener("click", () => {
    editor.value = "{\n  \"ebs_volumes\": [],\n  \"elastic_ips\": [],\n  \"nat_gateways\": [],\n  \"snapshots\": [],\n  \"load_balancers\": []\n}";
    clearEditorFeedback();
    document.querySelectorAll(".preset-card").forEach((c) => c.classList.remove("active"));
  });

  tabCli.addEventListener("click", () => {
    currentActiveTab = "cli";
    tabCli.classList.add("active");
    tabTf.classList.remove("active");
    updateScriptViewer();
  });

  tabTf.addEventListener("click", () => {
    currentActiveTab = "tf";
    tabTf.classList.add("active");
    tabCli.classList.remove("active");
    updateScriptViewer();
  });

  btnCopyScript.addEventListener("click", async () => {
    const textToCopy = scriptCodeDisplay.textContent;
    if (!textToCopy) return;

    try {
      await navigator.clipboard.writeText(textToCopy);
      const originalText = btnCopyScript.textContent;
      btnCopyScript.textContent = "✅ Copiado!";
      btnCopyScript.style.backgroundColor = "rgba(16, 185, 129, 0.3)";
      setTimeout(() => {
        btnCopyScript.textContent = originalText;
        btnCopyScript.style.backgroundColor = "";
      }, 2000);
    } catch (err) {
      console.warn("Falha ao copiar para o clipboard:", err);
    }
  });

  // Inicialização
  checkApiHealth();
  // Carrega o preset Startup Sprawl por padrão
  loadPreset("startup_waste");
})();
