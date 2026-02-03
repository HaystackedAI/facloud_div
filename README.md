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

Yes — it’s an orchestrated, tool-enabled agent.
The system controls the workflow, while the LLM handles reasoning, routing, and tool selection.

In production, we usually avoid fully autonomous agents and prefer controlled orchestration for reliability and compliance.


We use an orchestrated, tool-enabled agent where the LLM routes requests to SQL, RAG, or web search, with strict guardrails, validation, and fallbacks for production reliability.

4️⃣ 必须补的 5 个生产级能力（缺一个都不算 production）
🔒 1. Guardrails

content safety

PII detection

SQL injection prevention

📊 2. Observability

记录：

chosen route

top-k docs

SQL template

token usage

latency

🔁 3. Retry & Fallback

tool error → retry

confidence low → RAG

everything fails → human escalation

💰 4. Cost Control

max tool calls

max tokens

route cache（same intent reuse）

🧪 5. Evaluation

golden questions

retrieval recall

tool accuracy

hallucination rate

5️⃣ 你现在这个 agent，JD 怎么说才“高级”

把你原来的话升级成：

“I designed a production-grade, tool-routed GenAI agent where the LLM dynamically selects between SQL queries, RAG pipelines, and web search, with strict guardrails, validation layers, and observability to ensure reliability and compliance.”

这句话 非常企业，非常加分。
For authoritative, single-source queries such as contacts or IDs, we intentionally bypassed LLM generation and returned structured SQL results directly to ensure accuracy, brevity, and user trust.
The LLM was used strictly for intent routing rather than answer generation.


In enterprise settings, I would build RAG using Azure Cognitive Search as the vector store for retrieval, then assemble retrieved chunks into a structured prompt in Python, and call Azure OpenAI for the final answer.
I would leverage a framework like LangChain or an internal orchestration library to manage the retrieval-generation workflow, ensure guardrails, logging, and integrate it with CI/CD pipelines for production deployment.


A data lake is a cloud-scale, immutable tape archive with modern indexing and access control.

We store original invoice documents immutably in a data lake so extraction logic can evolve without losing historical accuracy