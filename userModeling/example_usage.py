from UserVector import UserVector


def main() -> None:
    user = UserVector("user_1")
    print("Initial:", user.to_dict())

    articles = {
        "a": {"AI": 0.8, "Regulation": -0.4, "Open Source AI": 0.6},
        "b": {"AI": -0.7, "Regulation": 0.2, "Open Source AI": -0.5},
        "c": {"AI": 0.2, "Regulation": -0.1, "Open Source AI": 0.1},
        "d": {"AI": 0.9, "Regulation": -0.7, "Open Source AI": 0.7},
        "e": {"AI": -0.3, "Regulation": 0.8, "Open Source AI": -0.2},
        "f": {"AI": 0.1, "Regulation": 0.0, "Open Source AI": -0.6},
    }

    feedback = [
        ("like", "a"),
        ("like", "c"),
        ("dislike", "b"),
        ("like", "d"),
        ("dislike", "f"),
        ("like", "e"),
    ]

    for action, article_id in feedback:
        stances = articles[article_id]
        if action == "like":
            user.like(stances)
        else:
            user.dislike(stances)

    print("After feedback:", user.to_dict())
    print("Distances:")
    for article_id, stances in articles.items():
        print(f"  {article_id}: {user.distance_to(stances):.3f}")

    print("Top-k:", user.top_k(articles, k=3))


if __name__ == "__main__":
    main()
