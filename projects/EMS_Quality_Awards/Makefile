.PHONY: serve summary validate sync

serve:
	python3 -m http.server 8080

summary:
	python3 scripts/generate_summary.py

validate:
	python3 scripts/validate_data.py

sync:
	@echo "Downloading spreadsheet..."
	@command -v gdown >/dev/null || pip install gdown -q
	gdown "https://drive.google.com/uc?id=1sYsrwor9Eaou48im5Y0wLEtfFhAshy7VAjUUEXAq2wo" -O /tmp/ems-tracker.xlsx
	python3 scripts/sync_from_sheet.py /tmp/ems-tracker.xlsx
