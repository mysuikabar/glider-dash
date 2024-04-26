with tmp_log_with_first_last_record as (
  select
    *,
    first_value(altitude) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as first_altitude,
    last_value(altitude) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as last_altitude,
    first_value(timestamp) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as first_timestamp,
    last_value(timestamp) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as last_timestamp
  from
    flight_log.ds_flight_log
)

select
  min(flight_id) as flight_id,
  min(pilot) as pilot,
  min(glider_type) as glider_type,
  min(glider_id) as glider_id,
  timestamp_trunc(timestamp, minute) as timestamp,
  avg(latitude) as latitude,
  avg(longitude) as longitude,
  avg(altitude) as altitude,
  min(circling) as circling,
  (min(last_altitude) - min(first_altitude)) / timestamp_diff(min(last_timestamp), min(first_timestamp), second) as climb_rate
from
  tmp_log_with_first_last_record
group by
  timestamp
