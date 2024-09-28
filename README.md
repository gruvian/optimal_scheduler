# optimalScheduler
![](https://github.com/gruvian/optimalScheduler/blob/main/logo.png) <br />
Optimal Scheduler is a simple productivity aproject developed for creating an optimal weekly schedule that maximizes productivity while prioritizing mental wellbeing.<br />
While manual entry is possible, the program is designed to automatically create a timetable that prioritizes adequate sleep, working hours, personalized study hours per day for each subject 
and time allocated for mental wellbeing. <br />
It's written in Python, uses PyQt5 for GUI and stores and reads timetable data in JSON. <br /> 
Course/task difficulty is first modeled by traditional ECTS formula, user inputted rating and previous grades earned on similar subjects to give a personalized prediction and uses a Greedy algorithm to produce a maximally productive timetable. < br/>
\text{PredictedStudyTime} $= \alpha \times*w_{ECTS}+\beta \times w_{userRating} + \gamma \times w_{previousPerfromance}$
<br /> The app tracks user inputted sleep schedule adherence, number of hours adhered to exercise regimen and subject grade after exams and adjusts later predicted study hours and recommendations to support the user's productivity. <br />
<br />
<br /> This project was created for personal use which is reflected in design choices and functionality. 
