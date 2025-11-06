#!/bin/bash
# Dot Shell Wrapper with single overlay

# Variable to store PID of the current overlay
overlay_pid=""

while true; do
    # Read command from user
    read -e -p "$ " cmd

    # Skip empty commands
    [[ -z "$cmd" ]] && continue

    # Execute the command
    eval "$cmd"

    # Kill previous overlay if it exists
    if [[ -n "$overlay_pid" ]]; then
        kill "$overlay_pid" 2>/dev/null
    fi

    # Launch new overlay in background and save PID
    python3 ~/dot_overlay.py &
    overlay_pid=$!
done
