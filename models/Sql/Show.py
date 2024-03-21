class Show:
    def __init__(self, data: list) -> None:
        self.RecordId = data[0]
        self.ShowId = data[1]
        self.Title = data[2]
        self.MediumImage = data[3]
        self.LargeImage = data[4]
        self.Created = data[5]
        self.Modified = data[6]