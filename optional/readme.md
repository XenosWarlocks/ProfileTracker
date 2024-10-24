### I've created a flexible `ScrapingController` class that can be easily attach to any web scraping script. 

Here's how it works:

1. Create a controller with your desired ranges:
   ```python
   controller = ScrapingController(
    initial_range=(10, 20),    # First range of items
    second_range=(20, 50),     # Second range of items
    sleep_range=(30, 120),     # Sleep time (30min to 2hrs)
    max_duration=(8, 10)       # Run time (8 to 10hrs)
    )
   ```
