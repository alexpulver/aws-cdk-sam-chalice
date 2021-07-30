import json
import pathlib
import shutil
import tempfile
import unittest

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import core as cdk

from api.infrastructure import API
from database.infrastructure import Database


class APITestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp(dir="/tmp")
        cdk_out_dir = pathlib.Path(self.temp_dir, "cdk.out")
        cdk_out_dir.mkdir()
        self.app = cdk.App(outdir=str(cdk_out_dir))
        self.stack = cdk.Stack(self.app, "Stack")

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        chalice_config_path = pathlib.Path(__file__).resolve().parent.parent.joinpath(
            'api/runtime/.chalice/config.json'
        )
        with pathlib.Path.open(chalice_config_path, "r+") as chalice_config_file:
            chalice_config = json.load(chalice_config_file)
            del chalice_config["stages"][f"{self.stack.stack_name}/API"]
            chalice_config_file.seek(0)
            chalice_config_file.truncate()
            json.dump(chalice_config, chalice_config_file, indent=2)

    def test_endpoint_url_output_exists(self) -> None:
        database = Database(
            self.stack,
            "Database",
            dynamodb_billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        API(
            self.stack,
            "API",
            dynamodb_table=database.table,
            lambda_reserved_concurrency=1,
        )

        cloud_assembly = self.app.synth()
        template = cloud_assembly.get_stack_by_name(self.stack.stack_name).template

        self.assertEqual(
            template["Outputs"]["EndpointURL"]["Value"]["Fn::Sub"],
            "https://${RestAPI}.execute-api.${AWS::Region}.${AWS::URLSuffix}/v1/",
        )


if __name__ == '__main__':
    unittest.main()
