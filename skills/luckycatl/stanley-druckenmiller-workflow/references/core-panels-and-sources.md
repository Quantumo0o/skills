# Core Panels and Sources

Purpose: keep one compact reference for the V1/VNext panel hierarchy, key indicators, and practical source mapping.

Use this file when maintaining the skill, refining the data layer, or checking whether a panel belongs in the daily engine, weekly engine, or monthly background layer.

## 1) Product scope

This workflow is a first-layer macro environment engine.
It helps with:
- liquidity
- rates
- credit
- FX
- breadth / internal structure
- A-share transmission
- U.S. and China macro-to-execution translation

It does not replace second-layer execution judgment:
- exact asset
- exact level
- exact size
- discretionary trading nuance

## 2) Daily engine: required layers

### U.S. core
Use these as the default P0 daily stack:
- Fed net liquidity
- ON RRP balance
- 2s10s
- 3m10y
- 10Y TIPS real yield
- HY OAS
- DXY / dollar proxy
- USDJPY
- WTI
- VIX
- 10Y nominal yield
- IWM / SPY
- RSP / SPY
- KRE / SPY
- SPHB / SPLV

### A-share core
Use these as the default P0 daily stack:
- USDCNY or USDCNH
- northbound flow or valid proxy
- CSI300 vs CSI1000
- ChiNext vs CSI300
- breadth and turnover
- China liquidity anchor (DR007 or Shibor)
- China rates curve proxy
- property leader basket
- joint-stock banks vs big state banks
- HK / offshore China confirmation

## 3) Weekly / monthly extensions

### Weekly U.S.
Useful confirmation layer:
- initial jobless claims
- 5Y5Y or breakeven inflation
- EPS revision momentum
- broader breadth metrics
- housing / consumer high-frequency set
- thematic ETF flow proxies
- IG / CCC / EMB stress proxies

### Weekly China
Useful confirmation layer:
- DR007 / Shibor persistence
- China 10Y-1Y curve proxy
- credit impulse proxy
- property high-frequency sales
- HK China assets confirmation

### Monthly background
Use for slower regime calibration:
- QT progress
- financial conditions index
- ISM / PMI decomposition
- NFIB / business confidence
- China monthly credit impulse
- China property investment and sales
- global PMI split
- SLOOS

## 4) A-share transmission additions

### Internal structure
Most important A-share daily reads:
- CSI300 vs CSI1000
- ChiNext vs CSI300
- breadth
- turnover
- northbound continuity

### Flow / who is buying
Prefer:
- northbound day + continuity
- margin financing change
- style / sector destination when available
- ETF style flow as confirm, not thesis anchor

### Sector / single-name baskets
Use baskets, not isolated names:
- property
- joint-stock banks vs big state banks
- brokers
- machinery
- transport / logistics
- heavy-truck proxy
- premium consumer vs mass consumer
- credit-sensitive basket

### Preferred A-share second-order chains
Always try to include at least one explicit chain, e.g.:
- 外部汇率约束
  -> 外资回流门槛变化
  -> 北向连续性变化
  -> 宽基 / 小盘 / 成长相对强弱
  -> 行业表达切换

- 本地流动性变化
  -> 资金价格变化
  -> 估值修复 or 仅结构修复
  -> 成交与广度是否确认

- 信用传导变化
  -> 地产 / 银行 / 信用敏感资产确认与否
  -> 周期主线是否成立

## 5) Domestic Demand / Real Economy Nowcast

### A-share / China side
Preferred compact blocks:
- Housing
- Consumption
- Logistics / Trade
- Industrial Activity

Preferred fields by block:

#### Housing
- core-city second-hand viewings / listings
- 30-city new home weekly sales area
- land purchase / premium rate or construction proxy

#### Consumption
- CPCA passenger car sales
- dealer inventory coefficient or premium consumption proxy
- express delivery activity

#### Logistics / Trade
- SCFI
- port throughput
- freight / external demand proxy

#### Industrial Activity
- Daqin railway throughput
- electricity usage
- excavator domestic sales
- steel production / steel price when available

Always end with a single composite read:
- Domestic Demand Status: 修复 / 分化 / 偏弱
- implication for A-shares

### U.S. side
Use the same compact logic with local equivalents.
Do not require all blocks to be true daily-frequency series; stable latest-official weekly/monthly public series are acceptable if they can be fetched reliably on each daily run.

#### Housing
Default stable public core:
- 30Y mortgage rate (`MORTGAGE30US`)
- housing starts (`HOUST`)
- building permits (`PERMIT`)

Optional add-ons:
- mortgage applications
- new / existing home sales
- homebuilder sentiment

#### Consumption
Default stable public core:
- retail sales (`RSAFS`)
- total vehicle sales / SAAR (`TOTALSA`)
- real personal consumption expenditure (`PCEC96`) when available

Optional add-ons:
- card / restaurant / travel proxies

#### Logistics / Trade
Default stable public core:
- freight transportation services index (`TSIFRGHT`)

Optional add-ons:
- rail / truck / freight / shipping proxies

#### Industrial Activity
Default stable public core:
- industrial production (`INDPRO`)
- capacity utilization (`TCU`)
- durable goods new orders (`DGORDER`) when available

Optional add-ons:
- ISM new orders
- capex / machinery / energy demand proxies

#### Fundamental Validation
Default stable public core:
- corporate profits after tax (`CP`)
- unit labor costs (`ULCNFB`)
- labor productivity (`OPHNFB`)
- valuation compatibility versus rates / real yields

Optional enhanced layer:
- public earnings season surprise summary
- public guidance / revisions summary when reliably accessible

Use this layer to answer:
- is the profitability backdrop improving, flat, or deteriorating?
- are margins under pressure?
- is productivity offsetting that pressure?
- is the move earnings-backed or just multiple expansion?

Always end with:
- Domestic Demand Status: improving / mixed / weak
- implication for U.S. equities

## 6) Practical source mapping

### U.S. / global
Use the best available mix of:
- FRED
- Yahoo or Stooq style market proxies
- official or widely used public sources

Key examples:
- Fed liquidity / rates / HY OAS / VIX / DXY: FRED preferred where possible
- index / ETF / FX / commodity proxies: Yahoo / Stooq fallback mix
- MOVE fallback: 10Y Treasury realized-volatility proxy from daily yield changes
- JPY vol fallback: USDJPY 20-day realized volatility
- earnings-revision breadth fallback: corporate profits + unit labor costs + productivity + sector relative-strength proxy

### A-shares / China
For now, it is acceptable to document the primary operational source simply as:
- akshare

When some fields are unavailable, acceptable fallbacks are:
- official webpages
- public reports / PDFs
- stable proxy indicators

### General rule
Do not hardcode data values in the skill.
The skill should define:
- what to fetch
- from where
- update cadence
- fallback or proxy
- downgrade behavior when unavailable

## 7) Data quality and downgrade rules

If data is incomplete:
- keep the memo alive
- explicitly name missing panels
- reduce confidence
- avoid fake precision
- use a proxy only when the proxy truly preserves the transmission logic

Field status labels:
- ok
- stale
- proxy
- evidence insufficient

## 8) Output discipline

All final memos should preserve:
- conclusion first
- thesis before tape
- compact panels, then integrated read
- evidence anchors after the main memo
- explicit falsification
- no explicit trade orders

Use three reading layers:
1. decision layer
2. reasoning layer
3. evidence layer
