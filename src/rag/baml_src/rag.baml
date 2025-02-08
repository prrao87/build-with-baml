// --- Data models ---
class Answer {
    title string | null
    question string
    answer string | null @description("A concise answer to the question in 1-3 sentences")
}

class Document {
  title string | null
  year int | null
  summary string | null
  plot string | null
  distance float @skip  // We don't need distance for the context
}

class Context {
  documents Document[]
}

// --- Functions ---
function AnswerQuestion(question: string, context: Context) -> Answer {
  client Gemini15Flash
  prompt #"
    Answer the question using the provided context.
    Do not make up an answer. If you don't know the answer, return a null response.
    Always strive to provide concise, helpful, and context-aware answers.

    CONTEXT:
    {% for document in context.documents %}
    ----
    TITLE: {{ document.title }}
    SUMMARY: {{ document.summary }}
    PLOT: {{ document.plot }}
    ----
    {% endfor %}

    {{ ctx.output_format }}


    {{ _.role("user") }}

    QUESTION: {{ question }}

    ANSWER:
  "#
}

// --- Tests ---

test missing_context {
  functions [AnswerQuestion]
  args {
    question #"
      What does the engineer do when he is awoken?
    "#
    context {
      documents [
        {
          title null
          year null
          summary null
          plot #"
            The moon orbits the earth, which orbits the sun.
          "#
          distance 1.0
        }
      ]
    }
  }
}

test movie_1_response {
  functions [AnswerQuestion]
  args {
    question #"
      What does the engineer do when he is awoken?
    "#
    context {
      documents [
        {
          title "Prometheus"
          year 2012
          summary "Set in the late 21st century, the film centers on the crew of the spaceship Prometheus as it follows a star map discovered among the artifacts of several ancient Earth cultures. Seeking the origins of humanity, the crew arrives on a distant world and discovers a threat that could cause the extinction of the human species."
          plot #"
            Prometheus (2012 film): As a spacecraft departs a planet, a tall humanoid alien drinks a black liquid, causing its body to dissolve. Its remains crumble into a waterfall and the alien's DNA falls apart and starts to recombine. In 2089, archaeologists Elizabeth Shaw and Charlie Holloway discover a star map in Scotland that matches others from several unconnected ancient cultures. They interpret this as an invitation from humanity's forerunners, the "Engineers". Peter Weyland, the elderly CEO of Weyland Corporation, funds an expedition, aboard the scientific vessel Prometheus, to follow the map to the distant moon LV-223. The ship's crew travels in suspended animation while the android David monitors their voyage.  The Prometheus lands on the barren, mountainous surface near a large, artificial structure, which the team explores. Inside, they find stone cylinders, a monolithic statue of a humanoid head, and the decapitated corpse of a large alien, thought to be an Engineer; Shaw recovers its head. The crew finds other bodies, leading them to surmise that the species is extinct. Crew members Millburn and Fifield grow uncomfortable with the discoveries and attempt to return to Prometheus, but get lost in the structure. The expedition is cut short when a storm forces the crew to return to the ship. David secretly takes a cylinder vase with him, while most of them ooze a black liquid. In the ship's lab, the Engineer's DNA is found to match that of humans. David investigates the contents of the cylinder. He intentionally taints a drink with a minute sample and proposes a toast to the unsuspecting Holloway, who drinks it, having stated he would do anything for answers. Shortly after, Shaw and Holloway have sex. Inside the structure, a snake-like creature kills Millburn, and sprays a corrosive fluid that melts Fifield's helmet. Fifield falls face first into a puddle. When the crew returns, they find Millburn's corpse. David separately discovers a control room containing a surviving Engineer in stasis and a holographic star map highlighting coordinates to Earth. Meanwhile, Holloway sickens rapidly. He is rushed back to Prometheus, but mission director Meredith Vickers refuses to let him aboard. At his urging, she burns him to death with a flamethrower. Later, a medical scan reveals that Shaw, despite being previously infertile, is now in advanced pregnancy. Fearing the worst, she uses an automated surgery table to extract a squid-like creature from her abdomen. Shaw then discovers that Weyland, Vickers' father, has been in stasis aboard Prometheus. He explains that he wants to ask the Engineers how not to die from old age. A monstrous, mutated Fifield returns to the Prometheus and attacks, killing several crewmen before being killed by the captain of Prometheus, Janek. He speculates to Shaw that the structure was actually an Engineer military base that lost control of a virulent biological weapon. The structure also houses a spacecraft. Weyland and the team return to the structure, accompanied by Shaw. David wakes the Engineer from stasis and speaks to him in Proto-Indo-European to try to explain what Weyland wants. The Engineer responds by decapitating David and killing Weyland and his team, before reactivating the spacecraft. Shaw desperately flees and warns Janek that the Engineer is planning to release the menace on Earth to exterminate all life forms, convincing him to stop the spacecraft. Janek and the remaining crew sacrifice themselves by ramming the Prometheus into the alien craft, ejecting the lifeboat in the process. The Engineer's disabled spacecraft crashes onto the ground, crushing Vickers. Shaw goes to the lifeboat and finds her alien offspring is alive and has grown to gigantic size. The Engineer forces open the lifeboat's airlock and attacks Shaw, who releases her alien offspring onto him. It thrusts an ovipositor down the Engineer's throat, subduing him. Shaw recovers David's remains and intends to reach the Engineers' home world in an attempt to understand why they wanted to destroy humanity. With David's help, she launches another Engineer spacecraft and departs from LV-223. In the lifeboat left on the planet, an alien creature bursts out of the dead Engineer's chest.
          "#
          distance 0.5
        }
      ]
    }
  }
}