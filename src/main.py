import json
from datetime import timedelta
from typing import Dict, List, Optional

import httpx
from wox_plugin import (
    ActionContext,
    Context,
    Plugin,
    PluginInitParams,
    PublicAPI,
    Query,
    Result,
    ResultAction,
    WoxImage,
    WoxImageType,
)


class YouTubeSearchPlugin(Plugin):
    api: PublicAPI
    youtube_api_key: str
    max_results: int
    http_client: httpx.AsyncClient

    async def init(self, ctx: Context, init_params: PluginInitParams) -> None:
        self.api = init_params.api
        self.max_results = 10
        self.http_client = httpx.AsyncClient(timeout=10.0)

        # Load YouTube API key from settings
        try:
            self.youtube_api_key = await self.api.get_setting(ctx, "youtube_api_key")
        except Exception:
            self.youtube_api_key = ""

    def _parse_duration_iso8601(self, duration_str: str) -> Optional[timedelta]:
        """Parse ISO 8601 duration format (PT1H2M30S)"""
        if not duration_str or not duration_str.startswith("PT"):
            return None

        # Remove PT prefix
        duration_str = duration_str[2:]

        hours = 0
        minutes = 0
        seconds = 0

        # Parse hours
        if "H" in duration_str:
            parts = duration_str.split("H")
            hours = int(parts[0])
            duration_str = parts[1] if len(parts) > 1 else ""

        # Parse minutes
        if "M" in duration_str:
            parts = duration_str.split("M")
            minutes = int(parts[0])
            duration_str = parts[1] if len(parts) > 1 else ""

        # Parse seconds
        if "S" in duration_str:
            parts = duration_str.split("S")
            if parts[0]:
                seconds = int(parts[0])

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def _format_duration(self, duration: timedelta) -> str:
        """Format duration as human-readable string"""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

    def _format_number_human_readable(self, num: int) -> str:
        """Format large numbers in human readable format"""
        if num >= 1000000:
            return f"{num / 1000000:.1f}M".rstrip("0").rstrip(".")
        elif num >= 1000:
            return f"{num / 1000:.1f}K".rstrip("0").rstrip(".")
        else:
            return str(num)

    def _build_search_params(self, query: str, search_type: str, order: str, max_results: int) -> Dict[str, str]:
        """Build search parameters for YouTube API"""
        params = {
            "q": query,
            "part": "snippet",
            "type": search_type,
            "order": order,
            "maxResults": str(max_results),
            "key": self.youtube_api_key,
        }
        return params

    async def open_in_browser_action(self, ctx: ActionContext) -> None:
        """Open YouTube video/playlist/channel in browser"""
        data = json.loads(ctx.context_data)
        url = data.get("url", "")

        if not url:
            await self.api.notify(Context.new(), "Error: No URL found")
            return

        try:
            import subprocess
            import platform

            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.Popen(["open", url])
            elif system == "Linux":
                subprocess.Popen(["xdg-open", url])
            elif system == "Windows":
                subprocess.Popen(["start", url], shell=True)

            await self.api.notify(Context.new(), f"Opening: {url}")
        except Exception as e:
            await self.api.notify(Context.new(), f"Error opening URL: {str(e)}")

    async def copy_url_action(self, ctx: ActionContext) -> None:
        """Copy URL to clipboard"""
        data = json.loads(ctx.context_data)
        url = data.get("url", "")

        if not url:
            await self.api.notify(Context.new(), "Error: No URL found")
            return

        try:
            import subprocess
            import platform

            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["pbcopy"], input=url.encode(), check=True)
            elif system == "Linux":
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=url.encode(), check=True)
                except FileNotFoundError:
                    subprocess.run(["xsel", "--clipboard", "--input"], input=url.encode(), check=True)
            elif system == "Windows":
                subprocess.run(["clip"], input=url.encode(), check=True)

            await self.api.notify(Context.new(), "URL copied to clipboard")
        except Exception as e:
            await self.api.notify(Context.new(), f"Error copying URL: {str(e)}")

    async def copy_video_id_action(self, ctx: ActionContext) -> None:
        """Copy video ID to clipboard"""
        data = json.loads(ctx.context_data)
        video_id = data.get("video_id", "")

        if not video_id:
            await self.api.notify(Context.new(), "Error: No video ID found")
            return

        try:
            import subprocess
            import platform

            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["pbcopy"], input=video_id.encode(), check=True)
            elif system == "Linux":
                try:
                    subprocess.run(["xclip", "-selection", "clipboard"], input=video_id.encode(), check=True)
                except FileNotFoundError:
                    subprocess.run(["xsel", "--clipboard", "--input"], input=video_id.encode(), check=True)
            elif system == "Windows":
                subprocess.run(["clip"], input=video_id.encode(), check=True)

            await self.api.notify(Context.new(), f"Video ID copied to clipboard: {video_id}")
        except Exception as e:
            await self.api.notify(Context.new(), f"Error copying video ID: {str(e)}")

    async def query(self, ctx: Context, query: Query) -> List[Result]:
        """Search YouTube videos using YouTube Data API"""
        results: List[Result] = []
        search_term = query.search.strip() if query.search else ""

        # Return empty results if search term is empty
        if not search_term:
            return results

        # Check if API key is configured
        if not self.youtube_api_key:
            results.append(
                Result(
                    title="YouTube API key not configured",
                    sub_title="Please set your YouTube Data API key in plugin settings",
                    icon=WoxImage(
                        image_type=WoxImageType.RELATIVE,
                        image_data="image/app.png",
                    ),
                )
            )
            return results

        try:
            # Build search parameters
            params = self._build_search_params(search_term, "video", "relevance", self.max_results)

            # Make API request
            base_url = "https://www.googleapis.com/youtube/v3/search"
            response = await self.http_client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse results
            items = data.get("items", [])

            if not items:
                results.append(
                    Result(
                        title="No videos found",
                        sub_title=f"No results for: {search_term}",
                        icon=WoxImage(
                            image_type=WoxImageType.RELATIVE,
                            image_data="image/app.png",
                        ),
                    )
                )
                return results

            # Extract video IDs for detailed information
            video_ids = []
            for item in items:
                if item.get("id", {}).get("videoId"):
                    video_ids.append(item["id"]["videoId"])

            # Get detailed video information if we have video IDs
            video_details = {}
            if video_ids:
                details_params = {"part": "snippet,statistics,contentDetails", "id": ",".join(video_ids), "key": self.youtube_api_key}

                details_response = await self.http_client.get("https://www.googleapis.com/youtube/v3/videos", params=details_params)
                details_response.raise_for_status()
                details_data = details_response.json()

                # Create mapping of video ID to details
                for detail_item in details_data.get("items", []):
                    video_id = detail_item.get("id")
                    if video_id:
                        video_details[video_id] = detail_item

            # Process search results
            for item in items:
                snippet = item.get("snippet", {})
                video_id = item.get("id", {}).get("videoId")

                if not video_id:
                    continue

                # Basic information from search results
                title = snippet.get("title", "No Title")
                channel_title = snippet.get("channelTitle", "Unknown Channel")
                description = snippet.get("description", "")
                publish_date = snippet.get("publishedAt", "")

                # Format publish date
                if publish_date:
                    try:
                        # Extract just the date part (YYYY-MM-DD)
                        publish_date = publish_date.split("T")[0]
                    except Exception:
                        pass

                # Get detailed information
                details = video_details.get(video_id, {})
                statistics = details.get("statistics", {})
                content_details = details.get("contentDetails", {})

                # Extract statistics
                view_count = int(statistics.get("viewCount", 0))
                duration_str = content_details.get("duration", "")

                # Parse and format duration
                duration_formatted = ""
                if duration_str:
                    duration = self._parse_duration_iso8601(duration_str)
                    if duration:
                        duration_formatted = self._format_duration(duration)

                # Format view count
                view_count_formatted = self._format_number_human_readable(view_count)

                # Build subtitle
                subtitle_parts = []
                if channel_title:
                    subtitle_parts.append(f"Channel: {channel_title}")
                if duration_formatted:
                    subtitle_parts.append(f"Duration: {duration_formatted}")
                if view_count_formatted:
                    subtitle_parts.append(f"Views: {view_count_formatted}")
                if publish_date:
                    subtitle_parts.append(f"Published: {publish_date}")

                sub_title = " | ".join(subtitle_parts)

                # Build actions
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                actions = [
                    ResultAction(
                        name="Open in browser",
                        action=self.open_in_browser_action,
                        is_default=True,
                    ),
                    ResultAction(
                        name="Copy URL",
                        action=self.copy_url_action,
                    ),
                    ResultAction(
                        name="Copy video ID",
                        action=self.copy_video_id_action,
                    ),
                ]

                # Create result
                results.append(
                    Result(
                        title=title,
                        sub_title=sub_title,
                        icon=WoxImage(
                            image_type=WoxImageType.RELATIVE,
                            image_data="image/app.png",
                        ),
                        context_data=json.dumps(
                            {
                                "url": video_url,
                                "video_id": video_id,
                                "title": title,
                                "channel": channel_title,
                                "description": description,
                            }
                        ),
                        actions=actions,
                    )
                )

            # If no results found
            if not results:
                results.append(
                    Result(
                        title="No videos found",
                        sub_title=f"No results for: {search_term}",
                        icon=WoxImage(
                            image_type=WoxImageType.RELATIVE,
                            image_data="image/app.png",
                        ),
                    )
                )

        except httpx.HTTPError as e:
            error_msg = f"YouTube API error: {str(e)}"
            if "401" in str(e):
                error_msg = "Invalid YouTube API key. Please check your configuration."
            elif "403" in str(e):
                error_msg = "YouTube API quota exceeded or access denied."

            results.append(
                Result(
                    title="YouTube API Error",
                    sub_title=error_msg,
                    icon=WoxImage(
                        image_type=WoxImageType.RELATIVE,
                        image_data="image/app.png",
                    ),
                )
            )
        except Exception as e:
            results.append(
                Result(
                    title="Error searching YouTube",
                    sub_title=f"Error: {str(e)}",
                    icon=WoxImage(
                        image_type=WoxImageType.RELATIVE,
                        image_data="image/app.png",
                    ),
                )
            )

        return results


plugin = YouTubeSearchPlugin()
