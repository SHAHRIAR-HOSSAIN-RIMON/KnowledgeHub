# Copilot Instructions for KnowledgeHub

## Project Overview

KnowledgeHub is a Django-based monorepo structured for modular development. Each major feature (accounts, ai_tasks, files, pages, search, workspaces, usage) is implemented as a Django app within the workspace. The main configuration and entry points are in the `knowledgehub/` directory.

## Architecture & Data Flow

- **Apps**: Each folder under the root (e.g., `accounts/`, `ai_tasks/`, etc.) is a Django app with its own models, views, admin, and migrations.
- **Core**: The `knowledgehub/` directory contains project-wide settings (`settings.py`), URL routing (`urls.py`), and WSGI/ASGI entry points.
- **Data**: Models are defined per app. Migrations are managed via Django's standard workflow.
- **Communication**: Apps communicate via Django's ORM and view routing. Cross-app imports are allowed but should be minimized for loose coupling.

## Developer Workflows

- **Run Server**: `python manage.py runserver`
- **Create App**: `python manage.py startapp <appname>`
- **Migrate DB**: `python manage.py makemigrations` then `python manage.py migrate`
- **Run Tests**: `python manage.py test <appname>`
- **Debug**: Use Django's built-in error pages and logging. For advanced debugging, integrate with VS Code's Python debugger.

## Conventions & Patterns

- **App Structure**: Each app follows Django's conventions: `models.py`, `views.py`, `admin.py`, `tests.py`, and `migrations/`.
- **Settings**: All global settings are in `knowledgehub/settings.py`. Environment-specific settings are not separated; update this file directly.
- **URLs**: Main routing is in `knowledgehub/urls.py`. Apps may define their own `urls.py` for modular routing.
- **Static/Media**: Not explicitly configured; add settings in `settings.py` if needed.
- **Virtual Environment**: The project uses a local venv in `knowledgehub/`. Activate with `Scripts\Activate.ps1` (Windows PowerShell).

## External Dependencies

- **Django**: Core framework.
- **djangorestframework**: For API endpoints (see `rest_framework/` in site-packages).
- **django-cors-headers**: For CORS support.
- **PyJWT**: For JWT authentication (used with `djangorestframework_simplejwt`).

## Integration Points

- **REST API**: Use DRF for API views. JWT authentication is enabled via `djangorestframework_simplejwt`.
- **CORS**: Managed via `django-cors-headers` middleware.

## Examples

- To add a new model to `accounts`, edit `accounts/models.py`, run `makemigrations`, then `migrate`.
- To expose a new API endpoint, add a view in `<app>/views.py`, update `<app>/urls.py`, and include it in `knowledgehub/urls.py`.

## Key Files & Directories

- `manage.py`: Main CLI entry point
- `knowledgehub/settings.py`: Global settings
- `knowledgehub/urls.py`: Main URL routing
- `<app>/models.py`, `<app>/views.py`: App logic
- `Lib/site-packages/`: Installed dependencies

---

For questions or unclear patterns, please provide feedback to improve these instructions.
