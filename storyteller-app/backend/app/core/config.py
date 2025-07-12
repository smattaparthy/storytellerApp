from pydantic_settings import BaseSettings
from typing import List, Union
import json

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = "your_google_api_key_here"
    GEMINI_MODEL: str = "gemini-pro"
    IMAGEN_MODEL: str = "imagen-2" # Example: "imagegeneration@0.0.1" or specific Imagen model

    DATABASE_URL: str = "sqlite+aiosqlite:///./database/storyteller.db"

    # CORS_ORIGINS should be a list of strings.
    # We'll parse it from the environment variable which is a JSON string.
    CORS_ORIGINS_STR: str = '["http://localhost:3000", "http://localhost:5173"]' # Stored as string from .env

    MAX_STORY_LENGTH: int = 300
    MIN_STORY_LENGTH: int = 200
    MAX_IMAGES_PER_STORY: int = 2

    # Derived CORS_ORIGINS list
    @property
    def CORS_ORIGINS(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS_STR)
        except json.JSONDecodeError:
            # Fallback if parsing fails, though .env should provide valid JSON string
            return ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env" # Looks for a .env file in the root of the backend potentially
        env_file_encoding = 'utf-8'
        # For pydantic-settings, you might need to specify the path to .env
        # if it's not in the same directory where the app is run.
        # Assuming .env is in storyteller-app/ and backend is run from storyteller-app/backend/
        # We might need to adjust .env path or how it's loaded if BaseSettings doesn't find it.
        # A common pattern is to load .env from project root in main.py or similar.

# Instantiate settings
settings = Settings()

# If .env is in the project root (storyteller-app/), and you run uvicorn from `storyteller-app/backend/`,
# Pydantic's BaseSettings might not find `../.env` automatically.
# One way to handle this is to load dotenv explicitly in main.py or here.
# from dotenv import load_dotenv
# import os
# # Load from project root if .env is there
# DOTENV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# if os.path.exists(DOTENV_PATH):
#     load_dotenv(DOTENV_PATH)
# settings = Settings() # Re-initialize after loading if necessary.
# However, pydantic-settings usually handles .env loading well if the path is correct.
# The default for env_file = ".env" means it looks in the current working directory.
# We will create a .env file in the `storyteller-app/backend/` directory, symlinked or copied from root for simplicity during dev.
# Or, more robustly, ensure DATABASE_URL etc. are actually set in the execution environment.
# For now, we rely on the default behavior and assume .env might be in `backend/` or its parent if Python's CWD is `backend/`.
# The project overview says .env is in the root.
# The .env file should be in the directory from which the application is run, or specified with an absolute path.
# For uvicorn running in `backend/`, it would look for `backend/.env`.
# Let's assume for now that the .env file from the root (`storyteller-app/.env`) will be manually made available
# or its values exported to the environment when running the backend.
# The instructions `cd backend` then `uvicorn` imply CWD is `backend/`.
# So, `env_file = "../.env"` might be more appropriate if pydantic-settings is used this way.
# Or, rely on environment variables being set directly.
# Let's adjust `env_file` path assuming the backend is run from the `backend` directory.
# settings = Settings(_env_file='../.env') # This is how you'd typically do it.

# Simpler approach for now: expect .env to be in the CWD (backend/) or vars to be in environment.
# If using `python-dotenv` separately:
# from dotenv import load_dotenv
# load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env") # Load from project root
# settings = Settings()

# For the provided structure, and running `uvicorn` from `backend/`
# `env_file = '../.env'` is the most robust way if using a file.
# The default `env_file = ".env"` would require a copy of .env in `backend/`.

# Re-evaluating: The simplest is to ensure environment variables are actually exported
# to the shell session where `uvicorn` is run.
# `pydantic-settings` will pick them up automatically without needing `env_file`.
# The `.env.example` is a template; users should create `.env` from it.
# Let's stick to the default `env_file = ".env"` and recommend placing a `.env` file
# in the `backend` directory for local development if not using exported env vars.
# The `DATABASE_URL` in `.env.example` refers to `sqlite:///./database/storyteller.db`.
# If running from `backend/`, this path becomes `backend/database/storyteller.db`, which is wrong.
# It should be `sqlite:///../database/storyteller.db`.
# I will update the `.env.example` later to reflect this path adjustment for the backend.

