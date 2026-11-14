from pathlib import Path
from html import escape
import re
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
def write(path, content):
    (root / path).write_text(content, encoding="utf-8", newline="\n")

repo = "https://github.com/rohaan2802/KarachiStockMarket_PF"
pages = "https://rohaan2802.github.io/Karachi_Stock_Simulator/"
brief = repo + "/blob/1c8fdd524bdc24df7a0cf8496fdc51977b39e7ea/docs/Project.pdf"
links = [("Repository", repo), ("GitHub Pages", pages), ("Original assignment brief", brief)]
sections = [
("Overview", """Karachi Stock Simulator is a Windows console project by Mohammad Rohaan for Programming Fundamentals at FAST-NUCES. It models a local stock market and a personal portfolio using a bundled snapshot of 12 listed companies. The program generates mock prices locally in Pakistani rupees."""),
("What's Inside", """| Component | Purpose |
|---|---|
| [C++ simulator](src/market_simulator.cpp) | Complete application with market, ranking, export and portfolio views |
| [CMake project](CMakeLists.txt) | Build target and Visual Studio debugger configuration |
| [Technical walkthrough](docs/technical_walkthrough.md) | Architecture, data contracts and a recruiter demo script |
| [Company data](data/companies.csv) | Headerless symbol, company name and starting price rows |
| [Assignment brief](docs/project_brief.pdf) | Original course requirements |
| [Self-evaluation](docs/self_evaluation.pdf) | Original feature checklist |
| [Console display notes](docs/console_display_notes.pdf) | Earlier Windows console troubleshooting |
| [Saved sample](docs/portfolio_sample.txt) | Example portfolio text report |
| [Smoke test](tests/smoke_test.py) | Runs the built program with isolated inputs and checks its saved files |"""),
("Recruiter Demo", """| Step | Action | What to inspect |
|---|---|---|
| 1 | Launch with **run.bat** and press **Enter** | Previous price, current price, and the session high and low |
| 2 | Press **S** | The same companies sorted by percentage return from their opening prices |
| 3 | Press **X** | A spreadsheet-friendly snapshot in **session/market_snapshot.csv** |
| 4 | Open **P**, deposit cash with **M**, and buy two **PSO** shares with **A** | Cash decreases and the portfolio shows the open position |
| 5 | Sell one share with **R**, exit with **E**, and reopen the portfolio | One share and the resulting cash balance persist |

The [technical walkthrough](docs/technical_walkthrough.md) connects those screens to their C++ functions and explains the exported columns."""),
("Project Breakdown", """At startup the app loads a plain CSV, rejects malformed or duplicate entries, and fixes each stock’s opening price for that session. A refresh applies a randomized whole-rupee and fractional change, rounds to cents, clamps to the nearest allowed cent inside the ±15% band, and updates previous, high and low prices. The market board also shows the top percentage movers and the number of shares bought and sold in the session.

The session ranking sorts by return from the opening quote. The Live Market footer compares the current tick with the previous tick, so the two views can highlight different companies. Exporting writes a point-in-time CSV with opening, previous, current, high, low and return-from-open columns.

The portfolio uses dynamically resized arrays for symbols and share counts. Buying debits cash at the current simulated price. Selling credits cash and removes fully sold positions. Portfolio gain or loss compares current and previous tick values for shares still held. Cash and holdings are saved in a readable text report. The original report format remains readable by the application.

| Key | Action |
|---|---|
| Enter | Refresh every stock |
| P / L | Open Portfolio / return to Live Market |
| M / W | Deposit cash / withdraw cash (Portfolio only) |
| A / R | Buy / sell by stock symbol |
| S / X | Rank stocks by return from open / export the current market snapshot |
| E | Exit and save |"""),
("Folder Structure", """\x60\x60\x60text
Karachi_Stock_Simulator/
├── src/           Windows C++ simulator
├── data/          Tracked seed prices
├── docs/          Assignment, sample, display notes and archive
├── tests/         Executable smoke test
├── assets/        Site CSS, JavaScript, captures and previews
├── CMakeLists.txt C++17 build and IDE project
├── index.html     GitHub Pages entry point
├── build.bat      Compile using MSVC or MinGW-w64
└── run.bat        Build and start a local session
\x60\x60\x60

[Archive notes](docs/archive/README.md) identify the earlier versions and the original files.""".encode().decode()),
("Setup", """On Windows, install the MSVC C++ Build Tools or place MinGW-w64 C++ on PATH. From the project folder, run:

\x60\x60\x60powershell
.\\run.bat
\x60\x60\x60

Open **P** to create a portfolio and enter an owner name. Deposit **10,000** with **M**, buy **2 PSO** shares with **A**, and refresh the board with **Enter**. Try selling one share with **R** and exit with **E**. On the next run choose **P → 1** to resume. For a fresh start, close the simulator and remove the local **session/** folder. The launcher copies the bundled seed to that folder and the program writes current prices and portfolio state there.

For IDE review, open the repository folder as a CMake project in Visual Studio. The CMake target builds the same C++ source and puts a seed copy in the build directory’s session folder. For a command-line build:

```powershell
cmake -S . -B build/ide
cmake --build build/ide --config Debug
```

To run the executable-based verification suite with Python 3:

\x60\x60\x60powershell
.\\build.bat
python tests/smoke_test.py
\x60\x60\x60"""),
("Results", """The [saved portfolio sample](docs/portfolio_sample.txt) illustrates the block report, including owner, cash, per-symbol prices, share count, and totals. A normal local run writes updated quotes to **session/companies.txt** and creates **session/portfolio.txt** when a portfolio is set up. Closing an untouched session preserves any existing portfolio file. Local checks passed for the C++ build, 500 refreshes with prices inside their session bounds, deposits, withdrawals, buys, sells, rejection paths persistence, ranking order, and CSV calculation accuracy. The gallery was also checked at mobile, tablet and desktop widths in light and dark themes. Figures label their sources so readers can distinguish saved examples, source inspection, assignment excerpts and captured output."""),
("Limitations", """Prices come from a classroom snapshot and simulated random ticks. The console targets Windows and uses Win32 display APIs. The app supports one local portfolio and up to 50 company rows. The saved files are independent and the simulator expects one running instance per session folder. There are no fees, order book, real-time quotes, or cost-basis returns."""),
("About the Author", """**Mohammad Rohaan** developed the simulator as a Programming Fundamentals final project. [GitHub profile](https://github.com/rohaan2802)."""),
]
sections = [(a,b.replace(r"\x60",chr(96))) for a,b in sections]
source = (root / "src/market_simulator.cpp").read_text(encoding="utf-8").splitlines()
report = (root / "docs/portfolio_sample.txt").read_text(encoding="utf-8").splitlines()
csv = (root / "data/companies.csv").read_text(encoding="utf-8").splitlines()
def excerpt(pattern, after=18, skip=0):
    indices = [i for i,line in enumerate(source) if pattern in line]
    idx = indices[skip]
    return [f"{i+1:4}  {source[i]}" for i in range(idx,min(idx+after,len(source)))]
