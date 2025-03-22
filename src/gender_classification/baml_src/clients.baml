// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> GTP4oMini {
  provider openai
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
    temperature 0.1
  }
}

client<llm> OpenRouterGPT4oMini {
  provider "openai-generic"
  options {
    base_url "https://openrouter.ai/api/v1"
    api_key env.OPENROUTER_API_KEY
    model "openai/gpt-4o-mini"
    temperature 0.1
    headers {
      "HTTP-Referer" "https://thedataquarry.com" // Optional
      "X-Title" "thedataquarry" // Optional
    }
  }
}

// Custom LLM inference server by YourTechBud (wrapper for Ollama)
client<llm> OllamaGemma3_27b {
  provider openai-generic
  options {
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
    api_key env.INFERIX_API_KEY
    model "gemma3:27b"
    max_tokens 500
    temperature 1.0
    top_k 64
    top_p 0.95
    min_p 0.0
  }
}

client<llm> OllamaGemma3_12b {
  provider openai-generic
  options {
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
    api_key env.INFERIX_API_KEY
    model "gemma3:12b"
    max_tokens 500
    temperature 1.0
    top_k 64
    top_p 0.95
    min_p 0.0
  }
}

// https://docs.boundaryml.com/docs/snippets/clients/retry
retry_policy Constant {
  max_retries 3
  // Strategy is optional
  strategy {
    type constant_delay
    delay_ms 200
  }
}

retry_policy Exponential {
  max_retries 2
  // Strategy is optional
  strategy {
    type exponential_backoff
    delay_ms 300
    multiplier 1.5
    max_delay_ms 10000
  }
}