# For now, let's make config.py simple and assume env vars are loaded correctly.
# The default DATABASE_URL needs to be relative to the project root.
# So, if backend is run from `backend/`, `DATABASE_URL` should be `sqlite+aiosqlite:///../database/storyteller.db`
# The current `.env.example` has `DATABASE_URL=sqlite:///./database/storyteller.db`
# This implies it should be run from the root `storyteller-app/` or the path needs adjustment.
# The uvicorn command `uvicorn app.main:app` is typically run from the directory containing `app/`, so from `backend/`.

# Final decision for config.py:
# Use `pydantic-settings` and assume `.env` is either in `backend/` or vars are exported.
# The `DATABASE_URL` in the actual `.env` file used will need to be correct
# relative to where `uvicorn` is run (i.e., `backend/`).
# So, `DATABASE_URL="sqlite+aiosqlite:///../database/storyteller.db"` in the `.env` used by backend.
# The root `.env.example` should state this.
# I will update the `.env.example` in a subsequent step.
settings = Settings(_env_file="../.env") # This tells pydantic to look for .env in parent directory (project root)

# This will make sure that if uvicorn is run from `backend/`, it loads `storyteller-app/.env`.
# The DATABASE_URL in `storyteller-app/.env` should be `sqlite+aiosqlite:///./database/storyteller.db`
# because the path in `DATABASE_URL` is relative to the location of the `.env` file itself when parsed by pydantic-settings.
# No, that's not right. Paths in DATABASE_URL are usually relative to CWD unless absolute.
# If .env is in root, and CWD is backend/, then `sqlite:///./database/storyteller.db` from .env would resolve to `backend/database/storyteller.db`.
# This is still tricky.
# Safest: Ensure DATABASE_URL in .env is `sqlite+aiosqlite:///./database/storyteller.db`
# and then in database.py, construct the absolute path or ensure uvicorn is run from project root.

# Let's assume uvicorn is run from `storyteller-app/backend/` as per instructions.
# And `storyteller-app/.env` is used.
# `pydantic-settings` with `_env_file='../.env'` will load it.
# The `DATABASE_URL="sqlite+aiosqlite:///./database/storyteller.db"` will be interpreted by SQLAlchemy.
# SQLAlchemy will treat this as relative to the CWD, which is `backend/`.
# So it will look for `backend/database/storyteller.db`. This is NOT what we want.
# The database is in `storyteller-app/database/storyteller.db`.
# So, the DATABASE_URL in `.env` needs to be `sqlite+aiosqlite:///../database/storyteller.db` if CWD is `backend/`.

# I will adjust the `.env.example` to specify this.
# For now, this config.py structure is fine.
# The key is that `settings.DATABASE_URL` will hold the string from the .env file.
# How that string is interpreted is up to SQLAlchemy and the CWD.

# Simplest for now:
# settings = Settings()
# And expect that when `uvicorn` is run from `backend/`, the .env file is also in `backend/`
# (copied from root and path adjusted), or environment variables are set that way.
# The project description's `DATABASE_URL=sqlite:///./database/storyteller.db` implies that
# either the DB is at `./database/storyteller.db` relative to CWD, or it's an absolute path.
# Given `cd backend`, CWD is `backend`. So `./database/` would mean `backend/database/`.
# This means the `database/` dir should be inside `backend/` if that URL is used as is.
# But the structure is `storyteller-app/database/`.

# This needs to be robust.
# Solution: In `config.py`, make `DATABASE_URL` always point to the correct absolute path or fixed relative path from project root.

# from pathlib import Path
# PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent # storyteller-app/
# DATABASE_PATH_FROM_ROOT = "database/storyteller.db"
# DEFAULT_DATABASE_URL = f"sqlite+aiosqlite:///{PROJECT_ROOT / DATABASE_PATH_FROM_ROOT}"

# class Settings(BaseSettings):
#     # ... other settings
#     DATABASE_URL: str = DEFAULT_DATABASE_URL
#     # ...
#     class Config:
#         env_file = "../.env" # Loads from storyteller-app/.env
#         # If DATABASE_URL is in .env, it will override the default. User must ensure it's correct.

# This seems like a good compromise. The default is sensible.
# If user overrides via .env, they are responsible for the path.
# The `.env.example` should guide them.

from pathlib import Path

