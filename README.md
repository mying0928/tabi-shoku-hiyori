# 旅食日和 (tabi-shoku-hiyori) — N5+N4+N3 旅遊/美食單字 LINE Bot

每天 10:00 推送「旅遊」6個 + 「美食」8個（共14個）單字，
22:00 推送複習提醒。架構與設定方式同 [jp-vocab-line](https://github.com/mying0928/jp-vocab-line)，
詳細申請流程可參考該repo的 `GUIDE.md`。

## 結構說明

- `words_travel.json`：旅遊主題單字庫（120個，N5 44個＋N4 44個＋N3 32個，依序排列）
- `words_menu.json`：美食主題單字庫（160個，N5 50個＋N4 46個＋N3 64個，依序排列）
- `progress.json`：分別記錄旅遊/美食目前進度與今日推送內容
- `reminders.json`：記錄 GitHub PAT 的核發日/到期日，過期前會在訊息中提醒
- `send_words.py`：10:00推送，旅遊6個＋美食8個新單字，並檢查PAT是否快過期
- `send_review.py`：22:00推送，複習今天學過的單字
- `.github/workflows/schedule.yml`：排程定義（UTC 02:00 / UTC 14:00）

## 輪換機制

- 旅遊：120字 ÷ 6個/天 = **20天一輪**
- 美食：160字 ÷ 8個/天 = **20天一輪**

兩者剛好都是20天一輪，單字庫依「先N5、後N4、後N3」排序，
讓學習從基礎逐步進階，**不需要手動更新單字庫**。一輪跑完後會自動從頭
重新開始（用同一批單字複習）。

訊息最下面會顯示統一的進度「📅 進度：X/20」（不分旅遊/美食），
第20天送完後下一次會回到1/20，重新開始下一輪。

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

## 怎麼請 Claude 繼續擴充

開新對話直接說：

> 繼續 tabi-shoku-hiyori 單字庫擴充

Claude 會接續準備下一批旅遊/菜單單字（例如擴充成「第二輪」全新100字）。
