import os

def extract_coverage_summary(report_file):
    """
    Parses the pytest terminal output to extract the coverage summary.

    Args:
        report_file (str): Path to the pytest output file.

    Returns:
        str: A formatted markdown summary of the coverage report.
    """
    summary_lines = []
    in_summary_section = False

    with open(report_file, "r") as f:
        for line in f:
            # Check if we are in the summary section
            if "Name" in line and "Stmts" in line and "Cover" in line:
                in_summary_section = True
                summary_lines.append(line.strip())  # Append header line
            elif in_summary_section:
                if line.strip() == "" or "TOTAL" in line:  # Stop at TOTAL or empty line
                    summary_lines.append(line.strip())
                    break
                summary_lines.append(line.strip())

    # Convert summary to markdown
    markdown_summary = "### Coverage Summary\n\n"
    markdown_summary += "```\n"
    markdown_summary += "\n".join(summary_lines)
    markdown_summary += "\n```"
    return markdown_summary


if __name__ == "__main__":
    # Get the path to the pytest report
    report_path = "coverage_report.txt"
    if not os.path.exists(report_path):
        print("::error::Coverage report not found!")
        exit(1)

    # Extract and append the coverage summary
    summary = extract_coverage_summary(report_path)
    github_summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if github_summary_path:
        with open(github_summary_path, "a") as f:
            f.write(summary + "\n")
    else:
        print("::error::GITHUB_STEP_SUMMARY environment variable not found!")
        exit(1)
