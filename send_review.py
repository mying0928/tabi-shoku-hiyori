import json
from datetime import date

from line_utils import push_message

PROGRESS_FILE = "progress.json"
CYCLE_DAYS = 20

TITLES = {
    "travel": "✈️ 旅遊單字",
    "menu": "🍜 菜單單字",
}


def main():
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    today = date.today().isoformat()
    if progress.get("last_review_date") == today:
        print(f"今天 ({today}) 已經推送過複習提醒，跳過。")
        return

    today_words = progress.get("today_words", {})
    if not today_words.get("travel") and not today_words.get("menu"):
        push_message("📝 今天還沒有學習記錄喔！")
        progress["last_review_date"] = today
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        return

    lines = ["📝 晚上複習時間！今天學過的單字：\n"]
    for key, title in TITLES.items():
        words = today_words.get(key, [])
        if not words:
            continue
        lines.append(title)
        for i, w in enumerate(words, 1):
            lines.append(f"{i}. {w['word']}（{w['kana']}）- {w['meaning']}")
        lines.append("")

    day = progress.get("today_day", progress.get("day", 1))
    lines.append(f"📅 進度：{day}/{CYCLE_DAYS}")

    push_message("\n".join(lines))

    progress["last_review_date"] = today
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
