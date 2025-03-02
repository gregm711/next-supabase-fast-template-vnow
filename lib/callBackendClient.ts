import { createClient } from "@/utils/supabase/client";

export async function callBackendClient(
  endpoint: string,
  init: RequestInit = {}
) {
  const supabase = createClient();

  // Verify that the user is authenticated.
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    throw new Error("Not authenticated");
  }

  // Get the current session to extract the access token.
  const { data: session } = await supabase.auth.getSession();
  const token = session?.session?.access_token;
  if (!token) {
    throw new Error("Missing access token");
  }

  // Ensure the Authorization header is set.
  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${token}`);

  // Combine any additional fetch options.
  const fetchOptions: RequestInit = {
    method: init.method || "GET",
    ...init,
    headers,
  };

  // Get the base URL from environment variables.
  const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  if (!baseUrl) {
    throw new Error("Missing NEXT_PUBLIC_BACKEND_URL");
  }

  // Make the fetch call to your backend endpoint.
  const response = await fetch(`${baseUrl}${endpoint}`, fetchOptions);
  return response;
}
