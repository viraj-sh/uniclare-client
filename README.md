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

**Run from Source** – Clone and run the client in development mode for modification or contribution.

```bash
git clone https://github.com/viraj-sh/uniclare-client
cd uniclare-client/backend

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # macOS/Linux

pip install --upgrade pip
pip install -r requirements.txt

fastapi dev app/main.py 
```


---

> **Disclaimer:** Unofficial project for personal/educational use only. Not affiliated with or endorsed by Uniclare, the Student Portal, or the college. Use responsibly; the author is not liable for misuse, data loss, or policy violations.
