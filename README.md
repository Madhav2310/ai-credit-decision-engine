# AI Credit Decision Engine

A production-style **AI decision system for credit collections** that recommends borrower interventions using:

- rule-based policy overrides
- probabilistic repayment modeling
- LLM-powered strategy reasoning
- agent orchestration with LangGraph

The system simulates how modern fintech platforms determine the optimal action to recover overdue loans.

---

# System Architecture

The service is designed as a modular decision pipeline.

```
Borrower Request
        ↓
Policy Engine (hard rules)
        ↓
LangGraph Multi-Agent System
        ↓
LLM Strategy Reasoning
        ↓
Decision Logging + Metrics
        ↓
PostgreSQL Persistence
```

Infrastructure components:

- **FastAPI** → API layer  
- **LangGraph** → agent orchestration  
- **Ollama / OpenAI** → reasoning engine  
- **PostgreSQL** → borrower + decision storage  
- **Redis** → caching layer  
- **Docker Compose** → local infrastructure  

---

# Features

## AI Decision Engine

Recommends borrower interventions such as:

- SMS reminder
- automated call
- human collections call
- payment plan offer

## Policy Overrides

Critical rules bypass AI reasoning:

- hardship borrowers → payment plans
- very overdue borrowers → human calls
- unresponsive borrowers → escalation

## LangGraph Multi-Agent Workflow

The system decomposes decision-making into agents:

### Risk Agent
Determines borrower risk level.

### Strategy Agent
Chooses a collections strategy.

### Decision Agent (LLM)
Recommends the final borrower intervention.

---

## Persistence

All decisions are logged in **PostgreSQL**, including:

- borrower state
- recommended action
- risk classification
- LLM reasoning
- decision latency

---

## Redis Cache

Borrower repayment belief scores are cached to speed up repeated decisions.

---

## Observability

System metrics include:

- total requests
- LLM calls
- cache hits
- action distribution
- average decision latency

---

## Simulation Engine

A Monte Carlo simulator evaluates strategy performance across thousands of borrowers.

This allows experimentation with different intervention strategies.

---

# API Endpoints

## Recommend Action

```
POST /recommend_action
```

Returns the recommended borrower intervention.

Example response:

```json
{
  "borrower_id": 1,
  "recommended_action": "auto_call",
  "repayment_belief": 0.45
}
```

---

## Simulation

```
POST /simulate
```

Runs a borrower simulation.

Example response:

```json
{
  "borrowers_simulated": 1000,
  "total_recovered": 412000,
  "recovery_rate": 0.41,
  "avg_collection_cost": 0.72,
  "action_distribution": {
    "send_sms": 420,
    "auto_call": 310,
    "human_call": 210,
    "payment_plan": 60
  }
}
```

---

## Metrics

```
GET /metrics
```

Returns system metrics and observability data.

---

## Agent Graph

```
GET /agent_graph
```

Visualizes the LangGraph agent workflow.

---

## Health Check

```
GET /health
```

---

# Running the System

Start the infrastructure:

```
docker compose up --build
```

The API will run at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

# Example Request

```
POST /recommend_action
```

```json
{
  "borrower_id": 1,
  "original_loan_amount": 2000,
  "outstanding_balance": 1500,
  "interest_rate_daily": 0.01,
  "days_overdue": 10,
  "missed_payment_count": 2,
  "total_paid_so_far": 500,
  "last_contact_sentiment": -0.2,
  "engagement_score": 0.4,
  "income_volatility_score": 0.5,
  "hardship_flag": false,
  "promise_to_pay_flag": false,
  "repayment_belief": 0.45,
  "workflow_stage": "fresh_overdue",
  "interventions_used": 1
}
```

---

# Tech Stack

| Layer | Technology |
|------|------------|
| API | FastAPI |
| Agent orchestration | LangGraph |
| LLM interface | LangChain |
| Reasoning models | Ollama / OpenAI |
| Database | PostgreSQL |
| Cache | Redis |
| Infrastructure | Docker |

---

# Project Structure

```
ai-credit-decision-engine/

app/
  agents/
  llm/
  policy/
  simulation/
  observability/

docker-compose.yml
Dockerfile
requirements.txt
README.md
main.py
```

---

# Why This Project Exists

Credit collections systems must balance:

- recovery probability
- operational cost
- borrower behavior
- fairness

This project demonstrates how **AI + policy engines + simulation** can be combined to improve collection decisions.

---

# Future Improvements

- reinforcement learning for policy optimization
- real-time borrower behavior feedback loops
- multi-step collections workflows
- production observability with OpenTelemetry