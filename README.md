# Campus Lab Space Optimizer

A Python-based optimisation system that assigns university modules to computer laboratories while satisfying capacity and software constraints. The project generates an initial solution using a **Greedy Algorithm** and improves it using a **Hill Climbing Local Search** approach to minimise unused laboratory seats.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Input Files](#input-files)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Program](#running-the-program)
- [Example Output](#example-output)
- [Constraints](#constraints)
- [Objective Function](#objective-function)
- [Authors](#authors)

---

## Overview

Universities often face the challenge of assigning modules with different enrolment sizes and software requirements to a limited number of computer laboratories. Poor allocation can lead to underutilised resources or infeasible assignments.

This project solves this problem by:

- Assigning every module to a compatible laboratory.
- Ensuring all capacity constraints are satisfied.
- Ensuring software compatibility requirements are met.
- Minimising the total number of unused seats across all assignments.

The solution uses a two-stage optimisation approach:

1. **Greedy Algorithm** to generate a fast, feasible baseline solution.
2. **Hill Climbing Local Search** to iteratively improve the baseline solution where possible.

---

## Features

- Loads laboratory and module data from text files.
- Generates a feasible allocation using a Greedy Algorithm.
- Improves the allocation using Hill Climbing Local Search.
- Validates capacity and software compatibility constraints.
- Displays assignments grouped by laboratory.
- Calculates total unused seats.
- Measures execution time for both algorithms.
- Uses only Python's standard library.

---

## Algorithms

### Greedy Algorithm

The greedy algorithm creates the initial solution by:

- Sorting modules in descending order of student enrolment.
- Prioritising larger modules first.
- Selecting the smallest feasible laboratory that satisfies:
  - Capacity requirements
  - Software compatibility

This approach produces a valid solution quickly while attempting to minimise wasted laboratory space.

### Hill Climbing Local Search

The hill climbing algorithm starts with the greedy solution and attempts to improve it by:

- Exploring neighbouring solutions.
- Reassigning one module to another feasible laboratory.
- Accepting only moves that reduce the total number of unused seats.
- Repeating until no further improvements can be found.

---

## Project Structure

```text
Campus-Lab-Space-Optimiser/
│
├── main.py
├── Labs.txt
├── Modules.txt
├── README.md
└── Comp719 Semester Project – Task.pdf
```

---

## Input Files

### Labs.txt

Each laboratory should be entered in the following format:

```text
LabID,Lab Name,Capacity,Software Installed
```

Example:

```text
L1,Advanced Lab A,100,Python Java MATLAB
L2,Coding Lab B,60,Python Java
L3,Data Lab C,40,Python MATLAB
L4,Legacy Lab D,30,Java MATLAB
```

---

### Modules.txt

Each module should be entered in the following format:

```text
ModuleID,Module Name,Students,Software Needed
```

Example:

```text
M1,AI Systems,85,Python
M2,Control Systems,45,MATLAB
M3,Object Oriented,25,Java
M4,Machine Learning,55,Python
```

---

## Requirements

- Python 3.10 or newer
- No external libraries required

The project only uses the built-in Python module:

- `time`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/DarianRobert/Campus-Lab-Space-Optimiser.git
```

Navigate to the project folder:

```bash
cd Campus-Lab-Space-Optimiser
```

---

## Running the Program

Ensure the following files are in the same directory:

- `main.py`
- `Labs.txt`
- `Modules.txt`

Run the program using:

```bash
python main.py
```

---

## Example Output

```text
GREEDY SOLUTION

L1 - Advanced Lab A

M7 (Enterprise Systems)
Students: 90
Unused Seats: 10

M1 (AI Systems)
Students: 85
Unused Seats: 15

...

TOTAL UNUSED SEATS: 140

IMPROVED SOLUTION

L1 - Advanced Lab A

M7 (Enterprise Systems)
Students: 90
Unused Seats: 10

M1 (AI Systems)
Students: 85
Unused Seats: 15

...

TOTAL UNUSED SEATS: 140

Processing Times

Greedy Algorithm Time: 0.000028 seconds
Local Search Time: 0.000036 seconds
```

---

## Constraints

Capacity is checked for each module separately. Multiple modules may use the same lab; the program does not schedule time slots or check simultaneous room occupancy. Input files have no header row and each module specifies one required software name. If no compatible lab exists, the program stops with an error.

For a successful allocation:

- Every module is assigned to exactly one laboratory.
- Laboratory capacity is never exceeded.
- Required software is available in the assigned laboratory.
- All generated assignments are feasible.

---

## Objective Function

The objective of the optimisation is to minimise:

```text
Total Unused Seats = Σ (Laboratory Capacity − Module Students)
```

Lower values indicate better utilisation of available laboratory resources.

For this objective, each module is assigned independently and the greedy step already chooses its smallest feasible lab. The current single-module hill-climbing moves therefore cannot reduce the score further. Matching totals are expected for the supplied data; execution times vary by machine and run.

---

## Authors

Developed as part of a university optimisation project by:

- Arjun Ramphal
- Darian Robert
- Jerome Reddy
- Keolin Naicker
- Lokadi Naicker
- Preolan Narainsamy


[Original team repository](https://github.com/ArjunRamphal/CampusLabSpaceOptimizer) · [My portfolio](https://darianrobert.github.io/)
