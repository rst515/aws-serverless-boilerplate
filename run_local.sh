#!/bin/zsh

set -euo pipefail

export AWS_SAM_LOCAL=true
PORT=3000

# Check if port is in use
if lsof -i :$PORT | grep LISTEN >/dev/null; then
  echo "⚠️ Port $PORT is already in use."

  SAM_PID=$(lsof -ti tcp:$PORT)
  if [ -n "$SAM_PID" ]; then
    PROCESS_NAME=$(ps -p $SAM_PID -o comm=)
    echo "🔍 Port $PORT is being used by process: $PROCESS_NAME (PID $SAM_PID)"

    if [[ "$PROCESS_NAME" == "python"* || "$PROCESS_NAME" == "sam"* ]]; then
      echo -n "🔁 Kill it? (y/n): "
      read RESP
      if [[ "$RESP" == "y" ]]; then
        kill -9 $SAM_PID
        echo "✅ Killed process using port $PORT"
      else
        echo "❌ Exiting."
        exit 1
      fi
    else
      echo "❌ Another program is using port $PORT. Stop it manually."
      exit 1
    fi
  fi
fi

echo "🔧 Building..."
sam build

cleanup() {
  echo "🧹 Cleaning up..."
  if [[ -n "${API_PID:-}" ]]; then
    echo "🔻 Stopping sam local (PID $API_PID)"
    pkill -P $API_PID || kill -9 $API_PID || true
  fi
}
trap cleanup EXIT INT TERM

echo "🚀 Starting API..."
sam local start-api --port $PORT &
API_PID=$!

# Wait briefly for it to start
sleep 3

echo "📡 Testing /item POST"
curl -X POST "http://127.0.0.1:${PORT}/item" \
  -H "Content-Type: application/json" \
  -d '{"id": "123", "name": "test"}'

echo "✅ Test complete."