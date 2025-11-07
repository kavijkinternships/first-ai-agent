import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from dotenv import load_dotenv

# Load API key securely
load_dotenv("api.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

WATCH_FOLDER = os.path.join(os.getcwd(), "watch_folder")

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            file_name = os.path.basename(event.src_path)
            print(f"🆕 New file detected: {file_name}")
            self.summarize_text_file(event.src_path)

    def summarize_text_file(self, file_path):
        print(f"📖 Reading: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print("💬 Sending to GPT for summarization...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant that writes short, clear summaries."},
                    {"role": "user", "content": f"Summarize this:\n{content}"}
                ]
            )
            summary = response.choices[0].message.content.strip()
            print(f"✅ Summary received:\n{summary}\n")

            with open("summaries.txt", "a", encoding="utf-8") as log:
                log.write(f"\n📄 File: {os.path.basename(file_path)}\nSummary:\n{summary}\n{'-'*60}\n")

        except Exception as e:
            print(f"❌ Error summarizing file: {e}")

if __name__ == "__main__":
    print("🤖 AI File Agent Started — Watching for new .txt uploads...")
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
