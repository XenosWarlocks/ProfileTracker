import random
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional, Callable

class ScrapingController:
    def __init__(
        self,
        initial_range: Tuple[int, int] = (10, 20),
        second_range: Tuple[int, int] = (20, 50),
        sleep_range: Tuple[int, int] = (30, 120),  # minutes
        max_duration: Tuple[int, int] = (8, 10)    # hours
    ):
        self.initial_range = initial_range
        self.second_range = second_range
        self.sleep_range = sleep_range
        self.max_duration = max_duration
        self.start_time = None
        self.end_time = None
        
    def _get_random_sleep_time(self) -> int:
        """Returns random sleep time in seconds"""
        return random.randint(
            self.sleep_range[0] * 60,
            self.sleep_range[1] * 60
        )
    
    def _get_random_items_count(self, is_initial: bool = True) -> int:
        """Returns random number of items to scrape"""
        range_to_use = self.initial_range if is_initial else self.second_range
        return random.randint(range_to_use[0], range_to_use[1])
    
    def _should_continue(self) -> bool:
        """Check if we should continue based on max duration"""
        if not self.start_time:
            return True
        return datetime.now() < self.end_time
    
    def start(self, scraping_function: Callable[[int], None]) -> None:
        """
        Start the controlled scraping process
        
        Args:
            scraping_function: Function that takes number of items to scrape
        """
        self.start_time = datetime.now()
        duration_hours = random.randint(self.max_duration[0], self.max_duration[1])
        self.end_time = self.start_time + timedelta(hours=duration_hours)
        
        print(f"Starting scraping session. Will run for {duration_hours} hours.")
        print(f"Session will end at: {self.end_time}")
        
        while self._should_continue():
            # Alternate between initial and second range
            is_initial = random.choice([True, False])
            items_to_scrape = self._get_random_items_count(is_initial)
            
            print(f"\nScraping {items_to_scrape} items...")
            try:
                scraping_function(items_to_scrape)
            except Exception as e:
                print(f"Error during scraping: {e}")
                continue
                
            if not self._should_continue():
                break
                
            sleep_time = self._get_random_sleep_time()
            sleep_minutes = sleep_time / 60
            print(f"Going silent for {sleep_minutes:.1f} minutes...")
            time.sleep(sleep_time)
            
        print("\nScraping session completed!")
        print(f"Total duration: {datetime.now() - self.start_time}")

# Example usage
def example_usage():
    # Define your scraping function
    def my_scraper(num_items: int):
        print(f"Simulating scraping {num_items} items...")
        time.sleep(2)  # Simulate some work
        
    # Create controller with custom ranges
    controller = ScrapingController(
        initial_range=(10, 20),    # First range of items to scrape
        second_range=(20, 50),     # Second range of items to scrape
        sleep_range=(30, 120),     # Sleep time in minutes
        max_duration=(8, 10)       # Total duration in hours
    )
    
    # Start the controlled scraping
    controller.start(my_scraper)
