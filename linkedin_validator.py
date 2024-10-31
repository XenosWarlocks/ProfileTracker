from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime

import pandas as pd
import time
import os
import getpass
import tkinter as tk
# removed from tkinter import filedialog
# removed from tkinter import messagebox


class LinkedInValidator:
    def __init__(self):
        self.df = None
        self.driver = None
        self.profiles_list = []
        self.updates_list = []
        self.debug_mode = False
        # Initialize root window but keep it hidden
        self.root = tk.Tk()
        self.root.withdraw()
        
    def enable_debug(self):
        """Enable debug mode for detailed logging"""
        self.debug_mode = True
        print("Debug mode enabled")

    def validate_csv_file(self):
        """Get and validate CSV file using Tkinter file dialog"""
        while True:
            # Open file dialog for CSV files
            file_path = filedialog.askopenfilename(
                title='Select CSV File',
                filetypes=[('CSV Files', '*.csv'), ('All Files', '*.*')],
                initialdir=os.getcwd()
            )
            
            # User cancelled file selection
            if not file_path:
                if messagebox.askretrycancel("No File Selected", "Would you like to try again?"):
                    continue
                else:
                    return False
                
            try:
                # Try reading the CSV
                df = pd.read_csv(file_path)
                
                # Check required columns
                required_columns = [
                    'Company Name', 
                    'First Name', 
                    'Last Name', 
                    'Job Title', 
                    'LinkedIn URL'
                ]
                
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    error_message = f"Missing required columns:\n{', '.join(missing_columns)}\n\n"
                    error_message += f"Required columns are:\n{', '.join(required_columns)}\n\n"
                    error_message += f"Found columns:\n{', '.join(df.columns)}"
                    
                    messagebox.showerror("Invalid CSV Format", error_message)
                    continue
                
                # Check for empty values in required columns
                empty_columns = [col for col in required_columns if df[col].isna().any()]
                if empty_columns:
                    warning_message = f"Found empty values in columns:\n{', '.join(empty_columns)}"
                    proceed = messagebox.askyesno("Warning", warning_message + "\n\nWould you like to proceed anyway?")
                    if not proceed:
                        continue
                
                # Store DataFrame and create profiles list
                self.df = df
                self._create_profiles_list()
                messagebox.showinfo("Success", f"Successfully loaded CSV file with {len(df)} profiles")
                return True
                
            except Exception as e:
                messagebox.showerror("Error", f"Error reading CSV file:\n{str(e)}")
                continue

    def _create_profiles_list(self):
        """Create list of profiles from DataFrame"""
        self.profiles_list = []
        for _, row in self.df.iterrows():
            profile = {
                'first_name': row['First Name'].strip(),
                'last_name': row['Last Name'].strip(),
                'company_name': row['Company Name'].strip(),
                'job_title': row['Job Title'].strip(),
                'linkedin_url': row['LinkedIn URL'].strip()
            }
            self.profiles_list.append(profile)

    def get_linkedin_credentials(self):
        """Get LinkedIn credentials from user"""
        print("\nPlease enter your LinkedIn credentials:")
        while True:
            email = input("Email: ").strip()
            if '@' not in email:
                print("Please enter a valid email address.")
                continue
                
            # Use getpass for password input (hidden input)
            password = getpass.getpass("Password: ")
            if not password:
                print("Password cannot be empty.")
                continue
                
            return email, password

    def setup_driver(self):
        """Setup Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            
            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            print(f"Error setting up WebDriver: {str(e)}")
            return False

    def login_to_linkedin(self, email, password):
        """Login to LinkedIn"""
        try:
            print("\nAttempting to log in to LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(2)

            # Fill email
            email_field = self.driver.find_element(By.ID, 'username')
            email_field.send_keys(email)

            # Fill password
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(password)

            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()

            # Wait for login to complete
            time.sleep(5)

            # Check if login was successful
            if "checkpoint" in self.driver.current_url or "login" in self.driver.current_url:
                print("Login failed. Please check your credentials.")
                return False

            print("Successfully logged in to LinkedIn")
            return True
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False

    def extract_profile_info(self, url):
        """Extract profile information from LinkedIn page"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page load

            # Wait for profile section
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mt2.relative'))
            )

            # Extract name
            name_element = self.driver.find_element(
                By.CSS_SELECTOR, 
                'h1.text-heading-xlarge.inline.t-24'
            )
            full_name = name_element.text.strip()
            first_name, last_name = self._split_name(full_name)

            # Extract headline
            headline_element = self.driver.find_element(
                By.CSS_SELECTOR, 
                'div.text-body-medium.break-words'
            )
            headline = headline_element.text.strip()
            job_title, company_name = self._parse_headline(headline)

            return {
                'first_name': first_name,
                'last_name': last_name,
                'job_title': job_title,
                'company_name': company_name,
                'linkedin_url': url
            }

        except Exception as e:
            print(f"Error extracting profile info for {url}: {str(e)}")
            return None

    def _split_name(self, full_name):
        """Split full name into first and last name"""
        parts = full_name.split()
        if len(parts) >= 2:
            return parts[0], parts[-1]
        return parts[0], ""

    def _parse_headline(self, headline):
        """Parse job title and company from headline"""
        separators = [' at ', ' @ ', ' - ', ' in ', ' with ']
        
        for separator in separators:
            if separator.lower() in headline.lower():
                parts = headline.split(separator, 1)
                return parts[0].strip(), parts[1].strip()
        
        return headline, ""

    def verify_profiles(self):
        """Verify all profiles against LinkedIn"""
        print("\nStarting profile verification...")
        
        for profile in self.profiles_list:
            if self.debug_mode:
                print(f"\nVerifying profile: {profile['first_name']} {profile['last_name']}")
                
            current_info = self.extract_profile_info(profile['linkedin_url'])
            
            if current_info:
                # Check for changes
                if (current_info['company_name'].lower() != profile['company_name'].lower() or
                    current_info['job_title'].lower() != profile['job_title'].lower()):
                    
                    update = {
                        'original': profile,
                        'current': current_info,
                        'update_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    self.updates_list.append(update)
                    
                    if self.debug_mode:
                        print("Update found!")
                        print(f"Old: {profile['company_name']} - {profile['job_title']}")
                        print(f"New: {current_info['company_name']} - {current_info['job_title']}")

    def save_updates(self):
        """Save updates to CSV file"""
        if not self.updates_list:
            print("\nNo updates found to save.")
            return True

        try:
            updates_data = []
            for update in self.updates_list:
                updates_data.append({
                    'First Name': update['current']['first_name'],
                    'Last Name': update['current']['last_name'],
                    'Original Company': update['original']['company_name'],
                    'Original Job Title': update['original']['job_title'],
                    'New Company': update['current']['company_name'],
                    'New Job Title': update['current']['job_title'],
                    'LinkedIn URL': update['current']['linkedin_url'],
                    'Update Date': update['update_date']
                })

            updates_df = pd.DataFrame(updates_data)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'linkedin_updates_{timestamp}.csv'
            
            updates_df.to_csv(output_file, index=False)
            print(f"\nSaved {len(updates_data)} updates to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error saving updates: {str(e)}")
            return False

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        # Destroy the Tkinter root window
        if self.root:
            self.root.destroy()

    def run(self):
        """Main execution flow"""
        try:
            print("LinkedIn Profile Validator")
            print("-------------------------")
            
            # Validate CSV file
            if not self.validate_csv_file():
                return False
                
            # Get LinkedIn credentials
            email, password = self.get_linkedin_credentials()
            
            # Setup WebDriver
            if not self.setup_driver():
                return False
                
            # Login to LinkedIn
            if not self.login_to_linkedin(email, password):
                self.cleanup()
                return False
                
            # Verify profiles
            self.verify_profiles()
            
            # Save updates
            self.save_updates()
            
            messagebox.showinfo("Success", "Profile verification completed successfully!")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            return False
            
        finally:
            self.cleanup()

# Usage
if __name__ == "__main__":
    validator = LinkedInValidator()
    validator.run()
    
