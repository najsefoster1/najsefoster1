from icalendar import Calendar, Event
from datetime import datetime, timedelta

# Define the start date for the schedule (Monday of the current week)
start_date = datetime(2024, 10, 21, 11, 0)

# Create a calendar
cal = Calendar()

#Job application, gym, homework, and cleaning times between 11 am and 4 pm
time_slots = [
    ("Job Application", timedelta(hours=1)),
    ("Gym", timedelta(hours=1), "Workout focusing on losing weight and getting a bigger butt"),
    ("Homework", timedelta(hours=1)),
]

#Cleaning outside of 11 am and 4 pm and water reminders
other_tasks = [
    ("Clean the house", timedelta(hours=1)),
    ("Clean the cars", timedelta(hours=1), "On Monday"),
    ("Drink water reminder", timedelta(minutes=0), "Remember to drink plenty of water!")
]

#Create events for Monday-Friday between 11 am and 4 pm for the tasks
for i in range(5):  # For Monday to Friday
    day = start_date + timedelta(days=i)
    event_start = day
    
    #Schedule Job Application, Gym, and Homework between 11-4
    for task in time_slots:
        event = Event()
        event.add('summary', task[0])
        event.add('dtstart', event_start)
        event.add('dtend', event_start + task[1])
        if len(task) > 2:
            event.add('description', task[2])
        cal.add_component(event)
        event_start += task[1]
    
    #Cleaning tasks, distributed for Monday (cleaning cars) and the house (each day)
    event = Event()
    event.add('summary', other_tasks[0][0] if i != 0 else other_tasks[1][0])
    event.add('dtstart', datetime(2024, 10, 21 + i, 9, 0))  # Cleaning outside of 11-4 pm
    event.add('dtend', datetime(2024, 10, 21 + i, 10, 0))
    if i == 0:
        event.add('description', other_tasks[1][2])  # Clean the cars on Monday
    cal.add_component(event)

#Water reminders (throughout each day)
for i in range(5):
    for hour in range(8, 18, 2):  # Water reminders every 2 hours between 8 am and 6 pm
        event = Event()
        event.add('summary', other_tasks[2][0])
        event.add('dtstart', datetime(2024, 10, 21 + i, hour, 0))
        event.add('dtend', datetime(2024, 10, 21 + i, hour, 5))
        event.add('description', other_tasks[2][2])
        cal.add_component(event)

# Save the ICS file
with open("Najse_week_schedule_updated.ics", "wb") as f:
    f.write(cal.to_ical())
