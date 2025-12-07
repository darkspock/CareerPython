"""ICS Calendar Service for generating .ics calendar files."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import re


@dataclass
class ICSEvent:
    """Data class representing a calendar event."""
    uid: str
    summary: str
    start: datetime
    end: Optional[datetime] = None
    description: Optional[str] = None
    location: Optional[str] = None
    organizer_email: Optional[str] = None
    organizer_name: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self) -> None:
        # Default end time to 1 hour after start if not provided
        if self.end is None:
            self.end = self.start + timedelta(hours=1)


class ICSService:
    """Service for generating ICS calendar files."""

    PRODID = "-//CareerPython//Interview Calendar//EN"
    VERSION = "2.0"
    CALSCALE = "GREGORIAN"
    METHOD = "PUBLISH"

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        """Format datetime to ICS format (YYYYMMDDTHHmmssZ)."""
        # Convert to UTC and format
        return dt.strftime("%Y%m%dT%H%M%SZ")

    @staticmethod
    def _escape_text(text: str) -> str:
        """Escape special characters in ICS text fields."""
        if not text:
            return ""
        # Escape backslashes first, then other special chars
        text = text.replace("\\", "\\\\")
        text = text.replace(",", "\\,")
        text = text.replace(";", "\\;")
        text = text.replace("\n", "\\n")
        return text

    @staticmethod
    def _fold_line(line: str, max_length: int = 75) -> str:
        """Fold long lines according to ICS spec (max 75 chars)."""
        if len(line) <= max_length:
            return line

        result = []
        while len(line) > max_length:
            result.append(line[:max_length])
            line = " " + line[max_length:]  # Continuation lines start with space
        result.append(line)
        return "\r\n".join(result)

    def generate_event(self, event: ICSEvent) -> str:
        """Generate ICS content for a single event."""
        lines = [
            "BEGIN:VCALENDAR",
            f"PRODID:{self.PRODID}",
            f"VERSION:{self.VERSION}",
            f"CALSCALE:{self.CALSCALE}",
            f"METHOD:{self.METHOD}",
            "BEGIN:VEVENT",
            f"UID:{event.uid}",
            f"DTSTAMP:{self._format_datetime(datetime.utcnow())}",
            f"DTSTART:{self._format_datetime(event.start)}",
            f"DTEND:{self._format_datetime(event.end or event.start + timedelta(hours=1))}",
            f"SUMMARY:{self._escape_text(event.summary)}",
        ]

        if event.description:
            lines.append(f"DESCRIPTION:{self._escape_text(event.description)}")

        if event.location:
            lines.append(f"LOCATION:{self._escape_text(event.location)}")

        if event.url:
            lines.append(f"URL:{event.url}")

        if event.organizer_email:
            organizer_line = f"ORGANIZER"
            if event.organizer_name:
                organizer_line += f";CN={self._escape_text(event.organizer_name)}"
            organizer_line += f":mailto:{event.organizer_email}"
            lines.append(organizer_line)

        # Add reminder (15 minutes before)
        lines.extend([
            "BEGIN:VALARM",
            "TRIGGER:-PT15M",
            "ACTION:DISPLAY",
            "DESCRIPTION:Interview Reminder",
            "END:VALARM",
        ])

        lines.extend([
            "END:VEVENT",
            "END:VCALENDAR",
        ])

        # Fold long lines and join with CRLF
        folded_lines = [self._fold_line(line) for line in lines]
        return "\r\n".join(folded_lines) + "\r\n"

    def generate_feed(self, events: List[ICSEvent], calendar_name: str = "Interviews") -> str:
        """Generate ICS content for multiple events (calendar feed)."""
        lines = [
            "BEGIN:VCALENDAR",
            f"PRODID:{self.PRODID}",
            f"VERSION:{self.VERSION}",
            f"CALSCALE:{self.CALSCALE}",
            f"METHOD:{self.METHOD}",
            f"X-WR-CALNAME:{self._escape_text(calendar_name)}",
        ]

        for event in events:
            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{event.uid}",
                f"DTSTAMP:{self._format_datetime(datetime.utcnow())}",
                f"DTSTART:{self._format_datetime(event.start)}",
                f"DTEND:{self._format_datetime(event.end or event.start + timedelta(hours=1))}",
                f"SUMMARY:{self._escape_text(event.summary)}",
            ])

            if event.description:
                lines.append(f"DESCRIPTION:{self._escape_text(event.description)}")

            if event.location:
                lines.append(f"LOCATION:{self._escape_text(event.location)}")

            if event.url:
                lines.append(f"URL:{event.url}")

            if event.organizer_email:
                organizer_line = f"ORGANIZER"
                if event.organizer_name:
                    organizer_line += f";CN={self._escape_text(event.organizer_name)}"
                organizer_line += f":mailto:{event.organizer_email}"
                lines.append(organizer_line)

            lines.append("END:VEVENT")

        lines.append("END:VCALENDAR")

        # Fold long lines and join with CRLF
        folded_lines = [self._fold_line(line) for line in lines]
        return "\r\n".join(folded_lines) + "\r\n"

    @staticmethod
    def generate_google_calendar_url(event: ICSEvent) -> str:
        """Generate a Google Calendar 'Add Event' URL."""
        base_url = "https://calendar.google.com/calendar/render"

        # Format dates for Google Calendar (YYYYMMDDTHHmmssZ)
        start_str = event.start.strftime("%Y%m%dT%H%M%SZ")
        end_str = event.end.strftime("%Y%m%dT%H%M%SZ") if event.end else ""

        params = [
            "action=TEMPLATE",
            f"text={_url_encode(event.summary)}",
            f"dates={start_str}/{end_str}",
        ]

        if event.description:
            params.append(f"details={_url_encode(event.description)}")

        if event.location:
            params.append(f"location={_url_encode(event.location)}")

        return f"{base_url}?{'&'.join(params)}"

    @staticmethod
    def generate_outlook_url(event: ICSEvent) -> str:
        """Generate an Outlook.com 'Add Event' URL."""
        base_url = "https://outlook.live.com/calendar/0/deeplink/compose"

        # Format dates for Outlook (ISO format)
        start_str = event.start.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_str = event.end.strftime("%Y-%m-%dT%H:%M:%SZ") if event.end else ""

        params = [
            "path=/calendar/action/compose",
            "rru=addevent",
            f"subject={_url_encode(event.summary)}",
            f"startdt={start_str}",
            f"enddt={end_str}",
        ]

        if event.description:
            params.append(f"body={_url_encode(event.description)}")

        if event.location:
            params.append(f"location={_url_encode(event.location)}")

        return f"{base_url}?{'&'.join(params)}"


def _url_encode(text: str) -> str:
    """URL encode text for calendar URLs."""
    import urllib.parse
    return urllib.parse.quote(text, safe="")
