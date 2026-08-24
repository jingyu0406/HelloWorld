insert into public.admin_emails (email)
values ('jyweng0406@gmail.com')
on conflict (email) do nothing;
