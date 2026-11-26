# ==============================================================================
# Onion Zombie Hunter — Outputs Canônicos da Infraestrutura
# Camada 3: Infraestrutura (Terraform) & CI/CD
# ==============================================================================

output "api_url" {
  description = "URL base do Amazon API Gateway HTTP API v2"
  value       = trimsuffix(aws_apigatewayv2_stage.default.invoke_url, "/")
}

output "frontend_url" {
  description = "URL pública do Amazon S3 Static Website Hosting"
  value       = "http://${aws_s3_bucket_website_configuration.frontend.website_endpoint}"
}

output "s3_bucket_name" {
  description = "Nome físico do bucket S3 criado para o frontend"
  value       = aws_s3_bucket.frontend.id
}
