<div align="center"><a name="readme-top"></a>

![discord-icon-with-text]

# Hoox bot

a discord bot for downloading media, include video, audio, images and novel on multiple platforms. 
easy to use with simplified command. open source and free to use.

**English** · [繁體中文](./README.zh-TW.md) · [简体中文](./README.zh-CN.md) · [Changelog][changelog] · [Documents][github-wiki] · [Feedback][github-issues-link]

</div>

<details>
<summary><kbd>Table of contents</kbd></summary>

#### TOC

- [👋🏻 Getting Started & Join Our Community](#-getting-started--join-our-community)
- [✨ Features](#-features)
    - [`1` Downloading and Packaging](#1-downloading-and-packaging)
    - [`2` Multi-Media Type Support](#2-multi-media-type-support)
- [⚡️ Quick Start](#️-quick-start)
- [⌨️ Local Development](#️-local-development)
- [🤝 Contributing](#-contributing)
- [🛣 Roadmap](#-roadmap)
- [❤️ Sponsor](#️-sponsor)
- [🔗 More Products](#-more-products)
    - [`1` AI Diary](#1-ai-diary)
    - [`2` Prettier Mail](#2-prettier-mail)
    - [`3` Tagging Pro](#3-tagging-pro)  

####

<br/>

</details>

## 👋🏻 Getting Started & Join Our Community

hi there, welcome to discord-media-dl. this is a discord bot for downloading media, include video, audio, images and novel on multiple platforms.  

this project is now only developed by me, so if you have any idea or suggestion, please feel to open an [issue][github-issues-link] or become a [contributor](#-contributing).

> \[!IMPORTANT]
>
> **Star My Work**, You will receive all release notifications from GitHub without any delay \~ ⭐️

## ✨ Features

### `1` Downloading and Packaging

discord-media-dl lets you download media from multiple platforms through a simple discord bot command. 

while downloading a book or comic, you can choose if you want to receive packed up PDF or just the images. user will receive a ZIP file after the download is complete.

> \[!NOTE]
>
> if original data have metadata, it will automatically package into the file. 

### `2` Multi-Media Type Support

discord-media-dl supports multiple media types, including video, audio, images, and novel.


## ⚡️ Quick Start

1. clone this repository & change directory

    ``` shell
    git clone https://github.com/PhalisZequlard/discord-media-dl.git; 
    cd discord-media-dl; open .
    ```

1. set up environment

    ``` shell
    pyenv install 3.12.1 ; # if not already installed
    pyenv local 3.12.1     # sets Python version for this directory
    ```

1. create file .env in the root directory and fill in the following information

    ``` .env
    BOT_TOKEN=DISCORD_BOT_TOKEN
    APPLICATION_ID=DISCORD_APPLICATION_ID
    PUBLIC_KEY=PUBLIC_KEY
    ```

1. install dependencies & run the bot

    ``` shell
    pip install -r requirements.txt; python3 main.py
    ```

> \[!NOTE]
>
> GUI will be running on `http://localhost:10412` by default.


## ⌨️ Local Development

You can use GitHub Codespaces for online development:

[![codespaces-shield]][codespaces-link]

## 🤝 Contributing

Fork this repository, and make a pull request. please follow the commit rules when you make a commit or pull request.

## 🛣 Roadmap

- [ ] discord login support
- [ ] download media from GUI
- [ ] publish to discord bot store

## ❤️ Sponsor

Donate to support this project.  

## 🔗 More Products

### `1` AI Diary  

a diary that can write itself, chat with it!  

### `2` Prettier Mail  

VSCode extension, HTML email, using AJAX.  

### `3` Tagging Pro  

auto tagging & editing AI train images tag.  

---

<details><summary><h4>📝 License</h4></summary>

[Apache 2.0](./LICENSE) licensed.  
copyright © 2025 Phalis Zequlard

</details>

Copyright © 2025 [Zequlard][profile-link]. <br />
This project is [Apache 2.0](./LICENSE) licensed.

<!-- link group -->

[discord-icon]: media/discord-icon.svg
[discord-icon-with-text]: media/discord-icon-with-text.svg
[changelog]: https://github.com/PhalisZequlard/discord-media-dl/releases
[github-wiki]: https://github.com/PhalisZequlard/discord-media-dl/wiki
[github-issues-link]: https://github.com/PhalisZequlard/discord-media-dl/issues
[profile-link]: https://github.com/PhalisZequlard
[codespaces-link]: https://codespaces.new/PhalisZequlard/discord-media-dl
[codespaces-shield]: https://github.com/codespaces/badge.svg