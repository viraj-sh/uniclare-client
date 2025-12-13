<div align="center">

# Unofficial Uniclare Client

An unofficial [Uniclare](https://play.google.com/store/apps/details?id=com.uniclarepro&hl=en_IN&pli=1) / [Student Uni Portal](https://studentportal.universitysolutions.in/) client built to reveal full ESE marks and every hidden result field the official portal doesn’t display. Includes [Frontend](https://github.com/viraj-sh/uniclare-client/wiki/Frontend-Documentation), [MCP Server](https://github.com/viraj-sh/uniclare-client/wiki/MCP-Documentation), [API](https://github.com/viraj-sh/uniclare-client/wiki/API-Documentation), developed for personal educational purposes and not affiliated with Uniclare or Student Portal.

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

## Installation & Usage

The client can be run in several ways. For detailed steps, see the **[Getting Started](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started)** wiki page.

Option 1. **[Prebuilt Releases](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started#prebuilt-releases)** – Download and run the latest release for your platform:

   [![Windows (.exe)](https://img.shields.io/badge/Windows_\(.exe\)-x64-blue?style=flat-square)](https://github.com/viraj-sh/uniclare-client/releases/download/v1.1.1/uniclare-client-v1.1.1-win-x64.exe)
   [![Linux (.tar.gz)](https://img.shields.io/badge/Linux-x86__64-orange?style=flat-square)](https://github.com/viraj-sh/uniclare-client/releases/download/v1.1.1/uniclare-client-v1.1.1-linux-x86__64)
   [![macOS (.zip)](https://img.shields.io/badge/macOS-arm64-lightgrey?style=flat-square)](https://github.com/viraj-sh/uniclare-client/releases/download/v1.1.1/uniclare-client-v1.1.1-macos-arm64)

Option 2. **[One-Click Deployment](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started#one-click-deployment-render) (Render)** – Deploy the client instantly in the cloud:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/viraj-sh/uniclare-client)

Option 3. **[Run from Source](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started#running-from-source)** – Clone the repository and run the client directly in development mode.

  - For developers who want to modify the client.


    ```bash
    git clone https://github.com/viraj-sh/uniclare-client
    cd uniclare-client

    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate   # macOS/Linux

    pip install --upgrade pip
    pip install -r requirements/base.txt

    python app.py
    ```

Option 4. **[Build from Source](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started#building-from-source)** – For developers or contributors: clone the repo, install dependencies, and run locally.

Option 5. **[Docker](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started#docker-deployment)** – Run the client in a consistent containerized environment.

> For complete instructions, platform-specific steps, and Docker usage, see the **[Getting Started wiki](https://github.com/viraj-sh/uniclare-client/wiki/Getting-Started)**.

---
### Available Services

Once the client is running, these endpoints are accessible (host may vary):

* **[Frontend](https://github.com/viraj-sh/uniclare-client/wiki/Frontend-Documentation)** [[http://localhost:8000/](http://localhost:8000/)] : Static interface to interact with the API.
* **[MCP Server](https://github.com/viraj-sh/uniclare-client/wiki/MCP-Documentation)** [[http://localhost:8000/mcp](http://localhost:8000/mcp)] : Endpoint (`/mcp`) compatible with Model Context Protocol (MCP) clients like LLM Clients or LangChain bots.
* **[API](https://github.com/viraj-sh/uniclare-client/wiki/API-Documentation)** [[http://localhost:8000/api](http://127.0.0.1:8000/api)] : FastAPI backend for authentication, semesters, subjects, documents, and attendance.

  * **Interactive Docs:** [[http://localhost:8000/docs](http://127.0.0.1:8000/docs)] : API testing Swagger UI for developers.

---

## MCP Usage

> For full instructions on configuring the MCP server, check out the **[MCP Documentation](https://github.com/viraj-sh/uniclare-client/wiki/MCP-Documentation)**.
<!--
| Demo |
| :------------: |
| <img src="https://raw.githubusercontent.com/viraj-sh/uniclare-client/refs/heads/main/.github/assets/mcp_usage.gif" width="800"/> | -->

## Preview

| Detailed Result                                      | Login                                           |
| :-------------------------------------------- | :-------------------------------------------- |
| <img src="https://raw.githubusercontent.com/viraj-sh/uniclare-client/refs/heads/main/.github/assets/preview_result_detailed.png" width="500" height="300"/> | <img src="https://raw.githubusercontent.com/viraj-sh/uniclare-client/refs/heads/main/.github/assets/preview_login.png" width="500" height="300"/> |

| Result List                                    | Profile                                         |
| :------------------------------------------- | :-------------------------------------------- |
| <img src="https://raw.githubusercontent.com/viraj-sh/uniclare-client/refs/heads/main/.github/assets/preview_results.png" width="500" height="300"/> | <img src="https://raw.githubusercontent.com/viraj-sh/uniclare-client/refs/heads/main/.github/assets/preview_profile.png" width="500" height="300"/> |


---
## Disclaimer

This project is **unofficial** and intended for **personal and educational use only**.
Uniclare, Student Portal or the college has **no affiliation or endorsement** with this project.

Use responsibly. The author is **not liable** for misuse, data loss, or any violations of institutional policies.
