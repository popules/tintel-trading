import "./../styles/globals.css";
import { ReactNode } from "react";
import Logo from "@/components/Logo";

export const metadata = {
  title: "tintel",
  description: "trader intelligence for sub-$5 equities"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-bg text-ink min-h-screen">
        <header className="border-b border-white/5 sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <Logo />
            <span className="text-sm text-mute">trader intelligence</span>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
