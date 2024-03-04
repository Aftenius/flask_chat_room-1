test = {
    2: {
        'entity_id': 123,
        "name_room": 1,
        "type": 'labor_costs',
        "description": 'lorem lorem lorem'
    },
    3: {
        'entity_id': 123,
        "name_room": 1,
        "type": 'labor_costs',
        "description": 'lorem lorem lorem'
    },
    4: {
        'entity_id': 123,
        "name_room": 1,
        "type": 'labor_costs',
        "description": 'lorem lorem lorem'
    }
}

print(test)

del test[3]

print(test)

# print(list(test[0].keys())[-1])