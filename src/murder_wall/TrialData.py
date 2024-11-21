class TrialData:
    def __init__(self, subject_id: str, condition_id: str, activity_id: str):
        self.subject = subject_id
        self.condition = condition_id
        self.activity = activity_id

    def __repr__(self) -> str:
        return f"Subject {self.subject} | Condition {self.condition} | Activity {self.activity}"
