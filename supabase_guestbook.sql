-- ============================================================
-- 방명록 테이블 + RLS 설정
-- Supabase 대시보드 → SQL Editor에서 실행하세요.
-- ============================================================

-- 1. 테이블 생성
create table public.messages (
  id         bigint generated always as identity primary key,
  name       text        not null check (char_length(name) between 1 and 50),
  content    text        not null check (char_length(content) between 1 and 500),
  created_at timestamptz not null default now()
);

-- 2. RLS 활성화
alter table public.messages enable row level security;

-- 3. 누구나 읽기 허용 (anon + authenticated)
create policy "public read messages"
  on public.messages
  for select
  to anon, authenticated
  using (true);

-- 4. 누구나 쓰기 허용 (anon + authenticated)
create policy "public insert messages"
  on public.messages
  for insert
  to anon, authenticated
  with check (true);

-- 5. 최신순 조회 인덱스
create index on public.messages (created_at desc);
