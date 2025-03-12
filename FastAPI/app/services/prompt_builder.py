from app.services.prompt_templates import post_type_prompts, post_type_properties, creative_guidelines, extension, FIELD_PROMPT_MAP, post_type_fields

def generate_prompt(request_data):
    prompt_parts = []

    post_type = request_data.get("post_type", "").strip().lower()

    if post_type and post_type in post_type_prompts:
        prompt_parts.append(post_type_prompts[post_type])

    if post_type and post_type in post_type_properties:
        properties = post_type_properties[post_type]
        formatted_properties = " ".join(f"{key}: {value}" for key, value in properties.items() if value)
        if formatted_properties:
            prompt_parts.append(formatted_properties)

    if post_type in post_type_fields:
        for field in post_type_fields[post_type]:
            field_value = request_data.get(field)
            if field_value:  # Exclude empty or None values
                prompt_parts.append(FIELD_PROMPT_MAP[field](field_value))

    general_fields = ["message", "brand_name", "font", "colors"]
    for field in general_fields:
        field_value = request_data.get(field)
        if field_value:
            prompt_parts.append(FIELD_PROMPT_MAP[field](field_value))

    if post_type in creative_guidelines:
        prompt_parts.append(creative_guidelines[post_type])

    if extension:
        prompt_parts.append(extension)

    final_prompt = "".join(filter(None, prompt_parts))
    return final_prompt