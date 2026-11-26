# ==============================================================================
# Onion Zombie Hunter — Variáveis de Entrada da Infraestrutura
# Camada 3: Infraestrutura (Terraform) & CI/CD
# ==============================================================================

variable "aws_region" {
  description = "Região da AWS para provisionamento dos recursos"
  type        = string
  default     = "us-east-2"
}

variable "project_prefix" {
  description = "Prefixo padronizado único para todos os recursos na AWS (onion-zh-*)"
  type        = string
  default     = "onion-zh"
}

variable "environment" {
  description = "Ambiente de deploy (ex: prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "lambda_handler" {
  description = "Handler da função AWS Lambda (handler.lambda_handler)"
  type        = string
  default     = "handler.lambda_handler"
}

variable "cors_allow_origins" {
  description = "Lista de origens permitidas para requisições CORS na HTTP API"
  type        = list(string)
  default     = ["*"]
}

variable "api_throttling_burst_limit" {
  description = "Limite máximo de requisições simultâneas em rajada para o API Gateway v2"
  type        = number
  default     = 50
}

variable "api_throttling_rate_limit" {
  description = "Taxa contínua máxima de requisições por segundo para o API Gateway v2"
  type        = number
  default     = 20
}
