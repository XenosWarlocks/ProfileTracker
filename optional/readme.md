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
### Key features of this version:

1. State Management:
   Uses a JSON file to maintain state between runs
   Allows other processes to check the current state
   Manages transitions between running, paused, and stopped states


4. Communication:
   Returns dictionaries with clear actions and parameters
   Can be easily integrated with async or sync code
   Maintains session timing across pauses


5. Flexibility:
   Can be imported and used by any script
   All ranges and timings are customizable
   State file location can be configured


4. Control Flow:
   Main script can check what to do next
   Handles timing of pauses and resumes
   Manages overall session duration
