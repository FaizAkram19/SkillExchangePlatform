# Skill Exchange Platform — API

A REST API for a peer-to-peer skill exchange platform, where users list the
skills they can teach and the skills they want to learn, and are matched with
people whose needs mirror their own.

**Live API:** https://skillexchange-api-tg37.onrender.com
**Live app:** https://skill-exchange-frontend-eight.vercel.app
**Frontend repo:** https://github.com/FaizAkram19/SkillExchangeFrontend.git

> Hosted on a free tier that sleeps when idle — the first request after a period
> of inactivity takes around a minute.

## Stack

- Django 6.0 / Django REST Framework
- PostgreSQL
- JWT authentication (`djangorestframework-simplejwt`)
- Gunicorn + WhiteNoise
- Deployed on Render

## The matching algorithm

The core feature is mutual matching, not a browsable user directory. A user is
suggested only if the relationship runs both ways:

- they offer at least one skill the current user is seeking, **and**
- they are seeking at least one skill the current user offers

This is implemented with two `UserSkill` queries reduced to ID sets via
`values_list()`, intersected in the ORM, with the current user excluded.
Django's lazy evaluation means the intersection resolves in a single database
query rather than in Python.

![Mutual matches on the Suggestions tab](docs/suggestions.png)

## Apps

| App | Responsibility |
|---|---|
| `accounts` | Custom user model, profiles, availability, password change |
| `skills` | Skill catalogue and per-user offered/sought skills |
| `connections` | Connection requests, responses, and mutual matching |

**Profiles are created automatically.** A `post_save` signal on the user model
creates the matching `Profile` row whenever a user is created, so registration
is a single request and no code path can produce a user without a profile. The
receiver is registered against `settings.AUTH_USER_MODEL` rather than an
imported model class, and uses a `dispatch_uid` so it cannot be connected twice
if the module is imported more than once.

**Skills use a hybrid approval model.** Any authenticated user can submit a new
skill, but it is created with `is_approved=False` and only appears in the public
catalogue after admin review. This keeps the catalogue clean without blocking
users on an admin.

## Endpoints

All routes are prefixed with `/api/` and require a `Bearer` token unless noted
otherwise.

**Auth**

```
POST   /api/token/                    obtain access + refresh (public)
POST   /api/token/refresh/            refresh access token (public)
POST   /api/users/                    register (public)
```

**Profile & skills**

```
GET    /api/user/profile/             current user's profile
PUT    /api/user/profile/             update profile
POST   /api/user/change-password/     change password (old password required)
GET    /api/skills/                   approved skill catalogue
POST   /api/skills/create/            submit a skill for approval
GET    /api/userskills/               current user's offered/sought skills
POST   /api/userskills/               add a skill
DELETE /api/userskills/<pk>/          remove a skill
```

**Connections**

```
GET    /api/connections/                  accepted connections
GET    /api/connections/pending/          requests received
GET    /api/connections/pending/<pk>/     a single received request
GET    /api/connections/sent/             requests sent
GET    /api/connections/suggestions/      mutual matches
POST   /api/connections/request/          send a request
PATCH  /api/connections/<pk>/respond/     accept or reject
DELETE /api/connections/sent/<pk>/cancel/ withdraw a sent request
```

## Design decisions

**Querysets are scoped to the requesting user.** Every list, retrieve, update,
and delete view filters on `request.user` rather than exposing
`Model.objects.all()`. Because `get_object()` resolves the lookup within
`get_queryset()`, requesting another user's record returns 404 rather than
leaking data — a valid token cannot be used to read or modify someone else's
records by guessing an ID.

**Ownership is set server-side.** `perform_create()` assigns
`user=self.request.user` rather than trusting a user ID in the request body.

**Rate limiting is enabled by default** — 30 requests/hour anonymous, 200/hour
authenticated, via DRF's throttle classes.

**Password reset by email is deliberately out of scope.** The platform sends no
email, so a reset flow would mean adding SMTP configuration and token plumbing
for a feature nothing else in the system needs. Authenticated password *change*
is supported instead.

## Running locally

Requires Python 3.12+ and PostgreSQL.

```bash
git clone <repo-url>
cd SkillExchangePlatform
python -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
LOCAL_DATABASE_URL=postgres://user:password@localhost/skillexchange
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://localhost:8000`.

## Tests

```bash
python manage.py test
```

The `connections` app is covered by DRF `APITestCase` tests, including
duplicate-request rejection and the matching endpoint.

## Roadmap

- Real-time chat between connected users (Django Channels)
- Google OAuth
- Rating endpoint
- Timestamps on connection requests