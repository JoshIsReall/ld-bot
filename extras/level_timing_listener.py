# /// script
# requires-python = ">=3.12"
# dependencies = ["pynput"]
# ///

from time import perf_counter_ns

from pynput import keyboard

KEYS = {
    keyboard.Key.left: "left",
    keyboard.Key.right: "right",
    keyboard.Key.down: "down",
    keyboard.Key.up: "up",
    keyboard.Key.space: "space",
}
TAP_KEYS = {"up", "space"}

events = []
held = set()
recording = False
start_ns = 0


def on_press(key):
    global recording, start_ns
    now = perf_counter_ns()

    if key == keyboard.Key.esc:
        # Close any recorded holds so replay won't leave keys down.
        if recording:
            for name in sorted(held - TAP_KEYS):
                events.append((now, ("keyUp", name)))
        return False

    if not recording:
        if getattr(key, "char", "").lower() == "l":
            start_ns = now
            recording = True
        return

    name = KEYS.get(key)
    if name is None or name in held:
        return

    held.add(name)
    action = name if name in TAP_KEYS else ("keyDown", name)
    events.append((now, action))


def on_release(key):
    now = perf_counter_ns()
    name = KEYS.get(key)

    if not recording or name not in held:
        return

    held.remove(name)
    if name not in TAP_KEYS:
        events.append((now, ("keyUp", name)))


print("Press L to start recording; Esc to finish.")

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
) as listener:
    listener.join()

# Round absolute offsets first, then subtract, avoiding accumulated
# rounding error from rounding each interval independently.
sequence = []
previous_seconds = 0.0

for timestamp, action in events:
    elapsed_seconds = round((timestamp - start_ns) / 1_000_000_000, 3)
    delay = round(elapsed_seconds - previous_seconds, 3)
    sequence.extend([delay, action])
    previous_seconds = elapsed_seconds

print("\nactions = [")
for item in sequence:
    print(f"    {item!r},")
print("]")