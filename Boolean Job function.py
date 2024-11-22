import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# List of ATS websites
ATS_SITES = [
    "lever.co",
    "greenhouse.io",
    "myworkdayjobs.com",
    "taleo.net",
    "jobs.ashbyhq.com"
]

# List of job titles and locations
JOB_TITLES = [
    {"title": "SharePoint Developer", "location": "Remote"},
    {"title": "SharePoint Developer", "location": "Austin, TX"},
    {"title": "SharePoint Administrator", "location": "Austin, TX"},
    {"title": "SharePoint Administrator", "location": "Remote"},
    {"title": "Business Analyst", "location": "Remote"},
    {"title": "Business Analyst", "location": "Austin, TX"},
    {"title": "Product Manager", "location": "Remote"}
]

# Boolean search generator
def generate_boolean_string(ats_site, job_title, location):
    return f'site:{ats_site} and "{job_title}" + "{location}"'

# Function to search and fetch results
def search_jobs(boolean_string):
    google_search_url = f"https://www.google.com/search?q={boolean_string}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(google_search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='g')  # Adjust if necessary for Google search changes
        return len(results)
    else:
        print(f"Error fetching results: {response.status_code}")
        return 0

# Log results to a file
def log_results_to_text(log_data):
    with open("job_search_log.txt", "a") as log_file:
        log_file.write(log_data + "\n")

# Export results to a spreadsheet
def export_to_spreadsheet(data, filename="job_search_results.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Results exported to {filename}")

# Main function to execute the job search
def main():
    log_data = f"Job Search Log - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_data += "-" * 50 + "\n"

    # Data for spreadsheet
    spreadsheet_data = []

    for ats_site in ATS_SITES:
        for job in JOB_TITLES:
            boolean_string = generate_boolean_string(ats_site, job["title"], job["location"])
            job_count = search_jobs(boolean_string)
            log_entry = f"{ats_site} | {job['title']} | {job['location']} | Jobs Found: {job_count}"
            log_data += log_entry + "\n"
            spreadsheet_data.append({
                "ATS Site": ats_site,
                "Job Title": job["title"],
                "Location": job["location"],
                "Job URL": link
            })

    log_data += "-" * 50 + "\n"
    print(log_data)
    log_results_to_text(log_data)

    # Export to spreadsheet
    export_to_spreadsheet(spreadsheet_data)

if __name__ == "__main__":
    main()
