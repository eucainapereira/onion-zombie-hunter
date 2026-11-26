# ==============================================================================
# Onion Zombie Hunter — Configuração do Provedor AWS e Tags Globais
# Camada 3: Infraestrutura (Terraform) & CI/CD
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

data "aws_caller_identity" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id

  common_tags = {
    Project     = "onion-zombie-hunter"
    ManagedBy   = "terraform"
    CostCenter  = "FinOps"
    Environment = var.environment
  }
}
