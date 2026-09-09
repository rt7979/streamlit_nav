"""下載指定公司歷史營收，並輸出為 CSV。

台股使用 FinMind 月營收；NVDA 與 AMD 使用 SEC 公開的季度營收，並在
``period_type`` 欄位標示為 quarterly，不把季度資料重複冒充成月資料。
"""

from __future__ import annotations

import argparse
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests


COMPANIES = {
    "2376.TW": {"name": "技嘉", "market": "TW", "code": "2376"},
    "2377.TW": {"name": "微星", "market": "TW", "code": "2377"},
    "2357.TW": {"name": "華碩", "market": "TW", "code": "2357"},
    "NVDA": {"name": "輝達", "market": "US", "cik": "0001045810"},
    "AMD": {"name": "AMD", "market": "US", "cik": "0000002488"},
}
FINMIND_URL = "https://api.finmindtrade.com/api/v4/data"
SEC_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
FIELDS = ["ticker", "company_name", "market", "revenue_period", "period_type", "revenue", "currency", "source"]


def month_range(start: date, end: date):
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        yield year, month
        month += 1
        if month == 13:
            year, month = year + 1, 1


def parse_revenue(value: object) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def get_tw_monthly_revenue(session: requests.Session, ticker: str, company: dict[str, str], start: date, end: date):
    response = session.get(
        FINMIND_URL,
        params={"dataset": "TaiwanStockMonthRevenue", "data_id": company["code"],
                "start_date": start.isoformat(), "end_date": end.isoformat()},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != 200:
        raise RuntimeError(payload.get("msg", "FinMind 回傳錯誤"))
    records = []
    for item in payload.get("data", []):
        revenue = parse_revenue(item.get("revenue"))
        if revenue is not None:
            records.append({"ticker": ticker, "company_name": company["name"], "market": "TW",
                            "revenue_period": f"{item['revenue_year']:04d}-{item['revenue_month']:02d}",
                            "period_type": "monthly", "revenue": revenue, "currency": "TWD",
                            "source": FINMIND_URL})
    return records


def get_us_quarterly_revenue(session: requests.Session, ticker: str, company: dict[str, str], start: date, end: date):
    response = session.get(SEC_URL.format(cik=company["cik"]), timeout=30)
    response.raise_for_status()
    facts = response.json().get("facts", {}).get("us-gaap", {})
    revenue_fact = next((facts[name] for name in ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues") if name in facts), None)
    if not revenue_fact:
        return []
    records = []
    for currency, values in revenue_fact.get("units", {}).items():
        for fact in values:
            if fact.get("form") not in {"10-Q", "10-K"} or not fact.get("start"):
                continue
            period_start = date.fromisoformat(fact["start"])
            period_end = date.fromisoformat(fact["end"])
            if not start <= period_end <= end or not 70 <= (period_end - period_start).days <= 110:
                continue
            records.append({"ticker": ticker, "company_name": company["name"], "market": "US",
                            "revenue_period": period_end.isoformat(), "period_type": "quarterly",
                            "revenue": fact["val"], "currency": currency,
                            "source": SEC_URL.format(cik=company["cik"])})
    return list({(item["ticker"], item["revenue_period"]): item for item in records}.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="匯出 2017-01 至 2026-09 的公司歷史營收 CSV")
    parser.add_argument("-o", "--output", type=Path, default=Path(__file__).with_name("vga_revenue_history.csv"))
    parser.add_argument("--start", type=date.fromisoformat, default=date(2017, 1, 1))
    parser.add_argument("--end", type=date.fromisoformat, default=date(2026, 9, 30))
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()
    if args.start > args.end:
        parser.error("--start 必須早於或等於 --end")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; revenue-history-parser/1.0)", "Referer": "https://mops.twse.com.tw/"})
    records, errors = [], []
    for ticker, company in COMPANIES.items():
        if company["market"] == "TW":
            try:
                records.extend(get_tw_monthly_revenue(session, ticker, company, args.start, args.end))
            except (OSError, requests.RequestException, RuntimeError, ValueError) as error:
                errors.append(f"{ticker}: {error}")
            time.sleep(max(0, args.delay))
        else:
            try:
                records.extend(get_us_quarterly_revenue(session, ticker, company, args.start, args.end))
            except (OSError, requests.RequestException, ValueError) as error:
                errors.append(f"{ticker}: {error}")

    result = pd.DataFrame(records, columns=FIELDS).drop_duplicates(subset=["ticker", "revenue_period", "period_type"])
    if not result.empty:
        result = result.sort_values(["revenue_period", "ticker"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"已儲存 {len(result)} 筆營收資料：{args.output}")
    if errors:
        print(f"警告：{len(errors)} 個查詢失敗，第一筆：{errors[0]}")
    print("台股資料為月營收；NVDA 與 AMD 為 SEC 公開的季度營收。")


if __name__ == "__main__":
    main()