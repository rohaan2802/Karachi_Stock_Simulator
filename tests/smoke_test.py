"""Build and exercise the real simulator using isolated Windows working directories."""
from pathlib import Path
import csv
from decimal import Decimal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "build/Karachi_Stock_Simulator.exe"
SEED = ROOT / "data/companies.csv"


def run(folder, commands, expected=0):
    process = subprocess.run([EXE], cwd=folder, input=commands, encoding="utf-8",
                             capture_output=True, timeout=15)
    assert process.returncode == expected, (process.returncode, process.stdout[-1500:], process.stderr)
    return process.stdout


def verify():
    with tempfile.TemporaryDirectory(prefix="karachi-", dir=EXE.parent) as temporary:
        folder = Path(temporary)
        (folder / "companies.csv").write_bytes(SEED.read_bytes())
        board = run(folder, "x\nE")
        assert "Loaded 12 companies" in board and "Session closed." in board
        assert not (folder / "portfolio.txt").exists()
        (folder / "companies.txt").unlink()
        prices = run(folder, "x" + "\n" * 500 + "E")
        with SEED.open() as source, (folder / "companies.txt").open() as saved:
            originals, current = list(csv.reader(source)), list(csv.reader(saved))
        assert len(originals) == len(current) == 12
        for (symbol, name, start), (actual, saved_name, end) in zip(originals, current):
            assert (symbol, name) == (actual, saved_name)
            assert Decimal(start) * Decimal(".85") <= Decimal(end) <= Decimal(start) * Decimal("1.15")

        ranking = run(folder, "xSxXxE")
        assert "SESSION RANKING" in ranking and "Exported market_snapshot.csv" in ranking
        ranks = ranking.split("SESSION RANKING | RETURN FROM OPEN", 1)[1].split("Press any key", 1)[0]
        ranked_rows = [line.split() for line in ranks.splitlines() if line.split() and line.split()[0] != "Symbol"]
        moves = [Decimal(row[-1]) for row in ranked_rows]
        assert len(moves) == 12 and moves == sorted(moves, reverse=True)
        with (folder / "market_snapshot.csv").open() as exported:
            snapshot = list(csv.DictReader(exported))
        assert {row[0] for row in ranked_rows} == {row["symbol"] for row in snapshot}
        for row in snapshot:
            opening = Decimal(row["open_pkr"])
            current = Decimal(row["current_pkr"])
            assert Decimal(row["low_pkr"]) <= current <= Decimal(row["high_pkr"])
            assert abs((current - opening) / opening * 100 - Decimal(row["return_from_open_pct"])) <= Decimal(".00005")

        session = run(folder, "xPReview Investor\nxM10000\nxAPSO\n2\nxRPSO\n1\nxW100\nxLE")
        report = (folder / "portfolio.txt").read_text(encoding="utf-8")
        assert "Review Investor" in report and "PSO" in report, (report, [line for line in session.splitlines() if any(word in line.lower() for word in ("error", "bought", "sold", "invalid", "balance", "withdr", "ps o", "owner", "[ok]"))][-80:])
        for word in ("Added Rs.", "Bought", "Sold", "Withdrew"):
            assert word.lower() in session.lower(), word
        run(folder, "xE")
        assert report == (folder / "portfolio.txt").read_text(encoding="utf-8")
        proof = run(folder, "xM25\nxAZZZ\nxAPSO\n100000\nxE")
        assert "Review Investor" in (folder / "portfolio.txt").read_text(encoding="utf-8")
        assert "invalid" in proof.lower() or "not found" in proof.lower()
        assert "insufficient" in proof.lower() or "not enough" in proof.lower()
        resumed = run(folder, "xP1\nE")
        assert "Review Investor" in resumed and "PSO" in resumed

        malformed = folder / "malformed"
        malformed.mkdir()
        (malformed / "companies.csv").write_text("OK,Valid stock,10.25\nok,Duplicate,12\nBAD,Bad,0\nBAD2,Bad,10a\n")
        invalid = run(malformed, "xE")
        assert "Loaded 1 companies" in invalid
        empty = folder / "empty"
        empty.mkdir()
        missing = run(empty, "", expected=1)
        assert "No companies loaded" in missing
        return dict(board=board, prices=prices, session=session, report=report,
                    proof=proof, resumed=resumed, invalid=invalid, missing=missing,
                    ranking=ranks, snapshot=snapshot)


if __name__ == "__main__":
    verify()
    print("PASS: market load, 500 refreshes, price bounds, trades, cash, save, reload, invalid input, missing data, ranking and CSV export")

