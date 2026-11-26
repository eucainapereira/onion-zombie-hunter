# ==============================================================================
# Onion Zombie Hunter — Políticas IAM e Role de Execução da Lambda
# Camada 5: Segurança, Políticas IAM & Integração no Terraform
# ==============================================================================

# Role de execução IAM para a AWS Lambda do motor FinOps Zombie Hunter
resource "aws_iam_role" "lambda_role" {
  name        = "${var.project_prefix}-lambda-role"
  description = "Role IAM com menor privilégio para execução da função AWS Lambda ${var.project_prefix}-engine"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LambdaAssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_prefix}-lambda-role"
    }
  )
}

# Política gerenciada com menor privilégio anexando iam/execution-policy.json
resource "aws_iam_policy" "lambda_execution_policy" {
  name        = "${var.project_prefix}-lambda-policy"
  description = "Política IAM de menor privilégio para envio de logs ao CloudWatch pela Lambda ${var.project_prefix}-engine"
  policy      = file("${path.module}/../iam/execution-policy.json")

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_prefix}-lambda-policy"
    }
  )
}

# Anexo da política de execução à role da Lambda
resource "aws_iam_role_policy_attachment" "lambda_execution_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}
