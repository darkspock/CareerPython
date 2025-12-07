class InAppNotificationNotFoundException(Exception):
    """Exception raised when an in-app notification is not found"""

    def __init__(self, notification_id: str):
        self.notification_id = notification_id
        super().__init__(f"In-app notification with id '{notification_id}' not found")
