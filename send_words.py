import json
import math

from line_utils import push_message

PROGRESS_FILE = "progress.json"
DAILY_COUNT = 10

CATEGORIES = {
    "travel": {"file": "words_travel.json", "title": "✈️ 旅遊單字", "index_key": "travel_index"},
    "menu": {"file": "words_menu.json", "title": "🍜 菜單單字", "index_key": "menu_index"},
}


def pick_words(words, start):
    total = len(words)
    return [words[(start + i) % total] for i in range(DAILY_COUNT)]


def main():
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    lines = ["📚 今天的日文單字 (N5 旅遊+菜單)\n"]
    today_words = {}
    day_info = []

    for key, cfg in CATEGORIES.items():
        with open(cfg["file"], encoding="utf-8") as f:
            words = json.load(f)

        start = progress[cfg["index_key"]]
        total = len(words)
        total_days = math.ceil(total / DAILY_COUNT)
        today_day = (start // DAILY_COUNT) + 1

        picked = pick_words(words, start)
        today_words[key] = picked

        lines.append(cfg["title"])
        for i, w in enumerate(picked, 1):
            lines.append(f"{i}. {w['word']}（{w['kana']}）- {w['meaning']}")
        lines.append("")

        progress[cfg["index_key"]] = (start + DAILY_COUNT) % total
        day_info.append((cfg["title"], today_day, total_days))

    progress["today_words"] = today_words

    lines.append("📅 進度：")
    for title, day, total_days in day_info:
        suffix = ""
        if day >= total_days:
            suffix = "（這輪結束，明天將從頭開始 🔄）"
        lines.append(f"{title} 第 {day} / {total_days} 天{suffix}")

    push_message("\n".join(lines))

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