figures = [
("Market", "Company snapshot", "Twelve bundled symbol, company and starting price records.", "data/companies.csv", csv),
("Market", "Market input validation", "The CSV parser validates names, prices and duplicate symbols.", "src/market_simulator.cpp", excerpt("if (ss.peek()")),
("Market", "Stock symbol lookup", "Linear search matches symbols regardless of letter case.", "src/market_simulator.cpp", excerpt("int findSymbolIndex",12)),
("Market", "Random tick generation", "The refresh combines a whole-number delta and a fractional delta.", "src/market_simulator.cpp", excerpt("prevPrice[i] = currPrice[i];",13)),
("Market", "The session price band", "Cent rounding stays inside the opening price’s ±15% limits.", "src/market_simulator.cpp", excerpt("double minAllowed =",19)),
("Market", "Highs, lows and tick change", "Each price refresh updates session extremes and the percentage move.", "src/market_simulator.cpp", excerpt("currPrice[i] = candidate;",13)),
("Market", "Top movers", "The scanner selects the largest and smallest percentage changes.", "src/market_simulator.cpp", excerpt("void findTopAdvancerDecliner",18)),
("Market", "Market display", "The console draws previous, current, high and low quotes using aligned columns.", "src/market_simulator.cpp", excerpt("void drawLiveMarket",19)),
("Portfolio", "Holdings allocation", "The holdings arrays grow as new symbols enter the portfolio.", "src/market_simulator.cpp", excerpt("void expandHoldings",20)),
("Portfolio", "Portfolio valuation", "The totals function marks held shares at previous and current prices.", "src/market_simulator.cpp", excerpt("void computePortfolioTotals",20)),
("Portfolio", "Portfolio setup", "The console creates a named portfolio when no saved file exists.", "src/market_simulator.cpp", excerpt('cout << " PORTFOLIO SETUP',19)),
("Portfolio", "Continuing a portfolio", "The startup menu offers a saved portfolio, a fresh portfolio, or cancel.", "src/market_simulator.cpp", excerpt('cout << "\\nPlease choose an option:',18)),
("Portfolio", "Deposit balance checks", "The deposit handler validates the amount before updating cash.", "src/market_simulator.cpp", excerpt('if (!isfinite(amount) || amount < 0)',17)),
("Portfolio", "Withdrawal flow", "The prompt accepts a rupee amount or zero to cancel the operation.", "src/market_simulator.cpp", excerpt('cout << "----- WITHDRAW MONEY',19)),
("Portfolio", "Buy order entry", "A buy starts with a symbol and validates it against the market universe.", "src/market_simulator.cpp", excerpt("void addStock",19)),
("Portfolio", "Sell order entry", "A sell is handled against the same quote arrays and the investor’s holdings.", "src/market_simulator.cpp", excerpt("void removeStock",19)),
("Files", "Saved portfolio header", "A stored sample identifies the owner, cash and held positions.", "docs/portfolio_sample.txt", report[:18]),
("Files", "Saved portfolio totals", "The sample footer reports the previous and current portfolio values.", "docs/portfolio_sample.txt", report[-17:]),
("Files", "Safer quote file replacement", "The writer builds the CSV beside the destination before replacing it.", "src/market_simulator.cpp", excerpt("bool saveCompanies",21)),
("Files", "Session exit", "Exit writes the market and writes the portfolio when it was opened or changed.", "src/market_simulator.cpp", excerpt("bool okCompanies",20)),
("Market", "Ranking sort logic", "Stable sorting orders symbols by return from their opening quote.", "src/market_simulator.cpp", excerpt("int order[MAX_COMPANIES]",10)),
("Files", "CSV export logic", "The export writes quotes and percentage returns, then replaces the previous snapshot.", "src/market_simulator.cpp", excerpt("output << fixed << setprecision(2);",16)),
("Verification", "Bounds verification", "The smoke test refreshes the real program 500 times and checks saved quotes.", "tests/smoke_test.py", (root/"tests/smoke_test.py").read_text().splitlines()[23:35]),
("Verification", "Portfolio regression checks", "The suite checks trades, quiet exit, invalid input and reopening saved holdings.", "tests/smoke_test.py", (root/"tests/smoke_test.py").read_text().splitlines()[34:49]),
]
def graph(market_output=None):
    if market_output:
        lines = market_output["board"].splitlines()
        first = next(i for i,l in enumerate(lines) if "KARACHI STOCK MARKET (LIVE)" in l)
        figures[7] = ("Market", "Live Market board", "Output from running the Windows simulator with the bundled quotes.", "Simulator stdout · first market tick", [f"{'Symbol':<7} {'Company':<31} {'Prev':>9} {'Current':>9} {'Move':>5} {'High':>9} {'Low':>9}"] +
            [f"{m[1]:<7} {m[2]:<31} {m[3]:>9} {m[4]:>9} {m[5]:>5} {m[6]:>9} {m[7]:>9}"
             for row in lines[first:first+24] if (m := re.match(r"^\s*([A-Z]+)\s+(.+?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+([↑↓=])\s+(\d+\.\d+)\s+(\d+\.\d+)\s*$", row))])
        rank_rows = [row for row in market_output["ranking"].splitlines() if row.strip()]
        figures[6] = ("Market", "Session ranking", "Companies sorted by percentage return from their opening quote.", "Simulator stdout · S", rank_rows)
        csv_rows = [[row[key] for key in ("symbol","open_pkr","current_pkr","high_pkr","low_pkr","return_from_open_pct")] for row in market_output["snapshot"]]
        headings = ["Symbol", "Open PKR", "Current PKR", "High PKR", "Low PKR", "Return %"]
        snapshot_rows = ["  ".join(f"{cell:>12}" for cell in row) for row in [headings, *csv_rows]]
        figures[18] = ("Files", "Exported market snapshot", "Selected columns from the CSV written during a smoke-test run.", "Simulator output · market_snapshot.csv", snapshot_rows)
        figures[17] = ("Files", "Saved portfolio totals", "Report footer produced after a deposit, buy, sell and withdrawal.", "Simulator output · portfolio.txt", market_output["report"].splitlines()[-17:])
        confirmations = [row.strip() for row in market_output["session"].splitlines()
                         if row.strip().startswith("[OK]")]
        figures[12] = ("Portfolio", "Trade and cash confirmations", "The simulator confirms the deposit, buy, sell and withdrawal.", "Simulator stdout · transaction workflow", confirmations)
        errors = [row.strip() for row in market_output["proof"].splitlines()
                  if row.startswith(("Invalid stock symbol", "Insufficient balance", "Required", "Available:"))]
        figures[14] = ("Portfolio", "Rejected buy orders", "The simulator rejects an unknown symbol and an order exceeding available cash.", "Simulator stdout · validation checks", errors)
        figures[16] = ("Files", "Saved PSO position", "The generated portfolio report records the remaining PSO share and cash.", "Simulator output · portfolio.txt", market_output["report"].splitlines()[5:20])
    for directory in ("assets/screenshots", "assets/thumbs"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    fonts = Path("C:/Windows/Fonts")
    def font(name,size):
        return ImageFont.truetype(str(fonts / name),size)
    entries=[]
    for folder, extension in (("screenshots", "*.png"), ("thumbs", "*.webp")):
        for path in (root / "assets" / folder).glob(extension):
            if re.match(r"^\d{2}-", path.name):
                path.unlink()
    for i,(category,title,caption,provenance,rows) in enumerate(figures,1):
        slug = f"{i:02d}-" +re.sub(r"[^a-z0-9]+","-",title.lower()).strip("-")
        full=f"assets/screenshots/{slug}-sage.png"
        preview=f"assets/thumbs/{slug}-sage.webp"
        im=Image.new("RGB",(1440,900),"#293d35")
        d=ImageDraw.Draw(im)
        d.rectangle((0,0,1440,8),fill="#b8dec2")
        d.text((72,48),category.upper(),font=font("segoeuib.ttf",24),fill="#b8dec2")
        d.text((72,82),title,font=font("segoeuib.ttf",55),fill="#fffdf3")
        d.text((74,160),caption,font=font("segoeui.ttf",26),fill="#e4eee6")
        d.rounded_rectangle((72,218,1368,790),radius=18,fill="#18251f",outline="#789687",width=2)
        rows=[row.strip("\r").expandtabs(4) for row in rows]
        rows=[row for row in rows if len(row.strip())<100 or any(c.isalnum() for c in row)]
        size=min(37, 510 // max(len(rows), 1) - 2)
        while size>20 and max((d.textlength(row,font=font("consola.ttf",size)) for row in rows),default=0)>1212:
            size-=1
        mono=font("consola.ttf",size)
        step=min(size + 16,514//max(len(rows),1))
        for j,row in enumerate(rows):
            if d.textlength(row,font=mono)>1212:
                while d.textlength(row+"…",font=mono)>1212: row=row[:-1]
                row+="…"
            if j % 2 == 0:
                d.rectangle((94,244+j*step,1346,244+(j+1)*step),fill="#253a30")
            if provenance.startswith(("src/", "tests/")):
                token_pattern = r'"[^"]*"|//.*|\b(?:if|else|return|bool|int|double|void|const|for|continue|assert|with|auto)\b'
                x = 108
                cursor = 0
                for token in re.finditer(token_pattern, row):
                    plain = row[cursor:token.start()]
                    d.text((x,246+j*step),plain,font=mono,fill="#fffdf3")
                    x += d.textlength(plain,font=mono)
                    value = token.group()
                    color = "#a7e4b5" if value.startswith(('"', '//')) else "#f3d19e"
                    d.text((x,246+j*step),value,font=mono,fill=color)
                    x += d.textlength(value,font=mono)
                    cursor = token.end()
                d.text((x,246+j*step),row[cursor:],font=mono,fill="#fffdf3")
            else:
                ink = "#c5eed1" if j == 0 else "#fffdf3"
                d.text((108,246+j*step),row,font=mono,fill=ink)
        d.text((74,823),provenance,font=font("segoeui.ttf",24),fill="#daeade")
        d.text((1284,823),f"{i:02d} / 24",font=font("segoeui.ttf",22),fill="#daeade")
        im.save(root/full,optimize=True)
        im.resize((960,600),Image.Resampling.LANCZOS).save(root/preview,quality=93,method=6)
        entries.append((category,title,caption,full,preview))
    return entries

def anchor(title):
    return re.sub("[^a-z0-9 -]","",title.lower()).replace(" ","-")

def gallery_order(entries):
    featured = (7, 6, 18)
    return [entries[i] for i in featured] + [entry for i, entry in enumerate(entries) if i not in featured]


def markdown():
    badges = [("Language","C%2B%2B","12675A","#project-breakdown"),("Platform","Windows","2C5863","#setup"),("Data","12%20companies","446034","data/companies.csv"),("Gallery","24%20figures","365E83","#gallery")]
    md = ['<div align="center">','','# Karachi Stock Simulator','','**A C++ Windows console simulator for trading a 12-company mock market in Pakistani rupees.**','']
    badges.extend([("Build","CMake","243D68","CMakeLists.txt"),("Demo","Walkthrough","74501D","#recruiter-demo"),("Export","CSV","175653","#project-breakdown"),("Checks","Smoke%20test","5B417B","tests/smoke_test.py")])
    icons = {"Language":"cplusplus", "Platform":"windowsterminal", "Build":"cmake", "Export":"microsoftexcel", "Checks":"python", "Demo":"github"}
    for name, value, color, target in badges:
        logo = "&logo=" + icons[name] + "&logoColor=white" if name in icons else ""
        md.append(f"[![{name}](https://img.shields.io/badge/{name}-{value}-{color}?style=for-the-badge{logo})]({target})")
    md += ['','</div>','','## Live Links','','| What | Link |','|---|---|']
    md += [f"| {name} | [{url}]({url}) |" for name,url in links]
    md += ["","## Contents",""]
    md += [f"- [{title}](#{anchor(title)})" for title in ["Live Links"]+[s[0] for s in sections[:-1]]+["Gallery",sections[-1][0]]]
    for title,body in sections[:-1]:
        md += ["",f"## {title}","",body]
    md += ["", "## Gallery", ""]
    for _, title, caption, full, preview in gallery_order(entries):
        image = f'<p align="left"><a href="{full}"><img src="{preview}" width="960" alt="{escape(title)}"></a></p>'
        md.extend([f"### {title}", "", image, "", caption, ""])
    return "\n".join(md+["","## About the Author","",sections[-1][1],""])

def inline(s):
    return re.sub(r"\[([^]]+)\]\(([^)]+)\)",r'<a href="\2">\1</a>',re.sub(r"\*\*(.+?)\*\*",r"<strong>\1</strong>",escape(s)))
def table(rows):
    head,*body=rows
    return '<div class="scroll" tabindex="0"><table><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in body)+'</tbody></table></div>'
def html_body(body):
    parts=[]
    for block in body.split("\n\n"):
        if block.startswith(chr(96)*3):
            parts.append('<pre tabindex="0"><code>'+escape("\n".join(block.splitlines()[1:-1]))+'</code></pre>')
        elif block.startswith("|"):
            rows=[[inline(c.strip()) for c in line.strip("|").split("|")] for i,line in enumerate(block.splitlines()) if i!=1]
            parts.append(table(rows))
        else: parts.append("<p>"+inline(block)+"</p>")
    return "\n".join(parts)
def cards():
    output=[]
    for cat, t, c, f, p in gallery_order(entries):
        output.append(f'<figure class="capture" data-category="{cat}"><a href="{f}" aria-label="Enlarge {escape(t)}"><img src="{p}" width="960" height="600" alt="{escape(t)}" loading="lazy"></a><figcaption><small>{cat}</small><h3>{escape(t)}</h3><p>{escape(c)}</p></figcaption></figure>')
    return "\n".join(output)
def section(title, body):
    return f'<section id="{anchor(title)}"><div class="container"><h2>{escape(title)}</h2>{body}</div></section>'
def website():
    live=table([["What","Link"]]+[[title,f'<a href="{url}">{url}</a>'] for title,url in links])
    gallery = '''<p>Browse the market board and ranking, exported data, portfolio output and the code behind them.</p>
<div class="gallery-tools"><label for="search">Search figures</label><input type="search" id="search" placeholder="Search titles and captions">
<div class="filters" aria-label="Filter by category">'''+''.join(f'<button type="button" data-filter="{cat}" aria-pressed="{str(cat=="All").lower()}">{cat}</button>' for cat in dict.fromkeys(["All"]+[e[0] for e in entries]))+'''</div></div>
<p id="gallery-status" role="status">24 figures</p><div class="gallery">'''+cards()+'''</div>
<dialog id="viewer" aria-labelledby="figure-title">
  <div class="viewer-bar"><h3 id="figure-title"></h3><button id="close" aria-label="Close viewer">Close</button></div>
  <div id="image-stage"><img id="figure-image" alt="" width="1440" height="900"></div>
  <p id="figure-caption" aria-live="polite"></p>
  <div class="viewer-bar viewer-controls"><button id="previous">Previous</button><button id="zoom" aria-pressed="false">Zoom in</button><button id="next">Next</button></div>
</dialog>'''
    contents="".join(f'<li><a href="#{anchor(t)}">{escape(t)}</a></li>' for t in ["Live Links"]+[s[0] for s in sections[:-1]]+["Gallery",sections[-1][0]])
    return '''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A C++ stock market simulator with a mock market, portfolio trading and local persistence.">
<title>Karachi Stock Simulator · Mohammad Rohaan</title>
<script>try { const choice = new URLSearchParams(location.search).get("theme"); const saved = localStorage.getItem("karachi-theme"); document.documentElement.dataset.theme = ["light","dark"].includes(choice) ? choice : saved || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"); } catch {}</script>
<link rel="stylesheet" href="assets/css/style.css"><script defer src="assets/js/main.js"></script></head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header><nav class="container nav" aria-label="Main navigation"><a class="brand" href="#main">Karachi Stock Simulator</a><button id="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu" hidden><svg class="menu-open" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg><svg class="menu-close" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg></button><div id="nav-links" class="nav-links"><a href="#overview">Overview</a><a href="#whats-inside">Files</a><a href="#recruiter-demo">Demo</a><a href="#project-breakdown">How It Works</a><a href="#setup">Setup</a><a href="#results">Results</a><a href="#gallery">Gallery</a><a href="#about-the-author">Author</a></div><button id="theme" type="button" aria-label="Toggle theme"><svg class="theme-moon" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 13a9 9 0 1 1-10-10 7.5 7.5 0 0 0 10 10Z" fill="currentColor"/></svg><svg class="theme-sun" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="currentColor"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></nav></header>
<main id="main">
<div class="hero"><div class="container hero-inner">
<div><p class="eyebrow">C++ / WINDOWS CONSOLE</p><h1>Karachi Stock<br>Simulator</h1>
<p class="lede">Trade a 12-company mock market, manage a portfolio in Pakistani rupees, and inspect how a local simulation handles price limits and saved state.</p>
<div class="actions"><a class="primary" href="#gallery">Explore the gallery</a><a class="secondary" href="#setup">Run on Windows</a></div></div>
<a class="hero-figure" href="#gallery"><img src="'''+entries[7][4]+'''" width="960" height="600" alt="Market board from the simulator gallery"></a>
</div></div>
'''+section("Live Links",live)+section("Contents",f'<ul class="contents">{contents}</ul>')+''.join(section(title,html_body(body)+(f'<p><a class="secondary" href="data/companies.csv" download>Download company CSV</a></p>' if title=="What's Inside" else "")) for title,body in sections[:-1])+section("Gallery",gallery)+section(*[sections[-1][0],html_body(sections[-1][1])])+'''
</main><footer><div class="container">Karachi Stock Simulator · Mohammad Rohaan</div></footer>
<button id="back-top" aria-label="Back to Top" hidden><svg width="28" height="28" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 13h6v8h8v-8h6z" fill="currentColor"/></svg></button>
</body></html>
'''

if __name__=="__main__":
    import sys
    saved = None
    if "--capture-run" in sys.argv:
        sys.path.insert(0,str(root/"tests"))
        from smoke_test import verify
        saved = verify()
    entries=graph(saved)
    write("README.md",markdown())
    write("index.html",website())

