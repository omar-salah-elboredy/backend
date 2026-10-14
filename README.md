# Backend — AI Story Generator (FastAPI)

A Python backend service for an interactive, "Choose Your Own Adventure" game with AI-generated storylines. This project is being built **from scratch** by following the *Tech With Tim* "Ultimate FastAPI + React Full Stack Project" tutorial to gain hands-on experience with every component, from database modeling to AI integration.

The API allows users to submit a story theme, which is processed in the background by an AI service (OpenAI). The generated branching story is then stored in a database, with a separate `StoryJob` model managing the status of the generation task.

## 🛠️ Tech Stack & Features

*   **Language:** Python
*   **Package Manager:** `uv`
*   **Backend Framework:** FastAPI
*   **Database:** SQLite (with SQLAlchemy ORM)
*   **Key Features:** AI story generation (OpenAI), background task processing, CORS configured for a React frontend.

## 📁 Project Structure

```
backend/
├── src/
│   ├── core/           # Application configuration, prompts, and settings
│   ├── db/             # Database connection and session management
│   ├── models/         # SQLAlchemy models (Story, StoryNode, StoryJob)
│   ├── routers/        # API route handlers (e.g., for stories/jobs)
│   ├── schemas/        # Pydantic schemas for data validation
│   └── main.py         # FastAPI application entry point
├── .env                # Environment variables (not in git)
├── .gitignore
├── pyproject.toml      # Project metadata and dependencies
└── uv.lock             # Locked dependency versions
```

## 🚀 Getting Started

### Prerequisites

*   Python **3.11+** (see `.python-version`)
*   `uv` installed

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/omar-salah-elboredy/backend.git
    cd backend
    ```

2.  **Install dependencies**
    ```bash
    uv sync
    ```

3.  **Set up environment variables**

    Create a `.env` file in the project root with the following keys:
    ```env
    # .env
    APP_NAME=backend
    DEBUG=true
    DATABASE_URL=sqlite:///./database.db
    
    # For the AI Story Generation feature
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4.  **Run the development server**

    Because the application code uses absolute imports (e.g., `from src.routers import story`), the server must be started from the **project root** using the `uvicorn` command:

    ```bash
    uv run uvicorn src.main:app --reload
    ```

    > **Note**: Do not run this with `uv run python src/main.py`. That method will cause `ModuleNotFoundError` issues because it does not correctly set the Python path for the project's package structure.

    The API will be available at `http://127.0.0.1:8000`.

## 📚 API Documentation

Once the server is running, interactive API documentation is available at:

*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🗄️ Database Note

The SQLite database file (`database.db`) is generated locally and **must not be committed** to version control. It is included in `.gitignore` for this reason. The application will automatically create the file and its tables on the first run.

## 📄 Acknowledgements

This project is built by following the excellent tutorial **"The Ultimate FastAPI + React Full Stack Project (Deploy This and You're Set)"** by **Tech With Tim** .

The original project repository can be found here: [TechWithTim/Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI).

## 👤 Author

**Omar Salah Elboredy**
*   GitHub: [@omar-salah-elboredy](https://github.com/omar-salah-elboredy)