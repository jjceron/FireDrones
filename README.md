# Multi-Agent Drone System Simulator for Urban Firefighting

---

## Description

FireDrones is a 2D grid-based multi-agent simulation where autonomous drones coordinate to respond to urban fires. The system models a rectangular workspace divided into square cells, featuring dynamic fire tasks, obstacle buildings, battery and water constraints, path planning with A* and Dijkstra, greedy task allocation, basic collision avoidance, and a real-time pygame visualization.

---

## Assignment Context

This project is an academic exercise in **multi-agent robotic motion planning**. It demonstrates:

1. Multi-agent path planning (A*, Dijkstra)
2. Task allocation (greedy nearest-agent assignment)
3. Basic combinatorial optimization (minimize total assignment cost)
4. Dynamic replanning (new fires appear mid-simulation)
5. Collision avoidance (wait-based strategy)
6. Battery and water resource management
7. GUI visualization with real-time metrics
8. Labeled test scenarios
9. Modular, testable code

---

## Features

- 30×20 grid workspace (configurable)
- 4 autonomous drone agents with state machines
- Fires dynamically spawn during the simulation
- A* and Dijkstra pathfinding (switchable at runtime)
- Greedy task allocator (minimize total distance)
- Priority-based task assignment (toggle with `P`)
- Wait-based collision avoidance
- Battery and water resource constraints with auto return-to-base
- Pygame GUI with sidebar metrics, path visualization, and keyboard controls
- 8 labeled predefined scenarios
- 30+ unit and scenario tests

---

## Installation

> **Prerequisites:** Python 3.11+ and an existing `.venv` virtual environment.

### Windows

```powershell
# Activate the virtual environment
.venv\Scripts\activate

# Install dependencies from requirements.txt
py -m pip install -r .\requirements.txt

# Install the project in editable mode
py -m pip install -e .
```

### Linux / macOS

```bash
# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
python -m pip install -r requirements.txt

# Install the project in editable mode
python -m pip install -e .
```

> Installing the project in editable mode allows Python to recognize the `firedrones` package inside the `src/` directory.

---

## How to Run

### Windows

```powershell
# Full GUI simulation
py -m firedrones.main

# Headless mode, without pygame window
py -m firedrones.main --headless
```

### Linux / macOS

```bash
# Full GUI simulation
python -m firedrones.main

# Headless mode, without pygame window
python -m firedrones.main --headless
```

---

## Run a Specific Scenario

Predefined scenarios can be loaded directly from the command line using `--scenario`. This is useful for recording demonstrations, reproducing test cases, and collecting metrics for the report.

### Windows

```powershell
py -m firedrones.main --scenario scenario_1
```

### Linux / macOS

```bash
python -m firedrones.main --scenario scenario_1
```

### Scenario Commands

| # | Scenario | What it demonstrates | GUI command |
|---|----------|----------------------|-------------|
| 1 | `scenario_1` | Basic navigation: one drone, one fire, no obstacles. | `py -m firedrones.main --scenario scenario_1` |
| 2 | `scenario_2` | Obstacle avoidance: the drone must detour around a wall. | `py -m firedrones.main --scenario scenario_2` |
| 3 | `scenario_3` | Multi-agent coordination: four drones serve multiple fires. | `py -m firedrones.main --scenario scenario_3` |
| 4 | `scenario_4` | Collision avoidance: drones must resolve a movement conflict. | `py -m firedrones.main --scenario scenario_4` |
| 5 | `scenario_5` | Priority handling: high-priority fire should be served first. | `py -m firedrones.main --scenario scenario_5` |
| 6 | `scenario_6` | Resource constraint: low battery forces a return to base. | `py -m firedrones.main --scenario scenario_6` |
| 7 | `scenario_7` | Dynamic replanning: a new fire appears mid-simulation. | `py -m firedrones.main --scenario scenario_7` |
| 8 | `scenario_8` | Unreachable fire: obstacles block access to a task. | `py -m firedrones.main --scenario scenario_8` |

### Scenario Commands With Metrics Export

Create a folder for metric logs:

```powershell
mkdir metrics
```

Run a scenario in headless mode and export its metrics:

```powershell
py -m firedrones.main --scenario scenario_1 --headless --ticks 100 --no-random-fires --export-json metrics\scenario_1.json
```

Then inspect the exported metrics:

```powershell
Get-Content metrics\scenario_1.json
```

Main report scenarios:

