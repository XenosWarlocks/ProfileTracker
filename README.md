
# Profile Tracker

Profile Tracker helps you monitor changes in job titles and company affiliations for a list of LinkedIn profiles. It compares current profile data against your records and generates reports of any changes detected.



## Features

- 🔍 Automated profile validation against LinkedIn
- 📊 CSV-based input and output
- 🖥️ User-friendly GUI for file selection
- 🔐 Secure credential handling
- 📝 Detailed change tracking
- 🐞 Debug mode for troubleshooting


## Prerequisites

- Python 3.7+
- Chrome browser installed
- ChromeDriver matching your Chrome version
- LinkedIn account with login credentials

```bash
  pip install pandas selenium tkinter
```

## Input CSV Format

Your input CSV must contain the following columns:

- Company Name
- First Name
- Last Name
- Job Title
- LinkedIn URL

## Examples

```csv
First Name,Last Name,Company Name,Job Title,LinkedIn URL
John,Doe,Tech Corp,Software Engineer,https://www.linkedin.com/in/johndoe
Jane,Smith,Data Inc,Data Scientist,https://www.linkedin.com/in/janesmith
```

## Usage
1. Clone the repository:
```
https://github.com/XenosWarlocks/ProfileTracker.git
```

2. Run the script:
```
python linkedin_validator.py
```
3. Follow the GUI prompts to:

- Select your input CSV file
- Enter LinkedIn credentials
- Wait for the validation process
- Review the generated report


## Output

The tool generates a timestamped CSV file (`linkedin_updates_YYYYMMDD_HHMMSS.csv`) containing:

- First Name
- Last Name
- Original Company
- Original Job Title
- New Company
- New Job Title
- LinkedIn URL
- Update Date

## Debug Mode
Enable debug mode for detailed logging:

```python
validator = LinkedInValidator()
validator.enable_debug()
validator.run()
```

## Key Classes and Methods
### LinkedInValidator

- `__init__()`: Initializes the validator and GUI components
- `validate_csv_file()`: Handles CSV file selection and validation
- `verify_profiles()`: Performs the profile verification process
- `save_updates()`: Generates the output report
- `cleanup()`: Handles resource cleanup

## Best Practices

- Rate Limiting: Add delays between profile checks to avoid - LinkedIn's rate limits
- Error Handling: Enable debug mode when troubleshooting issues
- Data Privacy: Never commit LinkedIn credentials to version control
- CSV Backup: Keep backups of your input CSV files
