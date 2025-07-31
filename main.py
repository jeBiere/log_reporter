import argparse
from pathlib import Path
from report import process_logs, generate_average_report

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', nargs='+', required=True)
    parser.add_argument('--report', required=True, choices=['average'])
    return parser.parse_args()

def main():
    args = parse_args()
    file_paths = [Path(path) for path in args.file]

    existing_files = [path for path in file_paths if path.exists()]
    missing_files = [path for path in file_paths if not path.exists()]

    if missing_files:
        print("Warning: The following files do not exist and will be skipped:")
        for path in missing_files:
            print(f"  - {path}")

    if not existing_files:
        print("Error: No valid log files found.")
        return 1

    stats = process_logs(existing_files)

    if args.report == 'average':
        output = generate_average_report(stats)
        print(output)

    return 0



if __name__ == '__main__':
    raise SystemExit(main())

