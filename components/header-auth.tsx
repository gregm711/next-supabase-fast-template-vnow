import { signOutAction } from "@/app/actions";
import Link from "next/link";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { createClient } from "@/utils/supabase/server";

export default async function Header() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <header className="w-full flex justify-between items-center p-4">
      {/* Logo Section */}
      <div className="flex items-center">
        <Link href="/">
          <span className="text-2xl font-bold">Boilerplate App</span>
        </Link>
      </div>

      {/* Auth Buttons Section */}
      <div>
        {user ? (
          <div className="flex items-center gap-4">
            <span className="text-sm">Hey, {user.email}!</span>
            <form action={signOutAction}>
              <Button type="submit" variant="outline" size="sm">
                Sign out
              </Button>
            </form>
          </div>
        ) : (
          <div className="flex gap-2">
            <Button asChild size="sm" variant="outline">
              <Link href="/sign-in">Sign in</Link>
            </Button>
            <Button asChild size="sm" variant="default">
              <Link href="/sign-up">Sign up</Link>
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}
