# Wox 2용 YouTube 검색 플러그인

> 한국어 | [English](README.md)

Wox 런처에서 직접 YouTube Data API를 사용하여 YouTube 동영상을 검색할 수 있는 Wox 2 플러그인입니다.

## 🚀 기능

- **빠른 YouTube 동영상 검색**: YouTube Data API v3를 사용한 동영상 검색
- **상세한 동영상 정보**:
  - 동영상 제목
  - 채널 이름
  - 재생 시간 (HH:MM:SS 또는 MM:SS 형식)
  - 조회수 (K/M 형식)
  - 게시 날짜
- **다양한 작업**:
  - 브라우저에서 동영상 열기
  - 동영상 URL 클립보드에 복사
  - 동영상 ID 클립보드에 복사
- 크로스 플랫폼 지원 (Windows, Linux, macOS)

## 📦 설치

1. Wox 플러그인 디렉토리로 이동:
   - **macOS**: `~/.wox/wox-user/plugins/`
   - **Windows**: `%APPDATA%\Wox\plugins\`
   - **Linux**: `~/.config/wox/plugins/`

2. 이 저장소를 플러그인 디렉토리에 클론하거나 다운로드:
   ```bash
   cd ~/.wox/wox-user/plugins/
   git clone https://github.com/hwiorn/Wox.Plugin.Youtube.Search.git
   ```

3. Wox 재시작

## 📋 필요 사항

- **Python 3.10+**
- **YouTube Data API Key** - 동영상 검색에 필수
  - [Google Cloud Console](https://console.cloud.google.com/apis/credentials)에서 API 키 발급
  - 프로젝트에 YouTube Data API v3 활성화 필요

## ⚙️ 설정

### YouTube API 키 발급 방법

1. [Google Cloud Console](https://console.cloud.google.com/)로 이동
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. YouTube Data API v3 활성화:
   - "API 및 서비스" > "라이브러리"로 이동
   - "YouTube Data API v3" 검색
   - "사용" 클릭
4. 사용자 인증 정보 만들기:
   - "API 및 서비스" > "사용자 인증 정보"로 이동
   - "사용자 인증 정보 만들기" > "API 키" 클릭
   - API 키 복사

### 플러그인 설정

1. Wox를 열고 트리거 키워드 입력 (예: `yt`)
2. 플러그인 설정으로 이동
3. "YouTube Data API Key" 필드에 API 키 붙여넣기

