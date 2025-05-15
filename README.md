# 🛠️ Community Hydrofabric Error Tracking

[![Workflow Status](https://github.com/lynker-spatial/Community_Hydrofabric/actions/workflows/export-map-errors.yml/badge.svg)](https://github.com/lynker-spatial/Community_Hydrofabric/actions/workflows/export-map-errors.yml)
![GitHub issues](https://img.shields.io/github/issues/lynker-spatial/Community_Hydrofabric)

- [Hydrolocations: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/map-error-hydrolocations)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Amap-error-hydrolocations)
- [Topo Fixes: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/map-error-topo-fixes)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Amap-error-topo-fixes)
- [Merge Flowpaths: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/map-error-merge-flowpaths)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Amap-error-merge-flowpaths)
- [Reid Divide: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/reid_divide-merge-flowpaths)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Areid_divide-merge-flowpaths)
- [Remove Flowpaths: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/reid_divide-remove-flowpaths)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Areid_divide-remove-flowpaths)
- [Union Divides: ![issues](https://img.shields.io/github/issues-raw/lynker-spatial/Community_Hydrofabric/reid_divide-union-divides)](https://github.com/lynker-spatial/Community_Hydrofabric/issues?q=is%3Aopen+is%3Aissue+label%3Areid_divide-union-divides)


Welcome to the **Community Hydrofabric** repository! This space is dedicated to tracking and managing errors related to map items within the hydrofabric, such as **hydrolocations**, **topology fixes**, and other geospatial issues.

We leverage **GitHub issue templates** to standardize the reporting process to automate validation and generate valuable CSV reports for easy tracking and analysis.

---

## 📄 Table of Contents

*   [Introduction](#introduction)
*   [Issue Types](#issue-types)
    *   [Hydrolocations](#hydrolocations)
    *   [Topo Fixes](#topo-fixes)
    *   [Merge Flowpaths](#merge-flowpaths)
    *   [Reid Divide](#reid-divide)
    *   [Remove Flowpaths](#remove-flowpaths)
    *   [Union Divides](#union-divides)
*   [How to Report an Issue](#how-to-report-an-issue)
    *   [Selecting the Right Template](#selecting-the-right-template)
    *   [Filling Out the Template](#filling-out-the-template)
    *   [Tips for Reporting](#tips-for-reporting)
*   [Validation and Automation](#validation-and-automation)
*   [Additional Information](#additional-information)

---

## 🌟 Introduction

This repository serves as a central hub for users to report errors in hydrofabric map data. This includes issues like:

*   Incorrect **hydrolocations** (POI assignments)
*   **Topology** problems (missing/incorrect flowpaths)
*   **Flowpath** and **divide** errors (merging, removing, re-identifying)

By using predefined **issue templates**, we ensure that all necessary information is collected in a consistent and structured format, Therefore streamlining the process of managing and resolving reported errors.

---

## 📝 Issue Types

There are six primary types of issues you can report, each with its own dedicated GitHub Issue Template.

### 📍 Hydrolocations

*   **Description:** Use this template to report issues with **hydrolocations** (Points of Interest on flowpaths), such as incorrect assignments, outdated information, or the need to add new hydrolocation features.
*   **Template:** [Open Hydrolocations Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=06-hydrolocations.yml) 
*   **Key Fields:**
    *   `Item Identifier`: Hydrolocation feature ID (e.g., `wb-620629`)
    *   `POI Identifier`: The hydrolocation poi_id (e.g., 3366)
    *   `VPU`: The VPU the feature belongs to (e.g., `01`)
    *   `Issue Type`: (e.g., `"Not indexed to the right flowpath"`, `"Add a hydrolocation feature"`)
    *   `New ID`: Required if "Not indexed to the right flowpath" is selected (e.g., `wb-620630`)
    *   `Coordinates`: `Latitude`, `Longitude`, `EPSG Code` if adding a new feature (e.g., `34.05`, `-118.25`, `5070`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

### 🗺️ Topo Fixes

*   **Description:** Use this template to report general **topology-related fixes**, such as missing or incorrectly directed flowpaths, or connectivity issues not covered by merge/remove templates.
*   **Template:** [Open Topo Fixes Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=01-topo-fixes.yml) 
*   **Key Fields:**
    *   `Item Identifier`: The feature ID related to the topo issue (e.g., `wb-1455862`)
    *   `Topology toid`: Specific topology ID if different (e.g., `wb-1455862`)
    *   `VPU`: The VPU the feature belongs to (e.g., `01`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

### ➡️ Merge Flowpaths

*   **Description:** Use this template to report issues where multiple flowpaths need to be **merged** into a single flowpath.
*   **Template:** [Open Merge Flowpaths Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=02-merge-flowpaths.yml) 
*   **Key Fields:**
    *   `Item Identifier`: The **new** flowpath ID after merging (e.g., `wb-620629`)
    *   `Topology toid`: Related topology ID (e.g., `wb-609109`)
    *   `IDs to Merge`: A **comma-separated list** of flowpath IDs to be merged (e.g., `wb-620629,wb-620609,wb-620610`)
    *   `VPU`: The VPU these features belong to (e.g., `01`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

### 🔄 Reid Divide

*   **Description:** Use this template to report issues requiring the **re-identification** (changing the ID) of a divide feature.
*   **Template:** [Open Reid Divide Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=03-reid-divide.yml) 
*   **Key Fields:**
    *   `Item Identifier`: The **current** divide ID (e.g., `cat-620629`)
    *   `New ID`: The **desired new** divide ID (e.g., `cat-620630`)
    *   `VPU`: The VPU the divide belongs to (e.g., `01`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

### ❌ Remove Flowpaths

*   **Description:** Use this template to report **flowpaths that need to be removed** from the hydrofabric.
*   **Template:** [Open Remove Flowpaths Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=04-remove-flowpaths.yml) 
*   **Key Fields:**
    *   `Item Identifier`: The flowpath ID to **remove** (e.g., `wb-620629`)
    *   `VPU`: The VPU the flowpath belongs to (e.g., `01`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

### 🤝 Union Divides

*   **Description:** Use this template to report issues where multiple divide features need to be **unionized** (merged spatially and assigned a single ID).
*   **Template:** [Open Union Divides Issue Template](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new?template=05-union-divides.yml) 
*   **Key Fields:**
    *   `Item Identifier`: The **new** divide ID after union (e.g., `cat-620629`)
    *   `IDs to Merge`: A **comma-separated list** of divide IDs to be unioned (e.g., `cat-620629,cat-620630,cat-620631`)
    *   `VPU`: The VPU these features belong to (e.g., `01`)
    *   `Hydrofabric Version`: The version affected (e.g., `v2.2`)
    *   `Description of the issue`: Detailed explanation (with option to attach files)

---

## ❓ How to Report an Issue

Follow these simple steps to report an issue effectively using the appropriate template:

### Selecting the Right Template

1.  Navigate to the **"Issues"** tab in this repository.
2.  Click the **"New issue"** button.
3.  Browse the available templates and choose the one that best matches the type of issue you want to report (e.g., `Map Error: Hydrolocations` or `Map Error: Topo Fixes`).
4.  Click on the selected template.

### Filling Out the Template

1.  **Required Fields:** Pay close attention to fields marked with an asterisk (\*). Ensure all required information is accurately provided (**except for title that should not be changed**).
2.  **Coordinates:** If providing coordinates, enter **numerical values** for `Latitude` and `Longitude`, and the **numerical EPSG code** (e.g., `5070` for NAD83 / Conus Albers).
3.  **New ID / IDs to Merge/Union:** For relevant issue types, follow the instructions carefully regarding providing a `New ID` or a `comma-separated list` of IDs.
4.  **Description:** Provide a clear and concise description of the issue. Include context, observed behavior, and expected behavior. You can also **upload images** directly into the description field by dragging and dropping them.
5.  **Hydrofabric Version:** Select the version of the hydrofabric you are working with from the dropdown.

### Tips for Reporting

*   ✅ Use the provided placeholders and examples in the template as guides.
*   🤷‍♀️ If you’re unsure about a specific field, refer to the description provided within the template itself or add a note in the main description.
*   📍 For coordinates, double-check the `EPSG code` to avoid validation errors.
*   📸 Screenshots or maps highlighting the issue location are highly encouraged and can be easily added to the description.

---

## 🤖 Validation and Automation

Our workflow is designed to help ensure data quality and streamline processing:

*   **Automatic Validation:** When you submit or edit an issue, a GitHub Action is triggered to automatically validate the input based on the specific issue type and the data you've entered.
    *   *Example:* If you select `"Add a hydrolocation feature"` in the Hydrolocations template, the action verifies that `Latitude`, `Longitude`, and `EPSG Code` are provided.
    *   *Example:* If you select `"Not indexed to the right flowpath"`, the action checks that a `New ID` is present.
*   **Feedback:** If the validation fails due to missing required fields or incorrect formatting, the GitHub Action will automatically post a **comment** on the issue, clearly indicating what needs to be corrected.

---

## 🌐 Additional Information

*   **Support:** For general questions about the hydrofabric, issues with the templates or automation workflows, or other related inquiries, please [open a general issue here](https://github.com/lynker-spatial/Community_Hydrofabric/issues/new) (if a general template exists, otherwise use the new issue button) or reach out to the maintainers.

Thank you for helping us improve the Community Hydrofabric!