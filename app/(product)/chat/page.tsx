import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Chat from "@/components/chat";
import { callBackendServer } from "@/lib/callBackendServer";

export default async function SearchPage() {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return redirect("/sign-in");
  }

  const response = await callBackendServer("/auth-health-check");
  const data = await response.json();

  return (
    <div className="max-w-4xl mx-auto w-full px-4 py-8">
      <h1 className="text-2xl font-semibold text-center mb-8">AI Chat</h1>
      <div>
        <h2>Server call backend health check</h2>
        <p>{data.message}</p>
      </div>

      <div className="relative mb-12">
        <Chat />
      </div>

      <div>
        <h2 className="text-lg font-medium mb-4">
          Recommended for AI Applications 🚀
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="cursor-pointer transform transition-transform duration-200 hover:scale-105">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">AI-Powered Insights</CardTitle>
                <CardDescription>
                  Uncover hidden trends and patterns in your data using advanced
                  analytics.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
          <div className="cursor-pointer transform transition-transform duration-200 hover:scale-105">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">
                  Interactive Visualizations
                </CardTitle>
                <CardDescription>
                  Transform raw data into engaging visuals for quick and
                  effective decision-making.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
          <div className="cursor-pointer transform transition-transform duration-200 hover:scale-105">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Automated Reporting</CardTitle>
                <CardDescription>
                  Streamline your workflow by generating comprehensive,
                  actionable reports automatically.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
