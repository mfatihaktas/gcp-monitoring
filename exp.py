# Refs:
# - https://github.com/googleapis/python-monitoring/tree/1295b60ccb7993d98790e0360161a5edd74e4ee2/samples/snippets/v3/cloud-client

import os
import pprint
import time
import uuid

from google.cloud import monitoring_v3


def list_time_series_reduce(project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 1200},  # 20 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": ["resource.zone"],
        }
    )

    results = client.list_time_series(
        request = {
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)


def list_time_series_reduce(project_id):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - 3600), "nanos": nanos},
        }
    )
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 1200},  # 20 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": ["resource.zone"],
        }
    )

    results = client.list_time_series(
        request = {
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )
    for result in results:
        print(result)

if __name__ == "__main__":
    list_time_series_reduce(project_id = "machinelearning-research")
