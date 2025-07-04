

import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import os

def ensure_data_directory():
    """確保數據目錄存在"""
    if not os.path.exists('stock_data'):
        os.makedirs('stock_data')

def load_companies():
    """載入公司列表"""
    with open('companies.json', 'r', encoding='utf-8') as f:
        companies = json.load(f)
    return companies

def get_full_history_data(symbol, ipo_date):
    """
    獲取股票從上市日期開始的完整歷史數據
    """
    try:
        stock = yf.Ticker(symbol)
        
        # 從上市日期開始獲取數據
        df = stock.history(start=ipo_date)
        
        if df.empty:
            return {}
        
        # 轉換為價格字典，只保留收盤價
        prices = {}
        for date, row in df.iterrows():
            if pd.notna(row['Close']):
                date_str = date.strftime('%Y-%m-%d')
                prices[date_str] = round(float(row['Close']), 2)
        
        return prices
        
    except Exception as e:
        print(f"  ❌ 獲取歷史數據失敗: {e}")
        return {}

def create_stock_data_file(symbol, company, prices):
    """
    創建股票數據文件
    """
    if not prices:
        return False
    
    # 排序價格數據
    sorted_prices = dict(sorted(prices.items()))
    
    # 創建完整的數據結構
    stock_data = {
        'symbol': symbol,
        'name': company.get('name', ''),
        'chinese_name': company.get('chinese_name', ''),
        'sector': company.get('sector', ''),
        'industry': company.get('industry', ''),
        'ipo_date': company.get('ipo_date', ''),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_records': len(sorted_prices),
        'date_range': {
            'start': min(sorted_prices.keys()) if sorted_prices else '',
            'end': max(sorted_prices.keys()) if sorted_prices else ''
        },
        'prices': sorted_prices
    }
    
    # 保存到文件
    file_path = f'stock_data/{symbol}.json'
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(stock_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"  ❌ 保存失敗: {e}")
        return False

def initialize_all_stock_data():
    """
    初始化所有股票的完整歷史數據
    """
    ensure_data_directory()
    companies = load_companies()
    
    success_count = 0
    total_count = len(companies)
    total_records = 0
    
    print(f"=== 股票數據初始化開始 ===")
    print(f"使用 Yahoo Finance 獲取完整歷史數據")
    print(f"股票數量: {total_count}")
    print()
    
    for i, (symbol, company) in enumerate(companies.items(), 1):
        print(f"[{i}/{total_count}] 初始化 {symbol} ({company.get('chinese_name', '')})")
        
        # 檢查是否有上市日期
        ipo_date = company.get('ipo_date')
        if not ipo_date:
            print(f"  ⚠️ 缺少上市日期，跳過")
            continue
        
        # 檢查文件是否已存在（初始化時強制覆蓋）
        file_path = f'stock_data/{symbol}.json'
        if os.path.exists(file_path):
            print(f"  ⚠️ 數據文件已存在，將重新初始化")
        
        # 獲取完整歷史數據
        prices = get_full_history_data(symbol, ipo_date)
        
        if not prices:
            print(f"  ❌ 無法獲取數據")
            continue
        
        # 創建數據文件
        if create_stock_data_file(symbol, company, prices):
            record_count = len(prices)
            print(f"  ✅ 成功獲取 {record_count} 筆歷史數據")
            total_records += record_count
            success_count += 1
        else:
            print(f"  ❌ 創建數據文件失敗")
        
        # 避免請求過於頻繁
        time.sleep(2)
    
    print()
    print(f"=== 初始化完成 ===")
    print(f"處理股票: {success_count}/{total_count}")
    print(f"總數據筆數: {total_records}")
    
    return success_count, total_count, total_records

def main():
    try:
        success, total, records = initialize_all_stock_data()
        
        if success == total:
            print("🎉 所有股票數據初始化成功！")
        else:
            print(f"⚠️ 部分股票初始化失敗，成功率: {success/total*100:.1f}%")
            
        print(f"📊 總共獲取了 {records} 筆歷史數據")
        print()
        print("💡 提示：初始化完成後，可以使用 daily_update.py 進行每日增量更新")
            
    except Exception as e:
        print(f"初始化過程中發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
