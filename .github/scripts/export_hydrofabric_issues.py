#!/usr/bin/env python3
# .github/scripts/export_hydrofabric_issues.py

import os
import csv
import re
import argparse
from github import Github
from pyproj import Transformer, CRS
from pyproj.exceptions import CRSError

def safe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

def safe_int(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        return None

def parse_issue_body(body: str) -> dict:
    data = {}
    if not body:
        return data
    pattern = re.compile(r"###\s*(.*?)\s*\n\n([\s\S]*?)(?=\n###|\Z)")
    for match in pattern.finditer(body):
        section_title = match.group(1).strip()
        section_content = match.group(2).strip()
        if section_content == "_No response_":
            section_content = ""
        elif section_content.startswith("```") and section_content.endswith("```"):
            # Attempt to extract content if it's a simple block, otherwise clear
            lines = section_content.splitlines()
            if len(lines) > 2: 
                content_between_ticks = "\n".join(lines[1:-1]).strip()
                if content_between_ticks and not content_between_ticks.lower().startswith("shell") and not content_between_ticks.lower().startswith("text"): # Avoid ```shell
                     section_content = content_between_ticks

        data[section_title] = section_content
    
    image_url_match = re.search(r'!\[.*?\]\((https?://[^\s)]+\.(?:png|jpg|jpeg|gif|svg)).*?\)', body, re.IGNORECASE)
    if not image_url_match:
        image_url_match = re.search(r'!\[.*?\]\((https?://[^\s)]+)\)', body)
    data['image_url'] = image_url_match.group(1) if image_url_match else ''
    return data

def get_value_from_parsed_data(parsed_data, keys_to_try):
    if not isinstance(keys_to_try, list):
        keys_to_try = [keys_to_try]
    for key in keys_to_try:
        value = parsed_data.get(key)
        if value is not None and value != "":
            if value.strip() == "```" or value.strip().lower().startswith("```shell") or value.strip().lower().startswith("e.g.,"):
                return "" 
            return value
    return ""

def get_list_from_textarea(raw_text):
    if not raw_text:
        return []
    
    ignore_lines = [
        "```", "```shell", 
    ]
    
    cleaned_lines = []
    for line in raw_text.splitlines():
        stripped_line = line.strip()
        if not stripped_line:  
            continue
        
        is_placeholder_line = False
        for ignore_pattern in ignore_lines:
            if stripped_line.lower() == ignore_pattern.lower() or \
               (ignore_pattern.endswith("...") and stripped_line.lower().startswith(ignore_pattern[:-3].lower())) or \
               stripped_line.lower().startswith("e.g.,"): 
                is_placeholder_line = True
                break
        
        if not is_placeholder_line:
            if stripped_line.startswith("```") and stripped_line.endswith("```") and len(stripped_line) > 6:
                content_in_ticks = stripped_line[3:-3].strip()
                if content_in_ticks.lower() not in ["shell", "text", ""]:
                    cleaned_lines.append(content_in_ticks)
                
            else:
                cleaned_lines.append(stripped_line)
                
    return cleaned_lines


def main():
    parser = argparse.ArgumentParser(description="Export GH issues with a specific label into CSV")
    parser.add_argument("--label", required=True, help="Label to filter issues")
    parser.add_argument("--output", default="issues.csv", help="Name of the output CSV file")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")

    if not token: print("Error: GITHUB_TOKEN environment variable not set."); exit(1)
    if not repo_name: print("Error: GITHUB_REPOSITORY environment variable not set (e.g., 'owner/repo')."); exit(1)

    try:
        gh = Github(token)
        repo = gh.get_repo(repo_name)
        print(f"Attempting to fetch issues with state='open' and label='{args.label}' from {repo_name}...")
        issues = repo.get_issues(state="open", labels=[args.label])
        issue_list = list(issues)
        print(f"Found {len(issue_list)} issues matching criteria.")
        if not issue_list:
            print("No issues found matching criteria. CSV will only contain header.")

        csv_headers = [
            "issue_number", "report_mode", "hydrofabric_version", "item_identifier", 
            "hl_id", "hl_reference", "hl_link", "hl_source", "flowpath_id", "poi_id",
            "topology_toid", "ds_to_merge", "new_id", "id_to_merge", "vpu", 
            "issue_type", "data_url", "latitude", "longitude", "epsg",
            "latitude_adjusted", "longitude_adjusted", "description", "image_url", 
            "reporter_user", "assignees", "created_at_utc", "issue_url"
        ]
        csv_headers = sorted(list(set(csv_headers)), key=csv_headers.index)

        with open(args.output, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)

            for issue in issue_list:
                print(f"Processing issue #{issue.number} ({issue.title})...")
                parsed_body_data = parse_issue_body(issue.body or "")
                assignees_str = ", ".join([assignee.login for assignee in issue.assignees])
                
                report_mode_raw = get_value_from_parsed_data(parsed_body_data, ["Report Mode"])
                report_mode = report_mode_raw if "many" in report_mode_raw.lower() else "Report a single instance"
                if args.label == "Hydrofabric-large-data-submission":
                    report_mode = "Report a single instance"
                
                
                description_content = ""
                if args.label == "Hydrofabric-hydrolocation-additions":
                    description_content = get_value_from_parsed_data(parsed_body_data, ["Describe the new hydrolocation(s) / Additional Details"])
                elif args.label == "Hydrofabric-hydrolocation-adjustments":
                    description_content = get_value_from_parsed_data(parsed_body_data, ["Describe the adjustment needed / Additional Details"])
                elif args.label == "Hydrofabric-large-data-submission":
                     description_content = get_value_from_parsed_data(parsed_body_data, ["Detailed Description of the Data"])
                if not description_content: 
                    description_content = get_value_from_parsed_data(parsed_body_data, [
                        "Describe the issue(s)", "Describe the merge operations", "Describe the reid operations",
                        "Describe why these flowpaths should be removed", "Describe the union operations",
                        "Describe the issue / Additional Details", "Describe the issue"
                    ])


                base_data_for_issue = {
                    "issue_number": issue.number,
                    "reporter_user": issue.user.login,
                    "assignees": assignees_str,
                    "created_at_utc": issue.created_at.isoformat(),
                    "issue_url": issue.html_url,
                    "report_mode": report_mode,
                    "hydrofabric_version": get_value_from_parsed_data(parsed_body_data, ["Hydrofabric Version", "Relevant Hydrofabric Version(s)"]),
                    "issue_type": get_value_from_parsed_data(parsed_body_data, ["Issue Type"]),
                    "description": description_content,
                    "image_url": parsed_body_data.get("image_url", ""),
                    "ds_to_merge": get_value_from_parsed_data(parsed_body_data, ["DS to Merge"]),
                    "data_url": get_value_from_parsed_data(parsed_body_data, ["Data URL (Optional)", "Data URL"])
                }
                for key in ["item_identifier", "hl_id", "hl_reference", "hl_link", "hl_source", "flowpath_id", "poi_id",
                            "topology_toid", "new_id", "id_to_merge", "vpu",
                            "latitude", "longitude", "epsg", "latitude_adjusted", "longitude_adjusted"]:
                    base_data_for_issue[key] = "" 


                item_identifiers_raw = ""
                hl_links_raw = hl_references_raw = hl_sources_raw = flowpath_ids_raw = ""
                hl_ids_raw = ""
                latitudes_raw = longitudes_raw = epsgs_raw = ""
                topology_toids_raw = new_ids_raw = ids_to_merge_raw = ""

                vpus_raw = get_value_from_parsed_data(parsed_body_data, ["VPU(s)"]) 

                if args.label == "Hydrofabric-hydrolocation-additions":
                    item_identifiers_raw = get_value_from_parsed_data(parsed_body_data, ["HL Link (Internal ID / Unique Identifier)(s)"])
                    hl_links_raw = item_identifiers_raw 
                    hl_references_raw = get_value_from_parsed_data(parsed_body_data, ["HL Reference(s)"])
                    hl_sources_raw = get_value_from_parsed_data(parsed_body_data, ["HL Source (Optional)"])
                    flowpath_ids_raw = get_value_from_parsed_data(parsed_body_data, ["Target Flowpath ID(s)"])
                    latitudes_raw = get_value_from_parsed_data(parsed_body_data, ["Latitude(s)"])
                    longitudes_raw = get_value_from_parsed_data(parsed_body_data, ["Longitude(s)"])
                    epsgs_raw = get_value_from_parsed_data(parsed_body_data, ["EPSG Code(s)"])
                elif args.label == "Hydrofabric-hydrolocation-adjustments":
                    item_identifiers_raw = get_value_from_parsed_data(parsed_body_data, ["Item Identifier(s) (hl_id)"])
                    hl_ids_raw = item_identifiers_raw
                    flowpath_ids_raw = get_value_from_parsed_data(parsed_body_data, ["Target Flowpath ID(s)"])
                    latitudes_raw = get_value_from_parsed_data(parsed_body_data, ["New Latitude(s)"])
                    longitudes_raw = get_value_from_parsed_data(parsed_body_data, ["New Longitude(s)"])
                    epsgs_raw = get_value_from_parsed_data(parsed_body_data, ["New EPSG Code(s)"])
                elif args.label == "Hydrofabric-large-data-submission":
                    item_identifiers_raw = get_value_from_parsed_data(parsed_body_data, ["Brief Description of Data (for Title)"])
                else: 
                    item_identifiers_raw = get_value_from_parsed_data(parsed_body_data, [
                        "Item Identifier(s) (Current Flowpath)", "Item Identifier(s) (Flowpath)", 
                        "Item Identifier(s) to Remove", "New Item Identifier(s)", 
                        "Current Item Identifier(s)", "Item Identifier(s)", "Item Identifier"
                    ])
                    topology_toids_raw = get_value_from_parsed_data(parsed_body_data, ["Topology toid(s)", "New Topology toid(s)"])
                    new_ids_raw = get_value_from_parsed_data(parsed_body_data, ["New Correct Flowpath ID(s)", "New ID(s)", "New ID"])
                    ids_to_merge_raw = get_value_from_parsed_data(parsed_body_data, ["List(s) of IDs to Merge", "IDs to Merge", "IDs to Union"])

                if "many" in report_mode.lower() and args.label not in ["Hydrofabric-large-data-submission"]:
                    item_identifiers_list = get_list_from_textarea(item_identifiers_raw)
                    num_items = len(item_identifiers_list)
                    
                    if num_items == 0: 
                        print(f"  WARN: Issue #{issue.number} in 'Report many...' mode but no valid primary Identifiers found after cleaning. Skipping.")
                        continue 

                    vpus_list = get_list_from_textarea(vpus_raw)
                    latitudes_list = get_list_from_textarea(latitudes_raw)
                    longitudes_list = get_list_from_textarea(longitudes_raw)
                    epsgs_list = get_list_from_textarea(epsgs_raw)
                    
                    hl_links_list = get_list_from_textarea(hl_links_raw)
                    hl_references_list = get_list_from_textarea(hl_references_raw)
                    hl_sources_list = get_list_from_textarea(hl_sources_raw)
                    flowpath_ids_list = get_list_from_textarea(flowpath_ids_raw)
                    hl_ids_list = get_list_from_textarea(hl_ids_raw)
                    
                    topology_toids_list = get_list_from_textarea(topology_toids_raw)
                    new_ids_list = get_list_from_textarea(new_ids_raw)
                    ids_to_merge_list = get_list_from_textarea(ids_to_merge_raw)

                    single_vpu_for_all = len(vpus_list) == 1 and num_items > 1
                    single_epsg_for_all = len(epsgs_list) == 1 and num_items > 1
                    single_hl_source_for_all = len(hl_sources_list) == 1 and num_items > 1

                    for i in range(num_items):
                        row_data = base_data_for_issue.copy()
                        # item_identifier column gets the primary ID for this row from item_identifiers_list
                        row_data["item_identifier"] = item_identifiers_list[i] 
                        row_data["vpu"] = vpus_list[0] if single_vpu_for_all else (vpus_list[i] if i < len(vpus_list) else "")
                        
                        if args.label == "Hydrofabric-hydrolocation-additions":
                            row_data["hl_link"] = item_identifiers_list[i] 
                            row_data["hl_reference"] = hl_references_list[i] if i < len(hl_references_list) else ""
                            hl_source_val = hl_sources_list[0] if single_hl_source_for_all else (hl_sources_list[i] if i < len(hl_sources_list) else "")
                            row_data["hl_source"] = hl_source_val if hl_source_val else issue.user.login
                            row_data["flowpath_id"] = flowpath_ids_list[i] if i < len(flowpath_ids_list) else ""
                            row_data["latitude"] = latitudes_list[i] if i < len(latitudes_list) else ""
                            row_data["longitude"] = longitudes_list[i] if i < len(longitudes_list) else ""
                            row_data["epsg"] = epsgs_list[0] if single_epsg_for_all else (epsgs_list[i] if i < len(epsgs_list) else "")
                        elif args.label == "Hydrofabric-hydrolocation-adjustments":
                            row_data["hl_id"] = item_identifiers_list[i] 
                            row_data["flowpath_id"] = flowpath_ids_list[i] if i < len(flowpath_ids_list) else ""
                            row_data["latitude"] = latitudes_list[i] if i < len(latitudes_list) else ""
                            row_data["longitude"] = longitudes_list[i] if i < len(longitudes_list) else ""
                            row_data["epsg"] = epsgs_list[0] if single_epsg_for_all else (epsgs_list[i] if i < len(epsgs_list) else "")
                        else: 
                            row_data["topology_toid"] = topology_toids_list[i] if i < len(topology_toids_list) else ""
                            row_data["new_id"] = new_ids_list[i] if i < len(new_ids_list) else ""
                            row_data["id_to_merge"] = ids_to_merge_list[i] if i < len(ids_to_merge_list) else ""

                        if args.label in ["Hydrofabric-hydrolocation-additions", "Hydrofabric-hydrolocation-adjustments"]:
                            lat = safe_float(row_data["latitude"])
                            lon = safe_float(row_data["longitude"])
                            epsg_code = safe_int(row_data["epsg"])
                            adj_lat, adj_lon = None, None
                            if lat is not None and lon is not None and epsg_code is not None:
                                if epsg_code == 5070: adj_lat, adj_lon = lat, lon
                                else:
                                    try:
                                        transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:5070", always_xy=True)
                                        adj_lon, adj_lat = transformer.transform(lon, lat)
                                    except Exception as e: print(f"  Transformation failed for issue #{issue.number}, item {i+1}: {e}")
                                row_data["latitude_adjusted"] = str(adj_lat) if adj_lat is not None else ''
                                row_data["longitude_adjusted"] = str(adj_lon) if adj_lon is not None else ''
                        
                        row_to_write = [str(row_data.get(h, "")) for h in csv_headers]
                        writer.writerow(row_to_write)
                    print(f"  Generated {num_items} rows for issue #{issue.number} (multi-instance mode).")

                else: # Report a single instance
                    row_data = base_data_for_issue.copy()
                    row_data["item_identifier"] = item_identifiers_raw 
                    row_data["vpu"] = get_list_from_textarea(vpus_raw)[0] if vpus_raw else "" 

                    if args.label == "Hydrofabric-hydrolocation-additions":
                        row_data["hl_link"] = item_identifiers_raw # Primary ID
                        row_data["hl_reference"] = get_list_from_textarea(hl_references_raw)[0] if hl_references_raw else ""
                        hl_source_val = get_list_from_textarea(hl_sources_raw)[0] if hl_sources_raw else ""
                        row_data["hl_source"] = hl_source_val if hl_source_val else issue.user.login
                        row_data["flowpath_id"] = get_list_from_textarea(flowpath_ids_raw)[0] if flowpath_ids_raw else ""
                        row_data["latitude"] = get_list_from_textarea(latitudes_raw)[0] if latitudes_raw else ""
                        row_data["longitude"] = get_list_from_textarea(longitudes_raw)[0] if longitudes_raw else ""
                        row_data["epsg"] = get_list_from_textarea(epsgs_raw)[0] if epsgs_raw else ""
                    elif args.label == "Hydrofabric-hydrolocation-adjustments":
                        row_data["hl_id"] = item_identifiers_raw # Primary ID
                        row_data["flowpath_id"] = get_list_from_textarea(flowpath_ids_raw)[0] if flowpath_ids_raw else ""
                        row_data["latitude"] = get_list_from_textarea(latitudes_raw)[0] if latitudes_raw else ""
                        row_data["longitude"] = get_list_from_textarea(longitudes_raw)[0] if longitudes_raw else ""
                        row_data["epsg"] = get_list_from_textarea(epsgs_raw)[0] if epsgs_raw else ""
                    elif args.label != "Hydrofabric-large-data-submission":
                        row_data["topology_toid"] = get_list_from_textarea(topology_toids_raw)[0] if topology_toids_raw else ""
                        row_data["new_id"] = get_list_from_textarea(new_ids_raw)[0] if new_ids_raw else ""
                        row_data["id_to_merge"] = get_list_from_textarea(ids_to_merge_raw)[0] if ids_to_merge_raw else ""
                    
                    if args.label in ["Hydrofabric-hydrolocation-additions", "Hydrofabric-hydrolocation-adjustments"]:
                        lat = safe_float(row_data.get("latitude",""))
                        lon = safe_float(row_data.get("longitude",""))
                        epsg_code = safe_int(row_data.get("epsg",""))
                        adj_lat, adj_lon = None, None
                        if lat is not None and lon is not None and epsg_code is not None:
                            if epsg_code == 5070: adj_lat, adj_lon = lat, lon
                            else:
                                try:
                                    transformer = Transformer.from_crs(f"EPSG:{epsg_code}", "EPSG:5070", always_xy=True)
                                    adj_lon, adj_lat = transformer.transform(lon, lat)
                                except Exception as e: print(f"  Transformation failed for issue #{issue.number} (single): {e}")
                            row_data["latitude_adjusted"] = str(adj_lat) if adj_lat is not None else ''
                            row_data["longitude_adjusted"] = str(adj_lon) if adj_lon is not None else ''
                    
                    # Only write a row if the primary identifier for the row is not empty
                    if row_data.get("item_identifier", "").strip():
                        row_to_write = [str(row_data.get(h, "")) for h in csv_headers]
                        writer.writerow(row_to_write)
                        print(f"  Generated 1 row for issue #{issue.number} (single-instance/large-data mode).")
                    else:
                        print(f"  WARN: Issue #{issue.number} (single-instance mode) - primary identifier is empty after cleaning. Skipping row.")


        print(f"Successfully exported issues to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()