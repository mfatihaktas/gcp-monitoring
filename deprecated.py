def get_num_req_arrivals(project_id, topic_id, subscription_id, subscription_id_regex, num_hours_back):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - num_hours_back * 60), "nanos": nanos},
        }
    )

    results = client.list_time_series(
        request = {
            "name": project_name,
            # "filter": 'resource.topic_id = "aggregate-prediction-requests-ml-dev"',
            # "filter": 'resource.type = "pubsub_topic"',
            # "filter": 'metric.type = "pubsub.googleapis.com/topic/send_request_count"' + " AND " + \
            #           'metric.labels.instance_name = "aggregate-prediction-requests-ml-dev"',
            # "filter": 'metric.type = "pubsub.googleapis.com/topic/send_request_count"' + " AND " + \
            #           'resource.labels.topic_id = "{}"'.format(topic_id),
            # "filter": 'metric.type = "pubsub.googleapis.com/subscription/sent_message_count"',
            # "filter": 'metric.type = "pubsub.googleapis.com/subscription/sent_message_count"' + " AND " + \
            #           'resource.labels.subscription_id = "{}"'.format(subscription_id),
            "filter": 'metric.type = "pubsub.googleapis.com/subscription/sent_message_count"' + " AND " + \
                      'resource.labels.subscription_id = monitoring.regex.full_match("{}")'.format(subscription_id_regex),
            
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": None,
        }
    )

    # log(DEBUG, "results= {}".format(results))
    for i, result in enumerate(results):
        log(DEBUG, "i= {}".format(i), result_points=result.points)
        # result=result

