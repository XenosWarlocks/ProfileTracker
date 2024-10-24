import random
import time
from datetime import datetime, timedelta
from typing import Tuple, Optional
from enum import Enum
import json
import os
from pathlib import Path

class ScrapingState(Enum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"

class ScrapingSignal(Enum):
    CONTINUE = "continue"
    PAUSE = "pause"
    STOP = "stop"

class ScrapingController:
    def __init__(
        self,
        state_file: str = "scraping_state.json",
        initial_range: Tuple[int, int] = (10, 20),
        second_range: Tuple[int, int] = (20, 50),
        sleep_range: Tuple[int, int] = (30, 120),  # minutes
        max_duration: Tuple[int, int] = (8, 10)    # hours
    ):
        self.state_file = Path(state_file)
        self.initial_range = initial_range
        self.second_range = second_range
        self.sleep_range = sleep_range
        self.max_duration = max_duration
        self.start_time = None
        self.end_time = None
        self.state = ScrapingState.STOPPED
        self._initialize_state_file()

    def _initialize_state_file(self) -> None:
        """Initialize or load the state file"""
        if not self.state_file.exists():
            self._save_state({
                "state": ScrapingState.STOPPED.value,
                "next_run_time": None,
                "items_to_scrape": 0,
                "current_session_end": None
            })

    def _save_state(self, state_data: dict) -> None:
        """Save current state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f)

    def _load_state(self) -> dict:
        """Load current state from file"""
        with open(self.state_file, 'r') as f:
            return json.load(f)

    def get_next_action(self) -> dict:
        """
        Get the next action for the main script to execute.
        Returns a dictionary with instructions for the main script.
        """
        current_state = self._load_state()
        
        if current_state["state"] == ScrapingState.STOPPED.value:
            return {"action": "stop", "message": "Scraping session completed"}

        if current_state["state"] == ScrapingState.PAUSED.value:
            next_run_time = datetime.fromisoformat(current_state["next_run_time"])
            if datetime.now() >= next_run_time:
                # Time to resume scraping
                items_to_scrape = current_state["items_to_scrape"]
                self._update_running_state()
                return {
                    "action": "scrape",
                    "items": items_to_scrape,
                    "message": f"Resume scraping {items_to_scrape} items"
                }
            else:
                # Still in pause period
                return {
                    "action": "wait",
                    "next_check": next_run_time,
                    "message": f"Waiting until {next_run_time}"
                }

        return {"action": "continue", "message": "Continue current operation"}

    def _update_running_state(self) -> None:
        """Update state to running with new scraping parameters"""
        is_initial = random.choice([True, False])
        items_to_scrape = self._get_random_items_count(is_initial)
        self._save_state({
            "state": ScrapingState.RUNNING.value,
            "items_to_scrape": items_to_scrape,
            "next_run_time": None,
            "current_session_end": self.end_time.isoformat() if self.end_time else None
        })

    def _update_paused_state(self) -> None:
        """Update state to paused with next run time"""
        sleep_time = self._get_random_sleep_time()
        next_run_time = datetime.now() + timedelta(seconds=sleep_time)
        items_to_scrape = self._get_random_items_count(random.choice([True, False]))
        
        self._save_state({
            "state": ScrapingState.PAUSED.value,
            "next_run_time": next_run_time.isoformat(),
            "items_to_scrape": items_to_scrape,
            "current_session_end": self.end_time.isoformat() if self.end_time else None
        })

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

    def start_session(self) -> dict:
        """Start a new scraping session"""
        self.start_time = datetime.now()
        duration_hours = random.randint(self.max_duration[0], self.max_duration[1])
        self.end_time = self.start_time + timedelta(hours=duration_hours)
        
        self._update_running_state()
        return {
            "action": "start",
            "planned_end": self.end_time,
            "duration_hours": duration_hours
        }

    def pause_scraping(self) -> dict:
        """Signal to pause scraping and go silent"""
        self._update_paused_state()
        current_state = self._load_state()
        return {
            "action": "pause",
            "next_run_time": current_state["next_run_time"],
            "items_next_run": current_state["items_to_scrape"]
        }

    def stop_session(self) -> dict:
        """Signal to stop the scraping session"""
        self._save_state({
            "state": ScrapingState.STOPPED.value,
            "next_run_time": None,
            "items_to_scrape": 0,
            "current_session_end": None
        })
        return {"action": "stop", "message": "Scraping session stopped"}

    def should_continue(self) -> bool:
        """Check if we should continue based on max duration"""
        if not self.end_time:
            return False
        return datetime.now() < self.end_time

# Example of how to use in main.py:
def example_usage():
    # Initialize controller
    controller = ScrapingController(
        state_file="scraping_state.json",
        initial_range=(10, 20),
        second_range=(20, 50),
        sleep_range=(30, 120),
        max_duration=(8, 10)
    )
    
    # Start the session
    session_info = controller.start_session()
    print(f"Starting session until: {session_info['planned_end']}")
    
    while controller.should_continue():
        # Get next action
        action = controller.get_next_action()
        
        if action["action"] == "stop":
            print("Stopping session")
            break
            
        elif action["action"] == "wait":
            print(f"Waiting until {action['next_check']}")
            time.sleep(60)  # Check every minute
            continue
            
        elif action["action"] == "scrape":
            print(f"Scraping {action['items']} items")
            # Your scraping logic here
            
            # After scraping, pause
            pause_info = controller.pause_scraping()
            print(f"Pausing until {pause_info['next_run_time']}")
