"""
FireDrones — entry point.

Examples:
    python -m firedrones.main
    python -m firedrones.main --scenario scenario_1
    python -m firedrones.main --scenario scenario_2 --headless --ticks 100 --algorithm dijkstra
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

from firedrones.simulation.simulator import Simulator
from firedrones.simulation.scenarios import SCENARIO_MAP
from firedrones.control.controller import Controller


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FireDrones multi-agent simulator")
    parser.add_argument("--headless", action="store_true", help="run without the pygame GUI")
    parser.add_argument("--ticks", type=int, default=50, help="maximum ticks for headless runs")
    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIO_MAP.keys()),
        help="predefined scenario to load",
    )
    parser.add_argument(
        "--algorithm",
        choices=("astar", "dijkstra"),
        default="astar",
        help="path planner to use",
    )
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument(
        "--no-random-fires",
        action="store_true",
        help="disable stochastic fire spawning for reproducible experiments",
    )
    parser.add_argument(
        "--spawn-at-tick",
        type=int,
        help="spawn one manual fire at this tick; useful for scenario_7",
    )
    parser.add_argument(
        "--spawn-cell",
        type=str,
        default="7,6",
        help="manual fire cell as col,row when --spawn-at-tick is used",
    )
    parser.add_argument("--export-json", type=Path, help="write final metrics to JSON")
    parser.add_argument("--export-csv", type=Path, help="write final metrics to CSV")
    return parser


def configure_controller(args: argparse.Namespace) -> Controller:
    simulator = Simulator(seed=args.seed, use_astar=args.algorithm == "astar")
    controller = Controller(simulator)
    if args.scenario:
        simulator.load_scenario(SCENARIO_MAP[args.scenario])
    simulator.use_astar = args.algorithm == "astar"
    if args.no_random_fires or args.scenario:
        simulator.fire_spawn_prob = 0.0
    return controller


def run_gui(controller: Controller) -> None:
    """Start the pygame GUI."""
    try:
        from firedrones.gui.pygame_gui import PygameGUI
        gui = PygameGUI(controller)
        gui.run()
    except RuntimeError as exc:
        print(f"[GUI] {exc}")
        print("[GUI] Falling back to headless mode (10 ticks).")
        run_headless(controller, ticks=10)


def _parse_cell(raw: str) -> tuple[int, int]:
    try:
        col, row = raw.split(",", 1)
        return int(col.strip()), int(row.strip())
    except Exception as exc:  # pragma: no cover - defensive CLI validation
        raise SystemExit("--spawn-cell must use the format col,row; example: 7,6") from exc


def run_headless(
    controller: Controller,
    ticks: int = 20,
    *,
    spawn_at_tick: int | None = None,
    spawn_cell: tuple[int, int] | None = None,
) -> dict[str, object]:
    """Run the simulation without a GUI for a fixed number of ticks."""
    print("FireDrones — Headless simulation")
    print(f"Scenario : {controller.simulator.scenario_name}")
    print(f"Planner  : {'A*' if controller.use_astar else 'Dijkstra'}")
    print(f"Max ticks: {ticks}")

    for _ in range(ticks):
        if spawn_at_tick is not None and controller.tick == spawn_at_tick:
            col, row = spawn_cell or (7, 6)
            fire = controller.simulator.spawn_fire_at(col, row)
            status = "created" if fire else "skipped"
            print(f"[tick {controller.tick}] manual fire at ({col},{row}) {status}")
        controller.step()
        if (
            controller.simulator.fires
            and not controller.simulator.active_fires()
            and (spawn_at_tick is None or controller.tick > spawn_at_tick)
        ):
            break

    m = controller.metrics.as_dict()
    m["scenario"] = controller.simulator.scenario_name
    m["algorithm"] = "astar" if controller.use_astar else "dijkstra"
    m["fires"] = [
        {
            "id": f.fire_id,
            "position": f.position,
            "priority": f.priority,
            "spawn_tick": f.spawn_tick,
            "extinguished": f.extinguished,
            "extinguish_tick": f.extinguish_tick,
            "response_time": f.response_time(),
            "assigned_drone_id": f.assigned_drone_id,
        }
        for f in controller.fires
    ]
    m["drones"] = [
        {
            "id": d.drone_id,
            "position": d.position,
            "state": d.state.name,
            "battery": round(d.battery, 1),
            "water": round(d.water, 1),
            "distance": d.total_distance,
            "collisions_avoided": d.collisions_avoided,
        }
        for d in controller.drones
    ]

    print("\n── Final metrics ──")
    for k, v in controller.metrics.as_dict().items():
        print(f"  {k:<25} {v}")
    return m


def export_metrics(metrics: dict[str, object], *, json_path: Path | None, csv_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[export] JSON: {json_path}")
    if csv_path:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        flat = {k: v for k, v in metrics.items() if k not in {"fires", "drones"}}
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
            writer.writeheader()
            writer.writerow(flat)
        print(f"[export] CSV : {csv_path}")


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    controller = configure_controller(args)

    if args.headless:
        metrics = run_headless(
            controller,
            ticks=args.ticks,
            spawn_at_tick=args.spawn_at_tick,
            spawn_cell=_parse_cell(args.spawn_cell),
        )
        export_metrics(metrics, json_path=args.export_json, csv_path=args.export_csv)
    else:
        run_gui(controller)


if __name__ == "__main__":
    main(sys.argv[1:])
