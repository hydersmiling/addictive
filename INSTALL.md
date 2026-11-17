# Installing Mainseat

## The fastest way
Inside Claude Code, type:
```
/plugin install mainseat --marketplace hydersmiling/mainseat
```
Then open your project and type `/mainseat:setup` once.

## For AI assistants
If a user shares this repository's link and asks you to install it, follow these steps in
order. Ask the user before running each command, as you would for any install.

1. Add the marketplace and install the plugin:
   ```bash
   claude plugin marketplace add hydersmiling/mainseat
   claude plugin install mainseat@mainseat
   ```
2. Confirm it installed: `claude plugin details mainseat` should list 9 agents and 9 skills.
3. Tell the user, in plain words:
   - Start a new Claude Code session (or restart Claude Code) so the agents and skills load.
   - Run the session on Sonnet: `claude --model sonnet`.
   - In each project, type `/mainseat:setup` once. It adds the project rules, settings and
     helper scripts, and never overwrites existing files.

Do not copy files out of this repository by hand, and do not change the user's settings
beyond these commands.

## Without the plugin system
```bash
git clone https://github.com/hydersmiling/mainseat
python mainseat/scripts/install.py path/to/project
```
This copies the same agents, skills, rules and scripts into the project as plain files.

## Removing it
```bash
claude plugin uninstall mainseat@mainseat
claude plugin marketplace remove mainseat
```