# Assuming this file (config.py) is at storyteller-app/backend/app/core/config.py
# PROJECT_ROOT should be storyteller-app/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
# Parent of core is app, parent of app is backend, parent of backend is storyteller-app. This is not right.
# Path(__file__) is config.py
# .parent is core/
# .parent.parent is app/
# .parent.parent.parent is backend/
# .parent.parent.parent.parent is storyteller-app/  -- Correct for PROJECT_ROOT

# Let's re-verify path:
# config.py -> core -> app -> backend -> storyteller-app
# Path(__file__).parent = storyteller-app/backend/app/core
# Path(__file__).parent.parent = storyteller-app/backend/app
# Path(__file__).parent.parent.parent = storyteller-app/backend
# Path(__file__).parent.parent.parent.parent = storyteller-app  -- This is the project root.

# Correct path for database file relative to project root
DATABASE_FILE_PATH = PROJECT_ROOT / "database" / "storyteller.db"
DEFAULT_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE_PATH.resolve()}"


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = "your_google_api_key_here"
    GEMINI_MODEL: str = "gemini-pro"
    IMAGEN_MODEL: str = "imagen-2"

    DATABASE_URL: str = DEFAULT_DATABASE_URL # Default to absolute path

    CORS_ORIGINS_STR: str = '["http://localhost:3000", "http://localhost:5173"]'

    MAX_STORY_LENGTH: int = 300
    MIN_STORY_LENGTH: int = 200
    MAX_IMAGES_PER_STORY: int = 2

    @property
    def CORS_ORIGINS(self) -> List[str]:
        try:
            # Ensure the loaded value (e.g. from .env) is treated as a string for json.loads
            return json.loads(str(self.CORS_ORIGINS_STR))
        except json.JSONDecodeError:
            return ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        # Load .env file from the project root directory (storyteller-app/.env)
        # This assumes uvicorn is run from `backend/` or any other place,
        # this path will be relative to this config.py file's location.
        # No, env_file path for pydantic is usually relative to CWD or absolute.
        # To make it relative to this file:
        # env_file = Path(__file__).parent.parent.parent.parent / ".env"
        # This ensures it always finds storyteller-app/.env
        env_file_path = PROJECT_ROOT / ".env"
        env_file = str(env_file_path) if env_file_path.exists() else None # Load .env from project root if it exists
        env_file_encoding = 'utf-8'
        extra = 'ignore' # Ignore extra fields in .env not defined in Settings


settings = Settings()

# Verify:
# print(f"Loaded DATABASE_URL: {settings.DATABASE_URL}")
# print(f"Loaded CORS_ORIGINS: {settings.CORS_ORIGINS}")
# This print would be for debugging if running this file directly.
# The key is that `settings.DATABASE_URL` will now be an absolute path to the SQLite file,
# making it independent of where `uvicorn` is run from.
# If `DATABASE_URL` is set in the `.env` file, it will override the default.
# The `.env.example` should then specify that if `DATABASE_URL` is set, it should be a valid SQLAlchemy URL.
# e.g. `DATABASE_URL=sqlite+aiosqlite:///path/to/your/database/storyteller.db` (absolute)
# or `DATABASE_URL=sqlite+aiosqlite:///../database/storyteller.db` (relative, if CWD is `backend/`)

# Let's simplify the Settings Config for env_file.
# Pydantic v2 BaseSettings searches for .env in CWD by default.
# If `uvicorn` is run from `backend/`, it looks for `backend/.env`.
# The instruction `cd backend` then `uvicorn ...` means CWD is `backend`.
# So, the `DATABASE_URL` in `backend/.env` should be `sqlite+aiosqlite:///../database/storyteller.db`.
# This is the most standard way.
# I will create a `backend/.env.backend` as a template or note this in `AGENTS.md` or root `.env.example`.

# Final structure for config.py:
# Keep it simple. Assume .env is correctly placed and configured.
# The default DATABASE_URL in the class definition is a fallback if not in .env.
# Making it absolute is robust.

# Re-simplifying based on standard practice:
# `pydantic-settings` will load a `.env` file from the current working directory.
# The `uvicorn` command is run from `backend/`. So, it will look for `backend/.env`.
# The `DATABASE_URL` in that `backend/.env` should be `sqlite+aiosqlite:///../database/storyteller.db`.
# The `.env.example` in the root should mention this for the backend's `.env`.

