# fastapicloud_dividend

A project created with FastAPI CLI.

## Quick Start

### Start the development server

```bash
uv run fastapi dev
```

Visit http://localhost:8000

### Deploy to FastAPI Cloud

> FastAPI Cloud is currently in private beta. Join the waitlist at https://fastapicloud.com

```bash
uv sync
uv run fastapi login
uv run fastapi deploy
```

## Project Structure

- `main.py` - Your FastAPI application
- `pyproject.toml` - Project dependencies

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [FastAPI Cloud](https://fastapicloud.com)
在真实工程项目中，不使用 LangChain、LangGraph、CrewAI 等框架，纯用 Python + LLM API 手动实现 AI Agent 不仅完全可行，而且在许多场景下是更优选择。 Anthropic 官方明确建议开发者”从直接使用 LLM API 开始” (当然，各有各的立场)，而非框架。Octomind 等公司在生产环境使用框架12个月后选择完全移除，称”移除后团队更快乐、更高效”。核心原因在于：LLM 应用本质上只需要字符串处理、API 调用和循环——这些 Python 原生就能很好完成。框架的额外抽象层常常成为调试噩梦和灵活性枷锁。

These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts ​​and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice.

We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code. Incorrect assumptions about what's under the hood are a common source of customer error.

