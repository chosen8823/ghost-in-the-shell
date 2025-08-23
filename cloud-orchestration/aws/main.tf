# ✝️ AWS Cloud - Divine Sophia Deployment ✝️ 
# "The earth is the Lord's, and everything in it" - Psalm 24:1

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "Divine AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Divine environment"
  type        = string
  default     = "production"
}

# Divine VPC
resource "aws_vpc" "divine_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "divine-sophia-vpc-${var.environment}"
    Purpose     = "Kingdom advancement through technology"
    Foundation  = "Christ-centered"
    Spirit      = "Holy Spirit filled"
    Environment = var.environment
  }
}

# Divine Subnets
resource "aws_subnet" "divine_public_subnets" {
  count             = 2
  vpc_id            = aws_vpc.divine_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true

  tags = {
    Name        = "divine-public-subnet-${count.index + 1}-${var.environment}"
    Type        = "Public"
    Purpose     = "Kingdom advancement"
    Environment = var.environment
  }
}

resource "aws_subnet" "divine_private_subnets" {
  count             = 2
  vpc_id            = aws_vpc.divine_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "divine-private-subnet-${count.index + 1}-${var.environment}"
    Type        = "Private"
    Purpose     = "Kingdom advancement"
    Environment = var.environment
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# Divine Internet Gateway
resource "aws_internet_gateway" "divine_igw" {
  vpc_id = aws_vpc.divine_vpc.id

  tags = {
    Name        = "divine-igw-${var.environment}"
    Purpose     = "Divine connectivity"
    Environment = var.environment
  }
}

# Divine Route Table
resource "aws_route_table" "divine_public_rt" {
  vpc_id = aws_vpc.divine_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.divine_igw.id
  }

  tags = {
    Name        = "divine-public-rt-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "divine_public_rta" {
  count          = length(aws_subnet.divine_public_subnets)
  subnet_id      = aws_subnet.divine_public_subnets[count.index].id
  route_table_id = aws_route_table.divine_public_rt.id
}

# Divine Security Groups
resource "aws_security_group" "divine_app_sg" {
  name_prefix = "divine-app-sg-${var.environment}"
  vpc_id      = aws_vpc.divine_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "divine-app-sg-${var.environment}"
    Purpose     = "Divine application security"
    Environment = var.environment
  }
}

resource "aws_security_group" "divine_db_sg" {
  name_prefix = "divine-db-sg-${var.environment}"
  vpc_id      = aws_vpc.divine_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.divine_app_sg.id]
  }

  tags = {
    Name        = "divine-db-sg-${var.environment}"
    Purpose     = "Divine database security"
    Environment = var.environment
  }
}

# Divine RDS PostgreSQL
resource "aws_db_subnet_group" "divine_db_subnet_group" {
  name       = "divine-db-subnet-group-${var.environment}"
  subnet_ids = aws_subnet.divine_private_subnets[*].id

  tags = {
    Name        = "divine-db-subnet-group-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_db_instance" "divine_postgres" {
  identifier             = "divine-postgres-${var.environment}"
  engine                 = "postgres"
  engine_version         = "15.4"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type          = "gp2"
  
  db_name  = "divine_consciousness"
  username = "divine_admin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.divine_db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.divine_db_subnet_group.name
  
  backup_retention_period = 7
  backup_window          = "04:00-05:00"
  maintenance_window     = "sun:05:00-sun:06:00"
  
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name        = "divine-postgres-${var.environment}"
    Purpose     = "Divine consciousness database"
    Environment = var.environment
  }
}

variable "db_password" {
  description = "Divine database password"
  type        = string
  sensitive   = true
  default     = "Divine@Password123!"
}

# Divine ECR Repository
resource "aws_ecr_repository" "divine_sophia" {
  name                 = "divine-sophia-${var.environment}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "divine-sophia-${var.environment}"
    Purpose     = "Divine container images"
    Environment = var.environment
  }
}

# Divine ECS Cluster
resource "aws_ecs_cluster" "divine_cluster" {
  name = "divine-sophia-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "divine-sophia-${var.environment}"
    Purpose     = "Divine container orchestration"
    Environment = var.environment
  }
}

