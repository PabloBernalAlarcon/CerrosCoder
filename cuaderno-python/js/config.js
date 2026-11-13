// ⚙️ Platform settings. Fill these in after creating your Supabase project (see README).
export const CONFIG = {
  APP_NAME: "Cerros Coder",
  COURSE_SUBTITLE: "Python Fundamentals, Grade 9",

  // URL: Project Settings → Data API → Project URL (https://xxxx.supabase.co)
  // Key: Project Settings → API Keys → Publishable key (sb_publishable_...). It's meant to be
  // public; the database rules (row-level security) are what protect students' data.
  SUPABASE_URL: "https://nwcbgdrouseyhejdpwos.supabase.co/rest/v1/",
  SUPABASE_ANON_KEY: "sb_publishable_Wmj0rb6LU9TcixFhdw19tw_YI25Ol_j",

  // Usernames become fake e-mail addresses behind the scenes (8a-07 → 8a-07@alumnos.example.com).
  // No e-mail is ever sent. Must match EMAIL_DOMAIN in scripts/estudiantes.py.
  EMAIL_DOMAIN: "alumnos.example.com",

  // Students who haven't worked for this many days are highlighted in the teacher panel.
  DIAS_INACTIVO: 14,
};
