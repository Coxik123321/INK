from integrity.b31g import b31g_failure_pressure
import json

def validate():
    with open("test_cases.json") as f:
        tests = json.load(f)

    for test in tests:
        Pf = b31g_failure_pressure(**test["input"])
        assert Pf > test["expected"]["min_failure_pressure"], test["name"]

    print("Валидация пройдена")
