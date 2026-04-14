
## Credential handling with AI tools

  1. Never type credentials directly in chat — they go straight into the model's context.
  2. Use env vars by reference — safe when Claude only writes code; risky if Claude also executes commands (env, printenv, echo $VAR).
  3. Exclude sensitive files with permission settings (see https://code.claude.com/docs/en/settings#excluding-sensitive-files)
  4. Restrict bash permissions in Claude Code settings to limit what commands can auto-execute.
  5. Use MCP servers for autonomous actions — credentials live in the MCP server, Claude calls tools without seeing the values.
  6. Use wrapper scripts that inject credentials internally, so Claude only calls the script.
  7. Least-privilege credentials — scope them to only what's needed for the task.
  8. Short-lived tokens — minimize damage if a credential is exposed.
  9. Dedicated AI credentials — separate from personal/production, easy to rotate or revoke.
  10. Review before running — check AI-generated commands for anything that might print or log credential values.

  Core principle: Claude sees everything in its context window — files it reads, command output, and what you type. Keep credentials out of all three.