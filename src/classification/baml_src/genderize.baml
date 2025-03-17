enum Gender {
  Male
  Female
  Unknown
}

function ClassifyGender(info: string) -> Gender {
  client Inferix_Gemma3_27b
  prompt #"
    Based on your knowledge of historical scholars and scientists, determine the likely gender of this person.
    Scholars who are termed "laureates" won the Nobel Prize in a category.

    ONLY respond with one gender.

    {{ ctx.output_format }}

    {{ _.role("user") }}
    {{ info }}
  "#
}


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

