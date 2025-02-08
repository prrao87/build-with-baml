###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "classifier.baml": "enum Genre {\n    SciFi\n    Romance\n    Historical\n    Fantasy\n    Mystery\n    Horror\n    Thriller\n    Drama\n    War\n    Other @description(#\"\n        Only use this genre if none of the other genres are a good fit.\n    \"#)\n}\n\nclass Output {\n    genres Genre[]\n    @@assert(genres_length_limit, {{ this.genres|length <= 3 }})\n}\n\n\nfunction ClassifyMovie(title: string, plot: string) -> Output {\n    client Gemini15Flash\n    prompt #\"\n        Given a title and plot, classify the movie into one, or AT MOST, three of the following genres:\n\n        {{ ctx.output_format }}\n\n        {{ _.role(\"user\") }}\n\n        Title:\n        {{ title }}\n\n        Plot:\n        {{ plot }}\n    \"#\n}\n\n\ntest movie_1 {\n    functions [ClassifyMovie]\n    args {\n        title \"The Lunchbox\"\n        plot \"Lonely housewife Ila decides to try adding some spice to her stale marriage by preparing a special lunch for her neglectful husband. Unfortunately, the delivery goes astray and winds up in the hands of Saajan, an irritable widower. Curious about her husband's lack of response, Ila adds a note to the next day's lunchbox, and thus begins an unusual friendship in which Saajan and Ila can talk about their joys and sorrows without ever meeting in person.\"\n    }\n}\n\n\ntest movie_2 {\n    functions [ClassifyMovie]\n    args {\n        title \"Prometheus\"\n        plot \"Set in the late 21st century, the film centers on the crew of the spaceship Prometheus as it follows a star map discovered among the artifacts of several ancient Earth cultures. Seeking the origins of humanity, the crew arrives on a distant world and discovers a threat that could cause the extinction of the human species.\"\n    }\n}\n\ntest movie_3 {\n    functions [ClassifyMovie]\n    args {\n        title \"Interstellar\"\n        plot \"In the mid-21st century, humanity faces extinction due to dust storms and widespread crop blights. Joseph Cooper, a widowed former NASA test pilot, works as a farmer and raises his children, Murph and Tom, alongside his father-in-law Donald. Living in a post-truth society, Cooper is reprimanded by Murph's teachers for telling her that the Apollo missions were not fabricated. During a dust storm, the two discover that dust patterns in Murph's room, which she first attributes to a ghost, result from a gravitational anomaly, and translate into geographic coordinates. These lead them to a secret NASA facility headed by Professor John Brand, who explains that, 48 years earlier, a wormhole appeared near Saturn, leading to a system in another galaxy with twelve potentially habitable planets located near a black hole named Gargantua. Volunteers of the Lazarus expedition had previously travelled through the wormhole to evaluate the planets, with Miller, Edmunds, and Mann reporting back desirable results. Cooper is enlisted to pilot the Endurance spacecraft through the wormhole as part of a mission to colonize a habitable planet with 5,000 frozen embryos and ensure humanity's survival. Meanwhile, Professor Brand would continue his work on solving a gravity equation whose solution would supposedly enable construction of spacecraft for an exodus from Earth. Cooper accepts against Murph's wishes and promises to return. When she refuses to see him off, he leaves her his wristwatch to compare their relative time when he returns. The crew, consisting of Cooper, robots TARS and CASE, and scientists Dr. Amelia Brand (Professor Brand's daughter), Romilly, and Doyle, traverse the wormhole after a two-year voyage to Saturn. Cooper, Doyle and Brand use a lander to investigate Miller's planet, where time is severely dilated. After landing in knee-high water and finding only wreckage from Miller's expedition, a gigantic tidal wave kills Doyle and waterlogs the lander's engines. By the time they leave the planet, Cooper and Brand discover that 23 years have elapsed on the Endurance. Having enough fuel left for only one of the other two planets, they vote to go to Mann's, as he is still broadcasting. En route, they receive messages from Earth and Cooper watches Tom grow up, get married, and lose his first son. An adult Murph is now a scientist working on the gravity equation with Professor Brand. On his deathbed, Brand confesses that the Endurance crew was never supposed to return, knowing that a complete solution to the equation was not feasible without observations of gravitational singularities from inside a black hole. On Mann's planet, they awaken him from cryostasis, and he assures them that colonization is possible, despite the extreme environment. During a scouting mission, Mann attempts to kill Cooper and reveals that he falsified his data in the hope of being rescued. He steals Cooper's lander and heads for the Endurance. While a booby trap set by Mann kills Romilly, Brand rescues Cooper with the other lander and they race back to the Endurance. Mann is killed in a failed manual docking operation, severely damaging the Endurance, but Cooper is able to regain control of the station through his own docking maneuver. With insufficient fuel, Cooper and Brand resort to a slingshot around Gargantua, which costs them 51 years due to time dilation. In the process, Cooper and TARS jettison their landers to lighten the Endurance so that Brand and CASE may reach Edmunds' planet. Falling into Gargantua's event horizon, they eject from their craft and find themselves in a tesseract made up of infinite copies of Murph's bedroom across moments in time. Cooper deduces that the tesseract was constructed by advanced humans in the far future, and realizes that he had always been Murph's \\\"ghost\\\". He uses Morse code to manipulate the second hand of the wristwatch he gave her before he left, giving Murphy the data that TARS collected, which enables her to complete Brand's solution. The tesseract, its purpose fulfilled, collapses before ejecting Cooper and TARS. Cooper wakes up on a station orbiting Saturn. He reunites with Murph, now on her deathbed, who tells him to seek out Brand. Cooper and TARS take a spacecraft to rejoin Brand and CASE, who are setting up the human colony on Edmunds' habitable planet.\"\n    }\n}\n\n\ntest movie_4 {\n    functions [ClassifyMovie]\n    args {\n        title \"Dunkirk\"\n        plot \"In 1940, during the Battle of France, Allied soldiers retreat to Dunkirk encircled by the enemy. Tommy flees through the perimeter held by French troops to the beach, where thousands await evacuation, and helps Gibson to bury a body. After Luftwaffe dive-bombers attack, they attempt to board a hospital ship at the single, vulnerable mole available for embarking on deep-draft ships, by rushing a wounded man on a stretcher but are ordered off. They overhear Commander Bolton, Colonel Winnant and a Rear Admiral discuss the best way to get their army evacuated. The ship is sunk by dive bombers; Tommy saves a Highlanders regiment soldier, Alex. The three board a destroyer, but it is hit by a torpedo before it can depart; Gibson saves Tommy and Alex as the ship sinks, and they return to the beach. The Royal Navy requisitions civilian vessels in England to get to Dunkirk. In Weymouth, civilian sailor Dawson, with his son Peter, set out in his boat Moonstone, rather than let the Navy commandeer her. Their teenage hand George joins them on impulse. In the English Channel, they save a shivering shell-shocked soldier from a ship destroyed by a U-boat. Realising that Dawson is going for Dunkirk, the soldier panics and Peter locks him up. The soldier escapes, urging they turn back and tries to wrest control of the boat; in the scuffle, he elbows George who suffers a head injury that blinds him; as the soldier dwells on his actions, George reveals to Peter he came hoping to do something noteworthy. Three Royal Air Force Spitfires fly towards Dunkirk, to provide cover for the evacuation, limited to one hour of operation by their fuel supply. They engage in a dogfight with an enemy fighter. One of the pilots, Farrier, has his fuel gauge smashed by another fighter. He and the second Spitfire pilot, Collins, determine that their leader has gone down and fly on. The crew of the Moonstone witness the two RAF pilots protect a minesweeper from a bomber: Collins’s Spitfire is hit by a fighter and he ditches. Although trapped in his canopy as the plane sinks, Collins is saved by Peter. Tommy, Alex and Gibson and Highlanders soldiers hide in a grounded trawler in the intertidal zone outside the perimeter, waiting for the rising tide. After its Dutch sailor returns, Germans start shooting at the boat for target practice, and water enters through the bullet holes. Alex, attempting to lighten the boat, accuses Gibson, who has been silent, of being a German spy. Gibson reveals he is French; he took the identity of the British soldier he buried. The group abandons the sinking boat, but Gibson is entangled in a chain and drowns. Farrier chooses to continue aiding the evacuation, despite realising that he will never make it home. The destroyer is bombed and sinks, as Moonstone manoeuvres to save men in the water, including Alex, as the shivering soldier starts helping. Peter finds George is dead; asked by the shivering soldier, he says George will be fine. Farrier shoots the bomber down; its crash ignites oil on the water, but Peter saves Tommy. Farrier reaches Dunkirk just as his fuel runs out. Gliding, he shoots down a dive-bomber approaching the mole, and is cheered on by the troops. Farrier lands his Spitfire on the beach beyond the perimeter, burns it and calmly awaits capture. Dawson has the boat evade aerial attack, using a technique taught by his deceased elder son, a pilot lost at the start of the war. With 300,000 men successfully evacuated, Commander Bolton stays to oversee the French evacuation. In Weymouth, the shivering soldier sees George's body and exchanges a glance with Dawson, as he and Collins depart. Tommy and Alex board a train with other soldiers and are heralded by the public at Woking. Tommy reads Churchill's address, encouraging Britain to fight on. Peter arranges for the media to eulogise George.\"\n    }\n}\n\n\ntest movie_5 {\n    functions [ClassifyMovie]\n    args {\n        title \"Inception\"\n        plot \"Dom Cobb and Arthur are \\\"extractors\\\" who perform corporate espionage using experimental dream-sharing technology to infiltrate their targets' subconscious and extract information. Their latest target, Saito, is impressed with Cobb's ability to layer multiple dreams within each other. He offers to hire Cobb for the ostensibly impossible job of implanting an idea into a person's subconscious; performing \\\"inception\\\" on Robert Fischer, the son of Saito's competitor Maurice Fischer, with the idea to dissolve his father's company. In return, Saito promises to clear Cobb's criminal status, allowing him to return home to his children. Cobb accepts the offer and assembles his team: a forger named Eames, a chemist named Yusuf, and a college student named Ariadne. Ariadne is tasked with designing the dream's architecture, something Cobb himself cannot do for fear of being sabotaged by his mind's projection of his late wife, Mal. Maurice Fischer dies, and the team sedates Robert Fischer into a three-layer shared dream on an airplane to America bought by Saito. Time on each layer runs slower than the layer above, with one member staying behind on each to perform a music-synchronized \\\"kick\\\" (using the French song \\\"Non, je ne regrette rien\\\") to awaken dreamers on all three levels simultaneously. The team abducts Robert in a city on the first level, but his trained subconscious projections attack them. After Saito is wounded, Cobb reveals that while dying in the dream would usually awaken dreamers, Yusuf's sedatives will instead send them into \\\"Limbo\\\": a world of infinite subconscious. Eames impersonates Robert's godfather, Peter Browning, to introduce the idea of an alternate will to dissolve the company. Cobb tells Ariadne that he and Mal entered Limbo while experimenting with dream-sharing, experiencing fifty years in one night due to the time dilation with reality. After waking up, Mal still believed she was dreaming. Attempting to \\\"wake up,\\\" she committed suicide and framed Cobb for her murder to force him to do the same. Cobb fled the U.S., leaving his children behind. Yusuf drives the team around the first level as they are sedated into the second level, a hotel dreamed by Arthur. Cobb persuades Robert that Browning has kidnapped him to stop the dissolution and that Cobb is a defensive projection, leading Robert to another third level deeper as part of a ruse to enter Robert's subconscious. In the third level, the team infiltrates an alpine fortress with a projection of Maurice inside, where the inception itself can be performed. However, Yusuf performs his kick too soon by driving off a bridge, forcing Arthur and Eames to improvise a new set of kicks synchronized with them hitting the water by rigging an elevator and the fortress, respectively, with explosives. Mal then appears and kills Robert before he can be subjected to the inception, and he and Saito are lost in Limbo, forcing Cobb and Ariadne to rescue them in time for Robert's inception and Eames's kick. Cobb reveals that during their time in Limbo, Mal refused to return to reality; Cobb had to convince her it was only a dream, accidentally incepting in her the belief that the real world was still a dream. Cobb makes peace with his part in Mal's death. Ariadne kills Mal's projection and wakes Robert up with a kick. Revived into the third level, he discovers the planted idea: his dying father telling him to create something for himself. While Cobb searches for Saito in Limbo, the others ride the synced kicks back to reality. Cobb finds an aged Saito and reminds him of their agreement. The dreamers all awaken on the plane, and Saito makes a phone call. Arriving in Los Angeles, Cobb passes the immigration checkpoint, and his father-in-law accompanies him to his home. Cobb uses Mal's \\\"totem\\\" – a top that spins indefinitely in a dream – to test if he is indeed in the real world, but he chooses not to observe the result and instead joins his children.\"\n    }\n}",
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> Gemini15Flash {\n  provider google-ai\n  options {\n    model \"gemini-1.5-flash\"\n    api_key env.GOOGLE_API_KEY\n    generationConfig {\n      temperature 0.1\n    }\n  }\n}\n\n\nclient<llm> Gemini2FlashLite {\n  provider google-ai\n  options {\n    model \"gemini-2.0-flash-lite-preview-02-05\"\n    api_key env.GOOGLE_API_KEY\n    generationConfig {\n      temperature 0.1\n    }\n  }\n}\n\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomGPT4oMini {\n  provider openai\n  retry_policy Exponential\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomSonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20241022\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n\nclient<llm> CustomHaiku {\n  provider anthropic\n  retry_policy Constant\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/round-robin\nclient<llm> CustomFast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [CustomGPT4oMini, CustomHaiku]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/fallback\nclient<llm> OpenaiFallback {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [CustomGPT4oMini, CustomGPT4oMini]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/retry\nretry_policy Constant {\n  max_retries 3\n  // Strategy is optional\n  strategy {\n    type constant_delay\n    delay_ms 200\n  }\n}\n\nretry_policy Exponential {\n  max_retries 2\n  // Strategy is optional\n  strategy {\n    type exponential_backoff\n    delay_ms 300\n    mutliplier 1.5\n    max_delay_ms 10000\n  }\n}",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.75.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode sync\n}\n",
}

def get_baml_files():
    return file_map