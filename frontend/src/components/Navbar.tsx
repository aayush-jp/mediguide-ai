"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, MessageCircle, FileText, Home } from "lucide-react";
import { clsx } from "clsx";

const navLinks = [
  { href: "/",                  label: "Home",            icon: Home },
  { href: "/symptom-checker",   label: "Symptom Checker", icon: Activity },
  { href: "/chat",              label: "AI Chat",         icon: MessageCircle },
  { href: "/report",            label: "Report Analysis", icon: FileText },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center group-hover:bg-blue-700 transition-colors">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-lg text-gray-900">
            MediGuide <span className="text-blue-600">AI</span>
          </span>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                pathname === href
                  ? "bg-blue-50 text-blue-700"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              )}
            >
              <Icon className="w-4 h-4" />
              {label}
            </Link>
          ))}
        </div>

        {/* Emergency badge */}
        <div className="hidden md:flex items-center">
          <span className="text-xs font-medium text-red-600 bg-red-50 border border-red-200 rounded-full px-3 py-1">
            Emergency: Call 112 / 911
          </span>
        </div>

        {/* Mobile nav */}
        <div className="flex md:hidden items-center gap-1">
          {navLinks.map(({ href, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={clsx(
                "p-2 rounded-lg transition-colors",
                pathname === href
                  ? "bg-blue-50 text-blue-600"
                  : "text-gray-500 hover:text-gray-900"
              )}
            >
              <Icon className="w-5 h-5" />
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
