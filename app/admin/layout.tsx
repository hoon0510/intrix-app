'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface AdminLayoutProps {
  children: React.ReactNode;
}

const menuItems = [
  { name: 'Analysis History', path: '/admin/analysis-history' },
  { name: 'Credit Log', path: '/admin/credit-log' },
  { name: 'Refund Requests', path: '/admin/refund' },
  { name: 'Promotions', path: '/admin/promotions' },
];

export default function AdminLayout({ children }: AdminLayoutProps) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="flex">
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-lg h-screen fixed">
          <div className="p-4">
            <h1 className="text-xl font-bold text-gray-800 mb-8">Admin Dashboard</h1>
            <nav>
              <ul className="space-y-2">
                {menuItems.map((item) => (
                  <li key={item.path}>
                    <Link
                      href={item.path}
                      className={`block px-4 py-2 rounded-lg ${
                        pathname === item.path
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="ml-64 flex-1 p-8">
          {children}
        </div>
      </div>
    </div>
  );
} 