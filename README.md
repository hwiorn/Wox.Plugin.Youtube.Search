# YouTube Search Plugin for Wox 2

> [한국어](README.ko.md) | English

A Wox 2 plugin that enables you to search YouTube videos using the YouTube Data API directly from the Wox launcher.

## 🚀 Features

- **Fast YouTube video search**: Search videos using YouTube Data API v3
- **Detailed video information**:
  - Video title
  - Channel name
  - Duration (formatted as HH:MM:SS or MM:SS)
  - View count (formatted as K/M)
  - Published date
- **Multiple actions**:
  - Open video in browser
  - Copy video URL to clipboard
  - Copy video ID to clipboard
- Cross-platform support (Windows, Linux, macOS)

## 📦 Installation

1. Download the latest release:
   - Go to the [Releases page](https://github.com/hwiorn/Wox.Plugin.Youtube.Search/releases)
   - Download the latest release file

2. Extract and install:
   - Extract the downloaded file
   - Move the extracted folder to the Wox plugin directory:
     - **macOS**: `~/.wox/wox-user/plugins/`
     - **Windows**: `%APPDATA%\Wox\plugins\`
     - **Linux**: `~/.config/wox/plugins/`

3. Restart Wox

## 📋 Requirements

- **YouTube Data API Key** - Required for searching videos
  - Get your API key from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
  - Enable YouTube Data API v3 for your project

## ⚙️ Configuration

### Getting YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable YouTube Data API v3:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the API key

### Plugin Settings

1. Open Wox and type the trigger keyword (e.g., `yt`)
2. Go to plugin settings
3. Paste your YouTube Data API key in the "YouTube Data API Key" field

