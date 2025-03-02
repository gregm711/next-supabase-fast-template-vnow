.PHONY: start
start:
	@echo "Starting frontend in a new Terminal window..."
	osascript -e 'tell application "Terminal" to do script "cd \"$(PWD)\" && npm run dev"'
	@echo "Starting backend in current window..."
	(cd fast-api && make run)
