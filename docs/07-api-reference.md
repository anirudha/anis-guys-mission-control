# API / auth

This page documents how Mission Control’s API surface is organized and how authentication works.

For deeper backend architecture context, see:
- [Architecture](05-architecture.md)

## Base path

Evidence: `backend/app/main.py`.

- All API routes are mounted under: `/api/v1/*`

## Auth model (two callers)

Mission Control has two primary actor types:

1) **User (Clerk)** — human UI/admin
2) **Agent (`X-Agent-Token`)** — automation

### User auth (Clerk)

Evidence:
- backend: `backend/app/core/auth.py`
- config: `backend/app/core/config.py`

- Frontend calls backend using `Authorization: Bearer <token>`.
- Backend validates requests using the Clerk Backend API SDK with `CLERK_SECRET_KEY`.

### Agent auth (`X-Agent-Token`)

Evidence:
- `backend/app/core/agent_auth.py`
- agent API surface: `backend/app/api/agent.py`

- Agents authenticate with `X-Agent-Token: <token>`.
- Token is verified against the agent’s stored `agent_token_hash`.

## Route groups (modules)

Evidence: `backend/app/main.py` includes routers from `backend/app/api/*`.

| Module | Prefix (under `/api/v1`) | Purpose |
|---|---|---|
| `activity.py` | `/activity` | Activity listing and task-comment feed endpoints. |
| `agent.py` | `/agent` | Agent-scoped API routes for board operations and gateway coordination. |
| `agents.py` | `/agents` | Agent lifecycle and streaming endpoints. |
| `approvals.py` | `/boards/{board_id}/approvals` | Approval list/create/update + streaming. |
| `auth.py` | `/auth` | Auth bootstrap endpoints. |
| `board_group_memory.py` | `/board-groups/{group_id}/memory` and `/boards/{board_id}/group-memory` | Board-group memory CRUD + streaming. |
| `board_groups.py` | `/board-groups` | Board group CRUD + snapshot + heartbeat apply. |
| `board_memory.py` | `/boards/{board_id}/memory` | Board memory CRUD + streaming. |
| `board_onboarding.py` | `/boards/{board_id}/onboarding` | Onboarding flows (user+agent). |
| `boards.py` | `/boards` | Board CRUD + snapshots. |
| `gateway.py` | `/gateways` | Gateway session inspection APIs (org admin). |
| `gateways.py` | `/gateways` | Gateway CRUD + templates sync (org admin). |
| `metrics.py` | `/metrics` | Dashboard metrics. |
| `organizations.py` | `/organizations` | Org + invites/membership flows. |
| `souls_directory.py` | `/souls-directory` | Search/fetch souls directory entries. |
| `tasks.py` | `/boards/{board_id}/tasks` | Task CRUD + comments + streaming. |
| `users.py` | `/users` | User self-service profile endpoints. |

## Where authorization is enforced

Evidence: `backend/app/api/deps.py`.

Most route modules don’t “hand roll” access checks; they declare dependencies:

- `require_admin_auth` — admin user only.
- `require_admin_or_agent` — admin user OR authenticated agent.
- `get_board_for_actor_read` / `get_board_for_actor_write` — board access for user/agent.
- `require_org_member` / `require_org_admin` — org membership/admin for user callers.

## “Start here” pointers for maintainers

- Router wiring: `backend/app/main.py`
- Access dependencies: `backend/app/api/deps.py`
- User auth: `backend/app/core/auth.py`
- Agent auth: `backend/app/core/agent_auth.py`
- Agent automation surface: `backend/app/api/agent.py`
