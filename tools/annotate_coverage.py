import xml.etree.ElementTree as ET
import os

def parse_coverage_and_annotate(report_path):
    tree = ET.parse(report_path)
    root = tree.getroot()

    for file in root.findall(".//class"):
        file_name = file.get("filename")
        for line in file.findall("lines/line"):
            line_no = line.get("number")
            hits = line.get("hits")
            if hits == "0":
                print(f"::warning file={file_name},line={line_no}::Line {line_no} is not covered.")

if __name__ == "__main__":
    coverage_path = os.getenv("COVERAGE_REPORT", "coverage.xml")
    parse_coverage_and_annotate(coverage_path)