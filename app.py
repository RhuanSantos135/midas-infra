#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.backend_stack import BackendStack

app = cdk.App()

BackendStack(
    app,
    "MidasBackendStack",
    env=cdk.Environment(
        account="765348135252",
        region="sa-east-1"
    )
)

app.synth()