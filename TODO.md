# TODO list:

+ add F.A.Q. section

+ detect ollama model name from user input

+ detect CPU and GPU company name from user input

+ add optional input fields to provide how many GB of RAM with the CPU and how many GB of GPU memory user have

+ add optional input fields to ask user the year the system was purchased and approximate price then

+ add optional input field to enter number of CPU cores

+ display collected performance stats on the main page

+ make possible to sort collected stats by different columns

+ make possible for admin to approve/reject performance records reported by users

+ make possible for admin to "trust" certain user and auto-approve all of his performance reports

+ make possible for admin to add and modify test inputs and let users copy those inputs to clipboard

+ make possible for admin to modify FAQ page via Django Admin

+ make possible for any user to view any report

+ record in the DB the date and time a result is submitted by user

+ add optional input field to provide operating system info

+ store latest user input in cookies and auto-populate cpu,gpu,ram,vram and other fields on next report

+ change favicon.ico

+ add text stating about data privacy

- add different filters to the main page to be able to select specific performance reports in the list

+ add standard text that people submit to models on the site and also "copy to clipboard" button for that

+ provide instructions to users how to learn CPU and GPU model name on different platforms

- configure fail2ban

- configure Google captcha

- add limitation on how many un-approved reports user may send

- make possible to estimated system cost

- make possible to export database to CSV file

- build command line tool similar to https://github.com/technovangelist/obm
