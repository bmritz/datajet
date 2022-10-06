# Tutorial

For this tutorial, we suppose you are a teacher who has given an exam, and is now comparing the exam results on different grading scales. The grades for the exams are numbers between 0-100, and you are experimenting with different cutoffs for letter grades, and different definitions of "passing" letter grades.

## Letter Grades
To start out, let's write a simple data map that defines a [resolver](./core-concepts.md#resolver) to derive `"exam_letter_grades"` from `"exam_scores"` and `"letter_grade_cutoffs"`.

```python
exam_scores = [98, 73, 65, 95, 88, 58, 40, 94]
default_letter_grade_cutoffs = {90: "A", 80: "B", 70: "C", 60: "D", 0: "F"}

data_map = {
    "exam_scores": exam_scores,
    "letter_grade_cutoffs": default_letter_grade_cutoffs,
    "exam_letter_grades": lambda exam_scores, letter_grade_cutoffs: [
        letter_grade_cutoffs[max((cut for cut in letter_grade_cutoffs if cut < score))]
        for score in exam_scores
    ]
}
```

Now we can import datajet and get the letter grades for our exam scores:
```python
import datajet
datajet.execute(data_map, fields=["exam_letter_grades"])
```
```python
# Result
# {'exam_letter_grades': ['A', 'C', 'D', 'A', 'B', 'F', 'F', 'A']}
```

Great, easy enough. Let's add a pass/fail component to the datamap now, and find how many are passing:
```python
data_map = {
    "exam_scores": exam_scores,
    "letter_grade_cutoffs": default_letter_grade_cutoffs,
    "exam_letter_grades": lambda exam_scores, letter_grade_cutoffs: [
        letter_grade_cutoffs[max((cut for cut in letter_grade_cutoffs if cut < score))]
        for score in exam_scores
    ],
    # We define passing as having a "A", "B", "C" or "D" grade
    "passing_grades": set(["A", "B", "C", "D"]),
    "exam_pass_fail_grades": lambda passing_grades, exam_letter_grades: [grade in passing_grades for grade in exam_letter_grades],
    "n_passing": {"in": ["exam_pass_fail_grades"], "f": sum},
}
```
Let's see how many students passed:
```python
datajet.execute(data_map, fields=["n_passing"])
```
```python
# Result
{'n_passing': 6}
```

Note we can also return several different fields:
```python
datajet.execute(data_map, fields=["pct_passing","exam_letter_grades","exam_pass_fail_grades"])
```
```python
# Result
{'exam_letter_grades': ['A', 'C', 'D', 'A', 'B', 'F', 'F', 'A'],
 'exam_pass_fail_grades': [True, True, True, True, True, False, False, True],
 'n_passing': 6}
```


### Overwrite DataMap at execute time
Say you wanted to calculate the `n_passing` on a different grading scale, this time with a pass/fail cutoff of 75:
```python
execute(
    data_map,
    context={
        "letter_grade_cutoffs": {75: "Pass", 0: "Fail"}, 
        "passing_grades": ["Pass"]
    }, 
    fields=["n_passing","exam_letter_grades","exam_pass_fail_grades"]
)
```
```python
# Result
{'exam_letter_grades': ['Pass', 'Fail', 'Fail', 'Pass', 'Pass', 'Fail', 'Fail', 'Pass'],
 'exam_pass_fail_grades': [True, False, False, True, True, False, False, True],
 'n_passing': 4}
```
#### Explanation 
In this example, the `context` field _overrides_ the default values we declared in our original datamap for `"letter_grade_cutoffs"` and `"passing_grades"`. We set `"letter_grade_cutoffs"` to `{75: "Pass"}`, which, according to the logic we originally declared in DataPoint `"exam_letter_grades"`, means that any exam with a score >=75 will be given the "letter grade" of `"Pass"`, while others will receive the "letter grade" `"F"` (derived from the default value we declared for the DataPoint `"lowest_grade"`). We also tell datajet via the `context` parameter that we accept only `"Pass"` as a "passing grade."

You can see the logic a little better if you ask for a few more fields:
```python
execute(
    data_map,
    context={
        "letter_grade_cutoffs": {75: "Pass", 0: "Fail"}, 
        "passing_grades": ["Pass"]
    }, 
    fields=["n_passing","exam_letter_grades","exam_pass_fail_grades","exam_scores"]
)

{'exam_scores': [98, 73, 65, 95, 88, 58, 40, 94],
 'exam_letter_grades': ['Pass', 'Fail', 'Fail', 'Pass', 'Pass', 'Fail', 'Fail', 'Pass'],
 'exam_pass_fail_grades': [True, False, False, True, True, False, False, True],
 'n_passing': 4}
```

### Find number of passing exams when you only have letter grades to start

Say, you _started_ with a set of letter grades, and wanted to know the pct passing, taking either As, Bs, or Cs as "passing".
```python
execute(
    data_map,
    context={
        "exam_letter_grades": ("A"*8)+("B"*18)+("C"*14)+("D"*13)+("F"*5), 
        "passing_grades": "ABC"
    },
    fields=['n_passing']
)

{'n_passing': 40}
```
In this case, datajet bypasses _calculating_ the `"exam_letter_grades"` from `"exam_scores"` because we gave it the letter grades as constants, and thus removed the dependency of `"exam_letter_grades"` on `"exam_scores"` that existed in our original DataMap declaration. DataJet takes the `"exam_letter_grades"` as-is from our `context`, and compares those grades with the `"passing_grades"` we also specified in the context, then uses the logic originally declared in the DataMap for `"exam_pass_fail_grades"` and `"n_passing"` to tell us that 40 of the exams had passing grades.