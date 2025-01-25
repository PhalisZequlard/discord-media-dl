# Discord Bot Development Guide

<details>  

<summary><kbd>Table of contents</kbd></summary>

#### 

- [👋🏻 Topic](#the-link)

####

</details> 

<details>  

<summary><kbd>Project Structure Overview</kbd></summary>

####

```
discord-bot/
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── config.py
├── main.py
├── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── test_api/
│   └── test_cogs/
├── cogs/
│   ├── __init__.py
│   ├── dl_media/
│   │   ├── __init__.py
│   │   ├── gallery_py/
│   │   └── yt_dlp/
│   ├── moderation/
│   └── utilities/
├── utils/
│   ├── __init__.py
│   ├── queue_manager.py
│   ├── format_handler.py
│   └── status_tracker.py
└── web/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── routes.py
    │   └── models.py
    ├── static/
    │   ├── css/
    │   └── js/
    ├── templates/
    ├── config.py
    └── app.py
```

</details> 

## Core Components

core folders brief explanation

### `root/cogs`
- Purpose: Extension/plugin system
- Structure explanation
- How features are organized
...

### `root/utils`
- Common utilities shared across features
- Core functionality helpers

### `root/web`
- Flask RESTful API structure
- API endpoints purpose
- Frontend organization
...

### `root/tests`
- Testing strategy
- How to write tests for new features
...

## Adding New Features

### Branch & Commit

1. Create new branch from develop branch, named it `feature/your-feature-name`
2. Commit changes following the commit rules

### Adding Files

A same feature should be grouped together in a folder

Create new folder in `root/cogs`, named it as your feature

## Development Workflow
...