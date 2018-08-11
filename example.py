from python_data_schema import and_, or_, for_each_item_, type_is_, equals_

test_data = [
    { "sequence": "FLPAIAGILSQLF", "hydrophobicity": 0.769231 },
    { "sequence": "PQPQPFPSQQPY", "type": "alpha-gliadin", "toxic": True },
    { "sequence": "YLQLQPFPQPQLPYP", "type": "alpha-gliadin", "immunogenic": True }
]

# A collection of documents is represented as a list of dicts
mongo_collection_validator = and_([
    type_is_(list),
    for_each_item_( and_([
        type_is_(dict),
        for_each_item_( or_({
            # Permitted keys ("fields" in mongo):
            "sequence": and_([
                # Constraints on this key's value:
                type_is_(str),
                lambda data: len(data) <= 50
            ]),
            "name": type_is_(str),
            "type": type_is_(str),
            "source": and_([
                type_is_(list),
                for_each_item_(type_is_(str))
            ]),
            "hydrophobicity": and_([
                type_is_(float),
                lambda data: data >= 0,
                lambda data: data <= 1
            ]),
            "toxic":            type_is_(bool),
            "immunogenic":      type_is_(bool),
            "insecticidal":     type_is_(bool),
            "allergen":         type_is_(bool),
            "antibacterial":    type_is_(bool),
            "anticancer":       type_is_(bool),
            "antifungal":       type_is_(bool),
            "antihypertensive": type_is_(bool),
            "antimicrobial":    type_is_(bool),
            "antiparasitic":    type_is_(bool),
            "antiviral":        type_is_(bool)

        }))
    ]))
])
