---
title: Building the multi-agent RAG system behind this site
date: 2026-08-21
excerpt: How this site routes visitor questions to specialist agents using LangGraph, Pinecone, and a fallback chain between OpenAI and Anthropic.
---

This site isn't just a static portfolio — the chat widget in the corner is backed by a small multi-agent system built with LangGraph.

## How it works

When a visitor asks a question, a classification node routes it into one of four categories: experience, projects, contact, or personal. Each category has its own specialist node that retrieves relevant context from a Pinecone index and answers using that grounding.

## Reliability first

Every LLM call in the graph — classification and answering — is wrapped in a fallback layer: try the primary model first, fall back to a secondary provider on failure, and degrade gracefully to a static message if both fail. This came directly from years of operations work, where "what happens when this breaks" matters more than the happy path.

## What's next

I'm planning to write more posts like this one covering the production API, the evaluation framework, and lessons from deploying AI systems that need to actually stay up.
