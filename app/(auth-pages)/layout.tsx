export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="flex-1 w-full flex flex-col gap-20 items-center">
      <div className="max-w-7xl flex flex-col gap-12 items-start">
        <div className="flex flex-col gap-20 max-w-5xl p-5">{children}</div>
      </div>
    </main>
  );
}
