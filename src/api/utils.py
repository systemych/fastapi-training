async def update_room_options(db, room_id, room_data, room_options_schema):
    current_room_options = await db.rooms_options.get_all(room_id=room_id)
    current_room_options_ids = [room_option.option_id for room_option in current_room_options]

    options_to_add = list(set(room_data.options_ids) - set(current_room_options_ids))
    options_to_delete = list(set(current_room_options_ids) - set(room_data.options_ids))

    if len(options_to_add) > 0:
        await db.rooms_options.add_bulk([room_options_schema(room_id=room_id, option_id=o_id) for o_id in options_to_add])
    if len(options_to_delete) > 0:
        await db.rooms_options.delete_bulk_by_option_id(options_to_delete)