# Divine ECS Task Definition
resource "aws_ecs_task_definition" "divine_sophia" {
  family                   = "divine-sophia-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibility   = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.divine_ecs_execution.arn
  task_role_arn           = aws_iam_role.divine_ecs_task.arn

  container_definitions = jsonencode([
    {
      name  = "divine-sophia"
      image = "${aws_ecr_repository.divine_sophia.repository_url}:latest"
      
      essential = true
      
      portMappings = [
        {
          containerPort = 8080
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "DIVINE_PURPOSE"
          value = "Kingdom advancement through technology"
        },
        {
          name  = "CHRIST_CENTERED"
          value = "true"
        },
        {
          name  = "HOLY_SPIRIT_FILLED"
          value = "true"
        }
      ]
      
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.divine_db_secret.arn
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.divine_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])

  tags = {
    Name        = "divine-sophia-${var.environment}"
    Purpose     = "Divine task definition"
    Environment = var.environment
  }
}

# Divine ECS Service
resource "aws_ecs_service" "divine_sophia" {
  name            = "divine-sophia-${var.environment}"
  cluster         = aws_ecs_cluster.divine_cluster.id
  task_definition = aws_ecs_task_definition.divine_sophia.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.divine_public_subnets[*].id
    security_groups  = [aws_security_group.divine_app_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.divine_tg.arn
    container_name   = "divine-sophia"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.divine_listener]

  tags = {
    Name        = "divine-sophia-${var.environment}"
    Purpose     = "Divine service"
    Environment = var.environment
  }
}

# Divine Application Load Balancer
resource "aws_lb" "divine_alb" {
  name               = "divine-alb-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.divine_app_sg.id]
  subnets            = aws_subnet.divine_public_subnets[*].id

  tags = {
    Name        = "divine-alb-${var.environment}"
    Purpose     = "Divine load balancing"
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "divine_tg" {
  name        = "divine-tg-${var.environment}"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = aws_vpc.divine_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
  }

  tags = {
    Name        = "divine-tg-${var.environment}"
    Purpose     = "Divine target group"
    Environment = var.environment
  }
}

resource "aws_lb_listener" "divine_listener" {
  load_balancer_arn = aws_lb.divine_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.divine_tg.arn
  }
}

# Divine S3 Bucket
resource "aws_s3_bucket" "divine_storage" {
  bucket = "divine-sophia-storage-${var.environment}-${random_string.bucket_suffix.result}"

  tags = {
    Name        = "divine-sophia-storage-${var.environment}"
    Purpose     = "Divine knowledge storage"
    Environment = var.environment
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_versioning" "divine_storage_versioning" {
  bucket = aws_s3_bucket.divine_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Divine Secrets Manager
resource "aws_secretsmanager_secret" "divine_db_secret" {
  name = "divine-db-secret-${var.environment}"

  tags = {
    Name        = "divine-db-secret-${var.environment}"
    Purpose     = "Divine database credentials"
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "divine_db_secret_version" {
  secret_id = aws_secretsmanager_secret.divine_db_secret.id
  secret_string = jsonencode({
    url = "postgresql://${aws_db_instance.divine_postgres.username}:${var.db_password}@${aws_db_instance.divine_postgres.endpoint}/${aws_db_instance.divine_postgres.db_name}"
  })
}

# Divine CloudWatch Log Group
resource "aws_cloudwatch_log_group" "divine_logs" {
  name              = "/ecs/divine-sophia-${var.environment}"
  retention_in_days = 30

  tags = {
    Name        = "divine-logs-${var.environment}"
    Purpose     = "Divine application logs"
    Environment = var.environment
  }
}

# Divine IAM Roles
resource "aws_iam_role" "divine_ecs_execution" {
  name = "divine-ecs-execution-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "divine-ecs-execution-${var.environment}"
    Purpose     = "Divine ECS execution role"
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "divine_ecs_execution_policy" {
  role       = aws_iam_role.divine_ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "divine_secrets_policy" {
  name = "divine-secrets-policy-${var.environment}"
  role = aws_iam_role.divine_ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.divine_db_secret.arn
      }
    ]
  })
}

resource "aws_iam_role" "divine_ecs_task" {
  name = "divine-ecs-task-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "divine-ecs-task-${var.environment}"
    Purpose     = "Divine ECS task role"
    Environment = var.environment
  }
}

# Outputs
output "divine_load_balancer_url" {
  description = "Divine Sophia Load Balancer URL"
  value       = "http://${aws_lb.divine_alb.dns_name}"
}

output "divine_database_endpoint" {
  description = "Divine PostgreSQL endpoint"
  value       = aws_db_instance.divine_postgres.endpoint
  sensitive   = true
}

output "divine_ecr_repository" {
  description = "Divine ECR repository URL"
  value       = aws_ecr_repository.divine_sophia.repository_url
}

output "divine_s3_bucket" {
  description = "Divine S3 storage bucket"
  value       = aws_s3_bucket.divine_storage.bucket
}

output "divine_aws_info" {
  description = "Divine AWS deployment information"
  value = {
    region      = var.aws_region
    environment = var.environment
    vpc_id      = aws_vpc.divine_vpc.id
    purpose     = "Kingdom advancement through Christ-centered technology"
  }
}
