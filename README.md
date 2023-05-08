# 183-Group-Project
The planner app would have a calendar with yearly, monthly, weekly, and daily views that users can edit in order to add in their own schedules and events. For example, users can add the time, dates, location or zoom links to their classes if they are a student. There can be options for recurring events or users can prioritize the to-do lists for each day by their importance. We would like to make this the kind of application that you would have to sign into so that users only see and edit their own tasks and events. For simplicity and feasibility, we will only make the calendar for 2023 at the moment, and perhaps add to the feature to expand to any year if we learn how to do that this quarter. 

## Main Pages Sketch
https://www.figma.com/file/jCpQ0TLeI0Rd0FI7ExIoNP/Untitled?t=xFOzC8V1wI7mfibk-1

## Data Organization 
We would need to store data about the tasks, and the order of tasks, and make sure they are in the same data table as their associated days and times. We need a data table with the following attributes: year (2023 by default), month, day, time (can be specific for things such as classes or “all day” for things like birthdays), name of event/task, and importance (can be unprioritized by default). We can link another table to specify which data is a “task” (and therefore, must have the option to be checked off) and which is an “event” (so it just has times associated with it on display).

## User Stories
A user can create an account in the planner and create their yearly, monthly, weekly, and daily schedules. For example, they could input friend and family birthdays, meetings, work deadlines, events, etc, and include links to outside info. 

Harold could log into his planner and see a visual layout of his day, showing a block of time from 9 to 5 for his job, and then a 7 to 9 block of time for dinner with his husband. He could zoom out to see he works every weekday except Friday that week, and zoom out again to see his sister’s birthday later that month.

## Implementation Plan
We will spend the first two-week period designing the layout of the calendar and making the calendar responsive to zooming in and out as well as deciding how many buttons we will need and where those should be placed on the layout. The second two-week period we will spend creating the necessary databases for our calendar. The third two-week period will be spent creating the webpage, and polishing the implementation of the calendar.
