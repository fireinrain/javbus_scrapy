# censored
# {'downloader/exception_count': 6,
#  'downloader/exception_type_count/twisted.web._newclient.ResponseNeverReceived': 6,
#  'downloader/request_bytes': 65748876,
#  'downloader/request_count': 72362,
#  'downloader/request_method_count/GET': 72362,
#  'downloader/response_bytes': 436464323,
#  'downloader/response_count': 72356,
#  'downloader/response_status_count/200': 55505,
#  'downloader/response_status_count/301': 16700,
#  'downloader/response_status_count/403': 97,
#  'downloader/response_status_count/404': 54,
#  'elapsed_time_seconds': 2666.256675,
#  'finish_reason': 'finished',
#  'finish_time': datetime.datetime(2022, 7, 7, 21, 34, 0, 331315),
#  'httpcompression/response_bytes': 1909389323,
#  'httpcompression/response_count': 55656,
#  'httperror/response_ignored_count': 151,
#  'httperror/response_ignored_status_count/403': 97,
#  'httperror/response_ignored_status_count/404': 54,
#  'item_scraped_count': 778777,
#  'log_count/DEBUG': 851149,
#  'log_count/INFO': 72569,
#  'memusage/max': 135659520,
#  'memusage/startup': 75005952,
#  'request_depth_max': 21,
#  'response_received_count': 55656,
#  'retry/count': 6,
#  'retry/reason_count/twisted.web._newclient.ResponseNeverReceived': 6,
#  'scheduler/dequeued': 72362,
#  'scheduler/dequeued/memory': 72362,
#  'scheduler/enqueued': 72362,
#  'scheduler/enqueued/memory': 72362,
#  'start_time': datetime.datetime(2022, 7, 7, 20, 49, 34, 74640)}


# uncensored
# {'downloader/exception_count': 1,
#  'downloader/exception_type_count/twisted.web._newclient.ResponseNeverReceived': 1,
#  'downloader/request_bytes': 17116734,
#  'downloader/request_count': 18944,
#  'downloader/request_method_count/GET': 18944,
#  'downloader/response_bytes': 128500683,
#  'downloader/response_count': 18943,
#  'downloader/response_status_count/200': 17835,
#  'downloader/response_status_count/301': 197,
#  'downloader/response_status_count/403': 32,
#  'downloader/response_status_count/404': 879,
#  'elapsed_time_seconds': 703.898865,
#  'finish_reason': 'finished',
#  'finish_time': datetime.datetime(2022, 7, 7, 21, 54, 43, 606223),
#  'httpcompression/response_bytes': 510809731,
#  'httpcompression/response_count': 18746,
#  'httperror/response_ignored_count': 911,
#  'httperror/response_ignored_status_count/403': 32,
#  'httperror/response_ignored_status_count/404': 879,
#  'item_scraped_count': 78132,
#  'log_count/DEBUG': 97086,
#  'log_count/ERROR': 1,
#  'log_count/INFO': 19878,
#  'memusage/max': 115830784,
#  'memusage/startup': 74477568,
#  'request_depth_max': 21,
#  'response_received_count': 18746,
#  'retry/count': 1,
#  'retry/reason_count/twisted.web._newclient.ResponseNeverReceived': 1,
#  'scheduler/dequeued': 18944,
#  'scheduler/dequeued/memory': 18944,
#  'scheduler/enqueued': 18944,
#  'scheduler/enqueued/memory': 18944,
#  'spider_exceptions/AttributeError': 1,
#  'start_time': datetime.datetime(2022, 7, 7, 21, 42, 59, 707358)}
# [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <404 https://www.javbus.com/uncensored/star/b7u>: HTTP status code is not handled or not allowed
# [scrapy.spidermiddlewares.httperror] INFO: Ignoring response <403 https://www.javbus.com/uncensored/star/tz8>: HTTP status code is not handled or not allowed

# 问题 爬取过程可能会出现 403 404  需要做补齐措施