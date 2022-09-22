# Tutorial

For this tutorial, we suppose you are a teaching who has given an exam, and is now comparing the exam results on different grading scales. The grades for the exams are numbers between 0-100, and you are experimenting with different cutoffs for letter grades, and different definitions of "passing" letter grades.

## Create a data map

First, we create a DataMap that represents our DataPoints:
```python
from bisect import bisect_right
from statistics import mean

def find_le(a, x, default=None):
    'Find rightmost value of `a` less than or equal to `x`'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    return default

data_map = {
    # NOTE:
    # any of these datapoints can be overwritten at "execute time"
    # as we will see below
    "exam_scores": [{"in": [], "f": lambda: [98, 73, 65, 95, 88, 58, 40, 94]}],
    "letter_grade_cutoffs": [{"in": [], "f": lambda: {90: "A", 80: "B", 70: "C", 60: "D"}}],
    "lowest_grade": [{"in": [], "f": lambda: "F"}],
    "passing_grades": [{"in": [], "f": lambda: set(["A", "B", "C", "D"])}],
    "exam_letter_grades": lambda exam_scores, letter_grade_cutoffs, lowest_grade: [
        letter_grade_cutoffs.get(find_le(sorted(letter_grade_cutoffs), grade), lowest_grade)
        for grade in exam_scores
    ],
    "exam_pass_fail_grades": lambda passing_grades, exam_letter_grades: [grade in passing_grades for grade in exam_letter_grades],
    "pct_passing": {"in": ["exam_pass_fail_grades"], "f": mean},
}
```

## Execute the datamap to find fields of interest

Now that we've declared our DataPoints, we can ask for fields from the datamap, given different values. 

### Find the percent of exams with a passing grade
To start, we will find the percent of exams with a passing grade, taking the exam scores as we first defined them in the datamap.
```python
from datajet import execute

execute(data_map, fields=['pct_passing'])

{'pct_passing': 0.75}
```
**ANSWER: 75% of our students passed the exam**, based on the default letter grade cutoffs (>90 is A, >80 is B, >70 is C, >60 is D, otherwise F), and our default passing letter grades (A,B,C,D) that we declared in our datamap.

### Find pct of exams with a passing grade with a different grading scale
Say you wanted to calculate the `pct_passing` on a different grading scale, this time with a pass/fail cutoff of 75:
```python
execute(
    data_map,
    context={
        "letter_grade_cutoffs": {75: "Pass"}, 
        "passing_grades": ["Pass"]
    }, 
    fields=["pct_passing","exam_letter_grades","exam_pass_fail_grades"]
)

{'pct_passing': 0.5}
```
#### Explanation 
In this example, the `context` field _overrides_ the default values we declared in our original datamap for `"letter_grade_cutoffs"` and `"passing_grades"`. We set `"letter_grade_cutoffs"` to `{75: "Pass"}`, which, according to the logic we originally declared in DataPoint `"exam_letter_grades"`, means that any exam with a score >=75 will be given the "letter grade" of `"Pass"`, while others will receive the "letter grade" `"F"` (derived from the default value we declared for the DataPoint `"lowest_grade"`). We also tell datajet via the `context` parameter that we accept only `"Pass"` as a "passing grade."

You can see the logic a little better if you ask for a few more fields:
```python
execute(
    data_map,
    context={
        "letter_grade_cutoffs": {75: "Pass"}, 
        "passing_grades": ["Pass"]
    }, 
    fields=["pct_passing","exam_letter_grades","exam_pass_fail_grades","exam_scores"]
)

{'exam_scores': [98, 73, 65, 95, 88, 58, 40, 94],
 'exam_letter_grades': ['Pass', 'F', 'F', 'Pass', 'Pass', 'F', 'F', 'Pass'],
 'exam_pass_fail_grades': [True, False, False, True, True, False, False, True],
 'pct_passing': 0.5}
```

### Find pct of passing exams when you only have letter grades to start

Say, you _started_ with a set of letter grades, and wanted to know the pct passing, taking either As, Bs, or Cs as "passing".
```python
execute(
    data_map,
    context={
        "exam_letter_grades": ("A"*8)+("B"*18)+("C"*14)+("D"*13)+("F"*5), 
        "passing_grades": "ABC"
    },
    fields=['pct_passing']
)

{'pct_passing': 0.6896551724137931}
```
In this case, datajet bypasses _calculating_ the `"exam_letter_grades"` from `"exam_scores"` because we gave it the letter grades as constants, and thus removed the dependency of `"exam_letter_grades"` on `"exam_scores"` that existed in our original DataMap declaration. DataJet takes the `"exam_letter_grades"` as-is from our `context`, and compares those grades with the `"passing_grades"` we also specified in the context, then uses the logic originally declared in the DataMap for `"exam_pass_fail_grades"` and `"pct_passing"` to tell us that just under 69% of the exams had passing grades.