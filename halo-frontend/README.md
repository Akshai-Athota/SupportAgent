# Halo — AI Support Chat (Frontend)

Production-ready React frontend for the FastAPI **support-agent** backend.
Friendly, warm UI with violet accents. Built with **Vite + React 18** and CSS Modules.

## Features

- **Auth** — sign up / log in against `/signup` and `/login`; JWT stored in `localStorage`.
- **Streaming chat** — live token streaming via `/chat/stream` (SSE), with a header toggle to fall back to the buffered `/chat` endpoint.
- **Conversations** — sidebar list (`/conversation/`), create-on-first-message, delete (`/conversation/{id}`).
- **Agent activity** — the agent's `tools_used` are surfaced as friendly chips ("Looked up order status", "Escalated to a human agent", …).
- **Account** — profile popover with the signed-in email + customer id, and logout.
- **History** — messages are cached locally per conversation (the API has no "get messages" endpoint), so history restores on reload.

## Getting started

```bash
npm install
cp .env.example .env     # set VITE_API_BASE_URL if your backend URL differs
npm run dev              # http://localhost:8080
```

Build for production:

```bash
npm run build            # outputs to dist/
npm run preview
```

## Configuration

| Env var             | Description                                  |
| ------------------- | -------------------------------------------- |
| `VITE_API_BASE_URL` | Base URL of the support-agent API (no trailing slash). |

## ⚠️ Backend CORS — required change

The browser will block requests unless the backend allows this app's origin.
In the backend `app/main.py`, the `origins` list currently only contains
`localhost`. Add your dev and deployed origins:

```python
origins = [
    "http://localhost:8080",          # vite dev server
    "https://your-frontend.example",  # deployed site
]
```

Until the frontend origin is allowed, login/chat calls fail with a network error.

## API contract used

| Method & path                         | Auth   | Notes                                            |
| ------------------------------------- | ------ | ------------------------------------------------ |
| `POST /signup`                        | —      | `{ first_name, last_name, email, password, phone_number? }` → `{ access_token }` |
| `POST /login`                         | —      | `{ email, password }` → `{ access_token }`       |
| `POST /chat?conversation_id=`         | Bearer | `{ query }` → `{ response, tools_used, conversation_id }` |
| `POST /chat/stream?conversation_id=`  | Bearer | SSE: `data: "<token>"` … `data: [DONE]`          |
| `GET /conversation/`                  | Bearer | `{ conversations: [{ conversation_id, title, updated_at }] }` |
| `POST /conversation/create?title=`    | Bearer | `{ conversation_id, title }`                     |
| `DELETE /conversation/{id}`           | Bearer | `{ deleted, conversation_id }`                   |

## Project structure

```
halo-frontend/
├─ index.html
├─ vite.config.js
├─ .env.example
└─ src/
   ├─ main.jsx                 # entry — mounts <AuthProvider><App/>
   ├─ App.jsx                  # session splash → AuthPage | ChatApp
   ├─ index.css                # design tokens, resets, keyframes
   ├─ api/                     # HTTP layer (one module per resource)
   │  ├─ client.js             #   fetch wrapper, API_BASE, ApiError
   │  ├─ auth.js               #   login / signup
   │  ├─ conversations.js      #   list / create / delete
   │  └─ chat.js               #   sendChat + streamChat (SSE parser)
   ├─ context/
   │  └─ AuthContext.jsx       # token + user + login/signup/logout
   ├─ hooks/
   │  ├─ useConversations.js   # conversation list state + sync
   │  └─ useChat.js            # messages + send/stream orchestration
   ├─ lib/                     # pure helpers
   │  ├─ jwt.js  tools.js
   │  ├─ storage.js  time.js
   └─ components/
      ├─ ui/                   # Icons, Spinner, Toast
      ├─ auth/                 # AuthPage, LoginForm, SignupForm
      └─ chat/                 # ChatApp, Sidebar, ConversationList,
                               # ChatHeader, MessageList, Message,
                               # Composer, WelcomeState, Profile
```

## How streaming works

`api/chat.js#streamChat` POSTs to `/chat/stream`, reads the `ReadableStream`,
splits on `\n\n`, JSON-parses each `data:` token, and calls `onToken` with the
accumulated text so the bubble fills in live. The stream ends on `data: [DONE]`.
Note: `tools_used` is only returned by the non-streaming `/chat` endpoint, so
tool chips appear after buffered responses.
