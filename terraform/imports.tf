# Import blocks for existing AWS resources (Terraform 1.5+)
import {
  to = aws_iam_role.lambda_role
  id = "onion-zh-lambda-role"
}

import {
  to = aws_iam_policy.lambda_execution_policy
  id = "arn:aws:iam::654341980060:policy/onion-zh-lambda-policy"
}

import {
  to = aws_iam_role_policy_attachment.lambda_execution_attachment
  id = "onion-zh-lambda-role/arn:aws:iam::654341980060:policy/onion-zh-lambda-policy"
}

import {
  to = aws_cloudwatch_log_group.lambda_log_group
  id = "/aws/lambda/onion-zh-engine"
}

import {
  to = aws_s3_bucket.frontend
  id = "onion-zh-frontend-654341980060-us-east-2"
}

import {
  to = aws_s3_bucket_public_access_block.frontend
  id = "onion-zh-frontend-654341980060-us-east-2"
}

import {
  to = aws_s3_bucket_ownership_controls.frontend
  id = "onion-zh-frontend-654341980060-us-east-2"
}

import {
  to = aws_s3_bucket_website_configuration.frontend
  id = "onion-zh-frontend-654341980060-us-east-2"
}

import {
  to = aws_s3_bucket_policy.frontend_public_read
  id = "onion-zh-frontend-654341980060-us-east-2"
}

import {
  to = aws_apigatewayv2_api.http_api
  id = "qpxbyua2l1"
}

import {
  to = aws_apigatewayv2_stage.default
  id = "qpxbyua2l1/$default"
}

import {
  to = aws_lambda_function.engine
  id = "onion-zh-engine"
}

import {
  to = aws_lambda_permission.api_gateway
  id = "onion-zh-engine/AllowAPIGatewayInvoke"
}

import {
  to = aws_apigatewayv2_integration.lambda_integration
  id = "qpxbyua2l1/8nampnb"
}

import {
  to = aws_apigatewayv2_route.presets_route
  id = "qpxbyua2l1/pbihuzh"
}

import {
  to = aws_apigatewayv2_route.health_route
  id = "qpxbyua2l1/yn3h63h"
}

import {
  to = aws_apigatewayv2_route.scan_route
  id = "qpxbyua2l1/m2lzg1j"
}
