from aws_cdk import (
    Stack,
    Duration,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_logs as logs,
    aws_ecs_patterns as ecs_patterns
)

from constructs import Construct


class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(
            self,
            "MidasVpc",
            max_azs=2,
            nat_gateways=1
        )

        # ECS Cluster
        cluster = ecs.Cluster(
            self,
            "MidasCluster",
            vpc=vpc,
            cluster_name="midas-cluster"
        )

        # ECR
        repository = ecr.Repository(
            self,
            "MidasRepository",
            repository_name="midas-accounts-service"
        )

        # Logs
        log_group = logs.LogGroup(
            self,
            "MidasLogs",
            log_group_name="/ecs/midas-accounts-service",
            retention=logs.RetentionDays.ONE_WEEK
        )

        # ECS Service
        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "MidasService",

            cluster=cluster,

            cpu=512,
            memory_limit_mib=1024,

            desired_count=1,

            public_load_balancer=True,

            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(

                image=ecs.ContainerImage.from_registry(
                    "public.ecr.aws/nginx/nginx:latest"
                ),

                container_port=80,

                environment={
                    "ENVIRONMENT": "production"
                },

                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix="midas",
                    log_group=log_group
                )
            )
        )

        service.target_group.configure_health_check(
            path="/",
            interval=Duration.seconds(30)
        )