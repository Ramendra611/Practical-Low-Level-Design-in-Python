class User:

    def __init__(self, user_id: str, name: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.phone = phone

        self.rating: float = 5.0  # this is the average rating
        self.total_ratings: int = 0  # to calculate the average rating

    def update_rating(self, new_score: int) -> None:
        total = self.rating * self.total_ratings + new_score
        self.total_ratings += 1
        self.rating = total / self.total_ratings

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(id={self.user_id!r}, name={self.name!r}, rating={self.rating:.2f})"
        )
