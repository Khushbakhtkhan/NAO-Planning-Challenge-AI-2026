"""Algorithm A: plan compatible NAO movements between mandatory positions.

Each movement must provide a name, start pose, end pose, and duration in
seconds. The planner uses only declared transitions; it does not guess whether
two movements are compatible.
"""

import heapq
import math

MAX_DURATION_SECONDS = 120.0
MIN_INTERMEDIATE_MOVEMENTS = 5

try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


def _positive_number(value, label):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError("%s must be a positive number" % label)
    if math.isnan(number) or math.isinf(number) or number <= 0:
        raise ValueError("%s must be a positive, finite number" % label)
    return number


def _validate_positions(mandatory_positions):
    if not isinstance(mandatory_positions, (list, tuple)):
        raise ValueError("mandatory_positions must be an ordered list or tuple")
    if len(mandatory_positions) < 2:
        raise ValueError("mandatory_positions must include an initial and final pose")
    for position in mandatory_positions:
        if not isinstance(position, string_types) or not position:
            raise ValueError("each mandatory position must be a non-empty string")
    if any(left == right for left, right in zip(
            mandatory_positions, mandatory_positions[1:])):
        raise ValueError("consecutive mandatory positions must be different")


def _validate_movements(movements):
    if not isinstance(movements, (list, tuple)):
        raise ValueError("movements must be a list or tuple of transition records")

    adjacency = {}
    for movement in movements:
        if not isinstance(movement, dict):
            raise ValueError("each movement must be a dictionary")
        for key in ("name", "start", "end", "duration"):
            if key not in movement:
                raise ValueError("each movement needs a %s field" % key)
        for key in ("name", "start", "end"):
            if not isinstance(movement[key], string_types) or not movement[key]:
                raise ValueError("movement %s must be a non-empty string" % key)
        duration = _positive_number(
            movement["duration"], "duration for %s" % movement["name"])
        edge = {
            "name": movement["name"],
            "start": movement["start"],
            "end": movement["end"],
            "duration": duration,
        }
        adjacency.setdefault(edge["start"], []).append(edge)

    for edges in adjacency.values():
        edges.sort(key=lambda edge: (
            edge["name"], edge["end"], edge["duration"]))
    return adjacency


def generate_sequence(mandatory_positions, movements, time_limit=120,
                      min_intermediate=5):
    """Return the fastest compatible plan meeting the global move minimum.

    ``mandatory_positions`` is an ordered pose list, including its initial and
    final pose. Each movement is a dict with ``name``, ``start``, ``end``, and
    positive ``duration`` fields. A movement is executable only when its
    ``start`` matches the current pose.

    The result includes every visited pose, the selected movement names, and
    total duration. ``intermediate_count`` counts optional movement instances
    across the whole plan, not separately between each mandatory pair.
    """
    _validate_positions(mandatory_positions)
    adjacency = _validate_movements(movements)
    time_limit = _positive_number(time_limit, "time_limit")
    if not isinstance(min_intermediate, int) or (
            min_intermediate < MIN_INTERMEDIATE_MOVEMENTS):
        raise ValueError("min_intermediate must be at least %d"
                         % MIN_INTERMEDIATE_MOVEMENTS)
    if time_limit > MAX_DURATION_SECONDS:
        raise ValueError("time_limit cannot exceed %.0f seconds"
                         % MAX_DURATION_SECONDS)

    # State: current pose, next mandatory index, optional moves used (capped).
    start_state = (mandatory_positions[0], 1, 0)
    best_time = {start_state: 0.0}
    previous = {}
    queue = [(0.0, 0, start_state)]
    serial = 0
    final_state = None

    while queue:
        elapsed, unused_serial, state = heapq.heappop(queue)
        if elapsed != best_time.get(state):
            continue
        position, next_required, move_count = state
        if (next_required == len(mandatory_positions)
                and move_count >= min_intermediate):
            final_state = state
            break
        if elapsed > time_limit:
            break

        for movement in adjacency.get(position, []):
            destination = movement["end"]
            required_index = next_required

            if (required_index < len(mandatory_positions)
                    and destination == mandatory_positions[required_index]):
                required_index += 1
            elif destination in mandatory_positions[required_index + 1:]:
                # Mandatory poses must be visited in the supplied order.
                continue

            next_count = min(min_intermediate, move_count + 1)
            next_state = (destination, required_index, next_count)
            next_time = elapsed + movement["duration"]
            if next_time > time_limit:
                continue
            if next_time >= best_time.get(next_state, float("inf")):
                continue

            best_time[next_state] = next_time
            previous[next_state] = (state, movement)
            serial += 1
            heapq.heappush(queue, (next_time, serial, next_state))

    if final_state is None:
        raise ValueError(
            "No compatible sequence meets the mandatory order, minimum of "
            "%d intermediate movements, and %.2f-second time limit"
            % (min_intermediate, time_limit))

    selected = []
    state = final_state
    while state != start_state:
        prior_state, movement = previous[state]
        selected.append((prior_state[0], movement))
        state = prior_state
    selected.reverse()

    positions = [mandatory_positions[0]]
    movement_names = []
    for unused_start, movement in selected:
        movement_names.append(movement["name"])
        positions.append(movement["end"])

    return {
        "positions": positions,
        "movements": movement_names,
        "duration_seconds": best_time[final_state],
        "intermediate_count": len(movement_names),
    }


if __name__ == "__main__":
    print("Algorithm A is ready. Call generate_sequence() with the assignment's")
    print("ordered mandatory poses and movement compatibility/duration data.")
