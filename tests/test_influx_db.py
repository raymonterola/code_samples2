import unittest
from uuid import uuid4

import dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
from influxdb_client.client.query_api import QueryApi


class TestInfluxDB(unittest.TestCase):
    def setUp(self):
        dotenv.load_dotenv()
        self.bucket = "test_bucket"
        # set environment variables INFLUXDB_V2_TOKEN, INFLUXDB_V2_URL, INFLUXDB_V2_ORG
        self.client = influxdb_client.InfluxDBClient.from_env_properties()
        self.write_api: WriteApi = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api: QueryApi = self.client.query_api()

    def tearDown(self) -> None:
        self.client.close()

    def test_connection(self):
        self.assertTrue(self.client.ping())

    def test_write(self):
        uid = str(uuid4())
        p = influxdb_client.Point("Testing").field("uuid", uid)
        self.write_api.write(bucket=self.bucket, record=p)
        query = 'from(bucket:"test_bucket") |> range(start: -10s) |> filter(fn: (r) => r._measurement == "Testing") |> filter(fn: (r) => r._field == "uuid") |> last()'
        tables = self.query_api.query(query)
        for table in tables:
            for record in table.records:
                self.assertEqual(record.get_value(), uid)