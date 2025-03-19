// Acceptable outputs from the LLM
enum Gender {
  Male
  Female
  Unknown @description("When you are not sure of the final answer")
}

// Conventional prompting
function ClassifyGender(info: string) -> Gender {
  client OllamaGemma3_27b
  prompt #"
    Based on your knowledge of historical scholars and scientists, determine the likely gender of this person.
    Scholars who are termed "laureates" won the Nobel Prize in a category.

    ONLY respond with one gender.

    {{ ctx.output_format }}

    {{ _.role("user") }}
    {{ info }}
  "#
}

// Chain-of-Draft (CoD) prompting
function ClassifyGenderCoD(info: string) -> Gender {
  client OllamaGemma3_27b
  prompt #"
    Based on your knowledge of historical scholars and scientists, determine the likely gender of this person.
    Scholars who are termed "laureates" won the Nobel Prize in a category.

    ONLY respond with one gender.

    {{ ctx.output_format }}

    Think step by step before answering. Only keep a minimum draft for each thinking step, with 10 words at most. Make sure you try to recall the answer from your internal memory.
    Return the final JSON object at the end of the thinking process.

    {{ _.role("user") }}
    {{ info }}
  "#
}

// Conventional prompting tests
test ClassifyAaronKlug {
  functions [ClassifyGender]
  args {
    info "name: Aaron Klug\ninfo: 1982 Chemistry Nobel Prize"
  }
}


test ClassifyAbbaLerner {
  functions [ClassifyGender]
  args {
    info "name: Abba Lerner\ninfo: 1974 Physics Nobel Prize"
  }
}

test ClassifyAJFMBrochantDeVilliers {
  functions [ClassifyGender]
  args {
    info "name: AJFM Brochant de Villiers\ninfo: scholar"
  }
}

test ClassifyElaineTuomanen {
  functions [ClassifyGender]
  args {
    info "name: Elaine Tuomanen\ninfo: scholar"
  }
}

test ClassifyAbdusSalam {
  functions [ClassifyGender]
  args {
    info "name: Abdus Salam\ninfo: 1979 Physics Nobel Prize"
  }
}

test ClassifyAndreaGhez {
  functions [ClassifyGender]
  args {
    info "name: Andrea Ghez\ninfo: 2020 Physics Nobel Prize"
  }
}

// Test with Chain-of-Draft (CoD) prompting
test ClassifyAimeCotton {
  functions [ClassifyGenderCoD]
  args {
    info "name: Aime Cotton\ninfo: scholar"
  }
}

test ClassifyLeonorMichaelis {
  functions [ClassifyGenderCoD]
  args {
    info "name: Leonor Michaelis\ninfo: scholar"
  }
}