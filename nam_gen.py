
from datetime import datetime
import string
import random
class UsernameGenerator:

    def __init__(self):
        self.used_patterns = set()

    def generate_random_string(self, length=3):
        """Generate a random string of letters and numbers"""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def get_year_variations(self):
        """Generate different year-related numbers"""
        current_year = datetime.now().year
        return [
            str(current_year)[-2:],
            str(random.randint(1980, current_year))[-2:],
            str(random.randint(1980, current_year)),
            str(random.randint(1, 999)).zfill(3),
            str(random.randint(1, 99)).zfill(2),
        ]
    
    def create_username_variations(self, first, middle, last):
        """Create a large pool of username variations"""
        variations = []
        
        # Clean and prepare names
        first = first.lower().replace(' ', '').replace('-', '')
        middle = middle.lower().replace(' ', '').replace('-', '') if middle else ''
        last = last.lower().replace(' ', '').replace('-', '')
        
        # Get initials
        first_initial = first[0] if first else ''
        middle_initial = middle[0] if middle else ''
        last_initial = last[0] if last else ''
        
        # Basic patterns
        patterns = [
            f"{first}{last}",
            f"{first}.{last}",
            f"{last}{first}",
            f"{first_initial}{last}",
            f"{first}{last_initial}",
            f"{first_initial}{middle_initial}{last}",
            f"{first}{middle_initial}{last}",
        ]
        
        if middle:
            patterns.extend([
                f"{first}{middle}{last}",
                f"{first}.{middle}.{last}",
                f"{first}{middle_initial}{last}",
            ])
        
        # Generate variations
        year_variations = self.get_year_variations()
        random_strings = [self.generate_random_string() for _ in range(5)]
        
        for pattern in patterns:
            variations.append(pattern)
            
            for year in year_variations:
                variations.extend([
                    f"{pattern}{year}",
                    f"{year}{pattern}",
                ])
            
            for rand_str in random_strings:
                variations.extend([
                    f"{pattern}{rand_str}",
                    f"{rand_str}{pattern}",
                ])
            
            variations.extend([
                f"{pattern}_{self.generate_random_string()}",
                f"{pattern}.{self.generate_random_string()}",
            ])
        
        # Add random variations
        for _ in range(5):
            rand_str = self.generate_random_string(random.randint(2, 4))
            variations.extend([
                f"{first}{rand_str}{last}",
                f"{first_initial}{rand_str}{last}",
                f"{first}{rand_str}{last_initial}",
            ])
        
        random.shuffle(variations)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_variations = []
        for v in variations:
            if v not in seen:
                seen.add(v)
                unique_variations.append(v)
        
        return unique_variations
