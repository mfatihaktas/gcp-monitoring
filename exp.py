# Refs:
# - https://github.com/googleapis/python-monitoring/tree/1295b60ccb7993d98790e0360161a5edd74e4ee2/samples/snippets/v3/cloud-client
import os
import pprint
import time
import uuid

from google.cloud import monitoring_v3

from debug_utils import *


client = monitoring_v3.MetricServiceClient()

def get_time_series_l(project_id, filter_, num_days_back):
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    num_hours_back = int(num_days_back * 24)
    log(DEBUG, "", num_hours_back=num_hours_back)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - int(num_hours_back * 60 * 60)), "nanos": nanos},
        }
    )
    aggregation = None
    # monitoring_v3.Aggregation(
    #     {
    #         "alignment_period": {"seconds": 1200},  # 20 minutes
    #         "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    #         "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    #         "group_by_fields": ["resource.zone"],
    #     }
    # )

    return client.list_time_series(
        request = {
            "name": project_name,
            "filter": f"{filter_}",
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )


def get_num_req_arrivals(project_id, subscription_id_regex, num_days_back):
    # https://cloud.google.com/monitoring/api/metrics_gcp#gcp-pubsub
    # filter_ = 'metric.type = "pubsub.googleapis.com/subscription/sent_message_count"' + " AND " + \
    #           'resource.labels.subscription_id = monitoring.regex.full_match("{}")'.format(subscription_id_regex)
    # filter_ = 'metric.type = "pubsub.googleapis.com/subscription/push_request_count"' + " AND " + \
    #           'resource.labels.subscription_id = monitoring.regex.full_match("{}")'.format(".*-predreq-queue-dev")

    # filter_ = 'metric.type = "pubsub.googleapis.com/topic/send_request_count"' + " AND " + \
    #           'resource.labels.topic_id = monitoring.regex.full_match("{}")'.format(".*-predreq-topic-dev")
    # filter_ = 'metric.type = "pubsub.googleapis.com/topic/send_request_count"'
    filter_ = 'metric.type = "pubsub.googleapis.com/topic/send_request_count"' + " AND " + \
              'resource.labels.topic_id = "aggregate-prediction-requests-ml-dev"'
    time_series_l = get_time_series_l(project_id, filter_, num_days_back)
    
    num_req_arrivals = 0
    for i, time_series in enumerate(time_series_l):
        print(time_series)
        log(DEBUG, "", i=i,
            num_points=len(time_series.points),
            resource=time_series.resource,
            metric=time_series.metric)
        # log(DEBUG, f"i= {i}", time_series_points=time_series.points)

        num_req_arrivals += sum(point.value.int64_value for point in time_series.points)
    return num_req_arrivals

if __name__ == "__main__":
    log_to_std()
    
    # list_time_series_reduce(project_id = "machinelearning-research")
    # list_num_publish_reqs(project_id = "machinelearning-research")

    project_id = "machinelearning-research"
    topic_id = "aggregate-prediction-requests-ml-dev"
    subscription_id_regex = "gcf-prediction_aggregator-sub-.*"
    
    num_days_back = 1/24 # 30
    
    num_req_arrivals = get_num_req_arrivals(project_id, subscription_id_regex, num_days_back)
    log(DEBUG, "", num_req_arrivals=num_req_arrivals, num_days_back=num_days_back)
