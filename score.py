students = [
    {
        'name': 'anne',
        'score': 10,
    },
    {
        'name': 'bob',
        'score': 0,
    }
]

def key_fun(student):
    return student['score']

print(list(sorted(students,key=key_fun)))
