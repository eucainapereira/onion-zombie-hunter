"""Onion Zombie Hunter — AWS Lambda Handler & Roteador REST FinOps.

Implementação 100% stdlib em Python 3.12 compatível com AWS API Gateway HTTP API v2
e REST Proxy Integrations. Suporta CORS irrestrito e rotas /health, /presets e /scan.
"""

import base64
import datetime
import json
import os
from typing import Any

from engine import run_finops_scan
from presets import get_preset_inventory, get_presets_catalog

MAX_PAYLOAD_BYTES = int(os.environ.get("MAX_PAYLOAD_BYTES", "524288"))  # 512 KB
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")

CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}


def _build_response(status_code: int, body_data: Any) -> dict[str, Any]:
    """Constrói resposta HTTP padronizada para o API Gateway."""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "isBase64Encoded": False,
        "body": json.dumps(body_data, ensure_ascii=False, indent=2),
    }


def _extract_request_info(event: dict[str, Any]) -> tuple[str, str, str | None, bool]:
    """Extrai método HTTP, caminho, body e flag base64 de eventos API Gateway v1/v2."""
    # Extração de Método HTTP
    method = ""
    http_ctx = event.get("requestContext", {}).get("http", {})
    if "method" in http_ctx:
        method = http_ctx["method"]
    elif "httpMethod" in event:
        method = event["httpMethod"]
    elif "routeKey" in event:
        parts = event["routeKey"].split()
        if len(parts) >= 1:
            method = parts[0]

    method = method.upper() if method else "GET"

    # Extração de Caminho
    path = ""
    if "rawPath" in event:
        path = event["rawPath"]
    elif "path" in event:
        path = event["path"]
    elif "routeKey" in event:
        parts = event["routeKey"].split()
        if len(parts) >= 2:
            path = parts[1]

    path = path.rstrip("/") if path else ""
    if not path:
        path = "/"

    # Body e Base64
    body = event.get("body")
    is_base64 = bool(event.get("isBase64Encoded", False))

    return method, path, body, is_base64


def lambda_handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    """Handler principal da AWS Lambda.

    Roteia requisições HTTP para /health, /presets e /scan com tratamento defensivo.
    """
    try:
        if not isinstance(event, dict):
            return _build_response(400, {"error": "Evento de invocação inválido"})

        method, path, body, is_base64 = _extract_request_info(event)

        # 1. Tratamento de CORS Preflight (OPTIONS)
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": "",
            }

        # 2. Rota GET /health
        if method == "GET" and path == "/health":
            now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            return _build_response(
                200,
                {
                    "status": "healthy",
                    "service": "onion-zombie-hunter",
                    "engine_version": "1.0.0",
                    "timestamp": now_iso,
                    "uptime_status": "operational",
                    "rules_loaded": 5,
                },
            )

        # 3. Rota GET /presets
        if method == "GET" and path == "/presets":
            catalog = get_presets_catalog()
            return _build_response(200, {"presets": catalog})

        # 4. Rota POST /scan
        if method == "POST" and path == "/scan":
            # Decodificação do body
            raw_body_bytes = b""
            if body:
                if is_base64:
                    try:
                        raw_body_bytes = base64.b64decode(body)
                    except Exception:
                        return _build_response(400, {"error": "Payload Base64 inválido"})
                elif isinstance(body, bytes):
                    raw_body_bytes = body
                else:
                    raw_body_bytes = str(body).encode("utf-8")

            # Validação do tamanho do payload (512 KB)
            if len(raw_body_bytes) > MAX_PAYLOAD_BYTES:
                return _build_response(
                    413,
                    {
                        "error": "Payload Too Large",
                        "message": f"Tamanho da requisição excede o limite máximo permitido de {MAX_PAYLOAD_BYTES} bytes.",
                    },
                )

            # Decodificação JSON
            payload: dict[str, Any] = {}
            if raw_body_bytes:
                try:
                    payload = json.loads(raw_body_bytes.decode("utf-8"))
                except json.JSONDecodeError as err:
                    return _build_response(
                        400,
                        {
                            "error": "Bad Request",
                            "message": f"Formato JSON inválido no corpo da requisição: {err}",
                        },
                    )

            if not isinstance(payload, dict):
                return _build_response(400, {"error": "Bad Request", "message": "O corpo deve ser um objeto JSON."})

            inventory_to_scan: dict[str, Any] = {}

            # Modalidade A: Presets
            if "preset" in payload:
                preset_id = str(payload["preset"]).strip()
                loaded_inv = get_preset_inventory(preset_id)
                if loaded_inv is None:
                    return _build_response(
                        400,
                        {
                            "error": "Bad Request",
                            "message": f"Preset '{preset_id}' não encontrado. Consulte GET /presets para lista válida.",
                        },
                    )
                inventory_to_scan = loaded_inv

            # Modalidade B: Inventário Customizado sob a chave 'inventory'
            elif "inventory" in payload and isinstance(payload["inventory"], dict):
                inventory_to_scan = payload["inventory"]

            # Modalidade C: Chaves diretas de recursos no payload
            elif any(k in payload for k in ("ebs_volumes", "elastic_ips", "nat_gateways", "snapshots", "load_balancers")):
                inventory_to_scan = payload

            # Inventário vazio padrão se nada for fornecido
            else:
                inventory_to_scan = {}

            scan_results = run_finops_scan(inventory_to_scan)
            return _build_response(200, scan_results)

        # 5. Rota não encontrada (404)
        return _build_response(
            404,
            {
                "error": "Not Found",
                "message": f"Rota '{method} {path}' não suportada pela API Onion Zombie Hunter.",
            },
        )

    except Exception as exc:
        # Captura defensiva de exceções não tratadas (evita vazamento de stacktrace)
        return _build_response(
            500,
            {
                "error": "Internal Server Error",
                "message": "Ocorreu um erro interno no processamento da auditoria FinOps.",
            },
        )
