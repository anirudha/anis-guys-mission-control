# Gateway Agent Provisioning and Check-In Troubleshooting

This guide explains how agent provisioning converges to a healthy state, and how to debug when an agent appears stuck.

## Fast Convergence Policy

Mission Control now uses a fast convergence policy for wake/check-in:

- Check-in deadline after each wake: **30 seconds**
- Maximum wake attempts without check-in: **3**
- If no check-in after the third attempt: agent is marked **offline** and provisioning escalation stops

This applies to both gateway-main and board agents.

## Expected Lifecycle

1. Mission Control provisions/updates the agent and sends wake.
2. A delayed reconcile task is queued for the check-in deadline.
3. Agent should call heartbeat quickly after startup/bootstrap.
4. If heartbeat arrives:
   - `last_seen_at` is updated
   - wake escalation state is reset (`wake_attempts=0`, check-in deadline cleared)
5. If heartbeat does not arrive by deadline:
   - reconcile re-runs lifecycle (wake again)
   - up to 3 total wake attempts
6. If still no heartbeat after 3 attempts:
   - agent status becomes `offline`
   - `last_provision_error` is set

## Startup Check-In Behavior

Templates now explicitly require immediate first-cycle check-in:

- Main agent heartbeat instructions require immediate check-in after wake/bootstrap.
- Board lead bootstrap requires heartbeat check-in before orchestration.
- Board worker bootstrap already included immediate check-in.

If a gateway still has older templates, run template sync and reprovision/wake.

## What You Should See in Logs

Healthy flow usually includes:

- `lifecycle.queue.enqueued`
- `queue.worker.success` (for lifecycle tasks)
- `lifecycle.reconcile.skip_not_stuck` (after heartbeat lands)

If agent is not checking in:

- `lifecycle.reconcile.deferred` (before deadline)
- `lifecycle.reconcile.retriggered` (retry wake)
- `lifecycle.reconcile.max_attempts_reached` (final fail-safe at attempt 3)

If you do not see lifecycle events at all, verify queue worker health first.

## Common Failure Modes

### Wake was sent, but no check-in arrived

Possible causes:

- Agent process never started or crashed during bootstrap
- Agent ignored startup instructions due to stale templates
- Heartbeat call failed (network/auth/base URL mismatch)

Actions:

1. Confirm current templates were synced to gateway.
2. Re-run provisioning/update to trigger a fresh wake.
3. Verify agent can reach Mission Control API and send heartbeat with `X-Agent-Token`.

### Agent stays provisioning/updating with no retries

Possible causes:

- Queue worker not running
- Queue/Redis mismatch between API process and worker process

Actions:

1. Verify worker process is running continuously.
2. Verify `rq_redis_url` and `rq_queue_name` are identical for API and worker.
3. Check worker logs for dequeue/handler errors.

### Agent ended offline quickly

This is expected when no check-in is received after 3 wake attempts. The system fails fast by design.

Actions:

1. Fix check-in path first (startup, network, token, API reachability).
2. Re-run provisioning/update to start a new attempt cycle.

## Operator Recovery Checklist

1. Ensure queue worker is running.
2. Sync templates for the gateway.
3. Trigger agent update/provision from Mission Control.
4. Watch logs for:
   - `lifecycle.queue.enqueued`
   - `lifecycle.reconcile.retriggered` (if needed)
   - heartbeat activity / `skip_not_stuck`
5. If still failing, capture:
   - gateway logs around bootstrap
   - worker logs around lifecycle events
   - agent `last_provision_error`, `wake_attempts`, `last_seen_at`
