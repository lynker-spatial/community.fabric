#!/usr/bin/env python3
# .github/scripts/export_map_errors.py
#!/usr/bin/env python3
import os
import csv
import re
import argparse
from github import Github
from pyproj import Transformer

def safe_float(s):
    try:
        return float(s)
    except ValueError:
        return None

def safe_int(s):
    try:
        return int(s)
    except ValueError:
        return None
    
def parse_issue_body(body: str) -> dict:
    data = {}
    if not body:
        return data
    lines = body.splitlines()
    current_section = None
    section_content = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("### "):
            if current_section:
                data[current_section] = "\n".join(section_content).strip()
            current_section = stripped_line[4:].strip()
            section_content = []
        elif current_section and stripped_line:
            section_content.append(stripped_line)
    if current_section:
        data[current_section] = "\n".join(section_content).strip()

    # Extract image URL
    image_url_match = re.search(r'!\[.*?\]\((https://user-images\.githubusercontent\.com/.*?)\)', body)
    data['image_url'] = image_url_match.group(1) if image_url_match else ''
    return data

def main():
    parser = argparse.ArgumentParser(description="Export GH issues with a specific label into CSV")
    parser.add_argument("--label", required=True, help="Label to filter issues (e.g. map-error-topo-fixes)")
    parser.add_argument("--output", default="issues.csv", help="Name of the output CSV file")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("REPO")

    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        exit(1)
    if not repo_name:
        print("Error: REPO environment variable not set.")
        exit(1)

    try:
        gh = Github(token)
        repo = gh.get_repo(repo_name)
        print(f"Attempting to fetch issues with state='open' and label='{args.label}' from {repo_name}...")
        issues = repo.get_issues(state="open", labels=[args.label])
        issue_list = list(issues)
        print(f"Found {len(issue_list)} issues matching criteria.")
        if not issue_list:
            print("No issues found matching criteria. CSV will only contain header.")

        with open(args.output, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "issue_number",
                "item_identifier",
                "topology_toid",
                "ds_to_merge",
                "new_id",
                "id_to_merge",
                "vpu",
                "issue_type",
                "latitude",
                "longitude",
                "epsg",
                "latitude_adjusted",
                "longitude_adjusted",
                "description",
                "image_url",
                "reporter_user",
                "assignees",          
                "created_at_utc",
                "issue_url"
            ])

            for issue in issue_list:
                print(f"Processing issue #{issue.number}...")
                data = parse_issue_body(issue.body or "")  
                print(f"Parsed data for issue #{issue.number}: {data}")

                assignees = ", ".join([assignee.login for assignee in issue.assignees])

                lat = safe_float(data.get('Latitude', ''))
                lon = safe_float(data.get('Longitude', ''))
                epsg = safe_int(data.get('EPSG Code', ''))
                if lat is None or lon is None or epsg is None:
                    adjusted_lat = None
                    adjusted_lon = None
                else:
                    if epsg == 5070:
                        adjusted_lat = lat
                        adjusted_lon = lon
                    else:
                        try:
                            transformer = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:5070", always_xy=True)
                            adjusted_lon, adjusted_lat = transformer.transform(lon, lat)
                        except Exception as e:
                            print(f"Transformation failed for issue #{issue.number}: {e}")
                            adjusted_lat = None
                            adjusted_lon = None

                writer.writerow([
                    issue.number,
                    data.get("Item Identifier", ""),
                    data.get("Topology toid", ""),
                    data.get("DS to Merge", ""),
                    data.get("New ID", ""),
                    data.get("IDs to Merge", ""),
                    data.get("VPU", ""),
                    data.get("Issue Type", ""),
                    lat if lat is not None else '',
                    lon if lon is not None else '',
                    epsg if epsg is not None else '',
                    adjusted_lat if adjusted_lat is not None else '',
                    adjusted_lon if adjusted_lon is not None else '',
                    data.get("Describe the issue", ""),
                    data.get("image_url", ""),
                    issue.user.login,
                    assignees,          
                    issue.created_at.isoformat(),
                    issue.html_url
                ])
        print(f"Successfully exported issues to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()