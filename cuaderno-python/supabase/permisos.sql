-- Table permissions for Python Notebook.
-- Newer Supabase projects don't give the API roles access to new tables automatically,
-- so we grant it here. Row-level security (in esquema.sql) still decides WHICH rows
-- each person can see: students only their own, the teacher everyone's.
-- Safe to run more than once.

grant usage on schema public to authenticated, service_role;

-- The account script (secret key)
grant select, insert, update, delete on public.profiles    to service_role;
grant select, insert, update, delete on public.submissions to service_role;

-- Logged-in students and the teacher (the website)
grant select                 on public.profiles    to authenticated;
grant select, insert, update on public.submissions to authenticated;
grant execute on function public.is_teacher() to authenticated;
