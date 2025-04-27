from flask import Flask, render_template, request, jsonify
from threading import Thread
from pathlib import Path
from ingestor import OsIngestor
from utils.log import Log
from threading import Lock

reload_lock = Lock()
app = Flask(__name__)

os = OsIngestor()
config = os.load_config()
log = Log("APP", config)

parsers_callable_dict = os.dynamic_load_parsers(config['parsers']['directory'])
parsers_callable = {k: v for k, v in parsers_callable_dict.items() if not k.endswith("entry")}
parsers = os.reload_dynamic_parsers()

# Stockage de l'état des tâches
tasks = {}


def ingest_thread(filename, parser, idx_name, task_id):
    global tasks, parsers_callable
    """Fonction exécutée dans un thread pour gérer l'ingestion."""
    tasks[task_id] = {"status": "In progress"}
    log_file_path = f"{config['data']['directory']}/{filename}"

    try:
        os.create_index(idx_name)
        os.ingest_file(log_file_path, idx_name, parsers_callable[parser])

        if os.create_index_pattern(idx_name, "time", parsers_callable[parser]):
            tasks[task_id]["status"] = "Success"
            log.info(f"### Task ID: {task_id} {tasks[task_id]['status']}")
        else:
            tasks[task_id]["status"] = "Failed to create index pattern, but data ingested"
            log.info(f"### Task ID: {task_id} {tasks[task_id]['status']}")
    except Exception as e:
        log.error(f"{e}")
        tasks[task_id]["status"] = f"Error: {str(e)}"
        log.info(f"### Task ID: {task_id} {tasks[task_id]['status']}")


@app.route("/", methods=["GET", "POST"])
def index():
    global tasks

    filenames = [f.name for f in Path(config['data']['directory']).iterdir() if f.is_file()]
    selected_file = None
    selected_parser = None
    message = None

    if request.method == "GET":
        global os, parsers
        parsers = os.reload_dynamic_parsers()

    elif request.method == "POST":
        # TODO : check is not null
        selected_file = request.form.get("filename")
        selected_parser = request.form.get("parser")
        selected_index = request.form.get("index_name")

        # Générer un ID de tâche unique
        task_id = f"{len(tasks) + 1}"
        tasks[task_id] = {"status": "Pending"}
        log.info(f"Task ID: {task_id}")
        log.info(f"### after creation Tasks {tasks}")

        # Lancer l'ingestion dans un thread
        thread = Thread(target=ingest_thread, args=(selected_file, selected_parser, selected_index, task_id))
        thread.start()
        log.info(f"### thread Tasks {tasks}")

        message = f"Task ID: {task_id}"

    return render_template("index.html", filenames=filenames, parsers=parsers,
                           selected_file=selected_file, selected_parser=selected_parser, message=message)

@app.route("/reload_parsers", methods=["GET"])
def reload_parsers():
    """Reload parsers dynamically.
    Endpoint works but not used by the button yet
    """
    global parsers
    try:
        parsers = os.reload_dynamic_parsers()
        log.info("Parsers reloaded successfully.")
        return jsonify({"status": "success", "message": "Parsers reloaded successfully.", "parsers": parsers}), 200
    except Exception as e:
        log.error(f"Failed to reload parsers: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/status/<task_id>", methods=["GET"])
def task_status(task_id):
    global tasks
    """Vérifie le statut d'une tâche."""
    log.info(f"### status Tasks {tasks}")
    task = tasks.get(task_id)

    if not task:
        return jsonify({"status": "Invalid Task ID"}), 404
    return jsonify(task)


if __name__ == "__main__":
    app.run(debug=False)