def process_user_data(users):
    total_age = 0
    active_users = 0
    inactive_users = 0
    for user in users:
        if user['age']:
            total_age += user['age']
        if user['status'] == 'active':
            active_users += 1
        elif user['status'] == 'inactive':
            inactive_users += 1
    average_age = total_age / len([user for user in users if user['age']])
    
    return {
        'average_age': average_age,
        'total_users': len(users),
        'active_users': active_users,
        'inactive_users': inactive_users
    }

