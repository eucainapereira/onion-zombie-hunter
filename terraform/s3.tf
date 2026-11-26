# ==============================================================================
# Onion Zombie Hunter — Frontend Estático S3 (Static Website Hosting)
# Camada 3: Infraestrutura (Terraform) & CI/CD
# ==============================================================================

# S3 Bucket para hospedagem do Frontend Estático (SPA)
resource "aws_s3_bucket" "frontend" {
  bucket        = "${var.project_prefix}-frontend-${local.account_id}-${var.aws_region}"
  force_destroy = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_prefix}-frontend-${local.account_id}-${var.aws_region}"
    }
  )
}

# Configuração de Website Estático no Bucket S3
resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

# Configuração de Propriedade de Objetos (BucketOwnerEnforced)
resource "aws_s3_bucket_ownership_controls" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Bloqueio de Acesso Público configurado para permitir políticas públicas de leitura
resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = false
  restrict_public_buckets = false
}

# Política do Bucket S3 para acesso público somente leitura (GET) aos assets estáticos
resource "aws_s3_bucket_policy" "frontend_public_read" {
  bucket = aws_s3_bucket.frontend.id

  depends_on = [
    aws_s3_bucket_public_access_block.frontend
  ]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}
