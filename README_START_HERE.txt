ASSIGNMENT 1 — TOPIC 12
Zero-Shot vs Few-Shot Prompting: Which Approach Works Better?

WINDOWS LAPTOP SETUP (NO PAID API OR PYTHON PACKAGES NEEDED)

1. Install Python 3.10+ if needed: https://www.python.org/downloads/
   During installation, select 'Add Python to PATH'.
2. Install and open Ollama if not already installed: https://ollama.com/
3. Open Windows Terminal or PowerShell and run:
      ollama pull llama3.2:1b
   If the model is already installed, skip the download.
4. Extract this ZIP, open its Topic12_Ollama_Project folder in File Explorer.
5. Click the address bar, type powershell, and press Enter.
6. Run:
      python run_experiment.py
   If python is not recognized, try: py run_experiment.py
7. Wait until all 120 runs finish. This may take several minutes or longer depending on hardware.
8. Open REPORT.html in Chrome. Verify real results and add your name/roll number.
9. Chrome > Ctrl+P > Destination: Save as PDF > Save as Topic12_Report.pdf.
10. Take screenshots of terminal progress, the report's results and graph, and Ollama model list.
11. Submit Topic12_Report.pdf, run_experiment.py, results.csv, summary.csv,
    and screenshots (or zip them together if your teacher requests one file).

IF OLLAMA DOES NOT CONNECT:
  Start the Ollama application. If necessary run 'ollama serve' in a separate terminal.
  Verify 'ollama list' shows llama3.2:1b.

IMPORTANT:
  This package contains no fabricated experimental results. results.csv,
  summary.csv, and REPORT.html are created only after you run the experiment.
  The script makes HTTP calls ONLY to 127.0.0.1 (local Ollama).
  You can change MODEL at the top of run_experiment.py to an installed model.

EXPERIMENT DESIGN:
  20 questions x 2 prompt methods x 3 repetitions = 120 model calls.
  The exact same test questions are used for both prompt methods.
  The script records output, correctness, tokens and elapsed seconds.
  It generates a styled printable report with results and a bar chart.