```powershell
py -m firedrones.main --scenario scenario_1 --headless --ticks 100 --no-random-fires --export-json metrics\scenario_1.json
py -m firedrones.main --scenario scenario_2 --headless --ticks 100 --no-random-fires --export-json metrics\scenario_2.json
py -m firedrones.main --scenario scenario_3 --headless --ticks 100 --no-random-fires --export-json metrics\scenario_3.json
py -m firedrones.main --scenario scenario_4 --headless --ticks 100 --no-random-fires --export-json metrics\scenario_4.json
py -m firedrones.main --scenario scenario_7 --headless --ticks 100 --no-random-fires --spawn-at-tick 10 --spawn-cell 7,6 --export-json metrics\scenario_7.json
```

View exported logs:

```powershell
Get-Content metrics\scenario_1.json
Get-Content metrics\scenario_2.json
Get-Content metrics\scenario_3.json
Get-Content metrics\scenario_4.json
Get-Content metrics\scenario_7.json
```

### Comparing A* and Dijkstra

```powershell
# Run scenario 2 with A*
py -m firedrones.main --scenario scenario_2 --algorithm astar --headless --ticks 100 --no-random-fires --export-json metrics\scenario_2_astar.json

# Run scenario 2 with Dijkstra
py -m firedrones.main --scenario scenario_2 --algorithm dijkstra --headless --ticks 100 --no-random-fires --export-json metrics\scenario_2_dijkstra.json

# View both metric logs
Get-Content metrics\scenario_2_astar.json
Get-Content metrics\scenario_2_dijkstra.json
```

---

## How to Run Tests

### Windows

```powershell
py -m pytest

# Or with verbose output
py -m pytest -v
```

### Linux / macOS

```bash
python -m pytest

# Or with verbose output
python -m pytest -v
```

Tests do not require pygame. They run entirely headlessly.

---

## Keyboard Controls

| Key      | Action                              |
|----------|-------------------------------------|
| `Space`  | Pause / Resume                      |
| `R`      | Reset simulation                    |
| `F`      | Manually spawn a fire               |
| `O`      | Move a random obstacle              |
| `P`      | Toggle task priority mode           |
| `D`      | Toggle A* / Dijkstra                |
| `1`-`8`  | Load predefined scenario            |
| `LClick` | Spawn fire at clicked cell          |
| `Esc`    | Quit                                |

---

## Project Structure

```text
FireDrones/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── firedrones/
│       ├── __init__.py
│       ├── main.py            ← entry point
│       ├── config.py          ← all constants
│       ├── environment/
│       │   ├── cell.py        ← Cell, CellType
│       │   ├── grid.py        ← Grid
│       │   ├── region.py      ← Region
│       │   └── fire.py        ← Fire task
│       ├── agents/
│       │   ├── drone.py       ← Drone agent
│       │   └── drone_state.py ← DroneState enum
│       ├── planning/
│       │   ├── astar.py       ← A* planner
│       │   ├── dijkstra.py    ← Dijkstra planner
│       │   ├── task_allocator.py
│       │   └── collision_avoidance.py
│       ├── control/
│       │   └── controller.py  ← GUI and simulator mediator
│       ├── simulation/
│       │   ├── simulator.py   ← core simulation engine
│       │   ├── metrics.py     ← performance indicators
│       │   └── scenarios.py   ← 8 predefined scenarios
│       ├── gui/
│       │   └── pygame_gui.py  ← rendering and input
│       └── utils/
│           └── priority_queue.py
└── tests/
    ├── conftest.py
    ├── test_astar.py
    ├── test_dijkstra.py
    ├── test_grid.py
    ├── test_task_allocator.py
    ├── test_collision_avoidance.py
    └── test_scenarios.py
```

---

## Algorithms

### A* Pathfinding

A* is a best-first search algorithm that uses a heuristic $h(n)$ to guide exploration toward the goal. For 4-connected grids with uniform movement cost 1, Manhattan distance is an admissible and consistent heuristic:

$$f(n) = g(n) + h(n)$$

$$h(n) = |col_n - col_{goal}| + |row_n - row_{goal}|$$

A* expands fewer nodes than uninformed search on typical grid problems, making it the default planner.

### Dijkstra

Dijkstra is Uniform Cost Search with no heuristic, equivalent to using $h(n) = 0$. It expands cells in non-decreasing distance order from the start and guarantees an optimal path on uniform-cost grids.

On the same grid, Dijkstra and A* produce paths of identical length, but Dijkstra usually visits more cells, making it slower.

**Why not RRT?** Rapidly-exploring Random Trees are designed for continuous configuration spaces. On a discrete grid, exhaustive search with a heuristic, such as A*, is more appropriate and efficient.

**Why not CBS?** Conflict-Based Search solves the full Multi-Agent Path Finding problem optimally, but it has high computational complexity. It is outside the scope of this academic project.

---

## Task Allocation

The simulator uses greedy nearest-agent assignment:

1. Collect all active and unassigned fires.
2. Sort fires by priority if priority mode is enabled.
3. For each fire, assign the nearest available drone.
4. Estimate cost using Manhattan distance or planned path length.

