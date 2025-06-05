# Timed Prime Number Calculator using Multiprocessing

This Python project calculates prime numbers using multiple processes. Each process runs for a random duration between **30 to 60 seconds**, computes prime numbers starting from a given input, and passes its result to the next process using a pipe. The results are saved to individual CSV files and archived into a ZIP file automatically.

---

## Features

- Parallel prime number calculation using Python's `multiprocessing` module.
- Time-constrained execution per process (30–60 seconds).
- Forward and reverse process execution.
- Detailed logging of prime numbers and timestamps in per-process CSV files.
- Automatic ZIP archiving of all results.
- Clean removal of individual CSV files after zipping.

---

## Requirements

This project uses only Python's **standard libraries**:

- `multiprocessing`
- `zipfile`
- `time`
- `csv`
- `os`
- `random`

> Tested with **Python 3.x**

---

## How It Works

1. **User Input**:
   - Number of processes.
   - Starting number for prime calculation.

2. **Forward Processing**:
   - Each process runs for a randomly selected duration between 30–60 seconds.
   - Finds prime numbers starting from the input number.
   - Results are written to `process(<id>)_cal_prime_num.csv`.

3. **Reverse Processing**:
   - Once all forward processes are completed, they are executed in reverse order.

4. **Archiving**:
   - All CSV files are zipped into a file named like `UiT_<timestamp>_(<n>-processes)_primeNum.zip`.
   - CSV files are deleted after archiving.

---

## Sample CSV Output

Each process generates a CSV file like:

```csv
Ser Num,Time Taken(in sec),Prime Numbers Generated
1,0.12,2
2,0.34,3
3,0.56,5
4,0.78,7
5,1.01,11
...
Random Time for this Process has been 45 seconds
```

---

### Prime Number Calculation Function
The `prime` function calculates prime numbers within a random time limit (30–60 seconds) and writes the results to a CSV file. It uses a pipe to send the last computed prime number to the next process.

### Main Execution
1. **Input Handling**:
    - Number of processes.
    - Starting number for prime calculation.

2. **Forward Processing**:
    - Each process computes prime numbers and writes results to a CSV file.
    - The last prime number is passed to the next process.

3. **Reverse Processing**:
    - Processes are executed in reverse order, appending results to the same CSV files.

4. **Archiving**:
    - All CSV files are zipped into a single archive.
    - CSV files are deleted after archiving.

---

## Notes

- Ensure Python 3.x is installed.
- Run the script in a directory with write permissions.
- The ZIP file will be named with a timestamp and the number of processes used.

---

## Example Usage

```bash
$ python main.py
Number of Processes: 3
Input Number starting from which Prime Numbers are to be computed: 10
```


