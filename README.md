# 旅食日和 (tabi-shoku-hiyori) — N5+N4+N3 旅遊/美食單字 LINE Bot

每天 10:00 推送「旅遊」6個 + 「美食」8個（共14個）單字，22:00 推送複習提醒。

## 結構說明

- `words_travel.json`：旅遊主題單字庫（120個，N5 44個＋N4 44個＋N3 32個，依序排列）
- `words_menu.json`：美食主題單字庫（160個，N5 50個＋N4 46個＋N3 64個，依序排列）
- `progress.json`：分別記錄旅遊/美食目前進度、整體進度天數（X/20）與今日推送內容
- `reminders.json`：記錄 GitHub PAT 的核發日/到期日，過期前會在訊息中提醒
- `send_words.py`：10:00推送，旅遊6個＋美食8個新單字，並檢查PAT是否快過期
- `send_review.py`：22:00推送，複習今天學過的單字
- `.github/workflows/schedule.yml`：定義 `workflow_dispatch`（由外部排程服務觸發，見下方「觸發機制」）

## 輪換機制

- 旅遊：120字 ÷ 6個/天 = **20天一輪**
- 美食：160字 ÷ 8個/天 = **20天一輪**

兩者剛好都是20天一輪，單字庫依「先N5、後N4、後N3」排序，讓學習從基礎逐步
進階，**不需要手動更新單字庫**。一輪跑完後會自動從頭重新開始（用同一批
單字複習）。

訊息最下面會顯示統一的進度「📅 進度：X/20」（不分旅遊/美食），第20天送完後
下一次會回到1/20，重新開始下一輪。

## 設定步驟

### 1. 建立 LINE Messaging API Channel

- 前往 [LINE Developers Console](https://developers.line.biz/console/)
- 建立一個 Provider，再建立一個 Messaging API Channel
- 在 Channel 設定中，找到 **Channel access token**，點「Issue」產生長期 token，複製下來
- 把這個 Channel 對應的 LINE Official Account 用手機 LINE「加好友」（掃描 QR code）

### 2. 取得自己的 userId

- 在 Messaging API 設定頁，關閉「Webhook」（可先不用設定）
- 最簡單的方式：在 LINE Developers Console 的 Messaging API 頁面，往下找
  「Your user ID」，那就是你自己的 userId
  （如果沒有顯示，需要先設一個簡單的 webhook 來抓 userId，可以再跟Claude說）

### 3. 設定 GitHub Secrets

到這個 repo 的 **Settings → Secrets and variables → Actions**，新增：

- `LINE_CHANNEL_ACCESS_TOKEN`：步驟1拿到的 token
- `LINE_USER_ID`：步驟2拿到的 userId

### 4. 推送到 GitHub

```
git add .
git commit -m "init: tabi-shoku-hiyori line bot"
git remote add origin https://github.com/mying0928/tabi-shoku-hiyori.git
git push -u origin main
```

Repo 需要有 push 權限，並確保 **Settings → Actions → General → Workflow
permissions** 設定為 **Read and write permissions**（讓 workflow 可以
commit 回 `progress.json`）。

### 5. 設定觸發機制（cron-job.org）

GitHub Actions 的原生 `schedule` 觸發實測下來不穩定（常常完全不觸發），
所以改用 [cron-job.org](https://cron-job.org)（免費）定時呼叫
`workflow_dispatch` API 來觸發。

1. 在 GitHub 建立一個 **fine-grained PAT**，只勾選這個 repo，權限給
   `Actions: Read and write`
2. 到 cron-job.org 建立兩個 cronjob：

   **Job 1 — 每天 10:00（台灣時間）：推送新單字**
   - URL: `https://api.github.com/repos/mying0928/tabi-shoku-hiyori/actions/workflows/schedule.yml/dispatches`
   - Method: `POST`
   - Headers:
     ```
     Authorization: Bearer <你的PAT>
     Accept: application/vnd.github+json
     Content-Type: application/json
     ```
   - Body: `{"ref":"main","inputs":{"task":"words"}}`

   **Job 2 — 每天 22:00（台灣時間）：複習提醒**
   - 同上 URL / Method / Headers
   - Body: `{"ref":"main","inputs":{"task":"review"}}`

3. `send_words.py` / `send_review.py` 內建防重複機制（檢查
   `progress.json` 的 `last_sent_date` / `last_review_date`），同一天
   重複觸發只會送一次。

### 6. 手動測試

到 GitHub repo 的 Actions 頁籤，選這個 workflow，點 **Run workflow**，
選擇 `task`（`words` 或 `review`）手動觸發測試。

## PAT 到期提醒

`reminders.json` 記錄了：

```json
{
  "pat_issued": "2026-06-14",
  "pat_expires": "2026-09-12",
  "remind_days_before": 3
}
```

- 到期前3天起，每天早上的訊息會附帶提醒：「GitHub PAT 將於 XXXX-XX-XX 過期」
- 過期後則提示「已過期，記得重新產生token」
- 重新產生PAT後，記得更新 `pat_issued` / `pat_expires`（push日 + 90天）

## 關於「30天沒commit」的提醒

這個排程**每天都會自動commit `progress.json`**，所以正常運作下不會發生
「30天沒commit」的狀況。

⚠️ 但如果某天發現訊息沒有正常送達（代表排程可能已停止），這個檢查程式本身
也跑不動，無法自動提醒你 —— 這是邏輯上的限制（排程停了，依賴排程的提醒
自然也不會跑）。

**建議：** 如果發現連續幾天沒收到LINE訊息，直接到
https://github.com/mying0928/tabi-shoku-hiyori/actions 確認排程狀態，
若顯示因不活躍被停用，點選重新啟用即可。

## 單字資料來源

旅遊/美食單字庫由使用者參考以下JLPT單字表整理而成：

- https://www.jwbooks.com.tw/DL/JLPT/JN028wordlist.pdf
- https://www.jwbooks.com.tw/DL/JLPT/JN027wordlist.pdf
- https://www.jwbooks.com.tw/DL/JLPT/JN026wordlist.pdf

## 怎麼請 Claude 繼續擴充

開新對話直接說：

> 繼續 tabi-shoku-hiyori 單字庫擴充

Claude 會接續準備下一批旅遊/菜單單字（例如擴充成「第二輪」全新100字）。
