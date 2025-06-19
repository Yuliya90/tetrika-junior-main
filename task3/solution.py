def appearance(intervals: dict[str, list[int]]) -> int:
    # Преобразуем интервалы в список кортежей (start, end)
    def process_intervals(intervals_list):
        return [(intervals_list[i], intervals_list[i + 1])
                for i in range(0, len(intervals_list), 2)]

    # Получаем интервалы урока, ученика и учителя
    lesson = process_intervals(intervals['lesson'])[0]
    pupil = process_intervals(intervals['pupil'])
    tutor = process_intervals(intervals['tutor'])

    # Объединяем пересекающиеся интервалы для ученика и учителя
    def merge_intervals(intervals):
        if not intervals:
            return []
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]
        for current in sorted_intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        return merged

    pupil_merged = merge_intervals(pupil)
    tutor_merged = merge_intervals(tutor)

    # Находим пересечение всех трех интервалов (урок, ученик, учитель)
    total = 0
    lesson_start, lesson_end = lesson

    # Проверяем все возможные комбинации интервалов ученика и учителя
    for p_start, p_end in pupil_merged:
        for t_start, t_end in tutor_merged:
            # Находим пересечение интервалов ученика и учителя
            start = max(p_start, t_start)
            end = min(p_end, t_end)
            # Проверяем, что пересечение есть и оно в рамках урока
            if start < end:
                # Находим пересечение с уроком
                start = max(start, lesson_start)
                end = min(end, lesson_end)
                if start < end:
                    total += end - start

    return total