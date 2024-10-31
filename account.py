import random
import string
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.common.action_chains import ActionChains

class IdentityGenerator:
    # Extended name databases
    NAMES_DB = {
        'christian': {
            'first': ['Matthew', 'John', 'Peter', 'Paul', 'Mary', 'Sarah', 'Elizabeth', 'Ruth', 'Michael', 'David', 'Daniel', 'Rachel'],
            'middle': ['Joseph', 'James', 'David', 'Michael', 'Anne', 'Grace', 'Faith', 'Hope', 'Thomas', 'Luke', 'Mark', 'Joy'],
            'last': ['Johnson', 'Smith', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Wilson', 'Anderson', 'Taylor', 'Moore', 'Jackson']
        },
        'jewish': {
            'first': ['Abraham', 'Isaac', 'Jacob', 'Benjamin', 'Sarah', 'Rachel', 'Rebecca', 'Leah', 'Moshe', 'David', 'Hannah', 'Miriam'],
            'middle': ['David', 'Solomon', 'Moses', 'Aaron', 'Miriam', 'Esther', 'Ruth', 'Naomi', 'Eli', 'Noah', 'Daniel', 'Rachel'],
            'last': ['Cohen', 'Levy', 'Goldberg', 'Shapiro', 'Friedman', 'Katz', 'Stern', 'Rosen', 'Schwartz', 'Weinberg', 'Kaplan', 'Abrams']
        },
        'hindu': {
            'first': ['Arjun', 'Krishna', 'Raj', 'Arun', 'Priya', 'Deepa', 'Meera', 'Anita', 'Rahul', 'Amit', 'Anjali', 'Kavita'],
            'middle': ['Kumar', 'Prasad', 'Devi', 'Kumari', 'Nath', 'Lal', 'Kant', 'Chand', 'Raj', 'Dev', 'Prakash', 'Bala'],
            'last': ['Patel', 'Shah', 'Singh', 'Kumar', 'Sharma', 'Gupta', 'Mehta', 'Verma', 'Reddy', 'Malhotra', 'Kapoor', 'Joshi']
        },
        'arabic': {
            'first': ['Mohammed', 'Ahmad', 'Ali', 'Hassan', 'Fatima', 'Aisha', 'Zainab', 'Maryam', 'Omar', 'Yusuf', 'Ibrahim', 'Layla'],
            'middle': ['Abdullah', 'Rahman', 'Hussein', 'Khalil', 'Noor', 'Din', 'Karim', 'Jamil', 'Malik', 'Aziz', 'Jamal', 'Kareem'],
            'last': ['Al-Sayed', 'Khan', 'Al-Rahman', 'Al-Hussein', 'Al-Ahmed', 'Al-Ali', 'Al-Hassan', 'Al-Mohammed', 'Malik', 'Sheikh', 'Rahman', 'Saleh']
        },
        'chinese': {
            'first': ['Wei', 'Jing', 'Ming', 'Lei', 'Hui', 'Xiao', 'Yuan', 'Ling', 'Chen', 'Jun', 'Feng', 'Hong'],
            'middle': ['', '', '', ''],  # Chinese names typically don't have middle names
            'last': ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Wu', 'Zhou', 'Sun', 'Zhao', 'Lin']
        },
        'japanese': {
            'first': ['Hiroshi', 'Takashi', 'Yuki', 'Kenji', 'Sakura', 'Yuko', 'Akiko', 'Haruki', 'Kaori', 'Shin', 'Ryu', 'Mei'],
            'middle': ['', '', '', ''],  # Japanese names typically don't have middle names
            'last': ['Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato', 'Yoshida', 'Yamada']
        }
    }

    # Dictionary to determine gender based on first names
    GENDER_MAP = {
        'christian': {
            'male': ['Matthew', 'John', 'Peter', 'Paul', 'Michael', 'David', 'Daniel'],
            'female': ['Mary', 'Sarah', 'Elizabeth', 'Ruth', 'Rachel']
        },
        'jewish': {
            'male': ['Abraham', 'Isaac', 'Jacob', 'Benjamin', 'Moshe', 'David'],
            'female': ['Sarah', 'Rachel', 'Rebecca', 'Leah', 'Hannah', 'Miriam']
        },
        'hindu': {
            'male': ['Arjun', 'Krishna', 'Raj', 'Arun', 'Rahul', 'Amit'],
            'female': ['Priya', 'Deepa', 'Meera', 'Anita', 'Anjali', 'Kavita']
        },
        'arabic': {
            'male': ['Mohammed', 'Ahmad', 'Ali', 'Hassan', 'Omar', 'Yusuf', 'Ibrahim'],
            'female': ['Fatima', 'Aisha', 'Zainab', 'Maryam', 'Layla']
        },
        'chinese': {
            'male': ['Wei', 'Ming', 'Lei', 'Chen', 'Jun', 'Feng'],
            'female': ['Hui', 'Xiao', 'Yuan', 'Ling', 'Hong']
        },
        'japanese': {
            'male': ['Hiroshi', 'Takashi', 'Kenji', 'Shin', 'Ryu'],
            'female': ['Sakura', 'Yuko', 'Akiko', 'Kaori', 'Mei']
        }
    }
    
    def __init__(self, culture='christian', password_length=16):
        self.culture = culture.lower()
        self.password_length = password_length
        self.identity = None
        self.driver = None
        self.wait = None

    def determine_gender(self, first_name):
        """Determine gender based on first name"""
        culture_genders = self.GENDER_MAP[self.culture]
        if first_name in culture_genders['male']:
            return 'male'
        elif first_name in culture_genders['female']:
            return 'female'
        return random.choice(['male', 'female'])
    
    def keyboard_enter(self):
        """Simulate pressing the Enter key with random delay"""
        self.random_delay(0.5, 1.5)
        active_element = self.driver.switch_to.active_element
        active_element.send_keys(Keys.RETURN)
        self.random_delay(1, 2)

    def random_delay(self, min_seconds=0.5, max_seconds=2):
        """Add a random delay to simulate human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def type_like_human(self, element, text):
        """Type text with random delays between keystrokes"""
        try:
            # Clear the field first
            element.clear()
            # Click to ensure focus
            self.safe_click(element)
            
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            self.random_delay(0.5, 1)
        except Exception as e:
            print(f"Error typing text: {str(e)}")
            self.take_screenshot("typing_error")
            raise
    
    def wait_and_find_element(self, by, value, timeout=10, condition="clickable"):
        """
        Wait for an element and return it when it's ready
        condition can be: "clickable", "present", "visible"
        """
        try:
            if condition == "clickable":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
            elif condition == "present":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            elif condition == "visible":
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by, value))
                )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.random_delay(0.5, 1)
            
            return element
        except Exception as e:
            print(f"Error finding element {value}: {str(e)}")
            self.take_screenshot(f"error_finding_{value}")
            raise

    def take_screenshot(self, name):
        """Take a screenshot for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.driver.save_screenshot(f"screenshots/{name}_{timestamp}.png")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

    def safe_click(self, element, max_attempts=3):
        """Attempt to click an element safely"""
        for attempt in range(max_attempts):
            try:
                # Try regular click
                element.click()
                return True
            except ElementClickInterceptedException:
                try:
                    # Try JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception:
                    # Try Actions click
                    try:
                        ActionChains(self.driver).move_to_element(element).click().perform()
                        return True
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            print(f"Failed to click element after {max_attempts} attempts: {str(e)}")
                            self.take_screenshot("click_error")
                            raise
                        time.sleep(1)
        return False
    
    def try_create_email(self, name_dict, max_attempts=5):
        """
        Attempt to create an email address and verify its availability.
        Returns a tuple (email, success) where success is True if an available email was found.
        """
        attempts = 0
        while attempts < max_attempts:
            email = self.create_email(name_dict)
            email_prefix = email.split('@')[0]
            
            try:
                # Enter the email
                email_input = self.wait_and_find_element(
                    By.NAME, 
                    "Username",
                    condition="clickable"
                )
                # Clear any existing input
                email_input.clear()
                self.type_like_human(email_input, email_prefix)
                
                # Click Next after email
                next_button = self.wait_and_find_element(
                    By.XPATH, 
                    "//span[text()='Next']",
                    condition="clickable"
                )
                self.safe_click(next_button)
                
                # Check for error message
                try:
                    error_message = self.wait_and_find_element(
                        By.XPATH,
                        "//*[contains(text(), 'That username is taken')]",
                        timeout=3
                    )
                    print(f"Username {email_prefix} is taken, trying another...")
                    attempts += 1
                    continue
                except:
                    # No error message found, username is available
                    print(f"Found available username: {email_prefix}")
                    return email, True
                    
            except Exception as e:
                print(f"Error checking username availability: {str(e)}")
                attempts += 1
        
        return None, False

    def create_gmail_account(self, headless=False, recovery_email=None, recovery_phone=None):
        """Create Gmail account following the exact sequence"""
        if not self.identity:
            self.create_identity()

        try:
            # Setup WebDriver
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 15)
            self.driver.maximize_window()

            # Navigate to Gmail signup
            self.driver.get('https://accounts.google.com/signup')
            self.random_delay(2, 3)

            try:
                # Step 1: First Name
                print("Entering first name...")
                first_name_input = self.wait_and_find_element(By.NAME, "firstName", condition="clickable")
                self.type_like_human(first_name_input, self.identity['first_name'])

                # Step 2: Last Name
                print("Entering last name...")
                last_name_input = self.wait_and_find_element(By.NAME, "lastName", condition="clickable")
                self.type_like_human(last_name_input, self.identity['last_name'])

                # Find and click the Next button
                print("Clicking Next after names...")
                next_button = self.wait_and_find_element(
                    By.XPATH, 
                    "//span[text()='Next']",
                    condition="clickable"
                )
                self.safe_click(next_button)

                # Press Enter after names
                self.keyboard_enter()

                # Step 3: Birthday and Gender
                print("Entering birthday information...")
                birth_date = self.generate_birth_date()
                
                # Month (dropdown)
                print("Selecting month...")
                month_select = self.wait_and_find_element(By.ID, "month", condition="clickable")
                Select(month_select).select_by_value(str(birth_date['month']))

                # Day
                print("Entering day...")
                day_input = self.wait_and_find_element(By.NAME, "day", condition="clickable")
                self.type_like_human(day_input, str(birth_date['day']))

                # Year
                print("Entering year...")
                year_input = self.wait_and_find_element(By.NAME, "year", condition="clickable")
                self.type_like_human(year_input, str(birth_date['year']))

                # Gender
                print("Selecting gender...")
                gender = self.determine_gender(self.identity['first_name'])
                gender_select = self.wait_and_find_element(By.ID, "gender", condition="clickable")
                Select(gender_select).select_by_value('1' if gender == 'male' else '2')

                # Click Next after birthday/gender
                print("Clicking Next after birthday/gender...")
                next_button = self.wait_and_find_element(
                    By.XPATH, 
                    "//span[text()='Next']",
                    condition="clickable"
                )
                self.safe_click(next_button)

                # Press Enter after birthday/gender
                self.keyboard_enter()

                # Step 4: Email Creation with retry logic
                print("Creating email...")
                email, success = self.try_create_email(
                    {
                        'first': self.identity['first_name'],
                        'middle': self.identity['middle_name'],
                        'last': self.identity['last_name']
                    }
                )
                
                if not success:
                    raise Exception("Failed to find an available username after multiple attempts")
                
                # Update the identity with the successful email
                self.identity['email'] = email

                # Click Next after email
                print("Clicking Next after email...")
                next_button = self.wait_and_find_element(
                    By.XPATH, 
                    "//span[text()='Next']",
                    condition="clickable"
                )
                self.safe_click(next_button)

                # Press Enter after email
                self.keyboard_enter()

                # Step 5: Password
                print("Entering password...")
                password_input = self.wait_and_find_element(
                    By.NAME, 
                    "Passwd",
                    condition="clickable"
                )
                self.type_like_human(password_input, self.identity['password'])

                # Step 6: Confirm Password
                print("Confirming password...")
                confirm_password_input = self.wait_and_find_element(
                    By.NAME, 
                    "ConfirmPasswd",
                    condition="clickable"
                )
                self.type_like_human(confirm_password_input, self.identity['password'])

                # Click Next after passwords
                print("Clicking Next after passwords...")
                next_button = self.wait_and_find_element(
                    By.XPATH, 
                    "//span[text()='Next']",
                    condition="clickable"
                )
                self.safe_click(next_button)

                # Press Enter after passwords
                self.keyboard_enter()

                # Optionally add recovery details if provided
                if recovery_email:
                    recovery_email_input = self.driver.find_element(By.NAME, "recoveryEmail")
                    self.type_like_human(recovery_email_input, recovery_email)
                    self.random_delay()

                if recovery_phone:
                    recovery_phone_input = self.driver.find_element(By.NAME, "phoneNumberId")
                    self.type_like_human(recovery_phone_input, recovery_phone)
                    self.random_delay()

                # Wait for potential phone/email verification request
                print("\nAccount creation initiated.")
                print("Please check for any verification requests or CAPTCHAs...")
                print("Current email:", self.identity['email'])
                print("Current password:", self.identity['password'])

                # Keep the browser open for manual intervention if needed
                input("\nPress Enter when you want to close the browser...")

            except Exception as e:
                print(f"Error during account creation: {str(e)}")
                self.take_screenshot("error_during_creation")
                raise

        except Exception as e:
            print(f"Failed to start account creation process: {str(e)}")
            return False

        finally:
            if self.driver:
                self.driver.quit()

    def generate_birth_date(self):
        """Generate a random birth date for someone between 18 and 35 years old"""
        today = datetime.now()
        start_date = today - timedelta(days=35*365)
        end_date = today - timedelta(days=18*365)
        
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        
        return {
            'day': random_date.day,
            'month': random_date.month,
            'year': random_date.year
        }


    def generate_name(self):
        """Generate a culturally appropriate name"""
        names_db = self.NAMES_DB[self.culture]
        
        first = random.choice(names_db['first'])
        # Handle cultures without middle names
        middle = '' if not names_db['middle'] else random.choice(names_db['middle'])
        last = random.choice(names_db['last'])
        
        full_name = f"{first} {middle} {last}".replace('  ', ' ').strip()
        
        return {
            'first': first,
            'middle': middle,
            'last': last,
            'full_name': full_name
        }

    def create_email(self, name_dict):
        """Create email with more varied patterns"""
        first = name_dict['first'].lower()
        middle = name_dict['middle'].lower() if name_dict['middle'] else ''
        last = name_dict['last'].lower()
        year = random.randint(1980, 2000)
        
        email_formats = [
            f"{first}.{last}@gmail.com",
            f"{first}{last}{year}@gmail.com",
            f"{first[0]}{last}@gmail.com",
            f"{first}.{last}{random.randint(1, 999)}@gmail.com",
            f"{first}{last[0]}{year}@gmail.com"
        ]
        
        # Add middle name variants if middle name exists
        if middle:
            email_formats.extend([
                f"{first}{middle[0]}{last}@gmail.com",
                f"{first}.{middle[0]}.{last}@gmail.com"
            ])
        
        return random.choice(email_formats)

    def generate_password(self):
        """Generate a more complex password"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure minimum requirements
        password = [
            random.choice(lowercase),
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(digits),
            random.choice(special),
            random.choice(special)
        ]
        
        # Fill remaining characters
        remaining_length = self.password_length - len(password)
        all_chars = lowercase + uppercase + digits + special
        remaining = ''.join(random.choices(all_chars, k=remaining_length))
        
        password.extend(list(remaining))
        random.shuffle(password)
        
        return ''.join(password)

    def create_identity(self):
        """Generate a complete identity"""
        name = self.generate_name()
        email = self.create_email(name)
        password = self.generate_password()
        
        self.identity = {
            'name': name['full_name'],
            'first_name': name['first'],
            'middle_name': name['middle'],
            'last_name': name['last'],
            'email': email,
            'password': password,
            'culture': self.culture
        }
        
        return self.identity


    def setup_driver(self, headless=False):
        """Initialize the Chrome WebDriver with appropriate options"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        
        # Add additional options to make automation more robust
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()


    def save_account_details(self, filename='accounts.txt'):
        """Save account details to a file"""
        if not self.identity:
            raise ValueError("No identity generated yet")
            
        with open(filename, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Account created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Culture: {self.identity['culture']}\n")
            f.write(f"Name: {self.identity['name']}\n")
            f.write(f"Email: {self.identity['email']}\n")
            f.write(f"Password: {self.identity['password']}\n")
            f.write(f"{'='*50}\n")

def main():

    # Create screenshots directory
    import os
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    
    # Example usage
    try:
        generator = IdentityGenerator(culture='christian')
        generator.create_identity()
        
        # Optional recovery contact information
        recovery_email = "your_recovery_email@example.com"  # Replace with actual recovery email
        recovery_phone = "+1234567890"  # Replace with actual phone number
        
        # Attempt to create Gmail account
        success = generator.create_gmail_account(
            headless=False,  # Set to True for headless mode
            recovery_email=recovery_email,
            recovery_phone=recovery_phone
        )
        
        if success:
            generator.save_account_details()
            print("Account details saved to accounts.txt")

    except Exception as e:
        print(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    main()

# python account.py
