import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export const createClient = async () => {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              // Force cookies to be available cross-site (e.g. in an iframe)
              cookieStore.set(name, value, {
                ...options,
                sameSite: "none",
                secure: true,
              });
            });
          } catch (error) {
            // The `set` method may be called from a Server Component.
            // This can be safely ignored if your middleware handles session refreshing.
          }
        },
      },
    }
  );
};
