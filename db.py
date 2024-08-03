import os

import pandas as pd
from telegram import User


class DB:
    def __init__(self, csv_file: str):
        self.CSV_FILE: str = csv_file

    def _log_interaction(
        self, user: User, user_message: str, bot_response: str
    ) -> None:
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
        if os.path.isfile(self.CSV_FILE):
            df_new.to_csv(self.CSV_FILE, mode="a", header=False, index=False)
        else:
            df_new.to_csv(self.CSV_FILE, mode="w", header=True, index=False)

    def _get_chat_history(self, user_id: str) -> list[dict[str, str]]:
        if not os.path.isfile(self.CSV_FILE):
            return []

        df = pd.read_csv(self.CSV_FILE)
        df["user_id"] = df["user_id"].astype(str)
        user_history = df[df["user_id"] == str(user_id)]

        his = []
        for _, row in user_history.iterrows():
            his.append({"role": "user", "content": row["user_message"] or ""})
            his.append({"role": "assistant", "content": row["bot_response"] or ""})

        return his

    def _clear_chat_history(self, user: User) -> None:
        if not os.path.isfile(self.CSV_FILE):
            return

        df = pd.read_csv(self.CSV_FILE)
        df["user_id"] = df["user_id"].astype(str)
        # Replace the user.id with "cleared_<user.id>"
        df.loc[df["user_id"] == str(user.id), "user_id"] = f"cleared_{user.id}"
        df.to_csv(self.CSV_FILE, index=False)

    def _check_user_messages(self, user: User) -> int:
        """Check how many total messages the user has sent"""
        df = pd.read_csv(self.CSV_FILE)

        filtered_df = df[df["user_id"] == str(user.id)]

        return filtered_df.shape[0]
