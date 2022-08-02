# TUMExamAutomation
This repository provides a small helper script that simplifies and speeds up the tedious corrections of exams and provides some shortcuts for correction. 
Currently, only google chrome is provided as browser.

## Getting started
Install the requirements
```
pip install -r requirements
```

## Usage

First, set the parameters in ```correct.py```.

```
# HERE COME YOUR PERSONAL SETTINGS
USERNAME: str ="ge73vow" # TUM user name
PASSWORD: str =  # TUM password
PROBLEM: int = 5 # Your problem
SUBPROBLEMS: List[int] = [1,2, 3] # subproblems
```

Then start the script with ```python correct.py```. 
A chrome browser opens and logs you into TUM exam and routes you to the correction page.

Now filter the problems and select the first exam you want to work on. Please make sure that the exam is not locked. 
Now type in ```start``` into the command line. You can now start with the correction using the commands below. 
You can still interact with the browser.

Please make sure to double check your inputs and first exams when you start working with this script.


```s``` : saves current exam and skips to next exam  
```m <COMMENT>```: Include comment for subproblem  
```e<SUBPROBLEM_NUMBER: int>```: Change to subproblem with number <SUBPROBLEM_NUMBER>  

```<SCORE: int>```: Set score for current subproblem  
```s<Score: int>```: set score for current subproblem and save exam. 
#### IMPORTANT: Scores are in terms of positions in the checkbox. So the real score is SCORE * 0.5 or depending on the score steps in the score checkbox
```n<Score: int>```: Set score for current subproblem and move to next subproblem from list of subproblems. If already at last subproblem, current exam is saved and next exam is opened.   
```f```: Forward to next   
```p0``` : previous page  
```p1```: next page  
```c```: Close browser and program  

Press ```ENTER``` after typing the command to confirm your input.

You can also combine multiple commands in one line. Here are some examples:  
```s2 m You are missing FC layer```: Sets score, adds comments, and saves exam  
```e4 s1```: Changes to subproblem 4 and sets score to 1  
```n2 m Batch size missing```: Set score, adds comments and move to next subproblem  


