# ==============================================================================
# Onion Zombie Hunter — AWS Lambda (Python 3.12 Engine) & CloudWatch Logs
# Camada 3: Infraestrutura (Terraform) & CI/CD
# ==============================================================================

# Compactação do código-fonte da pasta ../src para deploy na Lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda.zip"
}

# CloudWatch Log Group com retenção curta de 7 dias (FinOps)
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.project_prefix}-engine"
  retention_in_days = 7

  tags = local.common_tags
}

# Função AWS Lambda para o motor FinOps Zombie Hunter
resource "aws_lambda_function" "engine" {
  function_name    = "${var.project_prefix}-engine"
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.12"
  handler          = var.lambda_handler
  role             = aws_iam_role.lambda_role.arn
  timeout          = 15
  memory_size      = 128

  environment {
    variables = {
      ALLOWED_ORIGIN    = length(var.cors_allow_origins) > 0 ? var.cors_allow_origins[0] : "*"
      MAX_PAYLOAD_BYTES = "524288"
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_log_group
  ]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_prefix}-engine"
    }
  )
}

# Permissão para o API Gateway invocar a função Lambda
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.engine.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}
