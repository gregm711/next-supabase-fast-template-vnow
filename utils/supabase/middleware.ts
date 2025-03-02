import { createServerClient } from "@supabase/ssr";
import { type NextRequest, NextResponse } from "next/server";

export const updateSession = async (request: NextRequest) => {
  // When USE_SECURE_MODE is "true", we enforce production-like behavior:
  // - Redirect users based on auth status
  // - Force cookies to be secure
  const useSecureMode = process.env.USE_SECURE_MODE === "true";

  try {
    // Create an unmodified response
    let response = NextResponse.next({
      request: {
        headers: request.headers,
      },
    });

    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() {
            return request.cookies.getAll();
          },
          setAll(cookiesToSet) {
            // Update the request cookies first
            cookiesToSet.forEach(({ name, value }) =>
              request.cookies.set(name, value)
            );

            // Create a new response instance to attach updated cookies
            response = NextResponse.next({ request });
            // Attach cookies to the response – forcing secure cookies when in secure mode.
            cookiesToSet.forEach(({ name, value, options }) =>
              response.cookies.set(name, value, {
                ...options,
                secure: useSecureMode,
              })
            );
          },
        },
      }
    );

    // Refresh session (required for Server Components)
    const user = await supabase.auth.getUser();

    // Enforce auth redirects only when secure mode is enabled.
    if (useSecureMode) {
      // Redirect unauthenticated users trying to access protected routes.
      if (request.nextUrl.pathname.startsWith("/protected") && user.error) {
        return NextResponse.redirect(new URL("/sign-in", request.url));
      }
      // Redirect authenticated users from the home page to a protected route.
      if (request.nextUrl.pathname === "/" && !user.error) {
        return NextResponse.redirect(new URL("/protected", request.url));
      }
    }

    return response;
  } catch (e) {
    // If an error occurs (e.g. Supabase client failure), pass the request through.
    return NextResponse.next({
      request: {
        headers: request.headers,
      },
    });
  }
};
