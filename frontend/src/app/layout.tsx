import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "MediGuide AI — Clinical Support Assistant",
  description:
    "AI-powered clinical support: symptom checker, medical chatbot, and health report analysis. Not a substitute for professional medical advice.",
  keywords: ["symptom checker", "medical AI", "health assistant", "report analysis"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 antialiased">
        <Navbar />
        <main className="min-h-[calc(100vh-4rem)]">{children}</main>
        <footer className="border-t border-gray-200 bg-white py-6 mt-12">
          <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
            <p className="font-medium text-gray-700 mb-1">⚕️ Medical Disclaimer</p>
            <p>
              MediGuide AI is a clinical support tool for general health information only.
              It is <strong>not</strong> a substitute for professional medical advice, diagnosis, or treatment.
              Always consult a qualified healthcare professional. In an emergency, call{" "}
              <strong>112 / 911</strong> immediately.
            </p>
            <p className="mt-3 text-xs text-gray-400">
              © {new Date().getFullYear()} MediGuide AI · Built with Claude AI · For educational purposes
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
