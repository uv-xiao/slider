---
name: hello-world
description: "Minimal demo skill that prints 'Hello, world!' and can write a hello-world.txt file. Use when the user asks for a 'hello world' skill, wants to sanity-check skill triggering, or wants a minimal example of a Codex skill with a script."
---

# Hello World

## What to do

1. Run the bundled script to print `Hello, world!`.
2. If the user asks for a file artifact, write `hello-world.txt` with `Hello, world!` in the requested directory.

## Script

- Print to stdout: `python3 .codex/skills/hello-world/scripts/hello_world.py`

