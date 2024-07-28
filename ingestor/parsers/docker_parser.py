import re
from datetime import datetime

# Define the regex pattern to match the Docker log entries
log_pattern = re.compile(
    r'^(?P<node>[\w-]+)\s+\|\s+\[(?P<timestamp>[^\]]+)\]\[(?P<log_level>[^\]]+)\]\[(?P<component>[^\]]+)\]\s+\[(?P<node_name>[^\]]+)\]\s+(?P<message>.+)$'
)

"""
TODO : solve this issue : voir la norme car ici format différent avec du dict après le nom du node
Failed to parse log entry: opensearch-dashboards  | {"type":"log","@timestamp":"2024-07-28T05:37:57Z","tags":["info","savedobjects-service"],"pid":1,"message":"Starting saved objects migrations"}
Failed to parse log entry: opensearch-dashboards  | {"type":"log","@timestamp":"2024-07-28T05:37:57Z","tags":["warning","cross-compatibility-service"],"pid":1,"message":"Starting cross compatibility service"}
Failed to parse log entry: opensearch-dashboards  | {"type":"log","@timestamp":"2024-07-28T05:37:57Z","tags":["info","plugins-system"],"pid":1,"message":"Starting [52] plugins: [usageCollection,opensearchDashboardsUsageCollection,opensearchDashboardsLegacy,mapsLegacy,share,opensearchUiShared,legacyExport,embeddable,expressions,data,securityAnalyticsDashboards,savedObjects,home,apmOss,reportsDashboards,dashboard,mlCommonsDashboards,assistantDashboards,visualizations,visBuilder,visTypeMarkdown,visTypeVega,visTypeTimeline,visTypeTable,visAugmenter,anomalyDetectionDashboards,alertingDashboards,tileMap,regionMap,customImportMapDashboards,inputControlVis,visualize,ganttChartDashboards,searchRelevanceDashboards,indexManagementDashboards,management,indexPatternManagement,advancedSettings,console,notificationsDashboards,dataExplorer,bfetch,charts,visTypeVislib,visTypeTimeseries,visTypeTagcloud,visTypeMetric,discover,savedObjectsManagement,securityDashboards,observabilityDashboards,queryWorkbenchDashboards]"}
Failed to parse log entry: opensearch-dashboards  | {"type":"log","@timestamp":"2024-07-28T05:37:57Z","tags":["listening","info"],"pid":1,"message":"Server running at http://0.0.0.0:5601"}
Failed to parse log entry: opensearch-dashboards  | {"type":"log","@timestamp":"2024-07-28T05:37:58Z","tags":["info","http","server","OpenSearchDashboards"],"pid":1,"message":"http server running at http://0.0.0.0:5601"}
"""

def parse_docker(log_entry):
    match = log_pattern.match(log_entry)
    if match:
        log_dict = match.groupdict()

        # Convert timestamp to a datetime object
        try:
            log_dict['timestamp'] = datetime.strptime(log_dict['timestamp'], '%Y-%m-%dT%H:%M:%S,%f')
        except ValueError:
            log_dict['timestamp'] = None

        return log_dict
    else:
        print("Failed to parse log entry:", log_entry)
        return None

if __name__ == '__main__':
    # Sample Docker log entries
    log_entries = [
        "opensearch-node1       | [2024-07-28T05:53:58,900][WARN ][o.o.c.r.a.AllocationService] [opensearch-node1] Falling back to single shard assignment since batch mode disable or multiple custom allocators set",
        "opensearch-node1       | [2024-07-28T05:53:59,015][INFO ][o.o.p.PluginsService     ] [opensearch-node1] PluginService:onIndexModule index:[daemon-logs/fYPWwMp4Qjq6JjdUxecUig]",
        "opensearch-node1       | [2024-07-28T05:53:59,021][INFO ][o.o.c.m.MetadataMappingService] [opensearch-node1] [daemon-logs/fYPWwMp4Qjq6JjdUxecUig] create_mapping",
        "opensearch-node2       | [2024-07-28T05:53:59,339][INFO ][o.o.i.r.RecoverySourceHandler] [opensearch-node2] [daemon-logs][3][recover to opensearch-node1] finalizing recovery took [129.7ms]",
        "opensearch-node2       | [2024-07-28T05:53:59,412][INFO ][o.o.a.u.d.DestinationMigrationCoordinator] [opensearch-node2] Cancelling the migration process."
    ]

    # Parse and print the log entries
    for log in log_entries:
        parsed_log = parse_docker_log(log)
        print(parsed_log)
