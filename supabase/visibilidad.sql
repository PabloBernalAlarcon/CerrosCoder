-- Unit visibility per class (group), set by the teacher from the Visibility page.
-- Paste this whole file into Supabase → SQL Editor → New query, and press Run.
-- Safe to run more than once. (New projects get this from esquema.sql already.)

create table if not exists public.unit_visibility (
  grupo       text not null,
  unit_id     text not null,
  estado      text not null check (estado in ('open', 'locked', 'hidden')),
  updated_at  timestamptz not null default now(),
  primary key (grupo, unit_id)
);

-- The current user's group, readable inside policies
create or replace function public.my_group()
returns text
language sql
stable
security definer
set search_path = public
as $$
  select grupo from public.profiles where id = auth.uid();
$$;

grant execute on function public.my_group() to authenticated;
grant select, insert, update, delete on public.unit_visibility to authenticated;
grant select, insert, update, delete on public.unit_visibility to service_role;

alter table public.unit_visibility enable row level security;

drop policy if exists "visibility: own group, or teacher sees all" on public.unit_visibility;
create policy "visibility: own group, or teacher sees all"
  on public.unit_visibility for select
  using (grupo = public.my_group() or public.is_teacher());

drop policy if exists "visibility: teacher inserts" on public.unit_visibility;
create policy "visibility: teacher inserts"
  on public.unit_visibility for insert
  with check (public.is_teacher());

drop policy if exists "visibility: teacher updates" on public.unit_visibility;
create policy "visibility: teacher updates"
  on public.unit_visibility for update
  using (public.is_teacher())
  with check (public.is_teacher());

drop policy if exists "visibility: teacher deletes" on public.unit_visibility;
create policy "visibility: teacher deletes"
  on public.unit_visibility for delete
  using (public.is_teacher());
