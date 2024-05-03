from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/mysuikabar/glider-dash.git",
        entrypoint="./data_infrastructure/workflow/weather_data.py:load_weather_data_to_bq",
    ).deploy(
        name="weather-data-scraper", work_pool_name="managed-pool", cron="0 3 * * *"
    )
