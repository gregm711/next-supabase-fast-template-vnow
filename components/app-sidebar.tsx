import {
  Calendar,
  Home,
  Inbox,
  Search,
  Settings,
  Mic,
  Book,
  MessageSquare,
} from "lucide-react";
import { createClient } from "@/utils/supabase/server";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

// Menu items
const items = [
  {
    title: "Chat",
    url: "/chat",
    icon: Search,
  },
  {
    title: "settings",
    url: "/settings",
    icon: Settings,
  },
];

interface Chat {
  id: string;
  title: string;
  created_at: string;
}

export async function AppSidebar() {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Boilerplate</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
