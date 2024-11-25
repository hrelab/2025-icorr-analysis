class TrialData:

    demographicDict = {
        "02" : ["M", "20", "Left", False],
        "03" : ["M", "23", "Right", False],
        "04" : ["M", "22", "Left", False],
        "05" : ["M", "22", "Right", False],
        "07" : ["F", "31", "Right", False],
        "08" : ["M", "28", "Right", False],
        "09" : ["F", "23", "Right", False],
        "12" : ["M", "22", "Right", False],
        "13" : ["F", "29", "Right", False],
        "14" : ["F", "21", "Right", False],
        "15" : ["M", "27", "Right", False],
        "19" : ["F", "70", "Left", False],
        "20" : ["F", "46", "Right", False],
        "21" : ["F", "24", "Right", True],
        "22" : ["M", "34", "Left", True]
    }
    
    def __init__(self, subject_id: str, condition_id: str, activity_id: str):
        self.subject = subject_id
        self.condition = condition_id
        self.activity = activity_id
        self.hand = self.demographicDict[subject_id][2]
        self.impaired = self.demographicDict[subject_id][3]

    def __repr__(self) -> str:
        return f"Subject {self.subject} | Condition {self.condition} | Activity {self.activity}"