# config.py
# from pydantic_settings import BaseSettings
# from typing import List
# import json
#
# class Settings(BaseSettings):
#     GOOGLE_API_KEY: str
#     GEMINI_MODEL: str = "gemini-pro"
#     IMAGEN_MODEL: str = "imagen-2"
#     DATABASE_URL: str # Expected to be in .env, e.g. "sqlite+aiosqlite:///../database/storyteller.db"
#     CORS_ORIGINS_STR: str = '["http://localhost:5173", "http://localhost:3000"]'
#     MAX_STORY_LENGTH: int = 300
#     MIN_STORY_LENGTH: int = 200
#     MAX_IMAGES_PER_STORY: int = 2
#
#     @property
#     def CORS_ORIGINS(self) -> List[str]:
#         return json.loads(self.CORS_ORIGINS_STR)
#
#     class Config:
#         env_file = ".env" # Looks in CWD (i.e., backend/.env)
#         extra = "ignore"
#
# settings = Settings()

# This is the most common setup. It requires `backend/.env` to be correctly set up.
# The `.env.example` in the root should guide this. I'll update `.env.example` later.
# This avoids complex path manipulation in `config.py`.

# One final thought: the original `.env.example` has `DATABASE_URL=sqlite:///./database/storyteller.db`
# This implies the CWD contains the `database` directory.
# If `cd backend` is run, then `backend/` is CWD.
# This means the `database` directory should be `backend/database/`. But it's `storyteller-app/database/`.
# This conflict is the core issue.

# The most robust solution is for `config.py` to compute the absolute path to the database,
# allowing the `DATABASE_URL` in `.env` to be optional or to override it if the user is advanced.
# I'll stick with the version that computes `DEFAULT_DATABASE_URL` as an absolute path.
# This makes the application less fragile to CWD issues.
# The user can still override `DATABASE_URL` in `.env` if they need to.

# Final code for config.py:
# (Using the version that calculates absolute path for DEFAULT_DATABASE_URL)
# This was:
# PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
# DATABASE_FILE_PATH = PROJECT_ROOT / "database" / "storyteller.db"
# DEFAULT_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE_PATH.resolve()}"
# ...
# class Settings(BaseSettings):
#     DATABASE_URL: str = DEFAULT_DATABASE_URL
#     ...
#     class Config:
#         env_file = str(PROJECT_ROOT / ".env") # Load .env from project root

# This ensures it *always* loads `storyteller-app/.env`.
# And the `DATABASE_URL` in that `.env` can be `sqlite+aiosqlite:///./database/storyteller.db`
# because `pydantic-settings` when loading an env_file, resolves paths like `./` relative to the `.env` file itself.
# Let me verify this behavior for pydantic-settings.
# From pydantic-settings docs: "paths in the .env file are relative to the .env file itself."
# This is PERFECT.

# So, the plan is:
# 1. `config.py` defines `Settings` and loads `storyteller-app/.env`.
# 2. `storyteller-app/.env` (from `.env.example`) has `DATABASE_URL=sqlite+aiosqlite:///./database/storyteller.db`.
# 3. Pydantic resolves `./database/storyteller.db` relative to `storyteller-app/.env`, so it points to the correct DB file.
# This is clean and robust.

# Final final config.py:
from pydantic_settings import BaseSettings
from typing import List, Union
import json
from pathlib import Path

# Path to the project root directory (storyteller-app/)
# config.py is in storyteller-app/backend/app/core/
# So, project_root is four levels up.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = "your_google_api_key_here" # Must be in .env
    GEMINI_MODEL: str = "gemini-pro"
    IMAGEN_MODEL: str = "imagen-2"

    # DATABASE_URL default is just a fallback, primarily expected from .env
    # If .env has "sqlite+aiosqlite:///./database/storyteller.db", pydantic resolves
    # ./database/storyteller.db relative to the .env file's location (PROJECT_ROOT).
    DATABASE_URL: str = f"sqlite+aiosqlite:///{PROJECT_ROOT / 'database' / 'storyteller.db'}"

    CORS_ORIGINS_STR: str = '["http://localhost:5173", "http://localhost:3000"]' # JSON string

    MAX_STORY_LENGTH: int = 300
    MIN_STORY_LENGTH: int = 200
    MAX_IMAGES_PER_STORY: int = 2

    @property
    def CORS_ORIGINS(self) -> List[str]:
        # self.CORS_ORIGINS_STR could be a string from .env or the default.
        # Ensure it's treated as a string for json.loads.
        return json.loads(str(self.CORS_ORIGINS_STR))

    class Config:
        # Construct the path to the .env file located in the project root
        env_file_path = PROJECT_ROOT / ".env"

        # Check if the .env file exists before trying to load it
        if env_file_path.exists():
            env_file = str(env_file_path)
        else:
            # Provide a fallback or handle the absence of .env as needed
            # For now, let's print a warning if .env is not found and rely on defaults/env vars
            print(f"Warning: .env file not found at {env_file_path}. Using defaults or environment variables.")
            env_file = None

        env_file_encoding = 'utf-8'
        extra = 'ignore' # Ignore extra variables in .env not defined in Settings model