---

## Priority Handling

When priority mode is active, fires are sorted by ascending `priority` value, where `0` represents the most urgent fire.

The allocator attempts to assign the most urgent fire first. If a high-priority fire is unreachable, the system skips it safely and continues operating.

---

## Collision Avoidance

Before each movement tick:

1. Each drone proposes its next cell.
2. If two drones try to occupy the same cell, one drone waits.
3. If two drones try to swap positions directly, one drone waits.
4. The drone with the higher ID waits.

This is a simple wait-based strategy, not a full optimal MAPF solver.

---

## Dynamic Replanning

When a new fire appears or the environment changes, drone paths may become outdated. At each simulation tick, drones with invalid or empty paths automatically replan using the current grid state.

---

## Battery and Water Constraints

| Parameter             | Value     |
|-----------------------|-----------|
| Battery per move      | 1         |
| Water per extinguish  | 25        |
| Low battery threshold | 25        |
| Low water threshold   | 25        |
| Recharge rate         | 10 / tick |
| Refill rate           | 10 / tick |

When battery or water drops below the threshold, the drone abandons its current task, returns to base, and recharges or refills before accepting new assignments.

---

## Optimization Formulation

### No-Priority Mode

The objective is to minimize total assignment cost:

$$J = \sum \text{distance}(drone_i, fire_j)$$

where:

- `drone_i` is an available drone agent.
- `fire_j` is an active fire task.
- `distance` is Manhattan distance, A* path length, or travel time.
- The assignment should reduce the total cost of serving all fires.

The greedy algorithm approximates the optimal assignment by assigning each fire to the nearest available drone.

### Priority Mode

Tasks should be completed in strict ascending priority order whenever possible:

```text
priority(fire_a) < priority(fire_b)
→ fire_a should be completed before fire_b
```

If a higher-priority fire is unreachable due to obstacles, the system detects this and continues safely.

---

## Labeled Test Scenarios

| # | Name | Description | GUI command |
|---|------|-------------|-------------|
| 1 | `scenario_1` | Single drone, single fire, no obstacles | `py -m firedrones.main --scenario scenario_1` |
| 2 | `scenario_2` | Single drone, wall of obstacles, drone must detour | `py -m firedrones.main --scenario scenario_2` |
| 3 | `scenario_3` | 4 drones, 5 fires, greedy nearest-task allocation | `py -m firedrones.main --scenario scenario_3` |
| 4 | `scenario_4` | 2 drones on collision course, avoidance triggered | `py -m firedrones.main --scenario scenario_4` |
| 5 | `scenario_5` | Priority mode: high-priority fire served before low-priority | `py -m firedrones.main --scenario scenario_5` |
| 6 | `scenario_6` | Low battery, drone returns to base mid-mission | `py -m firedrones.main --scenario scenario_6` |
| 7 | `scenario_7` | New fire spawns mid-simulation, drone replans | `py -m firedrones.main --scenario scenario_7` |
| 8 | `scenario_8` | Fire surrounded by obstacles, system detects unreachability | `py -m firedrones.main --scenario scenario_8` |

---

## Suggested Recording Order

For a concise demonstration video, run the following scenarios:

```powershell
py -m firedrones.main --scenario scenario_1
py -m firedrones.main --scenario scenario_2
py -m firedrones.main --scenario scenario_3
py -m firedrones.main --scenario scenario_4
py -m firedrones.main --scenario scenario_7
```

These match the main report cases: basic navigation, obstacles, multi-agent coordination, collision avoidance, and dynamic replanning.

---

## Limitations

- Collision avoidance is wait-based.
- Task allocation is greedy and not globally optimal.
- No advanced MAPF solver is implemented.
- No multi-fire triage is included.
- One drone is assigned to one fire at a time.
- Grid movement is 4-connected, so diagonal movement is not supported.
- Pygame visualization requires a display. Use `--headless` when running without GUI support.

---

## Future Improvements

- Replace greedy allocation with the Hungarian algorithm.
- Implement Conflict-Based Search for optimal multi-agent path planning.
- Add drone-to-drone communication.
- Support diagonal movement with 8-connected grids.
- Add fire intensity and progressive extinguishing.
- Add real-time scenario loading through the GUI.
- Export simulation logs for offline analysis.
- Add multiple base coordination.

---

## Real-World Applications

- **Emergency drones:** Coordinate UAV fleets for wildfire or urban fire suppression.
- **Warehouse robots:** Route multiple robots to pick locations while avoiding collisions.
- **Autonomous vehicles:** Coordinate multiple vehicles in grid-like traffic environments.
- **Search and rescue:** Assign drones to emergency locations with priority triage.
