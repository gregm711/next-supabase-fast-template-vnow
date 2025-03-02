// app/layout.tsx or app/RootLayout.tsx

import HeaderAuth from "@/components/header-auth";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import "../globals.css";

const defaultUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : "http://localhost:3000";

export const metadata = {
  metadataBase: new URL(defaultUrl),
  title: "Boilerplate App",
  description: "Boilerplate App",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SidebarProvider>
      {/* AppSidebar renders the sidebar */}
      <AppSidebar />

      <main className="flex-1 w-full flex flex-col gap-20 items-center">
        {/* Navigation Bar */}
        <nav className="w-full flex justify-between items-center border-b border-b-foreground/10 h-16 px-5">
          <div className="flex gap-5 items-center font-semibold">
            {/* Sidebar Trigger Button */}
            <SidebarTrigger className="mr-4">
              {/* You can customize the trigger icon/text here */}☰
            </SidebarTrigger>
          </div>
          {<HeaderAuth />}
        </nav>

        {/* Main Content */}
        <div className="flex flex-col gap-20 max-w-5xl p-5 w-full">
          {children}
        </div>

        {/* Optional Spacer */}
        <div className="py-80"></div>

        {/* Footer */}
        <footer className="w-full flex items-center justify-center border-t mx-auto text-center text-xs gap-8 py-16">
          <ThemeSwitcher />
        </footer>
      </main>
    </SidebarProvider>
  );
}
