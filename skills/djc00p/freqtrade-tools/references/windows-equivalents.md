# Windows PowerShell & Command Prompt Equivalents

## PowerShell Functions

Add these to your PowerShell profile (`$PROFILE`) or dot-source this file.

### ftdata — Download Data

```powershell
function ftdata {
  param(
    [string]$Pair = "BTC/USDT",
    [int]$Days = 30,
    [string]$Timeframe = "5m",
    [string]$Erase = ""
  )
  $StartDate = (Get-Date).AddDays(-$Days).ToString("yyyyMMdd")
  docker-compose run --rm freqtrade download-data `
    --exchange kraken `
    --pairs $Pair `
    --timerange "${StartDate}-" `
    --timeframe $Timeframe `
    $Erase
}
```

**Usage Examples:**
```powershell
ftdata "BTC/USDT" 90 5m           # Download 90 days of 5-min BTC/USDT data
ftdata "ETH/USDT" 30 1h           # 30 days of 1-hour ETH/USDT
ftdata "SOL/USDT"                 # Use defaults: 30 days, 5-min
ftdata "XRP/USDT" 365 5m "--erase" # Download 1 year, erase old data first
```

**Critical Notes:**
- Call with ONE pair at a time. Multiple pairs cause errors.
- Use `--erase` when extending your data range backward in time.

### ftback — Run Backtest

```powershell
function ftback {
  param(
    [string]$Strategy = "SampleStrategy",
    [int]$Days = 30,
    [string]$Timeframe = "5m",
    [string]$Pairs = ""
  )
  $StartDate = (Get-Date).AddDays(-$Days).ToString("yyyyMMdd")
  if ([string]::IsNullOrEmpty($Pairs)) {
    docker-compose run --rm freqtrade backtesting `
      --strategy $Strategy `
      --timerange "${StartDate}-" `
      --timeframe $Timeframe `
      --breakdown day
  } else {
    docker-compose run --rm freqtrade backtesting `
      --strategy $Strategy `
      --timerange "${StartDate}-" `
      --timeframe $Timeframe `
      --pairs $Pairs `
      --breakdown day
  }
}
```

**Usage Examples:**
```powershell
ftback "MyStrategy" 60 5m                      # Test MyStrategy for 60 days
ftback "MyStrategy" 90 1h "BTC/USDT"          # Test on specific pair
ftback                                         # Use defaults: SampleStrategy, 30 days, 5m
```

### Bot Control — One-Liners

```powershell
function ftstop    { docker-compose stop }
function ftstart   { docker-compose start }
function ftrestart { docker-compose restart }
function ftlogs    { docker-compose logs -f freqtrade }
function ftstatus  { 
  docker-compose ps
  docker-compose logs --tail=20 freqtrade
}
function ftlist    { 
  if (Test-Path user_data/data/kraken/) {
    Get-ChildItem -Path user_data/data/kraken/ -Recurse | `
      Format-Table FullName, Length
  } else {
    Write-Host "No data. Run ftdata first."
  }
}
function ftui      { Start-Process "http://localhost:8080" }
```

---

## Command Prompt (.bat) Equivalents

For traditional `cmd.exe`, create batch files or use `doskey` macros.

### ftdata.bat

```batch
@echo off
setlocal enabledelayedexpansion

REM Parameters: ftdata.bat PAIR DAYS TIMEFRAME [--erase]
set PAIR=%~1
if "%PAIR%"=="" set PAIR=BTC/USDT
set DAYS=%~2
if "%DAYS%"=="" set DAYS=30
set TIMEFRAME=%~3
if "%TIMEFRAME%"=="" set TIMEFRAME=5m
set ERASE=%~4

REM Calculate start date (DAYS ago)
for /f %%A in ('powershell -Command "(Get-Date).AddDays(-!DAYS!).ToString('yyyyMMdd')"') do (
  set START_DATE=%%A
)

docker-compose run --rm freqtrade download-data ^
  --exchange kraken ^
  --pairs "%PAIR%" ^
  --timerange !START_DATE!- ^
  --timeframe %TIMEFRAME% ^
  %ERASE%

endlocal
```

**Usage (from cmd.exe):**
```batch
ftdata.bat "BTC/USDT" 90 5m           # Download 90 days of 5-min BTC/USDT data
ftdata.bat "ETH/USDT" 30 1h           # 30 days of 1-hour ETH/USDT
ftdata.bat "SOL/USDT"                 # Use defaults: 30 days, 5-min
ftdata.bat "XRP/USDT" 365 5m --erase  # Download 1 year, erase old data first
```

### ftback.bat

```batch
@echo off
setlocal enabledelayedexpansion

REM Parameters: ftback.bat STRATEGY DAYS TIMEFRAME [PAIRS]
set STRATEGY=%~1
if "%STRATEGY%"=="" set STRATEGY=SampleStrategy
set DAYS=%~2
if "%DAYS%"=="" set DAYS=30
set TIMEFRAME=%~3
if "%TIMEFRAME%"=="" set TIMEFRAME=5m
set PAIRS=%~4

for /f %%A in ('powershell -Command "(Get-Date).AddDays(-!DAYS!).ToString('yyyyMMdd')"') do (
  set START_DATE=%%A
)

if "%PAIRS%"=="" (
  docker-compose run --rm freqtrade backtesting ^
    --strategy %STRATEGY% ^
    --timerange !START_DATE!- ^
    --timeframe %TIMEFRAME% ^
    --breakdown day
) else (
  docker-compose run --rm freqtrade backtesting ^
    --strategy %STRATEGY% ^
    --timerange !START_DATE!- ^
    --timeframe %TIMEFRAME% ^
    --pairs %PAIRS% ^
    --breakdown day
)

endlocal
```

**Usage (from cmd.exe):**
```batch
ftback.bat "MyStrategy" 60 5m                      # Test MyStrategy for 60 days
ftback.bat "MyStrategy" 90 1h "BTC/USDT"          # Test on specific pair
ftback.bat                                         # Use defaults: SampleStrategy, 30 days, 5m
```

### Bot Control — doskey Macros

```batch
doskey ftstop=docker-compose stop
doskey ftstart=docker-compose start
doskey ftrestart=docker-compose restart
doskey ftlogs=docker-compose logs -f freqtrade
doskey ftstatus=docker-compose ps $t docker-compose logs --tail=20 freqtrade
doskey ftui=start http://localhost:8080
doskey ftlist=dir /s user_data\data\kraken\
```

**Installation:** Save the above to `freqtrade-macros.bat` and run it in each cmd session, or add to your startup folder.
