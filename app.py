from flask import Flask, jsonify, request

from crawler import fetch_trending

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/repos")
def repos():
    language = request.args.get("language")
    try:
        repo_list = fetch_trending(language=language)
        return jsonify({
            "count": len(repo_list),
            "repos": [r.model_dump() for r in repo_list],
        })
    except Exception as e:
        return jsonify({
            "error": "크롤링 실패",
            "message": str(e),
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
