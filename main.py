import requests
from datetime import datetime
import os

USERNAME = "osimfavour"
TOKEN = os.environ.get("PIXELA_TOKEN")
today = datetime.now()


class Tracker:
    def __init__(self, graph_id, unit, habit) -> None:
        self.graph_id = graph_id
        self.unit = unit
        self.habit = habit
        self.pixela_endpoint = "https://pixe.la/v1/users"

        self.graph_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs"

        self.headers = {
            "X-USER-TOKEN": TOKEN
        }

    def make_commits(self):
        """Post a Pixel"""
        pixel_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs/{self.graph_id}"
        pixel_data = {
            "date": today.strftime("%Y%m%d"),
            "quantity": input(f"How many {self.unit} did you {self.habit} today? ")
        }

        response = requests.post(url=pixel_endpoint, json=pixel_data, headers=self.headers)
        if "Success" in response.text:
            print(f"{response.text}\nsuccess in commit")
        else:
            print(response.text)

    def update_today(self):
        """Update a Pixel"""
        update_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs/{self.graph_id}/{today.strftime('%Y%m%d')}"
        pixel_update = {
            "quantity": input(f"How many {self.unit} did you {self.habit} today? ")
        }

        response = requests.put(url=update_endpoint, json=pixel_update, headers=self.headers)
        if "Success" in response.text:
            print(f"{response.text}\nToday's commit updated")
        else:
            print(response.text)

    def delete_today(self):
        """Delete a Pixel"""
        delete_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs/{self.graph_id}/{today.strftime('%Y%m%d')}"

        response = requests.delete(url=delete_endpoint, headers=self.headers)
        if "Success" in response.text:
            print(f"{response.text}\nToday's commit deleted successfully")
        else:
            print(response.text)

    def update_other_day(self):
        """Update a Pixel for some other day"""
        year = int(input("Input Year: "))
        month = int(input("Input Month: "))
        day = int(input("Input Day: "))
        date_to_update = datetime(year=year, month=month, day=day)
        update_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs/{self.graph_id}/{date_to_update.strftime('%Y%m%d')}"
        pixel_update = {
            "quantity": input(f"How many {self.unit} was it? ")
        }

        response = requests.put(url=update_endpoint, json=pixel_update, headers=self.headers)
        if "Success" in response.text:
            print(f"{response.text}\nUpdated Successfully")
        else:
            print(response.text)

    def delete_other_day(self):
        """Delete a Pixel for some other day"""
        year = int(input("Input Year: "))
        month = int(input("Input Month: "))
        day = int(input("Input Day: "))
        date_to_delete = datetime(year=year, month=month, day=day)
        delete_endpoint = f"{self.pixela_endpoint}/{USERNAME}/graphs/{self.graph_id}/{date_to_delete.strftime('%Y%m%d')}"

        response = requests.delete(url=delete_endpoint, headers=self.headers)
        if "Success" in response.text:
            print(f"{response.text}\nDeleted Successfully")
        else:
            print(response.text)

    def instructions(self):
        question = input("Do you want to MAKE, UPDATE, or DELETE a commit? ")
        if "MAKE".lower() in question:
            self.make_commits()
        elif "UPDATE".lower() in question:
            update_question = input("Change for CURRENT DAY or DAY IN THE PAST? ")
            if "CURRENT".lower() in update_question:
                self.update_today()
            elif "PAST".lower() or "BEFORE".lower() in update_question:
                self.update_other_day()
        elif "DELETE".lower() in question:
            delete_question = input("Delete for CURRENT DAY or DAY IN THE PAST? ")
            if "CURRENT".lower() in delete_question:
                self.delete_today()
            elif "PAST".lower() or "BEFORE".lower() in delete_question:
                self.delete_other_day()
        else:
            print("Typo Error!")


code_tracker = Tracker("graph1", "hours", "code")
mental_dimension = Tracker("graph2", "pages", "read")
word_study = Tracker("graph3", "hours", "study")
power_shift = Tracker("graph4", "hours", "pray")

tracking_habits = True
while tracking_habits:
    question_answer = input("What Habit do you want to track?\nCODE TRACKER, MENTAL DIMENSION, WORD STUDY, POWER SHIFT\n")
    if "CODE".lower() in question_answer:
        code_tracker.instructions()
    elif "MENTAL".lower() in question_answer:
        mental_dimension.instructions()
    elif "WORD".lower() in question_answer:
        word_study.instructions()
    elif "POWER".lower() or "PRAYER".lower() in question_answer:
        power_shift.instructions()
    else:
        print("Sorry, you made a Typo!")
        tracking_habits = False
