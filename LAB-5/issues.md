# Lab 5: Static Code Analysis — Issue Log

File analyzed: `pharmacy_system.py`

## Identified Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL query built using string formatting | Security | 19–22 | The patient name is inserted directly into the SQL query, allowing specially crafted input to alter the query. | Use a parameterized SQL query with a `?` placeholder. |
| Mutable default argument | Code Quality / Bug | 24 | `batch_log=[]` creates a default list that can be shared between function calls. | Change the default to `None` and initialize a new list inside the function. |
| Overly broad exception handling in dispensing | Code Quality / Bug | 29–39 | A bare `except` hides different failures, including missing patients and missing stock, making errors difficult to diagnose. | Validate patient, stock, and quantity explicitly; catch only expected exceptions where needed. |
| File opened without a context manager during export | Code Quality | 49–52 | The file is opened and closed manually. If an error occurs before `close()`, cleanup may not happen correctly. | Use `with open(...)` to manage the file safely. |
| File opened without a context manager during stock loading | Code Quality | 54–59 | The JSON file is opened directly inside `json.load()`, and a bare `except` silently ignores all errors. | Use a context manager and handle expected file and JSON decoding errors explicitly. |
| Inadequate stock quantity validation | Logic Bug | 24–27, 35, 69–72 | Negative quantities can be added to stock, and dispensing can reduce stock below zero. | Reject non-positive stock additions and dispensing quantities; check availability before dispensing. |
| Inconsistent medicine-name and allergy comparison | Logic Bug | 32, 75 | The allergy check uses a case-sensitive substring comparison. The medicine name `ibuprofen` does not consistently match stock entry `Ibuprofen` in other operations. | Normalize medicine names and allergy values before comparing them, and use exact matching. |
| Non-standard function naming | Code Style | 61 | `printStock()` does not follow the conventional `snake_case` naming style for Python functions. | Rename it to `print_stock()` and update its call sites. |
| Unused import | Code Quality | 3 | The `os` module is imported but not used in the program. | Remove the unused import. |



