#!/usr/bin/env python3
"""Scaffold a web project with Flask backend and Bootstrap/ECharts frontend."""

import argparse
import os


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


APP_PY = '''from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/items", methods=["GET"])
def get_items():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name", "")
    value = data.get("value", 0)
    if not name:
        return jsonify({"error": "name is required"}), 400
    with get_db() as conn:
        conn.execute("INSERT INTO items (name, value) VALUES (?, ?)", (name, value))
        conn.commit()
    return jsonify({"message": "ok"}), 201
'''

APP_PY_PART2 = """

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    with get_db() as conn:
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
    return jsonify({"message": "deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
"""

REQUIREMENTS = """flask>=3.0
pytest>=8.0
"""

BASE_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Web App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Web App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="/">首页</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    <footer class="text-center text-muted py-4 mt-5 border-top">
        <small>&copy; 2026 Web App</small>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
'''

INDEX_HTML = r'''{% extends "base.html" %}
{% block title %}首页{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card shadow-sm">
            <div class="card-header"><h5 class="mb-0">数据图表</h5></div>
            <div class="card-body">
                <div id="chart" style="width:100%;height:400px;"></div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm">
            <div class="card-header"><h5 class="mb-0">添加数据</h5></div>
            <div class="card-body">
                <form id="addForm">
                    <div class="mb-3">
                        <label for="name" class="form-label">名称</label>
                        <input type="text" class="form-control" id="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="value" class="form-label">数值</label>
                        <input type="number" class="form-control" id="value" step="0.01" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">添加</button>
                </form>
            </div>
        </div>
    </div>
</div>
<div class="row mt-4">
    <div class="col-12">
        <div class="card shadow-sm">
            <div class="card-header"><h5 class="mb-0">数据列表</h5></div>
            <div class="card-body">
                <table class="table table-hover" id="dataTable">
                    <thead><tr><th>ID</th><th>名称</th><th>数值</th><th>操作</th></tr></thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

STYLE_CSS = """body {
    background-color: #f8f9fa;
}
.card {
    border-radius: 0.5rem;
}
"""

MAIN_JS = r"""// Load data and render chart
document.addEventListener("DOMContentLoaded", function () {
    loadData();
    document.getElementById("addForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const name = document.getElementById("name").value;
        const value = parseFloat(document.getElementById("value").value);
        fetch("/api/items", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, value }),
        }).then(() => {
            document.getElementById("addForm").reset();
            loadData();
        });
    });
});

function loadData() {
    fetch("/api/items")
        .then((r) => r.json())
        .then((data) => {
            renderTable(data);
            renderChart(data);
        });
}

function renderTable(data) {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = data
        .map(
            (item) =>
                `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.value}</td>` +
                `<td><button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">删除</button></td></tr>`
        )
        .join("");
}

function deleteItem(id) {
    fetch(`/api/items/${id}`, { method: "DELETE" }).then(() => loadData());
}

function renderChart(data) {
    const chart = echarts.init(document.getElementById("chart"));
    chart.setOption({
        tooltip: { trigger: "axis" },
        xAxis: { type: "category", data: data.map((d) => d.name) },
        yAxis: { type: "value" },
        series: [{ data: data.map((d) => d.value), type: "bar", itemStyle: { color: "#0d6efd" } }],
    });
    window.addEventListener("resize", () => chart.resize());
}
"""

TEST_APP = '''import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import app, init_db
import pytest

@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    import app as app_module
    app_module.DATABASE = str(tmp_path / "test.db")
    init_db()
    with app.test_client() as c:
        yield c

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_add_and_get_items(client):
    rv = client.post("/api/items", json={"name": "test", "value": 42})
    assert rv.status_code == 201
    rv = client.get("/api/items")
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data) >= 1
    assert data[0]["name"] == "test"

def test_delete_item(client):
    client.post("/api/items", json={"name": "del", "value": 1})
    items = client.get("/api/items").get_json()
    item_id = items[0]["id"]
    rv = client.delete(f"/api/items/{item_id}")
    assert rv.status_code == 200
'''

GITIGNORE = """__pycache__/
*.pyc
*.db
.env
venv/
instance/
"""

def scaffold(project_name, project_dir):
    dirs = ["", "static/css", "static/js", "static/img", "templates", "tests"]
    for d in dirs:
        create_dir(os.path.join(project_dir, d))

    write_file(os.path.join(project_dir, "app.py"), APP_PY + APP_PY_PART2)
    write_file(os.path.join(project_dir, "requirements.txt"), REQUIREMENTS)
    write_file(os.path.join(project_dir, "templates", "base.html"), BASE_HTML)
    write_file(os.path.join(project_dir, "templates", "index.html"), INDEX_HTML)
    write_file(os.path.join(project_dir, "static", "css", "style.css"), STYLE_CSS)
    write_file(os.path.join(project_dir, "static", "js", "main.js"), MAIN_JS)
    write_file(os.path.join(project_dir, "tests", "test_app.py"), TEST_APP)
    write_file(os.path.join(project_dir, ".gitignore"), GITIGNORE)

    print(f"[OK] Project '{project_name}' scaffolded at {project_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a web project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--dir", default=".", help="Parent directory")
    args = parser.parse_args()
    project_dir = os.path.join(args.dir, args.name)
    scaffold(args.name, project_dir)
