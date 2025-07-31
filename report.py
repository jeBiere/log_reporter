import json
from collections import defaultdict
from tabulate import tabulate

def process_logs(file_paths):
    stats = defaultdict(lambda: [0, 0.0])
    for path in file_paths:
        with open(path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    url = entry['url']
                    response_time = entry['response_time']
                    stats[url][0] += 1
                    stats[url][1] += response_time
                except (KeyError, json.JSONDecodeError):
                    continue
    return stats

def generate_average_report(stats):
    report = []
    for url, (count, total_time) in sorted(stats.items()):
        average_time = total_time / count if count else 0
        report.append([url, count, round(average_time, 3)])
    return tabulate(report, headers=['Endpoint', 'Requests', 'Avg Response Time'], tablefmt='github')