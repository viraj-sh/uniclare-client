<div align="center">

# Unofficial Uniclare Client

An unofficial [Uniclare](https://play.google.com/store/apps/details?id=com.uniclarepro&hl=en_IN&pli=1) / [Student Uni Portal](https://studentportal.universitysolutions.in/) client that reveals full ESE marks and hidden result fields. Includes client, MCP Server, and API documentation. Built for personal educational use and not affiliated with Uniclare or Student Portal.

</div>

---

### Features Compared to the Official [Uniclare App](https://play.google.com/store/apps/details?id=com.uniclarepro&hl=en_IN&pli=1) and [Student Uni Portal](https://studentportal.universitysolutions.in/)

- Displays ESE, IA, viva/practical marks, and totals.
- Reveals percentage, credits, grade points, and credit points.
- Supports MCP server integration.

---

## Getting Started
**Prerequisites** – [Python 3.10+](https://www.python.org/) and [Node.js](https://nodejs.org/) (with npm) installed and available on your PATH.

### Run from Source
```bash
git clone https://github.com/viraj-sh/uniclare-client 
cd uniclare-client 
python app.py
```
`--debug` for verbose install/build/server logs. Available at http://localhost:3000.

### Running with Docker
**Prerequisites** – [Docker](https://www.docker.com/) installed and available on your PATH.

**Production** (latest Hub image):
```bash
wget https://raw.githubusercontent.com/viraj-sh/uniclare-client/main/compose.yaml 
docker compose up -d
# or
docker run -d --name uniclare-client -p 3000:80 --restart unless-stopped virajsh/uniclare-client:latest
```
Available at http://localhost:3000.

**Development** (local build, hot reload):
```bash
git clone https://github.com/viraj-sh/uniclare-client 
cd uniclare-client
docker compose -f compose.dev.yaml up -d
# or
docker build -t uniclare-client . 
docker run --rm -p 8080:80 -v ./backend/app:/app uniclare-client fastapi dev main.py --port 80
```
Available at http://localhost:8080.


---

> **Disclaimer:** Unofficial project for personal/educational use only. Not affiliated with or endorsed by Uniclare, the Student Portal, or the college. Use responsibly; the author is not liable for misuse, data loss, or policy violations.
