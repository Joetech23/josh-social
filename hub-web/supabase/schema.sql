-- EAGLESCROFT Content Hub: Supabase schema.
-- Run once in the Supabase dashboard: SQL Editor -> New query -> paste this file -> Run.
-- Safe to re-run: every statement is idempotent.
--
-- Access model: only emails listed in public.hub_members can read or write anything,
-- including the files in the private "hub" storage bucket. Everyone else, signed in or not,
-- sees nothing. Claude publishes posts with the service-role key, which bypasses these rules.

-- People allowed into the hub ------------------------------------------------------------
create table if not exists public.hub_members (
  email text primary key check (email = lower(email)),
  added_at timestamptz not null default now()
);
alter table public.hub_members enable row level security;

create or replace function public.is_hub_member()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.hub_members
    where email = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;
revoke all on function public.is_hub_member() from public;
grant execute on function public.is_hub_member() to authenticated;

drop policy if exists "members read members" on public.hub_members;
create policy "members read members" on public.hub_members
  for select to authenticated using (public.is_hub_member());

-- Posts (written by Claude, read by members) ---------------------------------------------
create table if not exists public.posts (
  id text primary key,                       -- tracker id: 005, J03 ...
  week text not null,                        -- 2026-W44
  account text not null check (account in ('eaglescroft', 'joshua')),
  date date not null,
  ord int not null default 0,
  series text not null default '',
  title text not null,
  format text not null default '',
  build text not null default 'design' check (build in ('ready', 'design', 'needs-you')),
  needs text not null default '',
  tip text not null default '',
  times jsonb not null default '[]',         -- [{platform, time}]
  media jsonb not null default '[]',         -- [{path, name}]  paths inside the "hub" bucket
  files jsonb not null default '[]',         -- [{path, name, label}]
  captions jsonb not null default '[]',      -- [{label, text}]
  updated_at timestamptz not null default now()
);
create index if not exists posts_week_idx on public.posts (week, account, date);
alter table public.posts enable row level security;
drop policy if exists "members read posts" on public.posts;
create policy "members read posts" on public.posts
  for select to authenticated using (public.is_hub_member());

-- Reviews: Joshua's decision and note per post -------------------------------------------
create table if not exists public.reviews (
  post_id text primary key references public.posts (id) on delete cascade,
  status text not null default '' check (status in ('', 'approved', 'changes', 'posted')),
  note text not null default '',
  updated_at timestamptz not null default now(),
  updated_by uuid default auth.uid()
);
alter table public.reviews enable row level security;
drop policy if exists "members read reviews" on public.reviews;
create policy "members read reviews" on public.reviews
  for select to authenticated using (public.is_hub_member());
drop policy if exists "members add reviews" on public.reviews;
create policy "members add reviews" on public.reviews
  for insert to authenticated with check (public.is_hub_member());
drop policy if exists "members change reviews" on public.reviews;
create policy "members change reviews" on public.reviews
  for update to authenticated using (public.is_hub_member()) with check (public.is_hub_member());

-- Inbox: files Joshua sends to Claude ------------------------------------------------------
create table if not exists public.inbox (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  path text not null,                        -- inside the "hub" bucket, under inbox/
  content_type text not null default '',
  size_bytes bigint not null default 0,
  for_post text references public.posts (id) on delete set null,
  note text not null default '',
  seen boolean not null default false,
  created_at timestamptz not null default now(),
  created_by uuid default auth.uid()
);
alter table public.inbox enable row level security;
drop policy if exists "members read inbox" on public.inbox;
create policy "members read inbox" on public.inbox
  for select to authenticated using (public.is_hub_member());
drop policy if exists "members add inbox" on public.inbox;
create policy "members add inbox" on public.inbox
  for insert to authenticated with check (public.is_hub_member() and path like 'inbox/%');

-- Messages: notes for Claude -------------------------------------------------------------
create table if not exists public.messages (
  id uuid primary key default gen_random_uuid(),
  text text not null check (length(text) between 1 and 5000),
  week text not null default '',
  account text not null default '',
  seen boolean not null default false,
  reply text not null default '',
  created_at timestamptz not null default now(),
  created_by uuid default auth.uid()
);
alter table public.messages enable row level security;
drop policy if exists "members read messages" on public.messages;
create policy "members read messages" on public.messages
  for select to authenticated using (public.is_hub_member());
drop policy if exists "members add messages" on public.messages;
create policy "members add messages" on public.messages
  for insert to authenticated with check (public.is_hub_member());

-- Table privileges (RLS above still decides which rows) -----------------------------------
revoke all on public.hub_members, public.posts, public.reviews, public.inbox, public.messages from anon;
grant select on public.hub_members, public.posts to authenticated;
grant select, insert, update on public.reviews to authenticated;
grant select, insert on public.inbox, public.messages to authenticated;

-- Private storage bucket for graphics and uploads ----------------------------------------
insert into storage.buckets (id, name, public, file_size_limit)
values ('hub', 'hub', false, 52428800)
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit;

drop policy if exists "members read hub files" on storage.objects;
create policy "members read hub files" on storage.objects
  for select to authenticated using (bucket_id = 'hub' and public.is_hub_member());
drop policy if exists "members upload to inbox" on storage.objects;
create policy "members upload to inbox" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'hub' and (storage.foldername(name))[1] = 'inbox' and public.is_hub_member());

-- Add yourself (change the email, then run this line once) ------------------------------
-- insert into public.hub_members (email) values ('you@example.com') on conflict do nothing;
