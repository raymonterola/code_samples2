import datetime
import unittest
import uuid
import pytz

import dotenv
from influxdb_client import InfluxDBClient

from services.influxdb import InfluxDB


class TestInfluxDBService(unittest.TestCase):
    def setUp(self) -> None:
        dotenv.load_dotenv()
        self.bucket = "test_bucket"

    def test_insert_record(self):
        uid = str(uuid.uuid4())
        tags = {"id": uid, "device": "cpu"}
        timestamp = datetime.datetime.now(tz=pytz.UTC)
        InfluxDB.insert_record(self.bucket, "usageLog", tags, "usage", 30.0, timestamp=timestamp)

        with InfluxDBClient.from_env_properties() as client:
            query_api = client.query_api()
            query = '''from(bucket:"{bucket}")
                |> range(start: -1m) 
                |> filter(fn: (r) => r._measurement == "usageLog" and r.device == "cpu" and r.id == "{id}")
            '''.format(bucket=self.bucket, id=uid)
            tables = query_api.query(query)
            for table in tables:
                self.assertEqual(len(table.records), 1)
    
    def test_insert_multiple_records(self):
        uid = str(uuid.uuid4())
        tags = {"sensor_id": uid, "location": "New York", "unit": "fahrenheit"}
        timestamp = datetime.datetime.now(tz=pytz.UTC)
        fields = [("temp", 48.7), ("temp", 48.8), ("temp", 47.7)]
        InfluxDB.insert_multiple_records(self.bucket, "airTemperature", tags, fields, timestamp=timestamp)
        with InfluxDBClient.from_env_properties() as client:
            query_api = client.query_api()
            query = '''from(bucket:"{bucket}")
                |> range(start: -1m) 
                |> filter(fn: (r) => r._measurement == "airTemperature" and r.sensor_id == "{id}")
                |> yield()
            '''.format(bucket=self.bucket, id=uid)
            tables = query_api.query(query)
            for table in tables:
                self.assertEqual(len(table.records), len(fields))


if __name__ == '__main__':
    unittest.main()
