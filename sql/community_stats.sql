create or replace view community_stats as
select
  count(*) as total_resolutions,
  -- Conteggio per categoria (considera che resolution_category è un array)
  (
    select json_agg(json_build_object('category', cat.category, 'count', cat.count))
    from (
      select unnest(resolution_category) as category, count(*) as count
      from messages
      group by category
      order by count desc
      limit 10
    ) cat
  ) as category_counts,
  
  -- Conteggio per motivazione
  (
    select json_agg(json_build_object('motivation', mot.motivation, 'count', mot.count))
    from (
      select unnest(motivation) as motivation, count(*) as count
      from messages
      group by motivation
      order by count desc
      limit 10
    ) mot
  ) as motivation_counts,

  avg(past_year_score) as avg_past_year_score,
  avg(new_year_score) as avg_new_year_score

from messages;