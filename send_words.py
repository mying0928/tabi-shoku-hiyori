import json
from datetime import date

from line_utils import push_message

PROGRESS_FILE = "progress.json"
REMINDERS_FILE = "reminders.json"

CATEGORIES = {
    "travel": {"file": "words_travel.json", "title": "✈️ 旅遊單字", "index_key": "travel_index", "daily_count": 6},
    "menu": {"file": "words_menu.json", "title": "🍜 菜單單字", "index_key": "menu_index", "daily_count": 8},
}

CYCLE_DAYS = 20


def pick_words(words, start, daily_count):
    total = len(words)
    return [words[(start + i) % total] for i in range(daily_count)]


def pat_reminder_line():
    with open(REMINDERS_FILE, encoding="utf-8") as f:
        reminders = json.load(f)

    expires = date.fromisoformat(reminders["pat_expires"])
    days_left = (expires - date.today()).days

    if 0 <= days_left <= reminders["remind_days_before"]:
        return f"\n⚠️ GitHub PAT 將於 {expires.isoformat()} 過期(剩 {days_left} 天),記得去重新產生並更新給Claude！"
    if days_left < 0:
        return f"\n⚠️ GitHub PAT 已於 {expires.isoformat()} 過期,單字庫擴充推送可能會失敗,記得重新產生token！"
    return ""


def main():
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    lines = ["📚 今天的日文單字 (N5+N4+N3 旅遊+美食)\n"]
    today_words = {}

    for key, cfg in CATEGORIES.items():
        with open(cfg["file"], encoding="utf-8") as f:
            words = json.load(f)

        daily_count = cfg["daily_count"]
        start = progress[cfg["index_key"]]
        total = len(words)

        picked = pick_words(words, start, daily_count)
        today_words[key] = picked

        lines.append(cfg["title"])
        for i, w in enumerate(picked, 1):
            lines.append(f"{i}. {w['word']}（{w['kana']}）- {w['meaning']}")
        lines.append("")

        progress[cfg["index_key"]] = (start + daily_count) % total

    progress["today_words"] = today_words

    day = progress.get("day", 1)
    lines.append(f"📅 進度：{day}/{CYCLE_DAYS}")

    lines.append(pat_reminder_line())

    push_message("\n".join(lines))

    progress["today_day"] = day
    progress["day"] = day % CYCLE_DAYS + 1

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
