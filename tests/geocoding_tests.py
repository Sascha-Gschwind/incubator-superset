# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Unit tests for geocoding"""
import threading
import time

import simplejson as json
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.engine import reflection

import superset.models.core as models
from superset import conf, db
from superset.connectors.sqla.models import SqlaTable
from superset.models.core import Database
from superset.utils.geocoding_utils import GeocoderUtilMock
from superset.views.geocoding import Geocoder

from .base_tests import SupersetTestCase


class GeocodingTests(SupersetTestCase):

    def __init__(self, *args, **kwargs):
        super(GeocodingTests, self).__init__(*args, **kwargs)

    def setUp(self):
        self.login()
        Geocoder.geocoder_util = GeocoderUtilMock(conf)

    def tearDown(self):
        self.logout()

    def init_department_table(self):
        database = db.session.query(Database).first()
        database.allow_dml = True
        db.session.commit()

        if not database.has_table_by_name("departments"):
            meta = MetaData()
            departments = Table(
                "departments",
                meta,
                Column("department_id", Integer, primary_key=True),
                Column("name", String(60), nullable=False, key="name"),
                Column("street", Integer, nullable=False, key="street"),
                Column("city", Integer, nullable=False, key="city"),
                Column("country", Integer, nullable=False, key="country"),
            )
            departments.create(db.engine)

            db.engine.connect().execute(
                departments.insert(),
                [
                    {
                        "department_id": 1,
                        "name": "Logistics",
                        "street": "Oberseestrasse 10",
                        "city": "Rapperswil",
                        "country": "Switzerland",
                    },
                    {
                        "department_id": 2,
                        "name": "Marketing",
                        "street": "Grossmünsterplatz",
                        "city": "Zürich",
                        "country": "Switzerland",
                    },
                    {
                        "department_id": 3,
                        "name": "Facility Management",
                        "street": "Uetliberg",
                        "city": "Zürich",
                        "country": "Switzerland",
                    },
                    {
                        "department_id": 4,
                        "name": "Personal",
                        "street": "Zürichbergstrasse 221",
                        "city": "Zürich",
                        "country": "Switzerland",
                    },
                    {
                        "department_id": 5,
                        "name": "Finances",
                        "street": "Bahnhofstrasse",
                        "city": "Zürich",
                        "country": "Switzerland",
                    },
                ],
            )

    def test_menu_entry_geocode_exist(self):
        url = "/dashboard/list/"
        dashboard_page = self.get_resp(url)
        assert "Geocode Addresses" in dashboard_page

    def test_geocode_adresses_view_load(self):
        url = "/geocoder/geocoding"
        form_get = self.get_resp(url)
        assert "Geocode Addresses" in form_get

    def test_get_editable_tables(self):
        database = db.session.query(Database).first()
        database.allow_dml = True
        db.session.commit()

        table_name = (
            db.session.query(SqlaTable)
            .filter_by(database_id=database.id)
            .first()
            .table_name
        )

        table_names = [table.name for table in Geocoder()._get_editable_tables()]
        assert table_name in table_names

    def test_get_columns(self):
        url = "/geocoder/geocoding/columns"

        table = db.session.query(SqlaTable).first()
        tableDto = models.TableDto(
            table.id, table.table_name, table.schema, table.database_id
        )
        columns = reflection.Inspector.from_engine(db.engine).get_columns(
            table.table_name
        )

        data = {"table": tableDto.to_json()}
        response = self.get_resp(url, json_=data)
        assert columns[0].get("name") in response

    def test_get_invalid_columns(self):
        url = "/geocoder/geocoding/columns"
        tableDto = models.TableDto(10001, "no_table")

        data = {"table": tableDto.to_json()}
        response = self.get_resp(url, json_=data)

        message = "No columns found for table with name {0}".format(tableDto.name)
        assert message in response

    def test_does_valid_column_name_exist(self):
        self.init_department_table()
        table_name = "departments"
        column_name = (
            reflection.Inspector.from_engine(db.engine)
            .get_columns(table_name)[0]
            .get("name")
        )

        response = Geocoder()._does_column_name_exist(table_name, column_name)
        assert True is response

    def test_does_invalid_column_name_exist(self):
        self.init_department_table()
        table_name = "departments"
        column_name = "no_column"

        response = Geocoder()._does_column_name_exist(table_name, column_name)
        assert False is response

    def test_load_data_from_all_columns(self):
        table_name = "birth_names"
        columns = ["name", "gender"]

        data = Geocoder()._load_data_from_columns(table_name, columns)
        assert ("Aaron", "boy") in data
        assert ("Amy", "girl") in data

    def test_load_data_from_columns_with_none(self):
        table_name = "birth_names"
        columns = ["name", None, "gender", None]

        data = Geocoder()._load_data_from_columns(table_name, columns)
        assert ("Aaron", "boy") in data
        assert ("Amy", "girl") in data

    def test_add_lat_lon_columns(self):
        self.init_department_table()

        table_name = "departments"
        lat_column_name = "latitude"
        lon_column_name = "longitude"

        columns = reflection.Inspector.from_engine(db.engine).get_columns(table_name)
        number_of_columns_before = len(columns)

        Geocoder()._add_lat_lon_columns(table_name, lat_column_name, lon_column_name)

        columns = reflection.Inspector.from_engine(db.engine).get_columns(table_name)
        number_of_columns_after = len(columns)
        assert number_of_columns_after == number_of_columns_before + 2
        column_names = [column["name"] for column in columns]
        assert lon_column_name in column_names
        assert lat_column_name in column_names

    def test_insert_geocoded_data(self):
        table_name = "birth_names"

        selected_columns = ["name", "gender"]
        data = [
            ("Aaron", "boy", 1, "2.2"),
            ("Amy", "girl", 3, "4.4"),
            ("Barbara", "girl", 5, "6.6"),
            ("Bradley", "boy", 7, "8.8"),
        ]
        first_column_name = "num"
        second_column_name = "state"

        Geocoder()._insert_geocoded_data(
            table_name, first_column_name, second_column_name, selected_columns, data
        )
        result = db.engine.execute(
            "SELECT name, gender, num, state FROM birth_names WHERE name IN ('Aaron', 'Amy', 'Barbara', 'Bradley')"
        )
        for row in result:
            assert row in data

    def _geocode_post(self):
        return {
            "datasource": "departments",
            "streetColumn": "street",
            "cityColumn": "city",
            "countryColumn": "country",
            "latitudeColumnName": "lat",
            "longitudeColumnName": "long",
            "overwriteIfExists": True,
            "saveOnErrorOrInterrupt": True,
        }

    def test_geocode(self):
        expected_coordinates = GeocoderUtilMock(conf).get_mocked_data().values()
        url = "/geocoder/geocoding/geocode"

        self.init_department_table()

        geocoded_data = self.get_resp(url, json_=self._geocode_post())

        for coordinates in expected_coordinates:
            assert str(coordinates[0]) in geocoded_data
            assert str(coordinates[1]) in geocoded_data

        geocoded_list = json.loads(geocoded_data)
        assert 5 == len(geocoded_list)
        for address in geocoded_list:
            assert 5 == len(address)

    def test_progress(self):
        geocode_url = "/geocoder/geocoding/geocode"
        progress_url = "/geocoder/geocoding/progress"

        self.init_department_table()
        geocode = threading.Thread(
            target=self.get_resp,
            args=(geocode_url, None, True, True, self._geocode_post()),
        )
        geocode.start()
        time.sleep(
            4
        )  # Wait to be sure geocode has geocoded some data, but not all (5 addresses * 2 sec)

        progress = json.loads(self.get_resp(progress_url))
        assert 0 < progress.get("progress")
        assert True == progress.get("is_in_progress")
        assert 0 < progress.get("success_counter")

        geocode.join()

    def test_interrupt(self):
        geocode_url = "/geocoder/geocoding/geocode"
        interrupt_url = "/geocoder/geocoding/interrupt"
        progress_url = "/geocoder/geocoding/progress"

        self.init_department_table()
        geocode = threading.Thread(
            target=self.get_resp,
            args=(geocode_url, None, True, True, self._geocode_post()),
        )
        geocode.start()
        time.sleep(
            4
        )  # Wait to be sure geocode has geocoded some data, but not all (5 addresses * 2 sec)

        interrupt = self.get_resp(interrupt_url, json_=json.dumps("{}"))
        assert "" == interrupt

        time.sleep(1)  # Wait to be sure geocode has geocoded another data

        progress = json.loads(self.get_resp(progress_url))
        #assert 0 == progress.get("progress")
        #assert False == progress.get("is_in_progress")

        geocode.join()
