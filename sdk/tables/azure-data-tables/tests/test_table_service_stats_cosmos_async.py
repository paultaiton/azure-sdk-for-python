# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest
import pytest

# from azure.data.tabless import TableServiceClient
from azure.data.tables.aio import TableServiceClient
from _shared.cosmos_testcase import CachedCosmosAccountPreparer

from devtools_testutils import CachedResourceGroupPreparer
from _shared.testcase import TableTestCase, RERUNS_DELAY, SLEEP_DELAY

SERVICE_UNAVAILABLE_RESP_BODY = '<?xml version="1.0" encoding="utf-8"?><StorageServiceStats><GeoReplication><Status' \
                                '>unavailable</Status><LastSyncTime></LastSyncTime></GeoReplication' \
                                '></StorageServiceStats> '

SERVICE_LIVE_RESP_BODY = '<?xml version="1.0" encoding="utf-8"?><StorageServiceStats><GeoReplication><Status' \
                         '>live</Status><LastSyncTime>Wed, 19 Jan 2021 22:28:43 GMT</LastSyncTime></GeoReplication' \
                         '></StorageServiceStats> '

# --Test Class -----------------------------------------------------------------
class TableServiceStatsTest(TableTestCase):
    # --Helpers-----------------------------------------------------------------
    def _assert_stats_default(self, stats):
        assert stats is not None
        assert stats['geo_replication'] is not None

        assert stats['geo_replication']['status'] ==  'live'
        assert stats['geo_replication']['last_sync_time'] is not None

    def _assert_stats_unavailable(self, stats):
        assert stats is not None
        assert stats['geo_replication'] is not None

        assert stats['geo_replication']['status'] ==  'unavailable'
        assert stats['geo_replication']['last_sync_time'] is None

    @staticmethod
    def override_response_body_with_unavailable_status(response):
        response.http_response.text = lambda _: SERVICE_UNAVAILABLE_RESP_BODY

    @staticmethod
    def override_response_body_with_live_status(response):
        response.http_response.text = lambda _: SERVICE_LIVE_RESP_BODY

    # --Test cases per service ---------------------------------------

    @pytest.mark.skip("invalid json")
    @CachedResourceGroupPreparer(name_prefix="tablestest")
    @CachedCosmosAccountPreparer(name_prefix="tablestest", sku='Standard_RAGRS')
    async def test_table_service_stats_f(self, resource_group, location, cosmos_account, cosmos_account_key):
        # Arrange
        tsc = TableServiceClient(self.account_url(cosmos_account, "cosmos"), cosmos_account_key)

        # Act
        stats = await tsc.get_service_stats(raw_response_hook=self.override_response_body_with_live_status)
        # Assert
        self._assert_stats_default(stats)

        if self.is_live:
            sleep(SLEEP_DELAY)

    @pytest.mark.skip("invalid json")
    @CachedResourceGroupPreparer(name_prefix="tablestest")
    @CachedCosmosAccountPreparer(name_prefix="tablestest", sku='Standard_RAGRS')
    async def test_table_service_stats_when_unavailable(self, resource_group, location, cosmos_account, cosmos_account_key):
        # Arrange
        tsc = TableServiceClient(self.account_url(cosmos_account, "cosmos"), cosmos_account_key)

        # Act
        stats = await tsc.get_service_stats(
            raw_response_hook=self.override_response_body_with_unavailable_status)

        # Assert
        self._assert_stats_unavailable(stats)

        if self.is_live:
            sleep(SLEEP_DELAY)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
