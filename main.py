"""Assign modules to compatible labs using greedy search and hill climbing."""

import argparse
import csv
import time
from pathlib import Path


def read_records(filename):
    """Read the four-column input format and report errors with line numbers."""
    records = {}
    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row or all(not value.strip() for value in row):
                continue
            context = f"{filename}:{reader.line_num}"
            if len(row) != 4 or any(not value.strip() for value in row):
                raise ValueError(f"{context}: expected four non-empty columns")
            record_id, name, count, software = (value.strip() for value in row)
            if record_id in records:
                raise ValueError(f"{context}: duplicate ID {record_id!r}")
            try:
                count = int(count)
            except ValueError as exc:
                raise ValueError(
                    f"{context}: capacity/student count must be an integer"
                ) from exc
            if count < 0:
                raise ValueError(
                    f"{context}: capacity/student count cannot be negative"
                )
            records[record_id] = (name, count, software)
    if not records:
        raise ValueError(f"{filename}: no records found")
    return records


def load_labs(filename):
    return {
        lab_id: {"name": name, "capacity": capacity, "software": set(software.split())}
        for lab_id, (name, capacity, software) in read_records(filename).items()
    }


def load_modules(filename):
    return {
        module_id: {"name": name, "students": students, "software": software}
        for module_id, (name, students, software) in read_records(filename).items()
    }


def is_feasible(module_id, lab_id, modules, labs):
    module, lab = modules[module_id], labs[lab_id]
    return (
        module["students"] <= lab["capacity"] and module["software"] in lab["software"]
    )


def total_unused_seats(assignment, modules, labs):
    return sum(
        labs[lab_id]["capacity"] - modules[module_id]["students"]
        for module_id, lab_id in assignment.items()
    )


def greedy_assignment(modules, labs):
    assignment = {}
    sorted_modules = sorted(modules, key=lambda m: modules[m]["students"], reverse=True)
    for module_id in sorted_modules:
        feasible_labs = [
            lab_id for lab_id in labs if is_feasible(module_id, lab_id, modules, labs)
        ]
        if not feasible_labs:
            raise ValueError(f"No feasible lab found for {module_id}")
        assignment[module_id] = min(
            feasible_labs, key=lambda lab: labs[lab]["capacity"]
        )
    return assignment


def local_search(initial_assignment, modules, labs):
    """Accept single-module moves that reduce the total unused seats."""
    current_assignment = initial_assignment.copy()
    current_score = total_unused_seats(current_assignment, modules, labs)
    while True:
        improved = False
        for module_id in modules:
            current_lab = current_assignment[module_id]
            for lab_id in labs:
                if lab_id == current_lab or not is_feasible(
                    module_id, lab_id, modules, labs
                ):
                    continue
                # Only this module's capacity changes in a single-module move.
                new_score = (
                    current_score
                    + labs[lab_id]["capacity"]
                    - labs[current_lab]["capacity"]
                )
                if new_score < current_score:
                    current_assignment[module_id] = lab_id
                    current_score = new_score
                    improved = True
                    break
            if improved:
                break
        if not improved:
            return current_assignment


def print_solution(title, assignment, modules, labs):
    print(title)
    lab_groups = {lab_id: [] for lab_id in labs}
    for module_id, lab_id in assignment.items():
        lab_groups[lab_id].append(module_id)
    for lab_id, module_list in lab_groups.items():
        print(f"\n{lab_id} - {labs[lab_id]['name']}")
        if not module_list:
            print("  No modules assigned.")
            continue
        for module_id in module_list:
            module = modules[module_id]
            unused = labs[lab_id]["capacity"] - module["students"]
            print(f"  {module_id} ({module['name']})")
            print(f"     Students: {module['students']}")
            print(f"     Unused Seats: {unused}")
    print(f"\nTOTAL UNUSED SEATS: {total_unused_seats(assignment, modules, labs)}\n")


def main(argv=None):
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--labs", type=Path, default=base / "Labs.txt")
    parser.add_argument("--modules", type=Path, default=base / "Modules.txt")
    args = parser.parse_args(argv)
    try:
        labs = load_labs(args.labs)
        modules = load_modules(args.modules)
        start = time.perf_counter()
        greedy_solution = greedy_assignment(modules, labs)
        greedy_time = time.perf_counter() - start
        start = time.perf_counter()
        improved_solution = local_search(greedy_solution, modules, labs)
        local_time = time.perf_counter() - start
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print_solution("GREEDY SOLUTION", greedy_solution, modules, labs)
    print_solution("IMPROVED SOLUTION", improved_solution, modules, labs)
    print("Processing Times")
    print(f"Greedy Algorithm Time: {greedy_time:.6f} seconds")
    print(f"Local Search Time: {local_time:.6f} seconds")


if __name__ == "__main__":
    main()
