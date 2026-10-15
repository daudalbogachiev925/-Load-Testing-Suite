# -Load-Testing-Suite
Описание: нагрузочное тестирование 1С: генерация нагрузки, метрики, отчёты, анализ боттлнеков.
# Load Testing Suite для 1С

Нагрузочное тестирование: сценарии, виртуальные пользователи, метрики, анализ боттлнеков.

## Возможности
- YAML-сценарии с шагами и весами
- Ramp-up, think time, error rate
- Метрики: p50/p75/p90/p95/p99, RPS, error rate
- Bottleneck analysis + SLA check
- Рекомендации по масштабированию

## Запуск
```bash
pip install -r requirements.txt
streamlit run app.py
pytest -v
```
