// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> OpenRouterGPT4oMini {
  provider "openai-generic"
  options {
    base_url "https://openrouter.ai/api/v1"
    api_key env.OPENROUTER_API_KEY
    model "openai/gpt-4o-mini"
    headers {
      "HTTP-Referer" "https://thedataquarry.com" // Optional
      "X-Title" "thedataquarry" // Optional
    }
  }
}

client<llm> OpenRouterGemma3_27b {
  provider "openai-generic"
  options {
    base_url "https://openrouter.ai/api/v1"
    api_key env.OPENROUTER_API_KEY
    model "google/gemma-3-27b-it:free"
    headers {
      "HTTP-Referer" "https://thedataquarry.com" // Optional
      "X-Title" "thedataquarry" // Optional
    }
  }
}

// Custom LLM inference server by YourTechBud
client<llm> Inferix_Gemma3_27b {
  provider openai-generic
  options {
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
    api_key env.INFERIX_API_KEY
    model "gemma3:27b"
    max_tokens 500
  }
}

client<llm> Inferix_Gemma3_12b {
  provider openai-generic
  options {
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
    api_key env.INFERIX_API_KEY
    model "gemma3:12b"
    max_tokens 500
  }
}

client<llm> Ollama_Gemma3_27b {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "gemma3:27b"
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