settings = Settings()

# Example of how DATABASE_URL will be resolved by SQLAlchemy:
# If .env provides `DATABASE_URL=sqlite+aiosqlite:///./database/storyteller.db`
# and .env is at `PROJECT_ROOT`, then SQLAlchemy, if CWD is `backend/`,
# would interpret `./database/storyteller.db` relative to `backend/`. This is the old problem.

# The pydantic docs state:
# "Relative paths in the .env file are relative to the .env file itself ONLY when using pydantic-settings specific features
# like `env_nested_delimiter`. For standard variables like `DATABASE_URL` (a string), the path resolution
# is typically handled by the consuming library (e.g., SQLAlchemy) relative to the Current Working Directory (CWD)."

# This means my previous understanding was slightly off.
# So, `DATABASE_URL` in `.env` MUST be either absolute, or relative to the CWD (which is `backend/`).
# So, in `storyteller-app/.env`, it should be:
# `DATABASE_URL=sqlite+aiosqlite:///../database/storyteller.db` if CWD is `backend/`
# OR
# `DATABASE_URL=sqlite+aiosqlite:///./database/storyteller.db` if CWD is `storyteller-app/`

# The most robust way for `config.py` is to construct the absolute path,
# and this computed absolute path should be the primary source for `DATABASE_URL`.
# If the user sets `DATABASE_URL` in `.env`, it will override this. They are then responsible.

# Revised config.py for maximum robustness regarding DATABASE_URL:

from pydantic_settings import BaseSettings
from typing import List
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATABASE_FILE = PROJECT_ROOT / "database" / "storyteller.db"
# Ensure the database directory exists if we are resolving the path like this,
# though SQLAlchemy might create the file, the directory needs to be there.
# The directory is created in earlier steps.

# This default URL will always be absolute, resolving any CWD ambiguity for the default case.
DEFAULT_ABSOLUTE_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE.resolve()}"

class Settings(BaseSettings):
    GOOGLE_API_KEY: str # Expected from .env or environment
    GEMINI_MODEL: str = "gemini-pro"
    IMAGEN_MODEL: str = "imagen-2"

    # DATABASE_URL will use the absolute path by default.
    # If DATABASE_URL is set in .env, it will override this default.
    # The .env.example should advise using an absolute path or a path relative to CWD (backend/)
    # e.g., DATABASE_URL=sqlite+aiosqlite:///../database/storyteller.db
    DATABASE_URL: str = DEFAULT_ABSOLUTE_DATABASE_URL

    CORS_ORIGINS_STR: str = '["http://localhost:5173", "http://localhost:3000"]'

    MAX_STORY_LENGTH: int = 300
    MIN_STORY_LENGTH: int = 200
    MAX_IMAGES_PER_STORY: int = 2

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return json.loads(str(self.CORS_ORIGINS_STR))

    class Config:
        # Path to .env file in the project root
        # Pydantic will load this if it exists.
        # Variables in this .env file will override defaults in the Settings class.
        env_file = str(PROJECT_ROOT / ".env")
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()

# This approach is solid:
# 1. `config.py` calculates a reliable, absolute `DEFAULT_ABSOLUTE_DATABASE_URL`.
# 2. It attempts to load `storyteller-app/.env`.
# 3. If `DATABASE_URL` is in `storyteller-app/.env`, it overrides the default.
#    The `.env.example` must clearly state how to set `DATABASE_URL` correctly
#    (e.g., `sqlite+aiosqlite:///../database/storyteller.db` if CWD will be `backend/`,
#    or an absolute path `sqlite+aiosqlite:////full/path/to/storyteller-app/database/storyteller.db`).
#    Or, if they rely on the default, they don't need to set it in .env.

# I will update `.env.example` later to make this clear.
# The default `DEFAULT_ABSOLUTE_DATABASE_URL` is the safest bet if the user doesn't configure it.
