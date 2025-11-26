<div align="center">

# Unofficial Uniclare Client

An unofficial [Uniclare](https://play.google.com/store/apps/details?id=com.uniclarepro&hl=en_IN&pli=1) / [Student Uni Portal](https://studentportal.universitysolutions.in/) client built to reveal full ESE marks and every hidden result field the official portal doesn’t display, supported by a lightweight frontend, API, and MCP server for extended use. Includes [API](#), [Frontend](#), [MCP Server](#), developed for personal educational purposes and not affiliated with Uniclare or Student Portal.

<a href="https://github.com/viraj-sh/uniclare-client/releases/latest">
  <img src="https://img.shields.io/github/v/release/viraj-sh/uniclare-client?label=Latest%20Release&color=green&style=flat-square&cacheSeconds=3600" alt="Release"/>
</a>
<a href="https://hub.docker.com/r/virajsh/uniclare-client">
  <img src="https://img.shields.io/docker/v/virajsh/uniclare-client?label=Docker&color=blue&sort=semver&style=flat-square" alt="Docker"/>
</a>
<a href="https://github.com/viraj-sh/uniclare-client/wiki">
  <img src="https://img.shields.io/badge/docs-wiki-red?style=flat-square" alt="Wiki"/>
</a>

</div>

---

### What Makes This Client Better than the Official [Uniclare App](https://play.google.com/store/apps/details?id=com.uniclarepro&hl=en_IN&pli=1) or [Student Uni Portal](https://studentportal.universitysolutions.in/)

- **End-semester marks**: Shows full ESE marks for every subject, which the official client hides even though the backend provides them.
- **Complete marks breakdown**: Displays all components returned by the API — end marks, IA marks, viva/practical marks, and totals.
- **Additional result fields**: Reveals extra data like percentage, credits, grade points, credit points, and more that the official portal doesn’t show.
- **MCP server support**: Allows integration with LLMs for automation, summarization, or custom result analysis.

---

## Overview

This repository includes:

- **[API](https://github.com/viraj-sh/uniclare-client/wiki/API-Documentation):** FastAPI-based backend for authentication, semesters, subjects, documents, and attendance.
- **[Frontend](https://github.com/viraj-sh/uniclare-client/wiki/Frontend-Documentation):** Static interface for interacting with the API.
- **[MCP Server](https://github.com/viraj-sh/uniclare-client/wiki/MCP-Documentation):** Endpoint (`/mcp`) compatible with Model Context Protocol (MCP) clients such as LLM Clients, LangChain bots, etc.

The client can be run using a **[prebuilt release](https://github.com/viraj-sh/uniclare-client/releases/latest)** (recommended), **[built from source](#option-1-building-from-source-without-docker)**, or **[Docker](#option-2-running-with-docker)**. Quick deployment is also supported on **Render**.

<!-- Download Latest Releases -->
<div style="margin-bottom: 1em;">
  <strong style="font-size:1.1em;">Download Latest Releases:</strong>
  <div style="margin-top:0.5em;">
    <a href="https://github.com/viraj-sh/uniclare-client/releases/download/v1.1.0/uniclare-client.exe" target="_blank">
      <img src="https://img.shields.io/badge/Windows_(.exe)-x64-blue?style=flat-square" alt="Download Windows" />
    </a>
    <!-- <a href="https://github.com/viraj-sh/uniclare-client/releases/latest/download/uniclare-client-linux.tar.gz" target="_blank">
      <img src="https://img.shields.io/badge/Linux-x64-orange?style=flat-square" alt="Download Linux" />
    </a>
    <a href="https://github.com/viraj-sh/uniclare-client/releases/latest/download/uniclare-client-macos.zip" target="_blank">
      <img src="https://img.shields.io/badge/macOS-x64-ligvhtgrey?style=flat-square" alt="Download macOS" />
    </a> -->
  </div>
</div>

<!-- Quick Deployment -->
<div style="margin-top:1.5em;">
  <strong style="font-size:1.1em;">Quick Deployment:</strong>
  <div style="margin-top:0.5em;">
    <a href="https://render.com/deploy?repo=https://github.com/viraj-sh/uniclare-client" target="_blank">
      <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" width="180"/>
    </a>
  </div>
</div>

---

### Available Services

Once the client is running, the following endpoints are accessible (the host may vary, but the paths remain the same):

- **API:** [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)

  - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **Frontend:** [http://localhost:8000](http://localhost:8000)
- **MCP Server:** [http://localhost:8000/mcp](http://localhost:8000/mcp)

---

## Option 1: Building from Source (Without Docker)

```bash
git clone https://github.com/viraj-sh/uniclare-client
cd uniclare-client

python -m venv venv

venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux

pip install --upgrade pip
pip install -r requirements.txt

python app.py
```

---

## Option 2: Running with Docker

### 1. Use Prebuilt Image from Docker Hub (Recommended)

```bash
docker pull virajsh/uniclare-client:latest
docker run -p 8000:8000 virajsh/uniclare-client:latest
```

### 2. Build Locally

A `Dockerfile` is included in the repository.

```bash
git clone https://github.com/viraj-sh/uniclare-client
cd uniclare-client
docker build -t uniclare-client .
docker run -p 8000:8000 uniclare-client
```

### 3. Docker Compose

A [`docker-compose.yaml`](https://github.com/viraj-sh/uniclare-client/blob/main/docker-compose.yaml) is included in the repository.

```bash
# using curl
curl -L -o docker-compose.yaml https://github.com/viraj-sh/uniclare-client/raw/main/docker-compose.yaml

# using wget
wget -O docker-compose.yaml https://github.com/viraj-sh/uniclare-client/raw/main/docker-compose.yaml

docker-compose up -d
```

---

## Disclaimer

This project is **unofficial** and intended for **personal and educational use only**.
Uniclare, Student Portal or the college has **no affiliation or endorsement** with this project.

Use responsibly. The author is **not liable** for misuse, data loss, or any violations of institutional policies.
