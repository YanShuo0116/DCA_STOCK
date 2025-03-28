# 美股定期定額投資回測工具

這是一個幫助投資者分析美股定期定額投資策略的網頁工具。

## 功能特點

- 支援多檔知名美股及ETF回測
- 自訂投資起始日期、金額與頻率
- 分析投資報酬率與風險指標
- 數據每日自動更新（使用 GitHub Actions）
- 使用 Yahoo Finance 作為數據來源

## 使用方法

1. 訪問網站：[https://yanshuo0116.github.io/DCAstock/](https://yanshuo0116.github.io/DCAstock/)
2. 從列表中選擇想要分析的股票
3. 設定投資參數：
   - 投資起始日期
   - 每月投資金額
   - 投資日期（可多選）
   - 手續費率
4. 查看分析結果：
   - 總投資金額
   - 現值
   - 總報酬率
   - 年化報酬率
   - 手續費支出
   - 損益金額

## 技術實現

- 前端：HTML, CSS (Bootstrap), JavaScript
- 數據更新：Python (yfinance)
- 自動化部署：GitHub Actions
- 託管：GitHub Pages

## 本地開發

1. 克隆專案：
```bash
git clone https://github.com/YanShuo0116/DCAstock.git
```

2. 安裝依賴：
```bash
pip install yfinance pandas
```

3. 更新數據：
```bash
python update_data.py
```

## 授權

MIT License 