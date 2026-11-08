// ⚙️ Platform settings. Fill these in after creating your Supabase project (see README).
export const CONFIG = {
  APP_NAME: "Cuaderno Python",
  COURSE_SUBTITLE: "Fundamentos de Python, grado 8.º",

  // Supabase → Project Settings → API. The anon/publishable key is meant to be public;
  // the database rules (row-level security) are what protect students' data.
  SUPABASE_URL: "https://wqgpcqplftvnrkswbttx.supabase.co/rest/v1/",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxZ3BjcXBsZnR2bnJrc3didHR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQxNzAyMTQsImV4cCI6MjEwOTc0NjIxNH0.LOfcDeKwVrvlXh20ZLpYv-KMq_8fso5rzDvAGT4UfkE",

  // Usernames become fake e-mail addresses behind the scenes (8a-07 → 8a-07@alumnos.example.com).
  // No e-mail is ever sent. Must match EMAIL_DOMAIN in scripts/estudiantes.py.
  EMAIL_DOMAIN: "alumnos.example.com",

  // Students who haven't worked for this many days are highlighted in the teacher panel.
  DIAS_INACTIVO: 14,
};
