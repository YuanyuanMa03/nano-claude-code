"""Todo manager for v03 task planning."""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TodoItem:
    """
    A todo item.

    Attributes:
        id: Unique identifier
        text: Task description
        status: One of 'pending', 'in_progress', 'completed'
        created_at: Creation timestamp
    """
    id: str
    text: str
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TodoItem":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            text=data["text"],
            status=data.get("status", "pending"),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


class TodoManager:
    """
    Todo manager - An agent without a plan drifts.

    Features:
    - Single task in_progress constraint
    - Automatic reminder mechanism
    - Status management
    - Progress tracking

    Motto: "An agent without a plan drifts"
    """

    # Status emoji for rendering
    STATUS_EMOJI = {
        "pending": "⬜",
        "in_progress": "🔄",
        "completed": "✅"
    }

    def __init__(self):
        """Initialize the todo manager."""
        self.items: List[TodoItem] = []
        self.nag_counter = 0
        self.last_update = datetime.now()

    def update(self, items: List[Dict[str, Any]]) -> str:
        """
        Update the todo list with new items.

        Args:
            items: List of todo item dictionaries

        Returns:
            Rendered todo list as string

        Raises:
            ValueError: If more than one task is in_progress
        """
        # Validate items
        todo_items = [TodoItem.from_dict(item) for item in items]

        # Check constraint: only one in_progress
        in_progress_count = sum(
            1 for item in todo_items
            if item.status == "in_progress"
        )

        if in_progress_count > 1:
            raise ValueError(
                "Only one task can be in_progress. "
                f"Found {in_progress_count} tasks with status 'in_progress'."
            )

        # Update items
        self.items = todo_items
        self.nag_counter = 0  # Reset nag counter on update
        self.last_update = datetime.now()

        return self.render()

    def render(self) -> str:
        """
        Render the todo list as a formatted string.

        Returns:
            Formatted todo list
        """
        if not self.items:
            return "No tasks"

        lines = []
        for item in self.items:
            emoji = self.STATUS_EMOJI.get(item.status, "❓")
            lines.append(f"{emoji} {item.text}")

        return "\n".join(lines)

    def should_nag(self) -> bool:
        """
        Check if we should remind the agent to update todos.

        Returns:
            True if reminder should be shown
        """
        self.nag_counter += 1
        # Remind after 3 rounds without update
        return self.nag_counter >= 3

    def get_progress(self) -> float:
        """
        Get overall progress (0.0 to 1.0).

        Returns:
            Progress ratio
        """
        if not self.items:
            return 0.0

        completed = sum(1 for item in self.items if item.status == "completed")
        return completed / len(self.items)

    def get_stats(self) -> Dict[str, int]:
        """
        Get todo statistics.

        Returns:
            Dictionary with counts by status
        """
        stats = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "total": len(self.items)
        }

        for item in self.items:
            stats[item.status] = stats.get(item.status, 0) + 1

        return stats

    def to_dict_list(self) -> List[Dict[str, Any]]:
        """
        Convert items to list of dictionaries.

        Returns:
            List of todo item dictionaries
        """
        return [item.to_dict() for item in self.items]
