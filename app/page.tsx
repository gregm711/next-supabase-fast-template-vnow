import HeaderAuth from "@/components/header-auth";
import { ThemeSwitcher } from "@/components/theme-switcher";

export default async function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center">
      <div className="flex-1 w-full flex flex-col gap-20 items-center">
        <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
          <div className="w-full max-w-5xl flex justify-between items-center p-3 px-5 text-sm">
            <HeaderAuth />
          </div>
        </nav>
        <div className="flex flex-col gap-20 max-w-5xl p-5">
          <div className="min-h-screen flex flex-col">
            {/* Header */}
            <header className="bg-primary text-primary-foreground p-8 text-center">
              <h1 className="text-5xl font-bold">Build Fast, Scale Faster</h1>
              <p className="mt-4 text-xl">
                A boilerplate AI app powered by Next.js, Tailwind CSS, and
                Supabase Auth.
              </p>
            </header>

            {/* Main Content */}
            <main className="flex-1 px-4 py-16">
              <section className="max-w-3xl mx-auto text-center">
                <h2 className="text-4xl font-semibold mb-6">
                  Empower Your Next Project
                </h2>
                <p className="text-lg text-gray-700 mb-8">
                  Our application provides a solid foundation for building
                  modern web experiences. With an intuitive design, robust
                  authentication, and scalable architecture, you can focus on
                  creating innovative solutions that meet your business needs.
                </p>
                <a
                  href="/chat"
                  className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md text-lg hover:bg-blue-700 transition-colors"
                >
                  Get Started
                </a>
              </section>
            </main>

            {/* Footer */}
            <footer className="bg-gray-100 p-4 text-center">
              <p className="text-sm text-gray-500">
                &copy; {new Date().getFullYear()} Boilerplate App. All rights
                reserved.
              </p>
            </footer>
          </div>
        </div>

        <footer className="w-full flex items-center justify-center border-t mx-auto text-center text-xs gap-8 py-16">
          <ThemeSwitcher />
        </footer>
      </div>
    </main>
  );
}
