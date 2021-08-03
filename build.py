from typing import Any

from aws_cdk import aws_codebuild as codebuild
from aws_cdk import core as cdk

import constants


class Build(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        webhook_filters = [
            codebuild.FilterGroup.in_event_of(
                codebuild.EventAction.PULL_REQUEST_CREATED
            ).and_base_branch_is("future"),
            codebuild.FilterGroup.in_event_of(
                codebuild.EventAction.PULL_REQUEST_UPDATED
            ).and_base_branch_is("future"),
        ]
        git_hub_source = codebuild.Source.git_hub(
            owner=constants.GITHUB_OWNER,
            repo=constants.GITHUB_REPO,
            webhook_filters=webhook_filters,
        )
        build_environment = codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            compute_type=codebuild.ComputeType.SMALL,
        )
        build_spec = codebuild.BuildSpec.from_object(
            {
                "phases": {
                    "install": {
                        "runtime-versions": constants.CODEBUILD_INSTALL_RUNTIME_VERSIONS,
                        "commands": constants.CODEBUILD_INSTALL_COMMANDS,
                    },
                    "build": {"commands": constants.CODEBUILD_BUILD_COMMANDS},
                },
                "version": "0.2",
            }
        )
        codebuild.Project(
            self,
            "CodeBuild",
            source=git_hub_source,
            build_spec=build_spec,
            environment=build_environment,
        )
