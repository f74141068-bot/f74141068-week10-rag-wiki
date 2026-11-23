# 第十週作業｜用 LLM Wiki 做一份教學 HTML 簡報

**主題：** RAG（Retrieval-Augmented Generation，檢索增強生成）初學者入門。  
**學生欄位：** 成大 F74141068 資訊系 林晉伃（請在繳交前自行核對）。

## 直接閱讀

1. **雙擊 `index.html`**：專案導覽首頁。
2. **雙擊 `wiki.html`**：可實際瀏覽的六章 Wiki，所有來源可點選。
3. **雙擊 `slides.html`**：14 頁可操作的教學簡報。用左右箭頭／上下一頁按鈕操作，按「目錄」跳頁、按「筆記」顯示講者重點，第 13 頁可作答。
4. **雙擊 `workflow.html`**：Graph/Loop 節點、停機條件與退回流程。

全站使用相對連結與本地 JS/CSS，無需 API Key、帳號、安裝套件或網路才能瀏覽；但原始文獻連結需要網路。

## 作業對照

| 老師規定 | 對應交付項 |
|---|---|
| 至少 ingest 5 篇資料 | `raw/sources.json`、`raw/S01.md`～`S06.md`，共六篇來源紀錄 |
| 「先討論、後生成」 | `REQUIREMENTS.md` 八項設計問答 → `AGENTS.md` |
| LLM Wiki 主題與成果 | `wiki/index.md`、六篇條目、`wiki.html` |
| 可瀏覽的教學型 HTML 簡報 | `slides.html`（14 頁） |
| Graph / Loop | `workflow/GRAPH.md`、`workflow.html`、`.agents/workflows/topic-slides.md` |
| 一次實際執行與檢查 | `scripts/validate.py`、`reports/validation.txt`（以最終紀錄為準） |
| 反思 | `REPORT.md` |
| Wiki/簡報來源明確對應 | `SOURCE_MAPPING.md`、每頁 Sxx 編號 |

## 補充：什麼叫 ingest？

這個專案對每一份原始公開來源建立一筆 `raw/Sxx.md` **來源摘記**，紀錄原始連結、來源類型、核心主張與限制；再從中產出一張獨立證據卡，供 Wiki 使用。這是可稽核的「來源摘記型 ingest」，**沒有抓取並散布六篇文章的全文**；本專案也不是已上線可問答的 RAG 系統。

## 本機驗證

在專案根目錄執行：

```sh
python3 scripts/validate.py
```

只需要 Python 3 標準函式庫；檢查 Wiki 與簡報檔案、引用 ID、連結和頁數。另使用 `node scripts/test_deck_js.js` 做 9 項按鈕／鍵盤事件單元測試，並用 HTML 列印渲染檢視 14 頁版面。**Chromium 真實瀏覽測試在本環境因管理限制未能執行；請使用者手動打開 GitHub Pages 頁面檢查。** 詳見 `reports/`。

## 讓老師能點網路連結（學生需要自己做）

1. 在 GitHub 建一個新的公開 repository，名稱建議 `rag-wiki-week10`。
2. 將 **這個資料夾裡的所有內容**（包含 `index.html`、`slides.html`、`wiki.html`、`assets/`、`raw/`、`wiki/` 等）上傳至 repository 的根目錄。不要只上傳 ZIP，也不要讓 `index.html` 多包一層資料夾。
3. Repository 的 **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**。
4. 等 Pages 顯示實際網站網址，再逐一開啟首頁、`wiki.html`、`slides.html`、`workflow.html` 驗證。**請特別試按簡報「下一頁」、「目錄」、「筆記」與第 13 頁小測驗；手機打開檢查是否需要橫向捲動。**
5. 把實際連結填入 `SUBMISSION.txt` 後，**到課程平台自行繳交**。系統無法替你點擊繳交按鈕。

> 網址示意：`https://<你的GitHub帳號>.github.io/rag-wiki-week10/slides.html`，不代表網站目前已發布。若你的帳號或 repository 取不同名稱，請改用 Pages 實際顯示的網址。

## 誠實與品質說明

- 本專題只研究教學主題，不使用個資或學校未公開資料。
- 已查核來源頁面，正文採中文摘記，不複製大量受版權保護原文。
- 程式檢查不等於保證毫無事實錯誤；學生仍應核對關鍵來源並親自確認作業反思。
- 雖然設計依照 9–10 分項目製作，**是否滿分仍以教師實際評閱為準**。
