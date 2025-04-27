import re
from datetime import datetime
import argparse
import os
from utils.log import Log
from typing import Optional
from parsers_dir.abstract_parser import AbstractParser
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

class DockerParser(AbstractParser):
    def __init__(self, config: dict):
        self.log = Log("DockerParser", config)

    def file_parser(self, file_path: str) -> list[dict]:
        logs = []
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    parsed_line = self.parse_log_entry(line)

                except Exception as e:
                    self.log.error(f"Error processing line: {e}")
                    continue
                logs.append(parsed_line)
        return logs

    def get_index_pattern(self, idx_name: str) -> dict:
        self.log.error(f"get_index_pattern not implemented for this parser")
        return {}

    def parse_log_entry(self, log_entry: str) -> Optional[dict]:
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
            self.log.error("Failed to parse log entry:", log_entry)
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker logs file parser.")
    parser.add_argument('file_path', type=str, help='The path of the Docker log file to parse')

    # Parse the arguments
    args = parser.parse_args()
    """
    # Parse and print the log entries (Docker)
    dir_path = os.path.dirname(__file__)
    d = DockerParser()
    docker_logs_path = os.path.join(dir_path, args.file_path)
    parsed_log = d.file_parser(docker_logs_path)
    print(parsed_log)
    """
