"use server";

import { createClient } from "@/utils/supabase/server";

export async function callBackendServer(
  endpoint: string,
  init: RequestInit = {}
) {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    throw new Error("Not authenticated");
  }
  // its safe to get the session here because we already have the user: https://supabase.com/docs/guides/auth/server-side/nextjs?queryGroups=router&router=pages
  const { data: session } = await supabase.auth.getSession();

  const token = session.session?.access_token;
  // Ensure the Authorization header is set.
  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${token}`);

  // Combine any additional fetch options.
  const fetchOptions: RequestInit = {
    ...init,
    headers,
  };

  // Get the base URL from environment variables.
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  if (!baseUrl) {
    throw new Error("Missing NEXT_PUBLIC_BACKEND_URL");
  }

  // Make the fetch call to the custom backend endpoint.
  const response = await fetch(`${baseUrl}${endpoint}`, fetchOptions);
  return response;
}
