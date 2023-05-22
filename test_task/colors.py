import plotly.express as px


def get_colors():
    colors_source = px.colors.qualitative.Plotly
    colors = {
        "Простой": colors_source[3],
        "Вычисление": colors_source[2],
        "Работа": colors_source[4],
        "Наладка": colors_source[0],
        "Обед 60мин": colors_source[5],
        "Перерыв 5мин": colors_source[1],
        "См. задание выполнено": colors_source[2],
        "Обед 30мин": colors_source[7],
    }
    return colors


def update_colors(chosen_state):
    colors = get_colors()
    for state, color in colors.items():
        if state == chosen_state:
            continue
        colors[state] = "gray"
    return colors
