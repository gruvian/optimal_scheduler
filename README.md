# optimalScheduler
![](https://github.com/gruvian/optimalScheduler/blob/main/logo.png)
Optimal Scheduler is a simple productivity app developed as a personal project for creating an optimal weekly schedule that maximizes productivity while prioritizing mental wellbeing. 
While manual entry is possible, the app is designed to automatically create a timetable that prioritizes adequate sleep, working hours, personalized study hours per day for each subject 
and time allocated for mental wellbeing.   
It's written in Python, uses PyQt5 for GUI, stores and reads timetable data in JSON, models course/task difficulty at first by traditional ECTS formula, user inputted rating and previous grades earned
on similar subjects to give a personalized prediction and uses a Greedy algorithm to produce a maximally productive timetable. The app tracks user inputted sleep schedule adherence, number of
hours adhered to exercise regimen and subject grade after exams and adjusts later predicted study hours and recommendations to support the user's productivity.
