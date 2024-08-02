import os

import pandas as pd
from telegram import User

CSV_FILE = "chat_history/user_data.csv"


def _log_interaction(user: User, user_message: str, bot_response: str) -> None:
    df_new = pd.DataFrame(
        [
            {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_message": user_message,
                "bot_response": bot_response,
            }
        ]
    )

    # Append the new interaction to the existing CSV file
    if os.path.isfile(CSV_FILE):
        df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)


def _get_chat_history(user_id: int) -> list[dict[str, str]]:
    if not os.path.isfile(CSV_FILE):
        return []

    df = pd.read_csv(CSV_FILE)
    user_history = df[df["user_id"] == user_id]

    formatted_history = []
    for _, row in user_history.iterrows():
        formatted_history.append({"role": "user", "content": row["user_message"] or ""})
        formatted_history.append(
            {"role": "assistant", "content": row["bot_response"] or ""}
        )

    return formatted_history


def _clear_chat_history(user: User) -> None:
    if not os.path.isfile(CSV_FILE):
        return

    df = pd.read_csv(CSV_FILE)
    # Replace the username with "cleared_<username>"
    df.loc[df["user_id"] == user.id, "user_id"] = f"cleared_{user.id}"
    df.to_csv(CSV_FILE, index=False)
