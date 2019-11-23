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
import json
import time

import requests
from requests import RequestException


class GeoCoder:  # pylint: disable=too-few-public-methods
    """
    The GeoCoder object holds the logic for geocoding given data
    """

    interruptflag = False
    conf: dict = {}
    progress: dict = {}

    def __init__(self, config):
        self.conf = config

    def geocode(self, geocoder: str, data: list, async_flag=False):
        try:
            if geocoder == "MapTiler":
                return self.__geocode_maptiler(data, async_flag)
            return self.__geocode_testing(async_flag)
        except Exception as e:
            raise e
        finally:
            self.progress["progress"] = 0
            self.progress["is_in_progress"] = False

    def __geocode_maptiler(self, data: list, async_flag) -> list:
        if async_flag:
            raise Exception("Async not supported at this time")
        else:
            return self.__geocode_maptiler_sync(data)

    def __geocode_maptiler_sync(self, data: list) -> list:
        """
        geocode the data using the Maptiler API
        :param data: the addresses to be geocoded as a list of tuples
        :return: a dictionary containing the addresses and their long,lat values
        """
        data = [("HSR Oberseestrasse 10", "Rapperswil"), ("ETH", "Zürich")]
        geocoded_data = [()]
        data_length = len(data)
        counter = 0
        self.progress["success_counter"] = 0
        self.progress["is_in_progress"] = True
        self.progress["progress"] = 0

        # for row in data:
        # request_string = ""
        # for elem in row:
        # request_string = request_string + " " + elem
        # resp = requests.get(
        # baseurl + request_string + ".json?key=" + self.conf["MAPTILER_API_KEY"]
        # )
        for datum in data:
            try:
                if self.interruptflag:
                    self.interruptflag = False
                    self.progress["progress"] = 0
                    self.progress["is_in_progress"] = False
                    return geocoded_data
                address = " ".join(datum)
                geocoded = self.__get_values_from_address(address)
                if geocoded is not None:
                    geocoded_data.append(datum + tuple(geocoded))

                    self.progress["success_counter"] += 1
                counter += 1
                self.progress["progress"] = counter / data_length
            # TODO be more precise with the possible exceptions
            except RequestException as e:
                # TODO decide whether to interrupt here or keep going
                print(e)
        self.progress["progress"] = 100
        self.progress["is_in_progress"] = False
        # TODO also return amount of geocoded values or store in class-variable
        return geocoded_data

    def __get_values_from_address(self, address: str):
        baseurl = "https://api.maptiler.com/geocoding/"
        response = requests.get(
            baseurl + address + ".json?key=" + self.conf["MAPTILER_API_KEY"]
        )
        jsondat = json.loads(response.content.decode())
        # TODO give better names and clean
        # TODO make use of relevance if wanted
        features = jsondat["features"]
        feature_count = len(features)
        if feature_count != 0:
            feature = features[0]
            # TODO check if it is possible, that there is no center attribute
            #  -> get API doc from mr. Keller
            # TODO don't raise success_counter if there is no 'center' Attribute
            return feature["center"] or None
        return None

    def __geocode_testing(self, async_flag) -> dict:
        if async_flag:
            raise Exception("Async not supported at this time")
        else:
            return self.__geocode_testing_sync()

    def __geocode_testing_sync(self) -> dict:
        counter = 0
        datalen = 10
        self.progress["is_in_progress"] = True
        self.progress["progress"] = 0
        for _ in range(datalen):
            if self.interruptflag:
                self.interruptflag = False
                self.progress["is_in_progress"] = False
                self.progress["progress"] = 0
                return {0: ""}
            time.sleep(2)
            counter = counter + 1
            self.progress["progress"] = counter / datalen
        return {0: ""}