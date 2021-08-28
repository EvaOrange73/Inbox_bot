def get_social_tasks(list_of_social_tasks):
    if len(list_of_social_tasks) > 0:
        answer = "Социальные взаимодействия в процессе:"
        for i, task in enumerate(list_of_social_tasks):
            answer += f"\n\n{i + 1}) {list_of_social_tasks[i].text}:"
            answer += f"\nследующий шаг: {list_of_social_tasks[i].who}"
            answer += f"\nописание: {list_of_social_tasks[i].description}"

    else:
        answer = "Нет текущих социальных взаимодействий"

    return answer
