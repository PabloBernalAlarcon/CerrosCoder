-- Cuaderno Python: database setup.
-- Paste this whole file into Supabase → SQL Editor → New query, and press Run. Run it once.

-- ---------- Tables ----------

create table public.profiles (
  id          uuid primary key references auth.users (id) on delete cascade,
  username    text not null unique,
  grupo       text not null default '',
  role        text not null default 'student' check (role in ('student', 'teacher')),
  created_at  timestamptz not null default now()
);

create table public.submissions (
  user_id      uuid not null references public.profiles (id) on delete cascade,
  exercise_id  text not null,
  code         text not null default '',
  passed       boolean not null default false,
  attempts     integer not null default 0,
  passed_at    timestamptz,
  updated_at   timestamptz not null default now(),
  primary key (user_id, exercise_id)
);

-- ---------- Helper: is the current user a teacher? ----------

create or replace function public.is_teacher()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from public.profiles where id = auth.uid() and role = 'teacher');
$$;

-- ---------- Row-level security: students see only their own data ----------

alter table public.profiles enable row level security;
alter table public.submissions enable row level security;

create policy "profiles: own row, or teacher sees all"
  on public.profiles for select
  using (id = auth.uid() or public.is_teacher());
-- No insert/update/delete policies on profiles: students can't change their name, group or role.

create policy "submissions: own rows, or teacher sees all"
  on public.submissions for select
  using (user_id = auth.uid() or public.is_teacher());

create policy "submissions: insert own"
  on public.submissions for insert
  with check (user_id = auth.uid());

create policy "submissions: update own"
  on public.submissions for update
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

-- ---------- Triggers ----------

-- Create a profile automatically when an account is created (by scripts/estudiantes.py).
-- Everyone starts as a student; the teacher role is set separately.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, username, grupo)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'username', split_part(new.email, '@', 1)),
    coalesce(new.raw_user_meta_data ->> 'grupo', '')
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Once an exercise is solved it stays solved, and timestamps come from the server's clock.
create or replace function public.keep_progress()
returns trigger
language plpgsql
as $$
begin
  new.passed     := old.passed or new.passed;
  new.passed_at  := coalesce(old.passed_at, new.passed_at);
  new.attempts   := greatest(old.attempts, new.attempts);
  new.updated_at := now();
  return new;
end;
$$;

create trigger submissions_keep_progress
  before update on public.submissions
  for each row execute function public.keep_progress();

create or replace function public.stamp_insert()
returns trigger
language plpgsql
as $$
begin
  new.updated_at := now();
  if new.passed and new.passed_at is null then new.passed_at := now(); end if;
  return new;
end;
$$;

create trigger submissions_stamp_insert
  before insert on public.submissions
  for each row execute function public.stamp_insert();
